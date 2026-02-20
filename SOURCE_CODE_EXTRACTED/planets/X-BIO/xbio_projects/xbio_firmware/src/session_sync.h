#pragma once
#include <Arduino.h>
#include <vector>

// BLE chunk size (max MTU - 3 bytes overhead)
#define BLE_CHUNK_SIZE 180

// Sync commands
#define SYNC_CMD_SEND_LATEST      0x01
#define SYNC_CMD_SEND_BY_FILENAME 0x02
#define SYNC_CMD_DELETE_SESSION   0x03
#define SYNC_CMD_DELETE_ALL       0x04

enum class SyncState : uint8_t {
  IDLE = 0,
  LOADING_SESSION,
  SENDING_CHUNKS,
  DELETING_FILE,
  ERROR_STATE
};

struct SyncContext {
  SyncState state = SyncState::IDLE;
  String requestedFilename;
  std::vector<uint8_t> sessionData;
  size_t chunkIndex = 0;
  size_t totalChunks = 0;
  uint32_t lastChunkTime = 0;
  String lastError;
};

extern SyncContext g_syncCtx;

// Initialize session sync module
void sessionSyncInit();

// Main loop handler - call from loop()
void sessionSyncLoop();

// Get list of all session files as JSON array
void getSessionList(String& out);

// Load session file into buffer
bool loadSessionFile(const char* filename, std::vector<uint8_t>& out);

// Send session data via BLE chunks
void bleSendSessionChunks(const std::vector<uint8_t>& data);

// Handle sync commands from BLE
void handleSyncCommand(uint8_t cmd, const uint8_t* data, size_t len);

// Delete session file
bool deleteSessionFile(const char* filename);

// Delete all session files
bool deleteAllSessions();

// Get latest session filename
String getLatestSessionFilename();
