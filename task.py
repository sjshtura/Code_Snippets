# -*- coding: utf-8 -*-
"""
Functions for estimating electricity prices, eeg levies, remunerations and other components, based on customer type and annual demand

@author: Shakhawat
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import interpolate
from scipy.interpolate import InterpolatedUnivariateSpline


industrie_prices_without_VAT = pd.read_excel(r'/Users/shakhawathossainturag/Downloads/Energiepreisentwicklung.xlsx',sheet_name='5.8.3 Strom - € - Industrie', skiprows = 5, nrows = 26, index_col = 0)
industrie_prices_without_VAT = industrie_prices_without_VAT.iloc[:,0]
#household_prices_without_VAT.columns = ["year","price"]
industrie_prices_without_VAT = industrie_prices_without_VAT.reset_index()
industrie_prices_without_VAT.head()


industrie_prices_without_VAT["index"]= industrie_prices_without_VAT["index"].str.slice(start = 5)
industrie_prices_without_VAT.columns = ["year","price"]

industrie_prices_without_VAT

industrie_prices_without_VAT = industrie_prices_without_VAT.set_index("year")

industrie_prices_without_VAT.index = industrie_prices_without_VAT.index.astype(str)
industrie_prices_without_VAT.index =  pd.to_datetime(industrie_prices_without_VAT.index, errors='ignore')
industrie_prices_without_VAT = industrie_prices_without_VAT.astype(float)
industrie_prices_without_VAT = industrie_prices_without_VAT.resample('12M').mean()
industrie_prices_without_VAT.index = industrie_prices_without_VAT.index.astype(str)
industrie_prices_without_VAT

industrie_prices_without_VAT.index= industrie_prices_without_VAT.index.str.slice(start = 0, stop = -6)
industrie_prices_without_VAT

ht_industrie_prices_without_VAT = industrie_prices_without_VAT.price * 1.2148975797220616
nt_industrie_prices_without_VAT = industrie_prices_without_VAT.price * 0.8802060300272765
ht_industrie_prices_without_VAT
nt_industrie_prices_without_VAT

#industrie_prices_without_VAT = industrie_prices_without_VAT[6:].reset_index()
ht_industrie_prices_without_VAT = ht_industrie_prices_without_VAT.reset_index()
nt_industrie_prices_without_VAT = nt_industrie_prices_without_VAT.reset_index()


ht_industrie_prices_without_VAT
nt_industrie_prices_without_VAT

industrie_prices_without_VAT = industrie_prices_without_VAT.reset_index()


#industrial 70000-150000 MWh
big_industrial_prices_BDEW = {'year': range(2007,2021), 'price': [7.91, 8.56, 8.69, 8.63, 10.07, 9.26, 10.18, 10.48, 9.76, 8.37, 9.96, 8.96, 9.28, 10.07]}
big_industrial_prices_BDEW = pd.DataFrame(data=big_industrial_prices_BDEW)
big_industrial_prices_BDEW




print("What is the yearly demand?")
print("If the demand is between 2000-20000 then enter 1 and If the demand is between 700000-1500000 then enter 2!")
val_yearly_demand = input("Enter your value:")
val_yearly_demand = int(val_yearly_demand)

if (val_yearly_demand == 1):
    print("Do you have predefined value for electricity price?")
    print("Yes = 1 / No = 2")
    #choose = 0
    val = input("Enter your value: ")
    val = int(val)
    if (val == 1):
        print("Do you have predefined value for electricity price with HT & NT?")
        print("Yes = 1 / No = 2")
        val_ht_nt = input("Enter your value: ")
        val_ht_nt = int(val_ht_nt)
        if (val_ht_nt == 1):
            val1 = input("Enter your preferred price for Haupttarrif: ")
            val1 = float(val1)
            val2 = input("Enter your preferred price for Nebentarrif: ")
            val2 = float(val2)
            ht_industrie_prices_without_VAT["year"] = ht_industrie_prices_without_VAT["year"].astype(int)
            ht_year = ht_industrie_prices_without_VAT["year"]
            ht_price = ht_industrie_prices_without_VAT["price"]

            ht_new_year = np.append(ht_year, 2021)
            ht_new_price = np.append(ht_price, val1)
            print(ht_new_year)
            print(ht_new_price)
            plt.figure()
            plt.plot (ht_new_year, ht_new_price)
            plt.show()

            nt_industrie_prices_without_VAT["year"] = nt_industrie_prices_without_VAT["year"].astype(int)
            nt_year = nt_industrie_prices_without_VAT["year"]
            nt_price = nt_industrie_prices_without_VAT["price"]

            nt_new_year = np.append(nt_year, 2021)
            nt_new_price = np.append(nt_price, val1)
            print(nt_new_year)
            print(nt_new_price)
            plt.figure()
            plt.plot (nt_new_year, nt_new_price)
            plt.show()
        
        if (val_ht_nt == 2):
            val1 = input("Enter your preferred price: ")
            val1 = float(val1)
            industrie_prices_without_VAT["year"] = industrie_prices_without_VAT["year"].astype(int)
            year = industrie_prices_without_VAT["year"]
            price = industrie_prices_without_VAT["price"]

            new_year = np.append(year, 2021)
            new_price = np.append(price, val1)
            print(new_year)
            print(new_price)
            plt.figure()
            plt.plot (new_year, new_price)
            plt.show()

    elif (val == 2):
        industrie_prices_without_VAT["year"] = industrie_prices_without_VAT["year"].astype(int)
        year = industrie_prices_without_VAT["year"]
        price = industrie_prices_without_VAT["price"]

        f = interpolate.interp1d(year, price, fill_value = "extrapolate")


        p_2021 = f(2021)

        new_year = np.append(year, 2021)
        new_price = np.append(price, f(2021))
        print(new_price)
        
        plt.figure()
        plt.plot (new_year, new_price)
        plt.show()

elif (val_yearly_demand == 2):
    print("Do you have predefined value for electricity price?")
    print("Yes = 1 / No = 2")
    #choose = 0
    val = input("Enter your value: ")
    val = int(val)
    if (val == 1):
        val1 = input("Enter your preferred price: ")
        val1 = float(val1)
        big_industrial_prices_BDEW["year"] = big_industrial_prices_BDEW["year"].astype(int)
        year = big_industrial_prices_BDEW["year"]
        price = big_industrial_prices_BDEW["price"]

        new_year = np.append(year, 2021)
        new_price = np.append(price, val1)
        print(new_year)
        print(new_price)
        plt.figure()
        plt.plot (new_year, new_price)
        plt.show()

    elif (val == 2):
        big_industrial_prices_BDEW["year"] = big_industrial_prices_BDEW["year"].astype(int)
        year = big_industrial_prices_BDEW["year"]
        price = big_industrial_prices_BDEW["price"]

        f = interpolate.interp1d(year, price, fill_value = "extrapolate")


        p_2021 = f(2021)

        new_year = np.append(year, 2021)
        new_price = np.append(price, f(2021))
        print(new_price)
        
        plt.figure()
        plt.plot (new_year, new_price)
        plt.show()


