import os
import threading
from datetime import datetime
import time
import pathlib
import pandas as pd
import numpy as np
import serial
from tensorflow.keras.models import load_model

fereastra = 100


def achizitieDispozitiv(durata, User_ID, Activity_ID, Training):
    serial_port = "/dev/ttyUSB0"  # Înlocuiți cu portul serial pe care îl utilizați pe Raspberry Pi
    baud_rate = 115200
    ser = serial.Serial(serial_port, baud_rate)

    index = 0
    if Training == 0:
        denumireFisier = f"/home/mihai/Desktop/Date/{Activity_ID}_{User_ID}_{index}.xlsx"
    else:
        denumireFisier = f"/home/mihai/Desktop/Date/{Activity_ID}_{User_ID}_{index}.xlsx"
        while pathlib.Path(denumireFisier).exists():
            index += 1
            denumireFisier = f"/home/mihai/Desktop/Date/{Activity_ID}_{User_ID}_{index}.xlsx"

    # Inițializare bază de date
    database = []

    start_time = datetime.now()
    while (datetime.now() - start_time).total_seconds() < durata:
        data = ser.readline().decode("utf-8", errors="ignore").strip()
        data_split = tuple(data.split(";"))  # Se separă datele folosind ";"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]  # timpul cu milisecunde
        database.append((timestamp, *data_split))

    ser.close()
    print(f"Gata! Am achiziționat un număr de {len(database)} esantioane.")

    # Extrage datele și salvează într-un fișier Excel
    columns = ["Timp", "Accel_X", "Accel_Y", "Gyro_X", "Gyro_Y"]
    df = pd.DataFrame(database, columns=columns)
    df.to_excel(denumireFisier, index=False)
    print(f"Gata! Am salvat datele în fișierul {denumireFisier}.")


def split_and_save_data(path, output_folder):
    for file_name in os.listdir(path):
        if file_name.endswith('.xlsx') or file_name.endswith('.xls'):
            label = int(file_name.split('_')[0])
            file_path = os.path.join(path, file_name)
            df = pd.read_excel(file_path)
            label_folder = os.path.join(output_folder, f'label_{label}')
            os.makedirs(label_folder, exist_ok=True)

            data = df.iloc[:, 1:5].values
            num_windows = len(data) // fereastra
            if len(data) % fereastra != 0:
                num_windows += 1

            for i in range(num_windows):
                window_data = data[i * fereastra: (i + 1) * fereastra]
                if len(window_data) < fereastra:
                    pad_width = ((0, fereastra - len(window_data)), (0, 0))
                    window_data = np.pad(window_data, pad_width, mode='constant', constant_values=0)

                window_file_name = f"{file_name.split('.')[0]}_{i}.npy"
                np.save(os.path.join(label_folder, window_file_name), window_data)


def send_message(port, interval):
    ser = serial.Serial(port, baudrate=9600, timeout=1)
    while True:
        try:
            with open('/home/mihai/Desktop/predictions.txt', 'r') as file:
                message = file.read().strip()
            ser.write(message.encode('utf-8'))
            print(f"Mesaj trimis: {message}")
            time.sleep(interval)
        except Exception as e:
            print(f"Eroare la trimiterea mesajului: {e}")

    ser.close()


# Portul serial către care vrei să trimiți mesajul (ex: /dev/ttyUSB0)
serial_port = '/dev/rfcomm0'

# Intervalul de trimitere a mesajului în secunde
sending_interval = 1

# Creează și pornește thread-ul pentru trimiterea mesajelor
message_thread = threading.Thread(target=send_message, args=(serial_port, sending_interval))
message_thread.daemon = True
message_thread.start()

while True:
    try:
        medie = []
        achizitieDispozitiv(1, 0, 0, 0)
        test_data_path = '/home/mihai/Desktop/Date'
        model_path = '/home/mihai/Desktop/Incercarea1.h5'
        split_and_save_data(test_data_path, '/home/mihai/Desktop/Date/Processed')
        model = load_model(model_path)

        for file in os.listdir('/home/mihai/Desktop/Date/Processed/label_0'):
            filepath = os.path.join('/home/mihai/Desktop/Date/Processed/label_0', file)
            data = np.load(filepath)

            if len(data.shape) == 2:
                data = np.expand_dims(data, axis=0)

            prediction = model.predict(data)
            max_index = np.argmax(prediction)
            medie.append(max_index)

        final_prediction = np.round(np.mean(medie))
        print(f"Prediction: {final_prediction}")

        if final_prediction == 0:
            mesaj = ";Mers normal"
        elif final_prediction == 1:
            mesaj = ";Alergare"
        elif final_prediction == 2:
            mesaj = ";Stationare"

        with open('/home/mihai/Desktop/predictions.txt', 'w') as file:
            file.write(mesaj)

    except KeyboardInterrupt:
        print("Execuția a fost oprită de utilizator.")
        break
    except Exception as e:
        print(f"A apărut o eroare: {e}")
        break
