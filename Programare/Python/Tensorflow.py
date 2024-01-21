import serial
import time
import pandas as pd

# Configurațiile pentru portul serial
serial_port = "COM6"  # Înlocuiți cu portul serial pe care îl utilizați
baud_rate = 115200
ser = serial.Serial(serial_port, baud_rate)

duration = 10
start_time = time.time()
database = []

while (time.time() - start_time) < duration:
    # Citește datele de pe portul serial
    data = ser.readline().decode("utf-8").strip()
    database.append(data)

    # print(data)

database = database[1:]

ser.close()
#
# # Extrage datele și salvează într-un fișier Excel
# columns = ["Accel_X", "Accel_Y", "Gyro_X", "Gyro_Y", ""]
data_rows = [tuple(map(str, entry.split(";"))) for entry in database]
print(len(data_rows))
# df = pd.DataFrame(data_rows, columns=columns)
# df.to_excel("output.xlsx", index=False)
