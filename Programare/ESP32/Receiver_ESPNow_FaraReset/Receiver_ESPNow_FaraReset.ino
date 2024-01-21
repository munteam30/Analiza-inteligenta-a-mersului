//Receiver ---> COM5
#include <esp_now.h>
#include <WiFi.h>

uint8_t receivedData[32];
int data_len = 32;

void onDataReceived(const uint8_t *mac_addr, const uint8_t *data, int data_len) {
char buff[data_len + 1];
memcpy(buff, data, data_len);
buff[data_len] = '\0';
String buffStr = String(buff) + "\n";
Serial.print(buffStr);
delay(1);
}

void setup() {
Serial.begin(115200);
WiFi.mode(WIFI_STA);
if (esp_now_init() != ESP_OK) {
Serial.println("Error initializing ESP-NOW");
return;
}
esp_now_register_recv_cb(onDataReceived);
}

void loop() {
}