#include "ble_service.h"
#include "session_sync.h"
#include <NimBLEDevice.h>

static NimBLEServer* pServer = nullptr;
static NimBLECharacteristic* pCtrlChar = nullptr;
static NimBLECharacteristic* pStatusChar = nullptr;
static NimBLECharacteristic* pSessionListChar = nullptr;
static NimBLECharacteristic* pSessionDataChar = nullptr;
static NimBLECharacteristic* pSyncCtrlChar = nullptr;

static const char* SERVICE_UUID         = "12345678-1234-5678-1234-56789abc0001";
static const char* CTRL_CHAR_UUID       = "12345678-1234-5678-1234-56789abc0002";
static const char* STATUS_CHAR_UUID     = "12345678-1234-5678-1234-56789abc0003";
static const char* SESSION_LIST_UUID    = "12345678-1234-5678-1234-56789abc0004";
static const char* SESSION_DATA_UUID    = "12345678-1234-5678-1234-56789abc0005";
static const char* SYNC_CTRL_UUID       = "12345678-1234-5678-1234-56789abc0006";

class CtrlCallback : public NimBLECharacteristicCallbacks {
  void onWrite(NimBLECharacteristic* c) override {
    std::string v = c->getValue();
    if (v.size() < 1) return;
    uint8_t cmd = v[0];
    if (cmd == 0x01) {
      stateMachineOnTrigger();
    }
  }
};

class SyncCtrlCallback : public NimBLECharacteristicCallbacks {
  void onWrite(NimBLECharacteristic* c) override {
    std::string v = c->getValue();
    if (v.size() < 1) return;
    uint8_t cmd = v[0];
    const uint8_t* data = (v.size() > 1) ? (const uint8_t*)&v[1] : nullptr;
    size_t dataLen = (v.size() > 1) ? (v.size() - 1) : 0;
    handleSyncCommand(cmd, data, dataLen);
  }
};

class SessionListCallback : public NimBLECharacteristicCallbacks {
  void onRead(NimBLECharacteristic* c) override {
    String sessionList;
    getSessionList(sessionList);
    c->setValue(sessionList.c_str());
  }
};

void bleServiceInit() {
  NimBLEDevice::init("XBIO-S3");
  NimBLEDevice::setPower(ESP_PWR_LVL_P9);
  pServer = NimBLEDevice::createServer();
  NimBLEService* svc = pServer->createService(SERVICE_UUID);

  // Control characteristic (original)
  pCtrlChar = svc->createCharacteristic(
    CTRL_CHAR_UUID,
    NIMBLE_PROPERTY::WRITE
  );
  pCtrlChar->setCallbacks(new CtrlCallback());

  // Status characteristic (original)
  pStatusChar = svc->createCharacteristic(
    STATUS_CHAR_UUID,
    NIMBLE_PROPERTY::READ | NIMBLE_PROPERTY::NOTIFY
  );

  // Session List characteristic (NEW)
  pSessionListChar = svc->createCharacteristic(
    SESSION_LIST_UUID,
    NIMBLE_PROPERTY::READ
  );
  pSessionListChar->setCallbacks(new SessionListCallback());

  // Session Data characteristic (NEW)
  pSessionDataChar = svc->createCharacteristic(
    SESSION_DATA_UUID,
    NIMBLE_PROPERTY::READ | NIMBLE_PROPERTY::NOTIFY
  );

  // Sync Control characteristic (NEW)
  pSyncCtrlChar = svc->createCharacteristic(
    SYNC_CTRL_UUID,
    NIMBLE_PROPERTY::WRITE
  );
  pSyncCtrlChar->setCallbacks(new SyncCtrlCallback());

  svc->start();
  pServer->getAdvertising()->addServiceUUID(SERVICE_UUID);
  pServer->getAdvertising()->start();

  Serial.println("[BLE] Service started with sync characteristics");
}

void bleServiceLoop() {
  // NimBLE يعمل في الخلفية؛ لا حاجة لمعالجة مستمرة هنا
}

void bleNotifyState(const DeviceContext& ctx) {
  if (!pStatusChar) return;
  uint8_t payload[3];
  payload[0] = (uint8_t)ctx.state;
  payload[1] = (uint8_t)(ctx.sample_buffer ? (ctx.sample_buffer->count & 0xFF) : 0);
  payload[2] = (uint8_t)ctx.last_error;
  pStatusChar->setValue(payload, sizeof(payload));
  pStatusChar->notify();
}

void bleSendChunk(const uint8_t* data, size_t len, size_t chunkIndex, size_t totalChunks) {
  if (!pSessionDataChar) return;

  // Packet format: [chunkIndex(2)] [totalChunks(2)] [data...]
  uint8_t packet[BLE_CHUNK_SIZE + 4];
  packet[0] = (chunkIndex >> 8) & 0xFF;
  packet[1] = chunkIndex & 0xFF;
  packet[2] = (totalChunks >> 8) & 0xFF;
  packet[3] = totalChunks & 0xFF;
  
  memcpy(packet + 4, data, len);
  
  pSessionDataChar->setValue(packet, len + 4);
  pSessionDataChar->notify();
  
  Serial.printf("[BLE] Sent chunk %u/%u (%u bytes)\n", 
                chunkIndex + 1, totalChunks, len);
}

void bleNotifySyncComplete() {
  if (!pSessionDataChar) return;
  
  // Send completion marker: chunk 0xFFFF/0xFFFF
  uint8_t packet[4] = {0xFF, 0xFF, 0xFF, 0xFF};
  pSessionDataChar->setValue(packet, 4);
  pSessionDataChar->notify();
  
  Serial.println("[BLE] Sync complete notification sent");
}

void bleNotifySyncError(const String& error) {
  if (!pSessionDataChar) return;
  
  // Send error marker: chunk 0xFFFE/0xFFFE + error message
  uint8_t packet[BLE_CHUNK_SIZE + 4];
  packet[0] = 0xFF;
  packet[1] = 0xFE;
  packet[2] = 0xFF;
  packet[3] = 0xFE;
  
  size_t errorLen = min((size_t)error.length(), (size_t)BLE_CHUNK_SIZE);
  memcpy(packet + 4, error.c_str(), errorLen);
  
  pSessionDataChar->setValue(packet, errorLen + 4);
  pSessionDataChar->notify();
  
  Serial.printf("[BLE] Sync error notification sent: %s\n", error.c_str());
}
