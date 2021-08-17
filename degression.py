import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from xlsxwriter import Workbook
#erdgas Hausholds

# Anzulegende Werte in Cent/kWh - Marktprämienmodell:
df = pd.read_excel(r'DegressionsVergSaetze_05-07_21.xlsx',sheet_name='Solar', skiprows = 6, nrows = 18, usecols = "J:M")
df.columns = ["Inbetriebnahme", "bis_10_kW", "bis_40_kW", "bis_750_kW"]
mask1 = df["bis_40_kW"].isnull()
#mask2 = df["bis_750_kW"].isnull()
#df.loc[mask1, "bis_10_kW"] = df.loc[mask1, "bis_40_kW"]
#df.loc[mask2, "bis_10_kW"] = df.loc[mask2, "bis_750_kW"]
df['bis_40_kW'] = np.where(df['bis_40_kW'].isnull(), df['bis_10_kW'], df['bis_40_kW'])
df['bis_750_kW'] = np.where(df['bis_750_kW'].isnull(), df['bis_10_kW'], df['bis_750_kW'])
df["Inbetriebnahme"] = df["Inbetriebnahme"].str.replace(" 2", "")
df["Inbetriebnahme"] = df["Inbetriebnahme"].str.replace(" 3", "")
df["Inbetriebnahme"] = df["Inbetriebnahme"].str.replace(" 4", "")
df["Inbetriebnahme"] = df["Inbetriebnahme"].str.replace(" 5", "")
df_Marktpraemienmodell = df

# Vergütungssätze in Cent/kWh - Feste Einspeisevergütung:
 
df = pd.read_excel(r'DegressionsVergSaetze_05-07_21.xlsx',sheet_name='Solar', skiprows = 32, nrows = 7, usecols = "J:M")
df.columns = ["Inbetriebnahme", "bis_10_kW", "bis_40_kW", "bis_750_kW"]
df["Inbetriebnahme"] = df["Inbetriebnahme"].str.replace(" 2", "")
df["Inbetriebnahme"] = df["Inbetriebnahme"].str.replace(" 3", "")
df["Inbetriebnahme"] = df["Inbetriebnahme"].str.replace(" 4", "")
df["Inbetriebnahme"] = df["Inbetriebnahme"].str.replace(" 5", "")
df_Verguetungssaetze = df


# Anzulegende Werte für den Mieterstromzuschlag in Cent/kWh

df = pd.read_excel(r'DegressionsVergSaetze_05-07_21.xlsx',sheet_name='Solar', skiprows = 46, nrows = 19, usecols = "J:M")
df.columns = ["Inbetriebnahme", "bis_10_kW", "bis_40_kW", "bis_750_kW"]
mask1 = df["bis_40_kW"].isnull()
#mask2 = df["bis_750_kW"].isnull()
#df.loc[mask1, "bis_10_kW"] = df.loc[mask1, "bis_40_kW"]
#df.loc[mask2, "bis_10_kW"] = df.loc[mask2, "bis_750_kW"]
df['bis_40_kW'] = np.where(df['bis_40_kW'].isnull(), df['bis_10_kW'], df['bis_40_kW'])
df['bis_750_kW'] = np.where(df['bis_750_kW'].isnull(), df['bis_10_kW'], df['bis_750_kW'])
df["Inbetriebnahme"] = df["Inbetriebnahme"].str.replace(" 2", "")
df["Inbetriebnahme"] = df["Inbetriebnahme"].str.replace(" 3", "")
df["Inbetriebnahme"] = df["Inbetriebnahme"].str.replace(" 4", "")
df["Inbetriebnahme"] = df["Inbetriebnahme"].str.replace(" 5", "")
df_Anzulegende = df


writer = pd.ExcelWriter('degression_data.xlsx', engine='xlsxwriter')

# Write each dataframe to a different worksheet.
df_Anzulegende.to_excel(writer, sheet_name='Anzulegende')
df_Marktpraemienmodell.to_excel(writer, sheet_name='Marktpraemienmodell')
df_Verguetungssaetze.to_excel(writer, sheet_name='Verguetungssaetze')

# Close the Pandas Excel writer and output the Excel file.
writer.save()