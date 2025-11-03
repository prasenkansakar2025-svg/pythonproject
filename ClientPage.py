import pandas as pd

datafile

try:
    df = pd.read_csv('data.csv')

except FileNotFoundError:
    print("Error: The file 'data.csv' was not found.")
    df = None