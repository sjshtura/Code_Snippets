from typing import ValuesView
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import interpolate
from scipy.interpolate import InterpolatedUnivariateSpline

def plotting(x,y, title, x_label, y_label, name_plot):
    fig = plt.figure()
    values = x
    plt.plot (x,y)
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.xticks(x,values)
    plt.xticks(rotation = 45) 
    fig.savefig(name_plot, dpi=fig.dpi)

def extrapolate(df):
    new_df = df
    new_df["year"] = new_df["year"].astype(int)
    year = new_df["year"]
    price = new_df["price"]
    f = interpolate.interp1d(year, price, fill_value = "extrapolate")
    p_2021 = f(2021)

    new_year = np.append(year, 2021)
    new_price = np.append(price, (f(2021)))
    return new_year, new_price

#erdgas Hausholds

haushalt_prices_without_VAT = pd.read_excel(r'/Users/shakhawathossainturag/Downloads/Energiepreisentwicklung.xlsx',sheet_name='5.3.2  Erdgas-€-Haushalte', skiprows = 5, nrows = 26, index_col = 0)
haushalt_prices_without_VAT = haushalt_prices_without_VAT.iloc[:,0]
haushalt_prices_without_VAT = haushalt_prices_without_VAT.reset_index()
haushalt_prices_without_VAT

haushalt_prices_without_VAT[["index"]]= haushalt_prices_without_VAT["index"].str.slice(start = 5)
haushalt_prices_without_VAT.columns = ["year","price"]
haushalt_prices_without_VAT = haushalt_prices_without_VAT.set_index("year")
haushalt_prices_without_VAT

haushalt_prices_without_VAT.index = haushalt_prices_without_VAT.index.astype(str)
haushalt_prices_without_VAT.index =  pd.to_datetime(haushalt_prices_without_VAT.index, errors='ignore')
haushalt_prices_without_VAT = haushalt_prices_without_VAT.astype(float)
haushalt_prices_without_VAT = haushalt_prices_without_VAT.resample('12M').mean()
haushalt_prices_without_VAT.index = haushalt_prices_without_VAT.index.astype(str)
haushalt_prices_without_VAT

haushalt_prices_without_VAT.index= haushalt_prices_without_VAT.index.str.slice(start = 0, stop = -6)


haushalt_prices_without_VAT = haushalt_prices_without_VAT.reset_index()
haushalt_prices_without_VAT

new_year, new_price = extrapolate(haushalt_prices_without_VAT)

print(new_year)
print(new_price)
plotting(new_year, new_price, "haushalt_erdgas_Price", "Year", "Price", "images/haushalt_erdgas_Price.png")





#erdgas Industrie

industrie_prices_without_VAT = pd.read_excel(r'/Users/shakhawathossainturag/Downloads/Energiepreisentwicklung.xlsx',sheet_name='5.3.3  Erdgas-€-Unternehmen', skiprows = 5, nrows = 26, index_col = 0)
industrie_prices_without_VAT = industrie_prices_without_VAT.iloc[:,0]
industrie_prices_without_VAT = industrie_prices_without_VAT.reset_index()
industrie_prices_without_VAT

industrie_prices_without_VAT[["index"]]= industrie_prices_without_VAT["index"].str.slice(start = 5)
industrie_prices_without_VAT.columns = ["year","price"]
industrie_prices_without_VAT = industrie_prices_without_VAT.set_index("year")
industrie_prices_without_VAT

industrie_prices_without_VAT.index = industrie_prices_without_VAT.index.astype(str)
industrie_prices_without_VAT.index =  pd.to_datetime(industrie_prices_without_VAT.index, errors='ignore')
industrie_prices_without_VAT = industrie_prices_without_VAT.astype(float)
industrie_prices_without_VAT = industrie_prices_without_VAT.resample('12M').mean()
industrie_prices_without_VAT.index = industrie_prices_without_VAT.index.astype(str)
industrie_prices_without_VAT

industrie_prices_without_VAT.index= industrie_prices_without_VAT.index.str.slice(start = 0, stop = -6)


industrie_prices_without_VAT = industrie_prices_without_VAT.reset_index()
industrie_prices_without_VAT

new_year, new_price = extrapolate(industrie_prices_without_VAT)

print(new_year)
print(new_price)
plotting(new_year, new_price, "industrie_erdgas_Price", "Year", "Price", "images/industrie_erdgas_Price.png")



#Braunkohle prices

Braunkohle_prices_without_VAT = pd.read_excel(r'/Users/shakhawathossainturag/Downloads/Energiepreisentwicklung.xlsx',sheet_name='5.1 Steinkohle und Braunkohle', skiprows = 27, nrows = 16, usecols = "A,N")
Braunkohle_prices_without_VAT.columns = ["year","price"]
Braunkohle_prices_without_VAT.index = Braunkohle_prices_without_VAT["year"]
#industrie_prices_without_VAT.index = industrie_prices_without_VAT.index.astype(str)
Braunkohle_prices_without_VAT  = Braunkohle_prices_without_VAT[["price"]]
Braunkohle_prices_without_VAT.index= Braunkohle_prices_without_VAT.index.str.slice(start = 0, stop = 4)

Braunkohle_prices_without_VAT = Braunkohle_prices_without_VAT.reset_index()

new_year, new_price = extrapolate(Braunkohle_prices_without_VAT)
print(new_year)
print(new_price)
plotting(new_year, new_price, "Braunkohle_prices", "Year", "Price", "images/Braunkohle_prices.png")


# Steinkohle prices

Steinkohle_prices_without_VAT = pd.read_excel(r'/Users/shakhawathossainturag/Downloads/Energiepreisentwicklung.xlsx',sheet_name='5.1 Steinkohle und Braunkohle', skiprows = 6, nrows = 16, usecols = "A,N")
Steinkohle_prices_without_VAT.columns = ["year","price"]
Steinkohle_prices_without_VAT.index = Steinkohle_prices_without_VAT["year"]
#industrie_prices_without_VAT.index = industrie_prices_without_VAT.index.astype(str)
Steinkohle_prices_without_VAT  = Steinkohle_prices_without_VAT[["price"]]
Steinkohle_prices_without_VAT.index= Steinkohle_prices_without_VAT.index.str.slice(start = 0, stop = 4)
Steinkohle_prices_without_VAT

Steinkohle_prices_without_VAT = Steinkohle_prices_without_VAT.reset_index()

new_year, new_price = extrapolate(Steinkohle_prices_without_VAT)
print(new_year)
print(new_price)
plotting(new_year, new_price, "Steinkohle_prices", "Year", "Price", "images/Steinkohle_prices.png")