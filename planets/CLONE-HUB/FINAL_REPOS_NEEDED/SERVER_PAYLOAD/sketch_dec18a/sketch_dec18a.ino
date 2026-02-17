#include <WiFi.h>
#include <WebServer.h>
#include <HTTPClient.h>
#include <FFat.h>
#include <Preferences.h>

/* ================= CONFIG ================= */
#define WIFI_SSID   "ASSAF House"
#define WIFI_PASS   "103ASSAF103@"

#define AP_SSID     "XBIO_Sentinel"
#define AP_PASS     "12345678"

#define ADMIN_TOKEN "MrF_XBIO_ADMIN_2025"

/* 🔥 IMPORTANT: googleusercontent DIRECT */
#define GS_URL "https://script.google.com/macros/s/AKfycbx2sA0EUOWVV0WKBIkl9vL9q0_CjdBpOB7RAcdpsxwQNrGzzd6odQPvOyfBvBanlFNoUw/exec"

#define LOG_PATH "/xbio_log.csv"

#define T_PURGE    6000
#define T_SNIFF    8000
#define T_RECOVER  6000

#define PUSH_EVERY_MS  5000
#define PUSH_MAX_LINES 40
#define WIFI_TIMEOUT   10000
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

/* ===== SENSOR (PLACEHOLDER) ===== */
bool readSensors() {
  s.tC = 25.0;
  s.rh = 45.0;
  s.pHpa = 1000.0;
  s.gas[0]=10; s.gas[1]=20; s.gas[2]=30; s.gas[3]=40;
  s.lg[0]=1;  s.lg[1]=2;  s.lg[2]=3;  s.lg[3]=4;
  return true;
}
/* ================================= */

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

/* ========= PUSH TO GOOGLE SHEETS ========= */
bool pushToGS() {
  if (WiFi.status() != WL_CONNECTED) return false;

  size_t offset = prefs.getULong("ofs", 0);
  File f = FFat.open(LOG_PATH, FILE_READ);
  if (!f) return false;

  if (offset > f.size()) offset = 0;
  f.seek(offset);

  String rows = "[";
  int c = 0;
  while (f.available() && c < PUSH_MAX_LINES) {
    String line = f.readStringUntil('\n');
    line.trim();
    if (!line.length() || line.startsWith("schema,")) continue;
    rows += "\"" + line + "\"";
    c++;
    if (c < PUSH_MAX_LINES) rows += ",";
  }
  size_t newOfs = f.position();
  f.close();
  rows += "]";

  if (c == 0) { prefs.putULong("ofs", newOfs); return true; }

  String body =
    "{\"token\":\""+String(ADMIN_TOKEN)+"\","
    "\"rows\":"+rows+"}";

  HTTPClient http;
  http.begin(GS_URL);
  http.addHeader("Content-Type","application/json");

  int code = http.POST(body);
  String resp = http.getString();
  http.end();

  Serial.print("PUSH code="); Serial.println(code);
  Serial.println(resp);

  if (code == 200) {
    prefs.putULong("ofs", newOfs);
    return true;
  }
  return false;
}
/* ========================================= */

void startAll() {
  sniff_id++;
  phase = PURGE;
  phaseStart = millis();
  running = true;
}
void stopAll() { running = false; phase = IDLE; }

void tickFSM() {
  if (!running) return;

  uint32_t now = millis();
  uint32_t dur =
    (phase==PURGE)?T_PURGE:
    (phase==SNIFF)?T_SNIFF:T_RECOVER;

  if (readSensors() && phase==SNIFF) logCSV();

  if (now - phaseStart >= dur) {
    phase = (phase==PURGE)?SNIFF:(phase==SNIFF)?RECOVER:PURGE;
    phaseStart = now;
  }

  if (now - lastPush > PUSH_EVERY_MS) {
    lastPush = now;
    pushToGS();
  }
}

/* ========== WEB ========= */
void setupWeb() {
  server.on("/", HTTP_GET, [](){
    server.send(200,"text/html",
      "<h2>XBIO Sentinel</h2>"
      "<a href='/start'>START</a> | "
      "<a href='/stop'>STOP</a> | "
      "<a href='/push'>PUSH</a>");
  });
  server.on("/start",HTTP_GET,[]{startAll();server.send(200,"application/json","{\"ok\":true}");});
  server.on("/stop", HTTP_GET,[]{stopAll(); server.send(200,"application/json","{\"ok\":true}");});
  server.on("/push", HTTP_GET,[]{
    bool ok=pushToGS();
    server.send(200,"application/json",String("{\"ok\":")+(ok?"true":"false")+"}");
  });
  server.begin();
}
/* ======================= */

void setupWiFi() {
  WiFi.mode(WIFI_AP_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASS);

  uint32_t t=millis();
  while (WiFi.status()!=WL_CONNECTED && millis()-t<WIFI_TIMEOUT) delay(200);

  WiFi.softAP(AP_SSID, AP_PASS);
}

void setup() {
  Serial.begin(115200);
  prefs.begin("xbio",false);

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
