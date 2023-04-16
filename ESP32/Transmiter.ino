//Transmitter ---> COM5

#include <esp_now.h>
#include <WiFi.h>
#include <Wire.h>
#include "MPU9250.h"

MPU9250 mpu; // Pinii 21 si 22 pentru SDA respectiv SCL


esp_now_peer_info_t peerInfo;

void sendData(uint8_t* data, size_t sizeBuff) {
  esp_now_send(peerInfo.peer_addr, data, sizeBuff);
}

//void onDataSent(const uint8_t *mac_addr, esp_now_send_status_t status) {
//  Serial.print("\r\nLast Packet Send Status:\t");
//  Serial.println(status == ESP_NOW_SEND_SUCCESS ? "Delivery Success" : "Delivery Fail");
//}

void setup() {
  Serial.begin(115200);
  Wire.begin();
  
  mpu.setup(0x68);
  delay(2000);
  mpu.calibrateAccelGyro();
  
  
  WiFi.mode(WIFI_STA);
  WiFi.disconnect();
  if (esp_now_init() != ESP_OK) {
    Serial.println("Error initializing ESP-NOW");
    return;
  }

  memset(&peerInfo, 0, sizeof(peerInfo));
  peerInfo.channel = 0;
  peerInfo.encrypt = false;
  memcpy(peerInfo.peer_addr, "\xFF\xFF\xFF\xFF\xFF\xFF", ESP_NOW_ETH_ALEN);
  esp_now_add_peer(&peerInfo);
}

void loop() {

  if (mpu.update()) {
    
      String dataToSend = print_data();
      uint8_t* buffer = (uint8_t*)dataToSend.c_str();
      Serial.println(dataToSend);
// Functie pentru mediere -> afisare pe LCD
    
      size_t sizeBuff = sizeof(buffer) * dataToSend.length();
      sendData(buffer, sizeBuff);
      
    }
  }
  

// pentru functiile Yaw Pitch si Roll datele sunt in radiani; 
//daca vrem grade trebuie folosim getGyroX

String print_data() {
  return  String(mpu.getQuaternionX())+String(";")+String(mpu.getAccX())
  +String(";")+String(mpu.getLinearAccX())+String(";")+String(mpu.getQuaternionY())+String(";")+String(mpu.getAccY())
  +String(";")+String(mpu.getLinearAccY());
};
