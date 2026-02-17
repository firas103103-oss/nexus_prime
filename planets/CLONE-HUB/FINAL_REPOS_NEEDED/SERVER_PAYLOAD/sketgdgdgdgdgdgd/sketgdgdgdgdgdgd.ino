#include <WiFi.h>
#include <WebServer.h>
#include <HTTPClient.h>
#include <FFat.h>
#include <Preferences.h>

/* ================= CONFIG ================= */
#define WIFI_SSID   "ASSAF_House"
#define WIFI_PASS   "103ASSAF103@"

#define AP_SSID     "XBIO_Sentinel"
#define AP_PASS     "12345678"

#define ADMIN_TOKEN "MrF_XBIO_ADMIN_2025"
#define GS_URL      "https://script.google.com/macros/s/AKfycbytpDXl6omBsA_lep8JmBShGWi_uzMkFtrTfhlKyFdi5RVpjVV7or7ikU91hKz7r151AA/exec"

#define LOG_PATH "/xbio_log.csv"

#define T_PURGE    6000
#define T_SNIFF    8000
#define T_RECOVER  6000

#define PUSH_EVERY_MS  5000
#define PUSH_MAX_LINES 50
#define WIFI_CONNECT_TIMEOUT_MS 10000
/* ========================================== */

WebServer server(80);
Preferences prefs;

/* ========= STATE ========= */
enum Phase { IDLE=0, PURGE=1, SNIFF=2, RECOVER=3 };
Phase phase = IDLE;
bool running = false;

uint32_t phaseStart = 0;
uint32_t sniff_id = 0;
String session_id;
uint32_t lastPush = 0;
/* ========================= */

struct Sample {
  float tC, rh, pHpa;
  float gas[4];
  float lg[4];
} s;

/* ======== SENSOR READ (بدّلها لاحقاً بـ BME688) ======== */
bool readSensors() {
  s.tC = 25.0;
  s.rh = 45.0;
  s.pHpa = 1000.0;
  s.gas[0]=10; s.gas[1]=20; s.gas[2]=30; s.gas[3]=40;
  s.lg[0]=1;  s.lg[1]=2;  s.lg[2]=3;  s.lg[3]=4;
  return true;
}
/* ===================================================== */

static const char* phaseName(Phase p){
  switch(p){
    case IDLE: return "IDLE";
    case PURGE: return "PURGE";
    case SNIFF: return "SNIFF";
    case RECOVER: return "RECOVER";
  }
  return "IDLE";
}

void ensureHeader() {
  if (!FFat.exists(LOG_PATH)) {
    File f = FFat.open(LOG_PATH, FILE_WRITE);
    f.println("schema,session_id,sniff_id,phase,ms,tC,rh,pHpa,gas0,gas1,gas2,gas3,lg0,lg1,lg2,lg3");
    f.close();
  }
}

void logCSV() {
  File f = FFat.open(LOG_PATH, FILE_APPEND);
  if (!f) return;
  f.printf(
    "1,%s,%lu,%d,%lu,%.3f,%.3f,%.3f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f\n",
    session_id.c_str(), sniff_id, (int)phase, millis(),
    s.tC, s.rh, s.pHpa,
    s.gas[0], s.gas[1], s.gas[2], s.gas[3],
    s.lg[0],  s.lg[1],  s.lg[2],  s.lg[3]
  );
  f.close();
}

/* ========= HTTP POST with MANUAL REDIRECT ========= */
bool httpPostFollow302(const String& url, const String& body, int &outCode, String &outResp) {
  HTTPClient http;
  http.begin(url);
  http.addHeader("Content-Type","application/json");
  http.addHeader("Accept","application/json");

  outCode = http.POST(body);
  outResp = http.getString();
  String loc = http.header("Location");
  http.end();

  if ((outCode==301 || outCode==302 || outCode==303 || outCode==307 || outCode==308) && loc.length()) {
    HTTPClient http2;
    http2.begin(loc);
    http2.addHeader("Content-Type","application/json");
    http2.addHeader("Accept","application/json");
    outCode = http2.POST(body);
    outResp = http2.getString();
    http2.end();
  }
  return (outCode >= 200 && outCode < 300);
}

/* ========== PUSH TO GOOGLE SHEETS ========== */
bool pushToGS() {
  if (WiFi.status() != WL_CONNECTED) return false;
  if (!FFat.exists(LOG_PATH)) return false;

  size_t offset = prefs.getULong("push_ofs", 0);
  File f = FFat.open(LOG_PATH, FILE_READ);
  if (!f) return false;
  if (offset > (size_t)f.size()) offset = 0;
  f.seek(offset);

  String rowsJson = "[";
  int count = 0;
  while (f.available() && count < PUSH_MAX_LINES) {
    String line = f.readStringUntil('\n');
    line.trim();
    if (!line.length() || line.startsWith("schema,")) continue;

    rowsJson += "\"";
    for (char c: line) {
      if (c=='\\' || c=='\"') rowsJson += "\\";
      rowsJson += c;
    }
    rowsJson += "\"";
    count++;
    if (count < PUSH_MAX_LINES) rowsJson += ",";
  }
  size_t newOffset = (size_t)f.position();
  f.close();
  rowsJson += "]";

  if (count==0) {
    prefs.putULong("push_ofs", newOffset);
    return true;
  }

  String body =
    "{\"token\":\""+String(ADMIN_TOKEN)+"\","
    "\"session_id\":\""+session_id+"\","
    "\"log_path\":\""+String(LOG_PATH)+"\","
    "\"rows\":"+rowsJson+"}";

  int code=-1; String resp;
  bool ok = httpPostFollow302(GS_URL, body, code, resp);

  Serial.print("PUSH code="); Serial.println(code);
  Serial.println(resp);

  if (ok) {
    prefs.putULong("push_ofs", newOffset);
    return true;
  }
  return false;
}

/* ========== FSM ========= */
void startAll(){ sniff_id++; phase=PURGE; phaseStart=millis(); running=true; }
void stopAll(){ running=false; phase=IDLE; }

void tickFSM() {
  if (!running) return;
  uint32_t now=millis(), elapsed=now-phaseStart;
  uint32_t dur=(phase==PURGE)?T_PURGE:(phase==SNIFF)?T_SNIFF:T_RECOVER;

  if (readSensors() && phase==SNIFF) logCSV();

  if (elapsed>=dur) {
    phase=(phase==PURGE)?SNIFF:(phase==SNIFF)?RECOVER:PURGE;
    phaseStart=now;
  }
  if (now-lastPush>=PUSH_EVERY_MS) { lastPush=now; pushToGS(); }
}

/* ========== WEB ========= */
void setupWeb() {
  server.on("/",HTTP_GET,[](){
    server.send(200,"text/html",
      "<h2>XBIO Sentinel</h2>"
      "<a href='/start'>START</a> | "
      "<a href='/stop'>STOP</a> | "
      "<a href='/push'>PUSH</a> | "
      "<a href='/status'>STATUS</a>");
  });
  server.on("/start",HTTP_GET,[]{ startAll(); server.send(200,"application/json","{\"ok\":true}"); });
  server.on("/stop", HTTP_GET,[]{ stopAll();  server.send(200,"application/json","{\"ok\":true}"); });
  server.on("/push", HTTP_GET,[]{ bool ok=pushToGS(); server.send(200,"application/json",String("{\"ok\":")+(ok?"true":"false")+"}"); });
  server.on("/status",HTTP_GET,[]{
    server.send(200,"application/json",
      "{\"wifi\":"+String(WiFi.status()==WL_CONNECTED?"true":"false")+
      ",\"ip\":\""+WiFi.localIP().toString()+
      "\",\"ap\":\""+WiFi.softAPIP().toString()+
      "\",\"phase\":\""+phaseName(phase)+
      "\",\"sniff_id\":"+String(sniff_id)+"}");
  });
  server.begin();
}

/* ========== WIFI ========= */
void setupWiFi() {
  WiFi.mode(WIFI_AP_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASS);
  uint32_t t0=millis();
  while (WiFi.status()!=WL_CONNECTED && millis()-t0<WIFI_CONNECT_TIMEOUT_MS) delay(200);
  WiFi.softAP(AP_SSID, AP_PASS);
}

/* ========== SETUP / LOOP ========= */
void setup() {
  Serial.begin(115200);
  prefs.begin("xbio", false);
  setupWiFi();
  FFat.begin(true);
  ensureHeader();
  session_id = String((uint32_t)ESP.getEfuseMac(), HEX);
  setupWeb();
  Serial.println("READY");
}

void loop() {
  server.handleClient();
  tickFSM();
  delay(5);
}
