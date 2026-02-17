#include <WiFi.h>
#include <WebServer.h>
#include <HTTPClient.h>
#include <FFat.h>
#include <Preferences.h>

/* ============ EDIT ONLY THESE ============ */
#define WIFI_SSID "ASSAF_House"
#define WIFI_PASS "103ASSAF103@"
#define ADMIN_TOKEN "MrF_XBIO_ADMIN_2025"
#define GS_URL "https://script.google.com/macros/s/AKfycbxQLEekjztihKLxbdoutsUP9UeBQ8YamrMx6-2oZfG-gD6Go5qd0H2LRNmqtaZFum4p/exec"
/* ======================================== */

#define AP_SSID "XBIO_Sentinel"
#define AP_PASS "12345678"

#define LOG_PATH "/xbio_log.csv"

#define T_PURGE 6000
#define T_SNIFF 8000
#define T_RECOVER 6000

#define PUSH_EVERY_MS 5000
#define PUSH_MAX_LINES 50
#define WIFI_TIMEOUT_MS 10000

WebServer server(80);
Preferences prefs;

enum Phase { IDLE = 0,
             PURGE = 1,
             SNIFF = 2,
             RECOVER = 3 };
Phase phase = IDLE;
bool running = false;

uint32_t phaseStart = 0;
uint32_t sniff_id = 0;
uint32_t lastPush = 0;
String session_id;

struct Sample {
  float tC, rh, pHpa;
  float gas[4];
  float lg[4];
} s;

/* ===== SENSOR (بدّلها لاحقاً ببصمتك الحقيقية) ===== */
bool readSensors() {
  s.tC = 25.0;
  s.rh = 45.0;
  s.pHpa = 1000.0;
  s.gas[0] = 10;
  s.gas[1] = 20;
  s.gas[2] = 30;
  s.gas[3] = 40;
  s.lg[0] = 1;
  s.lg[1] = 2;
  s.lg[2] = 3;
  s.lg[3] = 4;
  return true;
}
/* =================================================== */

void ensureHeader() {
  if (!FFat.exists(LOG_PATH)) {
    File f = FFat.open(LOG_PATH, FILE_WRITE);
    if (!f) return;
    f.println("schema,session_id,sniff_id,phase,ms,tC,rh,pHpa,gas0,gas1,gas2,gas3,lg0,lg1,lg2,lg3");
    f.close();
  }
}

void logCSV() {
  File f = FFat.open(LOG_PATH, FILE_APPEND);
  if (!f) return;

  f.printf(
    "1,%s,%lu,%d,%lu,%.3f,%.3f,%.3f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f\n",
    session_id.c_str(),
    sniff_id,
    (int)phase,
    millis(),
    s.tC, s.rh, s.pHpa,
    s.gas[0], s.gas[1], s.gas[2], s.gas[3],
    s.lg[0], s.lg[1], s.lg[2], s.lg[3]);
  f.close();
}

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
    if (!line.length()) continue;
    if (line.startsWith("schema,")) continue;

    rowsJson += "\"";
    for (size_t i = 0; i < line.length(); i++) {
      char c = line[i];
      if (c == '\\' || c == '"') rowsJson += "\\";
      rowsJson += c;
    }
    rowsJson += "\"";
    count++;
    if (count < PUSH_MAX_LINES) rowsJson += ",";
  }

  size_t newOffset = (size_t)f.position();
  f.close();
  rowsJson += "]";

  if (count == 0) {
    prefs.putULong("push_ofs", newOffset);
    return true;
  }

  String body = "{";
  body += "\"token\":\"" + String(ADMIN_TOKEN) + "\",";
  body += "\"session_id\":\"" + session_id + "\",";
  body += "\"log_path\":\"" + String(LOG_PATH) + "\",";
  body += "\"rows\":" + rowsJson;
  body += "}";

  HTTPClient http;
  http.setFollowRedirects(HTTPC_STRICT_FOLLOW_REDIRECTS);
  http.begin(GS_URL);
  http.addHeader("Content-Type", "application/json");
  http.addHeader("Accept", "application/json");

  int code = http.POST(body);
  String resp = http.getString();
  http.end();

  Serial.print("PUSH code=");
  Serial.println(code);
  if (resp.length() > 0) Serial.println(resp);

  // نجاح مؤكد إذا الرد فيه ok:true (حتى لو كان الكود مو 200 بسبب جوجل)
  bool okJson = (resp.indexOf("\"ok\":true") >= 0) || (resp.indexOf("\"ok\": true") >= 0);
  if (okJson || (code >= 200 && code < 300)) {
    prefs.putULong("push_ofs", newOffset);
    return true;
  }
  return false;
}

void startAll() {
  sniff_id++;
  phase = PURGE;
  phaseStart = millis();
  running = true;
}

void stopAll() {
  running = false;
  phase = IDLE;
}

void tickFSM() {
  if (!running) return;

  uint32_t now = millis();
  uint32_t elapsed = now - phaseStart;
  uint32_t dur =
    (phase == PURGE) ? T_PURGE : (phase == SNIFF)   ? T_SNIFF
                               : (phase == RECOVER) ? T_RECOVER
                                                    : 0;

  if (readSensors()) {
    if (phase == SNIFF) logCSV();
  }

  if (elapsed >= dur) {
    if (phase == PURGE) phase = SNIFF;
    else if (phase == SNIFF) phase = RECOVER;
    else phase = PURGE;
    phaseStart = now;
  }

  if (now - lastPush >= PUSH_EVERY_MS) {
    lastPush = now;
    pushToGS();
  }
}

void setupWeb() {
  server.on("/", HTTP_GET, []() {
    server.send(200, "text/html",
                "<h2>XBIO</h2>"
                "<a href='/start'>START</a> | "
                "<a href='/stop'>STOP</a> | "
                "<a href='/push'>PUSH</a> | "
                "<a href='/status'>STATUS</a>");
  });

  server.on("/start", HTTP_GET, []() {
    startAll();
    server.send(200, "application/json", "{\"ok\":true}");
  });
  server.on("/stop", HTTP_GET, []() {
    stopAll();
    server.send(200, "application/json", "{\"ok\":true}");
  });
  server.on("/push", HTTP_GET, []() {
    bool ok = pushToGS();
    server.send(200, "application/json", String("{\"ok\":") + (ok ? "true" : "false") + "}");
  });

  server.on("/status", HTTP_GET, []() {
    String j = "{";
    j += "\"wifi\":" + String(WiFi.status() == WL_CONNECTED ? "true" : "false") + ",";
    j += "\"ip\":\"" + WiFi.localIP().toString() + "\",";
    j += "\"ap\":\"" + WiFi.softAPIP().toString() + "\",";
    j += "\"running\":" + String(running ? "true" : "false") + ",";
    j += "\"phase\":" + String((int)phase) + ",";
    j += "\"sniff_id\":" + String(sniff_id);
    j += "}";
    server.send(200, "application/json", j);
  });

  server.begin();
}

void setupWiFi() {
  WiFi.mode(WIFI_AP_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASS);

  uint32_t t0 = millis();
  while (WiFi.status() != WL_CONNECTED && millis() - t0 < WIFI_TIMEOUT_MS) delay(200);

  WiFi.softAP(AP_SSID, AP_PASS);

  Serial.print("STA IP=");
  Serial.println(WiFi.localIP());
  Serial.print("AP  IP=");
  Serial.println(WiFi.softAPIP());
}

void setup() {
  Serial.begin(115200);
  prefs.begin("xbio", false);

  setupWiFi();

  // مهم: false حتى ما يفرمت تلقائياً
  FFat.begin(false);
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
