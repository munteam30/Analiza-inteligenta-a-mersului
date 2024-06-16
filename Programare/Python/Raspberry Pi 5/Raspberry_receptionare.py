import pathlib
from datetime import datetime

import pandas as pd
import serial

# Solicită input de la utilizator pentru parametrii duration, User_ID și Activity_ID
duration = int(input("Introduceți durata (în secunde): "))
User_ID = int(input("Introduceți ID-ul utilizatorului: "))
Activity_ID = int(input("Introduceți ID-ul activității: "))

# Configurațiile pentru portul serial
serial_port = "/dev/serial0"  # Înlocuiți cu portul serial pe care îl utilizați
baud_rate = 115200
ser = serial.Serial(serial_port, baud_rate)

index = 0
denumireFisier = f"\\Desktop\\Data\\{Activity_ID}_{User_ID}_{index}.csv"
while pathlib.Path(denumireFisier).exists():
    index += 1
    denumireFisier = f".\Data\{Activity_ID}_{User_ID}_{index}.xlsx"

# Inițializare bază de date
database = []

start_time = datetime.now()

while (datetime.now()-start_time).total_seconds() < duration:
    data = ser.readline().decode("utf-8").strip()
    data_split = tuple(data.split(";"))  # Se separă datele folosind ";"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]  # timpul cu milisecunde
    database.append((timestamp, *data_split))

ser.close()

# Extrage datele și salvează într-un fișier Excel
columns = ["DataTimp", "Accel_X", "Accel_Y", "Gyro_X", "Gyro_Y", ""]
df = pd.DataFrame(database, columns=columns)
df = df.iloc[1:,:-1]
df.to_csv(denumireFisier, index=False)