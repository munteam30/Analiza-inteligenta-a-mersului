import serial
import time


ser = serial.Serial("COM7", 115200, timeout=1)
start = time.time()
data = []
durata_medie = 0
ranges = 400
for j in range(10):
    start = time.time()
    for i in range(ranges):
        data.append(ser.readline())
        # print(f"Data {i}: {data}")

    end = time.time()
    durata_medie =durata_medie + (end-start)
    print(f"Time taken to read {ranges} data: {end - start} seconds")


ser.close()
print(f"Durata medie este {durata_medie/10}")