#include <Wire.h>
#include "MPU9250.h"
#include <esp_now.h>
#include <WiFi.h>

esp_now_peer_info_t peerInfo;

MPU9250 imu;

// constante
const float alpha = 0.5; // constanta de filtrare
const float g = 9.81; // valoarea acceleratiei gravitationale (m/s^2)

// variabile
float accel_x, gyro_x, accel_y, gyro_y;
float accel_x_filtered, accel_x_unfiltered, accel_y_filtered, accel_y_unfiltered;
float theta_x, theta_y;

void sendData(uint8_t* data, size_t sizeBuff) {
  esp_now_send(peerInfo.peer_addr, data, sizeBuff);
}

void setup() {
  Serial.begin(115200);
  Wire.begin(); // init spi comm with the sensor

  MPU9250Setting setting;
  setting.accel_fs_sel = ACCEL_FS_SEL::A2G;
  setting.gyro_fs_sel = GYRO_FS_SEL::G500DPS;
  setting.fifo_sample_rate = FIFO_SAMPLE_RATE::SMPL_1000HZ;
  setting.gyro_fchoice = 0x03;
  setting.gyro_dlpf_cfg = GYRO_DLPF_CFG::DLPF_41HZ;
  setting.accel_fchoice = 0x01;
  setting.accel_dlpf_cfg = ACCEL_DLPF_CFG::DLPF_45HZ;
 
    

  imu.setup(0x68,setting);
//imu.setup(0x68);
  delay(2000);


  // Configure ESPNow
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
//  float temperature = temperatureRead();
//  Serial.print("Temperatura: ");
//  Serial.print(temperature);
//  Serial.println("°C");

  if (imu.update()) {
  accel_x = imu.getAccX()/8; // impartim la 16384 pentru a obtine acceleratia in unitati de g (9.81 m/s^2)
  gyro_x = imu.getGyroX(); // 131.0; // impartim la 131 pentru a obtine viteza unghiulara in grade/s

  accel_y = imu.getAccY()/8; // impartim la 16384 pentru a obtine acceleratia in unitati de g (9.81 m/s^2)
  gyro_y = imu.getGyroY(); // 131.0; // impartim la 131 pentru a obtine viteza unghiulara in grade/s
  String dataToSend = send_data(imu.getAccX(), imu.getAccY());
  uint8_t* buffer = (uint8_t*)dataToSend.c_str();
   Serial.println(dataToSend);
    size_t sizeBuff = sizeof(buffer) * dataToSend.length();
    sendData(buffer, sizeBuff);
    
  }
  delay(5);
  }

String send_data(float accel_x,float accel_y){
 
  // filtram acceleratia neprcesata cu un filtru pas-banda pentru a elimina zgomotul
  accel_x_unfiltered = accel_x;
  accel_x_filtered = alpha * (accel_x_filtered + gyro_x * 0.01) + (1 - alpha) * accel_x_unfiltered;
  
  accel_y_unfiltered = accel_y;
  accel_y_filtered = alpha * (accel_y_filtered + gyro_y * 0.01) + (1 - alpha) * accel_y_unfiltered;

  // calculam unghiul de inclinare al dispozitivului pe axa X fata de verticala
  theta_x = atan2(-accel_x_filtered, g) * 180 / M_PI;
  theta_y = atan2(-accel_y_filtered, g) * 180 / M_PI;

  // eliminam componenta gravitatioanala din acceleratia liniara
  accel_x_filtered = accel_x_filtered * cos(theta_x * M_PI / 180);
  Serial.println(accel_x_filtered);
  accel_y_filtered = accel_y_filtered * cos(theta_y * M_PI / 180);

//////   afisam valorile filtrate
////   Serial.print(imu.getAccX());
////   Serial.print(" ; ");
////   Serial.print(imu.getAccY());
////   Serial.print(" ; ");
////   Serial.print(imu.getRoll());
////   Serial.print(" ; ");
////   Serial.print(imu.getPitch());
////   Serial.print("\n"); 

  return  String(accel_x_filtered)+String(";")+String(accel_y_filtered)+String(";")+String(imu.getRoll())+String(";")+String(imu.getPitch());
  
}

