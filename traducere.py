import pandas as pd
import numpy as np

# Deschidem fișierul Excel
df = pd.read_excel('./Data/3_0_0.xlsx', engine='openpyxl')

# Parcurgem fiecare coloana
for column in df.columns:
    # Verificam daca toate valorile din coloana sunt de tipul string
    if df[column].dtypes == object:
        # Convertim valorile din string in double-uri
        df[column] = pd.to_numeric(df[column], errors='coerce')

# Inlocuim valorile NaN cu 0.0
df = df.fillna(0.0)

# Scriem datele inapoi in fisier
df.to_excel('3_0_0_editat.xlsx', index=False)
