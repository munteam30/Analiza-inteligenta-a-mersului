import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Deschidem fișierul Excel
df = pd.read_excel('./1_0_0_editat.xlsx', engine='openpyxl')

# Parcurgem fiecare dintre primele patru coloane
for i in range(4):
    # Selectam coloana si primele 5 randuri
    data = df.iloc[:5, i]

    # Convertim datele din string in float
    data = pd.to_numeric(data, errors='coerce')

    # Inlocuim valorile NaN cu 0.0
    data = data.fillna(0.0)

    # Cream graficul
    plt.figure(figsize=(10, 5))
    plt.plot(data)
    plt.title(f'Grafic pentru coloana {i + 1}')
    plt.xlabel('Index')
    plt.ylabel('Valoare')
    plt.grid(True)
    plt.show()
