import pandas as pd
import numpy as np
from scipy.signal import welch
from scipy.stats import kurtosis, skew


def calculate_characteristics(window, fs):
    # Mean Absolute Value (MAV)
    mav = np.mean(np.abs(window))

    # Zero Crossing Rate (ZCR)
    zcr = ((window[:-1] * window[1:]) < 0).sum()

    # Slope Sign Changes (SSC)
    ssc = np.diff(np.sign(np.diff(window))).nonzero()[0].size

    # Root Mean Square (RMS)
    rms = np.sqrt(np.mean(window ** 2))
    # Dominant Frequency and Spectral Entropy
    fft_values = np.fft.rfft(window)
    psd_values = np.abs(fft_values) ** 2
    psd_values /= np.sum(psd_values)  # normalize psd values
    freqs = np.fft.rfftfreq(len(window), 1 / fs)
    dominant_frequency = freqs[np.argmax(psd_values)]
    spectral_entropy = -np.sum(psd_values * np.log2(psd_values))

    return mav, zcr, ssc, rms, dominant_frequency, spectral_entropy


def process_signal(signal, window_length, overlap, fs):
    step = window_length - overlap
    windows = [signal[i:i + window_length] for i in range(0, len(signal), step)]
    characteristics = [calculate_characteristics(window,fs) for window in windows]
    return characteristics


# Încărcarea datelor din fișierul Excel
df = pd.read_excel(".\\Data\\0_0_0.xlsx")
df = df.drop(columns=["DataTimp"])
fs = 340
# Prelucrarea fiecărei coloane a DataFrame-ului
window_length = 100  # Lungimea ferestrei(număr de eșantioane)
overlap = 60  # Overlap(număr de eșantioane)
for column in df.columns:
    signal = df[column].values
    characteristics = process_signal(signal, window_length, overlap, fs)

    print(f"Caracteristicile pentru {column}: {characteristics}")