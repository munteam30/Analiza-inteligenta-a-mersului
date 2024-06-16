import serial
import time

def send_message(port, message, interval):
    ser = serial.Serial(port, baudrate=9600, timeout=1)

    while True:
        ser.write(message.encode('utf-8'))
        # print("Mesaj trimis:", message)
        time.sleep(interval)

    ser.close()

# Portul COM către care vrei să trimiți mesajul
com_port = '/dev/rfcomm0'

# Mesajul pe care vrei să-l trimiți
message_to_send = ";Mers Normal"

# Intervalul de trimitere a mesajului în secunde
sending_interval = 1

# Trimite periodic mesajul
send_message(com_port, message_to_send, sending_interval)