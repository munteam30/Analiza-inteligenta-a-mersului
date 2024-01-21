import numpy as np
import serial
import threading
import time
import pandas as pd
from datetime import datetime, timedelta
from itertools import repeat




def read_serial(port, database, timestamp_dict):
    while time.time()-start_time < duration:
        data = port.readline().decode("utf-8").strip()
        timestamp = datetime.now().strftime("%H:%M:%S")
        database.append(data)
        timestamp_dict[timestamp] = data

# Configurațiile pentru primul port serial
serial_port1 = "COM6"  # Înlocuiți cu portul serial pe care îl utilizați
baud_rate1 = 115200
ser1 = serial.Serial(serial_port1, baud_rate1)

# Configurațiile pentru al doilea port serial
serial_port2 = "COM11"  # Înlocuiți cu portul serial pe care îl utilizați
baud_rate2 = 115200
ser2 = serial.Serial(serial_port2, baud_rate2)

duration = 15
start_time = time.time()
database1 = []
database2 = []
timestamp_dict = {}

# Creare de fire de execuție pentru citirea datelor de pe portul 5
thread1 = threading.Thread(target=read_serial, args=(ser1, database1, timestamp_dict))

# Creare de fire de execuție pentru citirea datelor de pe portul 11
thread2 = threading.Thread(target=read_serial, args=(ser2, database2, timestamp_dict))
thread2.daemon = True  # Facem thread-ul 2 un daemon pentru a se opri când se oprește programul principal

# Pornirea firelor de execuție
thread2.start()
thread1.start()


# Oprire firelor de execuție
thread1.join()

# Nu este nevoie să oprim explicit thread-ul 2, pentru că l-am făcut daemon
ser1.close()
ser2.close()
print("Datele primite pe portul COM11:")
for data in database2:
    print(data)
# print("Datele primite pe portul COM5:")
# for data in database1:
#     print(data)

# Extrage datele și salvează într-un fișier Excel
columns = ["Timp","Latitudine", "Longitudine", "Altitudine", "Viteza" , "Accel_X", "Accel_Y", "Gyro_X", "Gyro_Y",""]
database1 = database1[1:]
data_rows = [tuple(map(str, entry.split(";"))) for entry in database1]
location_rows = [tuple(map(str, entry.split(";"))) for entry in database2]

data_rows = data_rows[:-1]
location_rows=location_rows[:-1]
multiplication_factor = np.floor(len(data_rows)/len(location_rows))
# print(multiplication_factor, 'multiplication f')
location_list = [sublist for sublist in location_rows for _ in range(int(multiplication_factor))]

data_rows = data_rows[:len(location_list)]

print(len(location_list), len(data_rows), len(location_list))
lista_legata = [a+b for a,b in zip(location_list, data_rows)]

df = pd.DataFrame(lista_legata, columns=columns)
df.to_excel("output.xlsx", index=False)


# Afișare datelor primite pe portul 11


# Afișare datelor primite pe portul COM5:
