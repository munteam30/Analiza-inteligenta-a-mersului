#include <Wire.h>
#include <MPU9250.h>
#include <SimpleKalmanFilter.h>
#include <BluetoothSerial.h>

BluetoothSerial SerialBT;
MPU9250 IMU(Wire, 0x68);  // Adresa I2C a senzorului MPU9250
SimpleKalmanFilter kfAccelX(1, 1, 0.01);
SimpleKalmanFilter kfAccelY(1, 1, 0.01);

void sendData(String data) {
  SerialBT.println(data);
  Serial.println(data);
}

void setup() {
  Serial.begin(115200);
  Wire.begin();
  IMU.begin();
  IMU.setAccelRange(MPU9250::ACCEL_RANGE_2G);
  IMU.setGyroRange(MPU9250::GYRO_RANGE_1000DPS);
  IMU.setDlpfBandwidth(MPU9250::DLPF_BANDWIDTH_20HZ);
  IMU.setSrd(0);
  kfAccelX.setProcessNoise(0.1);
  kfAccelY.setProcessNoise(0.1);

  SerialBT.begin("ESP32_BT");  // Numele dispozitivului Bluetooth
}

void loop() {
  String dataToSend = send_data();
  Serial.print(dataToSend);
  sendData(dataToSend);
  delay(1);
}

String send_data() {
  IMU.readSensor();

  float ax = IMU.getAccelX_mss();
  float ay = IMU.getAccelY_mss();
  float az = IMU.getAccelZ_mss();
  float accelMagnitude = sqrt(ax * ax + ay * ay + az * az);
  float g = 9.81;

  float relativeAccelX = ax - g * (ax / accelMagnitude);
  float relativeAccelY = ay - g * (ay / accelMagnitude);
  float relativeAccelZ = az - g * (az / accelMagnitude);

  float gx = IMU.getGyroX_rads();
  float gy = IMU.getGyroY_rads();
  float gz = IMU.getGyroZ_rads();
  float pitch = atan2(relativeAccelY, sqrt(relativeAccelX * relativeAccelX + relativeAccelZ * relativeAccelZ)) * 180 / PI;
  float roll = atan2(-relativeAccelX, relativeAccelZ) * 180 / PI;

  kfAccelX.updateEstimate(ax);
  float accelXFiltered = ax - kfAccelX.updateEstimate(ax);

  kfAccelY.updateEstimate(ay);
  float accelYFiltered = ay - kfAccelY.updateEstimate(ay);

  return "ST" + String(accelXFiltered, 4) + String(";") + String(accelYFiltered, 4) + String(";") + String(pitch, 4) + String(";") + String(roll, 4) + String(";") + "GT";
}
