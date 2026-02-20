#pragma once
#include "state_machine.h"
#include <vector>

void bleServiceInit();
void bleServiceLoop();
void bleNotifyState(const DeviceContext& ctx);

// Session sync BLE functions
void bleSendChunk(const uint8_t* data, size_t len, size_t chunkIndex, size_t totalChunks);
void bleNotifySyncComplete();
void bleNotifySyncError(const String& error);
