#include <Wire.h>
#include "MPU9250.h"
// Pentru instalarea librariei am optat pentru libraria din Arduino IDE

MPU9250 imu;

// constante
const float alpha = 0.5; // constanta de filtrare
const float g = 9.81; // valoarea acceleratiei gravitationale (m/s^2)

// variabile
float accel_x, gyro_x, accel_y, gyro_y;
float accel_x_filtered, accel_x_unfiltered, accel_y_filtered, accel_y_unfiltered;
float theta_x, theta_y;

void setup() {
  Serial.begin(9600);
  Wire.begin(); // init spi comm with the sensor

  MPU9250Setting setting;
  setting.accel_fs_sel = ACCEL_FS_SEL::A2G;
  setting.gyro_fs_sel = GYRO_FS_SEL::G500DPS;
  setting.fifo_sample_rate = FIFO_SAMPLE_RATE::SMPL_1000HZ;
  setting.gyro_fchoice = 0x03;
  setting.gyro_dlpf_cfg = GYRO_DLPF_CFG::DLPF_41HZ;
  setting.accel_fchoice = 0x00;
  setting.accel_dlpf_cfg = ACCEL_DLPF_CFG::DLPF_45HZ;

  imu.setup(0x68,settings);
  delay(2000);
}

void loop() {
  if (imu.update()) {
    accel_x = imu.getAccX() / 16384.0; // impartim la 16384 pentru a obtine acceleratia in unitati de g (9.81 m/s^2)
    gyro_x = imu.getGyroX() / 131.0; // impartim la 131 pentru a obtine viteza unghiulara in grade/s

    accel_y = imu.getAccY() / 16384.0; // impartim la 16384 pentru a obtine acceleratia in unitati de g (9.81 m/s^2)
    gyro_y = imu.getGyroY() / 131.0; // impartim la 131 pentru a obtine viteza unghiulara in grade/s
  }

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
  accel_y_filtered = accel_y_filtered * cos(theta_y * M_PI / 180);

  // afisam valorile filtrate
  Serial.print(accel_x_filtered);
  Serial.print(" ; ");
  Serial.print(accel_y_filtered);
  Serial.print(" ; ");
  Serial.print(imu.getRoll());
  Serial.print(" ; ");
  Serial.print(imu.getPitch());
  Serial.print("\n"); 


  delay(10);
}

