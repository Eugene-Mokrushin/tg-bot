import pandas as pd
import os

current_folder = os.getcwd()

read_file = pd.read_csv(f"{current_folder}/Ozon_Data.csv", delimiter=';')
read_file.to_excel(f"{current_folder}/Ozon_Data.xlsx", index=None, header=True)