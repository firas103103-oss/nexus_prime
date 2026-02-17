#include "session_sync.h"
#include "ble_service.h"
#include <LittleFS.h>
#include <ArduinoJson.h>

SyncContext g_syncCtx;

// Delay between chunks (ms) to avoid overwhelming BLE
#define CHUNK_DELAY_MS 50

void sessionSyncInit() {
  g_syncCtx.state = SyncState::IDLE;
  g_syncCtx.chunkIndex = 0;
  g_syncCtx.totalChunks = 0;
  g_syncCtx.sessionData.clear();
  g_syncCtx.requestedFilename = "";
  Serial.println("[SYNC] Session sync initialized");
}

void sessionSyncLoop() {
  switch (g_syncCtx.state) {
    case SyncState::IDLE:
      // Nothing to do
      break;

    case SyncState::LOADING_SESSION: {
      Serial.printf("[SYNC] Loading session: %s\n", g_syncCtx.requestedFilename.c_str());
      
      if (!loadSessionFile(g_syncCtx.requestedFilename.c_str(), g_syncCtx.sessionData)) {
        Serial.println("[SYNC] Failed to load session file");
        g_syncCtx.state = SyncState::ERROR_STATE;
        g_syncCtx.lastError = "Load failed";
        bleNotifySyncError(g_syncCtx.lastError);
        break;
      }

      if (g_syncCtx.sessionData.size() == 0) {
        Serial.println("[SYNC] Session file is empty");
        g_syncCtx.state = SyncState::ERROR_STATE;
        g_syncCtx.lastError = "Empty file";
        bleNotifySyncError(g_syncCtx.lastError);
        break;
      }

      Serial.printf("[SYNC] Loaded %u bytes\n", g_syncCtx.sessionData.size());
      g_syncCtx.chunkIndex = 0;
      g_syncCtx.totalChunks = (g_syncCtx.sessionData.size() + BLE_CHUNK_SIZE - 1) / BLE_CHUNK_SIZE;
      g_syncCtx.state = SyncState::SENDING_CHUNKS;
      g_syncCtx.lastChunkTime = millis();
      Serial.printf("[SYNC] Preparing %u chunks\n", g_syncCtx.totalChunks);
      break;
    }

    case SyncState::SENDING_CHUNKS: {
      uint32_t now = millis();
      if (now - g_syncCtx.lastChunkTime < CHUNK_DELAY_MS) {
        break; // Wait for delay
      }

      if (g_syncCtx.chunkIndex >= g_syncCtx.totalChunks) {
        Serial.println("[SYNC] All chunks sent");
        g_syncCtx.sessionData.clear();
        g_syncCtx.state = SyncState::IDLE;
        bleNotifySyncComplete();
        break;
      }

      // Calculate chunk boundaries
      size_t offset = g_syncCtx.chunkIndex * BLE_CHUNK_SIZE;
      size_t remaining = g_syncCtx.sessionData.size() - offset;
      size_t chunkSize = (remaining > BLE_CHUNK_SIZE) ? BLE_CHUNK_SIZE : remaining;

      // Send chunk
      bleSendChunk(g_syncCtx.sessionData.data() + offset, chunkSize, 
                   g_syncCtx.chunkIndex, g_syncCtx.totalChunks);

      g_syncCtx.chunkIndex++;
      g_syncCtx.lastChunkTime = now;
      break;
    }

    case SyncState::DELETING_FILE: {
      Serial.printf("[SYNC] Deleting session: %s\n", g_syncCtx.requestedFilename.c_str());
      
      if (deleteSessionFile(g_syncCtx.requestedFilename.c_str())) {
        Serial.println("[SYNC] Delete successful");
        g_syncCtx.state = SyncState::IDLE;
        bleNotifySyncComplete();
      } else {
        Serial.println("[SYNC] Delete failed");
        g_syncCtx.state = SyncState::ERROR_STATE;
        g_syncCtx.lastError = "Delete failed";
        bleNotifySyncError(g_syncCtx.lastError);
      }
      break;
    }

    case SyncState::ERROR_STATE:
      // Stay in error state until next command
      break;
  }
}

void getSessionList(String& out) {
  File root = LittleFS.open("/sessions");
  if (!root || !root.isDirectory()) {
    out = "[]";
    return;
  }

  StaticJsonDocument<2048> doc;
  JsonArray array = doc.to<JsonArray>();

  File file = root.openNextFile();
  while (file) {
    if (!file.isDirectory()) {
      String filename = file.name();
      // Remove path prefix if present
      int lastSlash = filename.lastIndexOf('/');
      if (lastSlash >= 0) {
        filename = filename.substring(lastSlash + 1);
      }
      array.add(filename);
    }
    file = root.openNextFile();
  }

  serializeJson(doc, out);
  Serial.printf("[SYNC] Session list: %s\n", out.c_str());
}

bool loadSessionFile(const char* filename, std::vector<uint8_t>& out) {
  out.clear();

  String path = "/sessions/";
  path += filename;

  File f = LittleFS.open(path, "r");
  if (!f) {
    Serial.printf("[SYNC] Failed to open: %s\n", path.c_str());
    return false;
  }

  size_t fileSize = f.size();
  if (fileSize == 0) {
    f.close();
    return false;
  }

  out.resize(fileSize);
  size_t bytesRead = f.read(out.data(), fileSize);
  f.close();

  if (bytesRead != fileSize) {
    Serial.printf("[SYNC] Read mismatch: %u/%u\n", bytesRead, fileSize);
    out.clear();
    return false;
  }

  return true;
}

void bleSendSessionChunks(const std::vector<uint8_t>& data) {
  if (g_syncCtx.state != SyncState::IDLE) {
    Serial.println("[SYNC] Already syncing, ignoring request");
    return;
  }

  g_syncCtx.sessionData = data;
  g_syncCtx.chunkIndex = 0;
  g_syncCtx.totalChunks = (data.size() + BLE_CHUNK_SIZE - 1) / BLE_CHUNK_SIZE;
  g_syncCtx.state = SyncState::SENDING_CHUNKS;
  g_syncCtx.lastChunkTime = millis();
}

void handleSyncCommand(uint8_t cmd, const uint8_t* data, size_t len) {
  Serial.printf("[SYNC] Command received: 0x%02X\n", cmd);

  if (g_syncCtx.state != SyncState::IDLE && g_syncCtx.state != SyncState::ERROR_STATE) {
    Serial.println("[SYNC] Busy, ignoring command");
    return;
  }

  switch (cmd) {
    case SYNC_CMD_SEND_LATEST: {
      String latest = getLatestSessionFilename();
      if (latest.length() == 0) {
        Serial.println("[SYNC] No sessions available");
        g_syncCtx.lastError = "No sessions";
        bleNotifySyncError(g_syncCtx.lastError);
        break;
      }
      g_syncCtx.requestedFilename = latest;
      g_syncCtx.state = SyncState::LOADING_SESSION;
      break;
    }

    case SYNC_CMD_SEND_BY_FILENAME: {
      if (len == 0 || data == nullptr) {
        Serial.println("[SYNC] No filename provided");
        g_syncCtx.lastError = "No filename";
        bleNotifySyncError(g_syncCtx.lastError);
        break;
      }
      g_syncCtx.requestedFilename = String((const char*)data, len);
      g_syncCtx.state = SyncState::LOADING_SESSION;
      break;
    }

    case SYNC_CMD_DELETE_SESSION: {
      if (len == 0 || data == nullptr) {
        Serial.println("[SYNC] No filename provided");
        g_syncCtx.lastError = "No filename";
        bleNotifySyncError(g_syncCtx.lastError);
        break;
      }
      g_syncCtx.requestedFilename = String((const char*)data, len);
      g_syncCtx.state = SyncState::DELETING_FILE;
      break;
    }

    case SYNC_CMD_DELETE_ALL: {
      Serial.println("[SYNC] Deleting all sessions");
      if (deleteAllSessions()) {
        Serial.println("[SYNC] All sessions deleted");
        bleNotifySyncComplete();
      } else {
        Serial.println("[SYNC] Failed to delete all sessions");
        g_syncCtx.lastError = "Delete all failed";
        bleNotifySyncError(g_syncCtx.lastError);
      }
      break;
    }

    default:
      Serial.printf("[SYNC] Unknown command: 0x%02X\n", cmd);
      g_syncCtx.lastError = "Unknown cmd";
      bleNotifySyncError(g_syncCtx.lastError);
      break;
  }
}

bool deleteSessionFile(const char* filename) {
  String path = "/sessions/";
  path += filename;

  if (!LittleFS.exists(path)) {
    Serial.printf("[SYNC] File not found: %s\n", path.c_str());
    return false;
  }

  return LittleFS.remove(path);
}

bool deleteAllSessions() {
  File root = LittleFS.open("/sessions");
  if (!root || !root.isDirectory()) {
    Serial.println("[SYNC] Sessions directory not found");
    return false;
  }

  bool allDeleted = true;
  File file = root.openNextFile();
  while (file) {
    if (!file.isDirectory()) {
      String path = String(file.path());
      file.close();
      
      if (!LittleFS.remove(path)) {
        Serial.printf("[SYNC] Failed to delete: %s\n", path.c_str());
        allDeleted = false;
      } else {
        Serial.printf("[SYNC] Deleted: %s\n", path.c_str());
      }
      
      file = root.openNextFile();
    } else {
      file = root.openNextFile();
    }
  }

  return allDeleted;
}

String getLatestSessionFilename() {
  File root = LittleFS.open("/sessions");
  if (!root || !root.isDirectory()) {
    return "";
  }

  String latestFile = "";
  time_t latestTime = 0;

  File file = root.openNextFile();
  while (file) {
    if (!file.isDirectory()) {
      time_t fileTime = file.getLastWrite();
      if (fileTime > latestTime) {
        latestTime = fileTime;
        latestFile = file.name();
        
        // Remove path prefix if present
        int lastSlash = latestFile.lastIndexOf('/');
        if (lastSlash >= 0) {
          latestFile = latestFile.substring(lastSlash + 1);
        }
      }
    }
    file = root.openNextFile();
  }

  return latestFile;
}
