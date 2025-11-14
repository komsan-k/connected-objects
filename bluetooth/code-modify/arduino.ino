#include <Wire.h>
#include <BLEDevice.h>
#include <BLEUtils.h>
#include <BLEServer.h>
#include <BLE2902.h>

#define LM73_ADDR        0x4D
#define SERVICE_UUID     "e1f4046e-2a5a-4a5b-8ee3-7c2f31d5b5a1"
#define CHARACTERISTIC_UUID "e1f4046f-2a5a-4a5b-8ee3-7c2f31d5b5a1"

BLECharacteristic *pCharacteristic;
bool deviceConnected = false;

class MyServerCallbacks : public BLEServerCallbacks {
  void onConnect(BLEServer* pServer) override {
    deviceConnected = true;
    Serial.println("✅ BLE client connected");
  }
  void onDisconnect(BLEServer* pServer) override {
    deviceConnected = false;
    Serial.println("❌ BLE client disconnected");
    pServer->getAdvertising()->start();
    Serial.println("🔁 Restart advertising");
  }
};

float readLM73() {
  Wire.beginTransmission(LM73_ADDR);
  Wire.write(0x00);
  Wire.endTransmission();
  Wire.requestFrom(LM73_ADDR, 2);

  if (Wire.available() == 2) {
    uint16_t raw = (Wire.read() << 8) | Wire.read();
    return (raw >> 5) *  0.25f;   // 0.25 °C/LSB if 11-bit and 0.0625 °C/LSB if 13-bit
  }
  return -100.0f;
}

void setup() {
  Serial.begin(115200);
  delay(1000);

  // I2C pins 
  Wire.begin(4, 5);   // SDA=4, SCL=5

  BLEDevice::init("ESP32_BLE_LM73"); // Modify a device name

  Serial.print("My ESP32 BLE MAC => ");
  Serial.println(BLEDevice::getAddress().toString().c_str());

  BLEServer *pServer = BLEDevice::createServer();
  pServer->setCallbacks(new MyServerCallbacks());

  BLEService *pService = pServer->createService(SERVICE_UUID);

  pCharacteristic = pService->createCharacteristic(
    CHARACTERISTIC_UUID,
    BLECharacteristic::PROPERTY_READ | BLECharacteristic::PROPERTY_NOTIFY
  );

  // IMPORTANT: CCCD descriptor so Bleak can enable notify
  pCharacteristic->addDescriptor(new BLE2902());

  pCharacteristic->setValue("LM73 Ready");
  pService->start();

  pServer->getAdvertising()->start();
  Serial.println("✅ BLE advertising: ESP32_BLE_LM73_KK");
}

void loop() {
  if (deviceConnected) {
    float tempC = readLM73();
    char buffer[32];
    snprintf(buffer, sizeof(buffer), "Temp: %.2f C", tempC);
    pCharacteristic->setValue(buffer);
    pCharacteristic->notify();
    Serial.println(buffer);
    delay(2000);
  } else {
    delay(500);
  }
}
