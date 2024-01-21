// Asta e un cod bun pentru un server de BL pe un ESP

#include <BluetoothSerial.h>

BluetoothSerial SerialBT;
uint8_t address[6] = { 0xD8, 0x0B, 0x9A, 0x6A, 0x69, 0xF7 };                              // BT: Variable used to store the CLIENT(Slave) MAC address used for the connection; Use your own andress in the same format

void setup() {
  Serial.begin(115200);
  SerialBT.begin("ESP32Server"); // Numele serverului Bluetooth
}

void loop() {

    // SerialBT.connect(address);                                                              // BT: Establishing the connection with the CLIENT(Slave) with the Mac address stored in the address variable
    if(SerialBT.connected())Serial.println("Connected");
    String dataReceived = SerialBT.readString();
    if(dataReceived.length() != 0)
    Serial.println(dataReceived);
    delay(1);

}
