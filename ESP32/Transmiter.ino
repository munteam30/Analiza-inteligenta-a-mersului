//Transmitter ---> COM5

#include <esp_now.h>
#include <WiFi.h>
#include <Wire.h>
#include "MPU9250.h"

#include <TFT_eSPI.h> // Graphics and font library for ST7735 driver chip
#include <SPI.h>


MPU9250 mpu; // Pinii 21 si 22 pentru SDA respectiv SCL


TFT_eSPI tft = TFT_eSPI();  // Invoke library, pins defined in User_Setup.h

esp_now_peer_info_t peerInfo;

void sendData(uint8_t* data, size_t sizeBuff) {
  esp_now_send(peerInfo.peer_addr, data, sizeBuff);
}

//void onDataSent(const uint8_t *mac_addr, esp_now_send_status_t status) {
//  Serial.print("\r\nLast Packet Send Status:\t");
//  Serial.println(status == ESP_NOW_SEND_SUCCESS ? "Delivery Success" : "Delivery Fail");
//}

void setup() {
  Serial.begin(9600);
  

  tft.init();
  tft.setRotation(2);
  tft.fillScreen(TFT_BLACK);

  tft.setTextSize(2);
  tft.setTextColor(TFT_WHITE);

  tft.setCursor(0, 0);
  tft.println("Accel x:");

  tft.setCursor(0, 32);
  tft.println("Accel y:");


  tft.setCursor(0, 96);
  tft.println("Gyro x:");


  tft.setCursor(0, 128);
  tft.println("Gyro y:");

  tft.setTextColor(TFT_YELLOW);

  Wire.begin();

  mpu.setup(0x68);
  //delay(2000);

// Serial.println("Accel Gyro calibration will start in 5sec.");
//  Serial.println("Please leave the device still on the flat plane.");
  //mpu.verbose(true);
  //(5000);
  //mpu.calibrateAccelGyro();
  //mpu.verbose(false);
  
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

int cont = 0;
int no_samples = 200;

float accel_x_sum = 0, accel_x_avg = 0, accel_y_sum = 0, accel_y_avg = 0;
float gyro_x_sum = 0, gyro_x_avg = 0, gyro_y_sum = 0, gyro_y_avg = 0 ;

void loop() {

  if (cont == no_samples) {

    accel_x_avg = accel_x_sum / no_samples;
    accel_y_avg = accel_y_sum / no_samples;
    gyro_x_avg = gyro_x_sum / no_samples;
    gyro_y_avg = gyro_y_sum / no_samples;

    cont = 0;
    accel_x_sum = 0;
    accel_y_sum = 0;
    gyro_x_sum = 0;
    gyro_y_sum = 0;

    tft.setCursor(0, 0);
    //     tft.fillScreen(TFT_BLACK);

    tft.fillRect(0, 16, 128, 16, TFT_BLACK);
    tft.fillRect(0, 48, 128, 16, TFT_BLACK);
    tft.fillRect(0, 112, 128, 16, TFT_BLACK);
    tft.fillRect(0, 144, 128, 16, TFT_BLACK);

    tft.setCursor(0, 16);
    tft.println(accel_x_avg);
    tft.setCursor(0, 48);
    tft.println(accel_y_avg);
    tft.setCursor(0, 112);
    tft.println(gyro_x_avg);
    tft.setCursor(0, 144);
    tft.println(gyro_y_avg);

  } else if (mpu.update()) {

    String dataToSend = print_data();
    uint8_t* buffer = (uint8_t*)dataToSend.c_str();
    Serial.println(dataToSend);
    
//    Serial.print((float)0);
//    Serial.print((float)mpu.getAccX());
//    Serial.print((float)mpu.getAccY());
//    Serial.print((float)mpu.getGyroX());
//    Serial.println((float)mpu.getGyroY());
    // Functie pentru mediere -> afisare pe LCD
    cont++;

    accel_x_sum = accel_x_sum + mpu.getAccX();
    accel_y_sum = accel_y_sum + mpu.getAccY();
    gyro_x_sum = gyro_x_sum + mpu.getGyroX();
    gyro_y_sum = gyro_y_sum + mpu.getGyroY();

    size_t sizeBuff = sizeof(buffer) * dataToSend.length();
    sendData(buffer, sizeBuff);

  }
}


// pentru functiile Yaw Pitch si Roll datele sunt in radiani;
//daca vrem grade trebuie folosim getGyroX

String print_data() {
  return  String(mpu.getGyroX()) + ";" + String(mpu.getGyroY())
         + ";" + String(mpu.getGyroZ());
//+ String(";")+"\t" + String(mpu.getRoll()) + "," + String(mpu.getPitch())
//          + "," + String(mpu.getYaw()) + String(";")+"\t" + String(mpu.getLinearAccX()) + String(";") + String(mpu.getLinearAccY()) + String(";") + String(mpu.getLinearAccZ());

  //  return String(mpu.getGyroY());
}
