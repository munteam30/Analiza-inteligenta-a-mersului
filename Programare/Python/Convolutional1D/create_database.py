#Create_database code
import os
import pandas as pd
import numpy as np

fereastra = 100


def split_and_save_data(df, label, file_name, output_folder):
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
            print(window_data.shape)
            exit(0)
        # Save the window data to a .npy file
        window_file_name = f"{file_name.split('.')[0]}_{i}.npy"
        np.save(os.path.join(output_folder, window_file_name), window_data)

if __name__ == "__main__":
    xls_database_path = 'D:\Dizertatie\Date\Date_Antrenare'

    # Directory containing the Excel files
    path = xls_database_path
    # Iterate through all files in the directory
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
            os.makedirs(label_folder, exist_ok=True)

            # Split data into windows of shape 4xfereastra and save them
            split_and_save_data(df, label, file_name, label_folder)
