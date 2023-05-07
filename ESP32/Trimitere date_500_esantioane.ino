#include <Wire.h>
#include <MPU9250.h>
#include <SimpleKalmanFilter.h>

#include <esp_now.h>
#include <WiFi.h>

esp_now_peer_info_t peerInfo;

MPU9250 IMU(Wire,0x68);  // Adresa I2C a senzorului MPU9250
SimpleKalmanFilter kfAccelX(1, 1, 0.01);
SimpleKalmanFilter kfAccelY(1, 1, 0.01);


void sendData(uint8_t* data, size_t sizeBuff) {
  esp_now_send(peerInfo.peer_addr, data, sizeBuff);
}

void setup() {
  Serial.begin(115200);
  Wire.begin();
  IMU.begin();
   // setting the accelerometer full scale range to +/-8G 
  IMU.setAccelRange(MPU9250::ACCEL_RANGE_2G);
  // setting the gyroscope full scale range to +/-500 deg/s
  IMU.setGyroRange(MPU9250::GYRO_RANGE_1000DPS);
  // setting DLPF bandwidth to 20 Hz
  IMU.setDlpfBandwidth(MPU9250::DLPF_BANDWIDTH_20HZ);
  // setting SRD to 19 for a 50 Hz update rate
  IMU.setSrd(0);
  kfAccelX.setProcessNoise(0.1);
  kfAccelY.setProcessNoise(0.1);

   // Configure ESPNow
  WiFi.mode(WIFI_STA);
  WiFi.disconnect();
  if (esp_now_init() != ESP_OK) {
    Serial.println("Error initializing ESP-NOW");
    return;}

  memset(&peerInfo, 0, sizeof(peerInfo));
  peerInfo.channel = 0;
  peerInfo.encrypt = false;
  memcpy(peerInfo.peer_addr, "\xFF\xFF\xFF\xFF\xFF\xFF", ESP_NOW_ETH_ALEN);
  esp_now_add_peer(&peerInfo);
}

void loop() {

    String dataToSend = send_data();
    uint8_t* buffer = (uint8_t*)dataToSend.c_str();
//   Serial.println(dataToSend);
    size_t sizeBuff = sizeof(buffer) * dataToSend.length();
    sendData(buffer, sizeBuff);
}
String send_data(){
  IMU.readSensor();

  // Obținerea accelerației relative
  float ax = IMU.getAccelX_mss();
  float ay = IMU.getAccelY_mss();
  float az = IMU.getAccelZ_mss();
  float accelMagnitude = sqrt(ax*ax + ay*ay + az*az);
  float g = 9.81;  // accelerația gravitatională standard



  float relativeAccelX = ax - g*(ax/accelMagnitude);
  float relativeAccelY = ay - g*(ay/accelMagnitude);
  float relativeAccelZ = az - g*(az/accelMagnitude);

  // Obținerea unghiului de înclinare (în grade)
  float gx = IMU.getGyroX_rads();
  float gy = IMU.getGyroY_rads();
  float gz = IMU.getGyroZ_rads();
  float pitch = atan2(relativeAccelY, sqrt(relativeAccelX*relativeAccelX + relativeAccelZ*relativeAccelZ))*180/PI;
  float roll = atan2(-relativeAccelX, relativeAccelZ)*180/PI;

  // Afisarea rezultatelor
  kfAccelX.updateEstimate(ax);
  float accelXFiltered =ax - kfAccelX.updateEstimate(ax);
  // Serial.print(accelXFiltered);

  // Serial.print(";");
  kfAccelY.updateEstimate(ay);
  float accelYFiltered =ay - kfAccelY.updateEstimate(ay);
  // Serial.print(accelYFiltered);

  // Serial.print(";");
  Serial.print(pitch);

  // Serial.print(";");
  Serial.println(roll);
  return String(accelXFiltered)+String(";")+String(accelXFiltered)+String(";")+String(pitch)+String(";")+String(roll);

}
