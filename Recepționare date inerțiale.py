import pathlib
from datetime import datetime

import pandas as pd
import serial

# Configurațiile pentru portul serial
serial_port = "COM7"  # Înlocuiți cu portul serial pe care îl utilizați
baud_rate = 115200
ser = serial.Serial(serial_port, baud_rate)

# Timpul de rulare în secunde
duration = 300
User_ID = 1
Activity_ID = 0         #Just for testing, TBD on the go
index = 0

denumireFisier = f".\Data\{Activity_ID}_{User_ID}_{index}.xlsx"
while pathlib.Path(denumireFisier).exists():
    index += 1
    denumireFisier = f".\Data\{Activity_ID}_{User_ID}_{index}.xlsx"

# Inițializare bază de date
database = []

start_time = datetime.now()

while (datetime.now()-start_time).total_seconds() < duration:
    while True:
        try:
            data = ser.readline().decode("utf-8").strip()
            break
            # procesați datele decodate
        except UnicodeDecodeError:
            print("A apărut o eroare la decodare, se încearcă din nou...")
            continue
    data_split = tuple(data.split(";"))  # Se separă datele folosind ";"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]  # timpul cu milisecunde
    database.append((timestamp, *data_split))

ser.close()

# Extrage datele și salvează într-un fișier Excel
columns = ["DataTimp", "Accel_X", "Accel_Y", "Gyro_X", "Gyro_Y", ""]
df = pd.DataFrame(database, columns=columns)
df = df.iloc[1:,:-1]
df.to_excel(denumireFisier, index=False)

# print("Au fost salvate ",len(df), "esantioane")