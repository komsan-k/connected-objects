/*
 * ESP32 BLE Peripheral: Receive counter via Write characteristic.
 * Name: ESP32_BLE_Counter
 * Service UUID:        e1f4046e-2a5a-4a5b-8ee3-7c2f31d5b5a1
 * Write Char UUID:     e1f40470-2a5a-4a5b-8ee3-7c2f31d5b5a1
 *
 * Payload format (from Python/bleak): ASCII string of a non-negative integer, e.g., "42".
 */

#include <BLEDevice.h>
#include <BLEServer.h>
#include <BLEUtils.h>
#include <BLE2902.h>

#define SERVICE_UUID     "e1f4046e-2a5a-4a5b-8ee3-7c2f31d5b5a1"
#define WRITE_CHAR_UUID  "e1f40470-2a5a-4a5b-8ee3-7c2f31d5b5a1"

#ifndef LED_BUILTIN
#define LED_BUILTIN 2   // Many ESP32 dev boards use GPIO 2 for onboard LED
#endif

BLECharacteristic* pWrite = nullptr;

void blinkAck(uint8_t times=1) {
  for (uint8_t i=0;i<times;i++) {
    digitalWrite(LED_BUILTIN, HIGH);
    delay(30);
    digitalWrite(LED_BUILTIN, LOW);
    delay(60);
  }
}

int parseIntSafe(const std::string& s, bool& ok) {
  ok = false;
  if (s.empty()) return 0;
  long val = 0;
  for (char c : s) {
    if (c < '0' || c > '9') return 0;
    val = val*10 + (c - '0');
    if (val > 2147483647L) return 0;
  }
  ok = true;
  return (int)val;
}

class WriteCallbacks: public BLECharacteristicCallbacks {
  void onWrite(BLECharacteristic* ch) override {
    std::string v = ch->getValue();
    bool ok=false;
    int cnt = parseIntSafe(v, ok);
    Serial.print("Write payload: \"");
    for (auto c: v) Serial.print(c);
    Serial.print("\"");
    if (ok) {
      Serial.printf("  parsed=%d\n", cnt);
      blinkAck(1);
    } else {
      Serial.println("  (non-integer payload)");
      blinkAck(2);
    }
  }
};

class ServerCallbacks: public BLEServerCallbacks {
  void onConnect(BLEServer* pServer) override {}
  void onDisconnect(BLEServer* pServer) override {
    // Resume advertising after central disconnects
    pServer->getAdvertising()->start();
  }
};

void setup() {
  Serial.begin(115200);
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, LOW);

  BLEDevice::init("ESP32_BLE_Counter");
  BLEServer* server = BLEDevice::createServer();
  server->setCallbacks(new ServerCallbacks());

  BLEService* svc = server->createService(SERVICE_UUID);

  pWrite = svc->createCharacteristic(
    WRITE_CHAR_UUID,
    BLECharacteristic::PROPERTY_WRITE | BLECharacteristic::PROPERTY_WRITE_NR
  );
  pWrite->setCallbacks(new WriteCallbacks());

  svc->start();

  BLEAdvertising* adv = BLEDevice::getAdvertising();
  adv->addServiceUUID(SERVICE_UUID);
  adv->setScanResponse(true);
  BLEDevice::startAdvertising();

  Serial.println("BLE advertising as ESP32_BLE_Counter");
}

void loop() {
  delay(100);
}
