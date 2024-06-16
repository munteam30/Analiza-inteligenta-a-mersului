import os
import pathlib
import threading
from datetime import datetime
import time
import pandas as pd
import numpy as np
import serial
from keras.models import load_model

fereastra = 100

def achizitieDispozitiv(durata, User_ID, Activity_ID, Training):
    serial_port = "COM6"  # Înlocuiți cu portul serial pe care îl utilizați
    baud_rate = 115200
    ser = serial.Serial(serial_port, baud_rate)

    index = 0
    if Training == 0:
        denumireFisier = f"D:\\Dizertatie\\Date\\Temporar\\{Activity_ID}_{User_ID}_{index}.xlsx"
    else:
        denumireFisier = f"D:\\Dizertatie\\Date\\{Activity_ID}_{User_ID}_{index}.xlsx"
        while pathlib.Path(denumireFisier).exists():
            index += 1
            denumireFisier = f"D:\\Dizertatie\\Date\\{Activity_ID}_{User_ID}_{index}.xlsx"

    # Inițializare bază de date
    database = []

    start_time = datetime.now()
    # print("Start")
    while (datetime.now() - start_time).total_seconds() < durata:
        data = ser.readline().decode("utf-8" , errors="ignore").strip()
        data_split = tuple(data.split(";"))  # Se separă datele folosind ";"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]  # timpul cu milisecunde
        database.append((timestamp, *data_split))

        # print((datetime.now() - start_time).total_seconds())
        # print(database)

    ser.close()
    print("Gata! Am achizitionat un numar de {} esantioane.".format(len(database)))

    # Extrage datele și salvează într-un fișier Excel
    columns = ["Timp", "Accel_X", "Accel_Y", "Gyro_X", "Gyro_Y"]
    for i in range(len(database) - 1):
        # print(len(database[i]))
        if (len(database[i]) != len(database[i - 1])): database.remove(database[i])
    df = pd.DataFrame(database, columns=columns)
    # print("Gata! Am achizitionat un numar de {} esantioane pentru activitatea {}.".format(len(database), Activity_ID))
    df = df.iloc[1:, :]
    df.to_excel(denumireFisier, index=False)
def split_and_save_data(path, output_folder):

    for file_name in os.listdir(path):
        # Check if the file is an Excel file
        if file_name.endswith('.xlsx') or file_name.endswith('.xls'):
            # Extract the label from the file name
            label = int(file_name.split('_')[0])

            # Full path to the Excel file
            file_path = os.path.join(path, file_name)

            # Read the Excel file
            df = pd.read_excel(file_path)

            # Create a subfolder for the label if it does not exist
            label_folder = os.path.join(path, f'label_{label}')

    # Extract columns 1 to 4 (assuming 0-based indexing)
    data = df.iloc[:, 1:5].values

    # Calculate the number of windows
    num_windows = len(data) // fereastra
    if len(data) % fereastra != 0:
        num_windows += 1

    # Split data into windows of shape 4xfereastra
    for i in range(num_windows):
        window_data = data[i*fereastra : (i+1)*fereastra]
        # Pad the last window if needed
        if len(window_data) < fereastra:
            pad_width = ((0, fereastra - len(window_data)), (0, 0))
            window_data = np.pad(window_data, pad_width, mode='constant', constant_values=0)

        # Save the window data to a .npy file
        window_file_name = f"{file_name.split('.')[0]}_{i}.npy"
        np.save(os.path.join(output_folder, window_file_name), window_data)


def send_message(port, interval):
    ser = serial.Serial(port, baudrate=9600, timeout=1)

    while True:
        try:
            with open('D:\Dizertatie\predictions.txt', 'r') as file:
                message = file.read().strip()
            ser.write(message.encode('utf-8'))
            print(f"Mesaj trimis: {message}")
            time.sleep(interval)
        except Exception as e:
            print(f"An error occurred while sending message: {e}")

    ser.close()


# Portul COM către care vrei să trimiți mesajul
com_port = 'COM11'

# Intervalul de trimitere a mesajului în secunde
sending_interval = 1

# Creează și pornește thread-ul pentru trimiterea mesajelor
message_thread = threading.Thread(target=send_message, args=(com_port, sending_interval))
message_thread.daemon = True
message_thread.start()

while True:
    try:
        medie = []
        achizitieDispozitiv(1,0,0,0)
        test_data_path = 'D:\Dizertatie\Date\Temporar'
        model_path = 'D:\Dizertatie\Programare\Python\Models\Incercarea1.h5'
        split_and_save_data(test_data_path,'D:\Dizertatie\Date\Temporar\Processed')
        model = load_model(model_path)
        for file in os.listdir('D:\Dizertatie\Date\Temporar\Processed'):
            filepath = os.path.join('D:\Dizertatie\Date\Temporar\Processed',file)
            data = np.load(filepath)
            # print(data.shape)

            if len(data.shape) == 2:  # Dacă datele sunt 2D (fereastra, 4)
                data = np.expand_dims(data, axis=0)  # Adăugăm dimensiunea batch-ului
            prediction = model.predict(data)
            max_index = np.argmax(prediction)
            # Afișăm rezultatul predicției
            # print(f"File: {file}, Prediction: {max_index}")
            medie.append(max_index)
        Final_prediction = np.round(np.mean(medie))
        print(f"Prediction: {Final_prediction}")
        if Final_prediction == 0:
            mesaj = ";Mers normal"
        elif Final_prediction == 1:
            mesaj = ";Alergare"
        elif Final_prediction == 2:
            mesaj = ";Stationare"
        with open('D:\Dizertatie\predictions.txt', 'w') as file:
            file.write(mesaj)

    except KeyboardInterrupt:
        print("Execuția a fost oprită de utilizator.")
        break
    except Exception as e:
        print(f"A apărut o eroare: {e}")
        break
