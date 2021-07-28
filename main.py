# -*- coding: utf-8 -*-
"""
Functions for estimating electricity prices, eeg levies, remunerations and other components, based on customer type and annual demand

@author: Shakhawat
"""

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
    fig.savefig(name_plot, dpi=fig.dpi)

# def plotting(x,y, title, x_label, y_label):
#         plt.figure()
#         plt.plot (x,y)
#         plt.title(title)
#         plt.xlabel(x_label)
#         plt.ylabel(y_label)
#         plt.show()




def haupt_tarif(data):
    #haupt_tarrif = df_with_data
    df_with_data = pd.read_excel(data)
    yearly_mean = df_with_data.price.mean()
    haupt_tarrif = df_with_data[df_with_data["hour"].isin([8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]) & df_with_data["Day"].isin(['Wednesday', 'Thursday', 'Friday', 'Monday', 'Tuesday'])]
    cond = df_with_data['hour'].isin(haupt_tarrif['hour'])
    df_with_data.drop(haupt_tarrif[cond].index, inplace = True)
    ht_factor = haupt_tarrif.price.mean()/yearly_mean
    return ht_factor

def neben_tarif(data):
    #neben_tarrif = df_with_data
    df_with_data = pd.read_excel(data)
    yearly_mean = df_with_data.price.mean()
    neben_tarrif = df_with_data[(df_with_data["hour"].isin([1, 2, 3, 4, 5, 6, 7, 20, 21, 22, 23, 24]) & df_with_data["Day"].isin(['Wednesday', 'Thursday', 'Friday', 'Monday', 'Tuesday'])) |(df_with_data["Day"].isin(['Saturday', 'Sunday']))]
    neben_tarrif.head()
    cond = df_with_data['hour'].isin(neben_tarrif['hour'])
    df_with_data.drop(neben_tarrif[cond].index, inplace = True)
    nt_factor = neben_tarrif.price.mean()/yearly_mean
    return nt_factor

ht_factor = haupt_tarif("ht_nt_price.xlsx")
nt_factor = neben_tarif("ht_nt_price.xlsx")

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

ht_industrie_prices_without_VAT = industrie_prices_without_VAT.price * ht_factor
nt_industrie_prices_without_VAT = industrie_prices_without_VAT.price * nt_factor
ht_industrie_prices_without_VAT
nt_industrie_prices_without_VAT

#industrie_prices_without_VAT = industrie_prices_without_VAT[6:].reset_index()
ht_industrie_prices_without_VAT = ht_industrie_prices_without_VAT.reset_index()
nt_industrie_prices_without_VAT = nt_industrie_prices_without_VAT.reset_index()


ht_industrie_prices_without_VAT
nt_industrie_prices_without_VAT

industrie_prices_without_VAT = industrie_prices_without_VAT.reset_index()


#industrial 150000 MWh
v_big_industrial_prices_BDEW = {'year': range(2019,2021), 'price': [3.77,3.05]}
v_big_industrial_prices_BDEW = pd.DataFrame(data=v_big_industrial_prices_BDEW)
v_big_industrial_prices_BDEW

#industrial 70000-150000 MWh
big_industrial_prices_BDEW = {'year': range(2007,2021), 'price': [7.91, 8.56, 8.69, 8.63, 10.07, 9.26, 10.18, 10.48, 9.76, 8.37, 9.96, 8.96, 9.28, 10.07]}
big_industrial_prices_BDEW = pd.DataFrame(data=big_industrial_prices_BDEW)
big_industrial_prices_BDEW


#industrial 20000-70000 MWh
mid_industrie_prices = pd.read_excel(r'output.xlsx')
mid_industrie_prices.columns = ['year', 'price']
mid_industrie_prices


#households 0-2000 MWh
household_prices = pd.read_excel(r'households_price.xlsx')
household_prices.columns = ['year', 'price']
household_prices

print("Whats your yearly electricity demand?")
print("Demand ranges are between 0-2000 MWh, 2000-20000 MWh, 20000 - 700000 MWh and 700000-1500000 MWh")
print("Please Input Demand:")
val_yearly_demand = input("Enter your value:")
val_yearly_demand = float(val_yearly_demand)


if ((val_yearly_demand > 0) & (val_yearly_demand < 2000)):
    print("Do you already know your electricty price?")
    print("Yes = 1 / No = 2")
    #choose = 0
    val = input("Enter your value: ")
    val = int(val)
    if (val == 1):
        print("Do you have a yearly mean or HT/NT electricity price structure?")
        val_ht_nt = input("Enter 0 (zero) for yearly mean price and Enter 1 for HT/NT price structure: ")
        val_ht_nt = int(val_ht_nt)
        if (val_ht_nt == 1):
            val1 = input("Enter HT value: ")
            val1 = float(val1)
            val2 = input("Enter NT value: ")
            val2 = float(val2)
            ht_industrie_prices_without_VAT = household_prices
            ht_industrie_prices_without_VAT["year"] = ht_industrie_prices_without_VAT["year"].astype(int)
            ht_year = ht_industrie_prices_without_VAT["year"]
            ht_price = ht_industrie_prices_without_VAT["price"]

            ht_new_year = np.append(ht_year, 2021)
            ht_new_price = np.append(ht_price, val1)
            print(ht_new_year)
            print(ht_new_price)
            plotting(ht_new_year, ht_new_price, "HT Price", "Year", "Price", "images/HT Price.png")
            # plotting(nt_new_year, nt_new_price, "NT Price", "Year", "Price", "images/NT Price.png")

            nt_industrie_prices_without_VAT = household_prices
            nt_industrie_prices_without_VAT["year"] = nt_industrie_prices_without_VAT["year"].astype(int)
            nt_year = nt_industrie_prices_without_VAT["year"]
            nt_price = nt_industrie_prices_without_VAT["price"]

            nt_new_year = np.append(nt_year, 2021)
            nt_new_price = np.append(nt_price, val2)
            print(nt_new_year)
            print(nt_new_price)
            plotting(nt_new_year, nt_new_price, "NT Price", "Year", "Price", "images/NT Price.png")

        elif (val_ht_nt == 0):
            val1 = input("Enter yearly mean price for electricity: ")
            val1 = float(val1)
            ht_industrie_prices_without_VAT = household_prices
            ht_industrie_prices_without_VAT["year"] = ht_industrie_prices_without_VAT["year"].astype(int)
            ht_year = ht_industrie_prices_without_VAT["year"]
            ht_price = ht_industrie_prices_without_VAT["price"]

            ht_new_year = np.append(ht_year, 2021)
            ht_new_price = np.append(ht_price, (val1*ht_factor))
            print(ht_new_year)
            print(ht_new_price)
            plotting(ht_new_year, ht_new_price, "HT Price", "Year", "Price", "images/HT Price.png")
            # plotting(nt_new_year, nt_new_price, "NT Price", "Year", "Price", "images/NT Price.png")


            nt_industrie_prices_without_VAT = household_prices
            nt_industrie_prices_without_VAT["year"] = nt_industrie_prices_without_VAT["year"].astype(int)
            nt_year = nt_industrie_prices_without_VAT["year"]
            nt_price = nt_industrie_prices_without_VAT["price"]

            nt_new_year = np.append(nt_year, 2021)
            nt_new_price = np.append(nt_price, (val1*nt_factor))
            print(nt_new_year)
            print(nt_new_price)
            # plotting(ht_new_year, ht_new_price, "HT Price", "Year", "Price", "images/HT Price.png")
            plotting(nt_new_year, nt_new_price, "NT Price", "Year", "Price", "images/NT Price.png")


    elif (val == 2):
        ht_industrie_prices_without_VAT = household_prices
        ht_industrie_prices_without_VAT["year"] = ht_industrie_prices_without_VAT["year"].astype(int)
        ht_year = ht_industrie_prices_without_VAT["year"]
        ht_price = ht_industrie_prices_without_VAT["price"]
        f = interpolate.interp1d(ht_year, ht_price, fill_value = "extrapolate")
        p_2021 = f(2021)

        ht_new_year = np.append(ht_year, 2021)
        ht_new_price = np.append(ht_price, (f(2021)*ht_factor))
        print(ht_new_year)
        print(ht_new_price)
        plotting(ht_new_year, ht_new_price, "HT Price", "Year", "Price", "images/HT Price.png")
        # plotting(nt_new_year, nt_new_price, "NT Price", "Year", "Price", "images/NT Price.png")

        nt_industrie_prices_without_VAT = household_prices
        nt_industrie_prices_without_VAT["year"] = nt_industrie_prices_without_VAT["year"].astype(int)
        nt_year = nt_industrie_prices_without_VAT["year"]
        nt_price = nt_industrie_prices_without_VAT["price"]
        
        f = interpolate.interp1d(nt_year, nt_price, fill_value = "extrapolate")
        p_2021 = f(2021)

        nt_new_year = np.append(nt_year, 2021)
        nt_new_price = np.append(nt_price, (f(2021)*nt_factor))
        print(nt_new_year)
        print(nt_new_price)
        # plotting(ht_new_year, ht_new_price, "HT Price", "Year", "Price", "images/HT Price.png")
        plotting(nt_new_year, nt_new_price, "NT Price", "Year", "Price", "images/NT Price.png")

elif ((val_yearly_demand >= 2000) & (val_yearly_demand <= 20000)):
    print("Do you already know your electricty price?")
    print("Yes = 1 / No = 2")
    #choose = 0
    val = input("Enter your value: ")
    val = int(val)
    if (val == 1):
        print("Do you have a yearly mean or HT/NT electricity price structure?")
        val_ht_nt = input("Enter 0 (zero) for yearly mean price and Enter 1 for HT/NT price structure: ")
        val_ht_nt = int(val_ht_nt)
        if (val_ht_nt == 1):
            val1 = input("Enter HT value: ")
            val1 = float(val1)
            val2 = input("Enter NT value: ")
            val2 = float(val2)
            ht_industrie_prices_without_VAT["year"] = ht_industrie_prices_without_VAT["year"].astype(int)
            ht_year = ht_industrie_prices_without_VAT["year"]
            ht_price = ht_industrie_prices_without_VAT["price"]

            ht_new_year = np.append(ht_year, 2021)
            ht_new_price = np.append(ht_price, val1)
            print(ht_new_year)
            print(ht_new_price)
            plotting(ht_new_year, ht_new_price, "HT Price", "Year", "Price", "images/HT Price.png")
            # plotting(nt_new_year, nt_new_price, "NT Price", "Year", "Price", "images/NT Price.png")

            nt_industrie_prices_without_VAT["year"] = nt_industrie_prices_without_VAT["year"].astype(int)
            nt_year = nt_industrie_prices_without_VAT["year"]
            nt_price = nt_industrie_prices_without_VAT["price"]

            nt_new_year = np.append(nt_year, 2021)
            nt_new_price = np.append(nt_price, val2)
            print(nt_new_year)
            print(nt_new_price)
            plotting(nt_new_year, nt_new_price, "NT Price", "Year", "Price", "images/NT Price.png")

        elif (val_ht_nt == 0):
            val1 = input("Enter yearly mean price for electricity: ")
            val1 = float(val1)
            ht_industrie_prices_without_VAT = industrie_prices_without_VAT
            ht_industrie_prices_without_VAT["year"] = ht_industrie_prices_without_VAT["year"].astype(int)
            ht_year = ht_industrie_prices_without_VAT["year"]
            ht_price = ht_industrie_prices_without_VAT["price"]


            ht_new_year = np.append(ht_year, 2021)
            ht_new_price = np.append(ht_price, (val1*ht_factor))
            print(ht_new_year)
            print(ht_new_price)
            plotting(ht_new_year, ht_new_price, "HT Price", "Year", "Price", "images/HT Price.png")
            # plotting(nt_new_year, nt_new_price, "NT Price", "Year", "Price", "images/NT Price.png")


            nt_industrie_prices_without_VAT = industrie_prices_without_VAT
            nt_industrie_prices_without_VAT["year"] = nt_industrie_prices_without_VAT["year"].astype(int)
            nt_year = nt_industrie_prices_without_VAT["year"]
            nt_price = nt_industrie_prices_without_VAT["price"]

            nt_new_year = np.append(nt_year, 2021)
            nt_new_price = np.append(nt_price, (val1*nt_factor))
            print(nt_new_year)
            print(nt_new_price)
            # plotting(ht_new_year, ht_new_price, "HT Price", "Year", "Price", "images/HT Price.png")
            plotting(nt_new_year, nt_new_price, "NT Price", "Year", "Price", "images/NT Price.png")


    elif (val == 2):
        # val1 = input("Enter your preferred price: ")
        # val1 = float(val1)
        ht_industrie_prices_without_VAT = industrie_prices_without_VAT
        ht_industrie_prices_without_VAT["year"] = ht_industrie_prices_without_VAT["year"].astype(int)
        ht_year = ht_industrie_prices_without_VAT["year"]
        ht_price = ht_industrie_prices_without_VAT["price"]
        f = interpolate.interp1d(ht_year, ht_price, fill_value = "extrapolate")
        p_2021 = f(2021)

        ht_new_year = np.append(ht_year, 2021)
        ht_new_price = np.append(ht_price, (f(2021)*ht_factor))
        print(ht_new_year)
        print(ht_new_price)
        plotting(ht_new_year, ht_new_price, "HT Price", "Year", "Price", "images/HT Price.png")
        # plotting(nt_new_year, nt_new_price, "NT Price", "Year", "Price", "images/NT Price.png")

        nt_industrie_prices_without_VAT = industrie_prices_without_VAT
        nt_industrie_prices_without_VAT["year"] = nt_industrie_prices_without_VAT["year"].astype(int)
        nt_year = nt_industrie_prices_without_VAT["year"]
        nt_price = nt_industrie_prices_without_VAT["price"]
        
        f = interpolate.interp1d(nt_year, nt_price, fill_value = "extrapolate")
        p_2021 = f(2021)

        nt_new_year = np.append(nt_year, 2021)
        nt_new_price = np.append(nt_price, (f(2021)*nt_factor))
        print(nt_new_year)
        print(nt_new_price)
        # plotting(ht_new_year, ht_new_price, "HT Price", "Year", "Price", "images/HT Price.png")
        plotting(nt_new_year, nt_new_price, "NT Price", "Year", "Price", "images/NT Price.png")

elif ((val_yearly_demand > 20000) & (val_yearly_demand <= 70000)):
    print("Do you already know your electricty price?")
    print("Yes = 1 / No = 2")
    #choose = 0
    val = input("Enter your value: ")
    val = int(val)
    if (val == 1):
        print("Do you have a yearly mean or HT/NT electricity price structure?")
        val_ht_nt = input("Enter 0 (zero) for yearly mean price and Enter 1 for HT/NT price structure: ")
        val_ht_nt = int(val_ht_nt)
        if (val_ht_nt == 1):
            val1 = input("Enter HT value: ")
            val1 = float(val1)
            val2 = input("Enter NT value: ")
            val2 = float(val2)
            ht_industrie_prices_without_VAT = mid_industrie_prices
            ht_industrie_prices_without_VAT["year"] = ht_industrie_prices_without_VAT["year"].astype(int)
            ht_year = ht_industrie_prices_without_VAT["year"]
            ht_price = ht_industrie_prices_without_VAT["price"]

            ht_new_year = np.append(ht_year, 2021)
            ht_new_price = np.append(ht_price, val1)
            print(ht_new_year)
            print(ht_new_price)
            plotting(ht_new_year, ht_new_price, "HT Price", "Year", "Price", "images/HT Price.png")
            # plotting(nt_new_year, nt_new_price, "NT Price", "Year", "Price", "images/NT Price.png")

            nt_industrie_prices_without_VAT = mid_industrie_prices
            nt_industrie_prices_without_VAT["year"] = nt_industrie_prices_without_VAT["year"].astype(int)
            nt_year = nt_industrie_prices_without_VAT["year"]
            nt_price = nt_industrie_prices_without_VAT["price"]

            nt_new_year = np.append(nt_year, 2021)
            nt_new_price = np.append(nt_price, val2)
            print(nt_new_year)
            print(nt_new_price)
            plotting(nt_new_year, nt_new_price, "NT Price", "Year", "Price", "images/NT Price.png")

        elif (val_ht_nt == 0):
            val1 = input("Enter yearly mean price for electricity: ")
            val1 = float(val1)
            ht_industrie_prices_without_VAT = mid_industrie_prices
            ht_industrie_prices_without_VAT["year"] = ht_industrie_prices_without_VAT["year"].astype(int)
            ht_year = ht_industrie_prices_without_VAT["year"]
            ht_price = ht_industrie_prices_without_VAT["price"]

            ht_new_year = np.append(ht_year, 2021)
            ht_new_price = np.append(ht_price, (val1*ht_factor))
            print(ht_new_year)
            print(ht_new_price)
            plotting(ht_new_year, ht_new_price, "HT Price", "Year", "Price", "images/HT Price.png")
            # plotting(nt_new_year, nt_new_price, "NT Price", "Year", "Price", "images/NT Price.png")


            nt_industrie_prices_without_VAT = mid_industrie_prices
            nt_industrie_prices_without_VAT["year"] = nt_industrie_prices_without_VAT["year"].astype(int)
            nt_year = nt_industrie_prices_without_VAT["year"]
            nt_price = nt_industrie_prices_without_VAT["price"]

            nt_new_year = np.append(nt_year, 2021)
            nt_new_price = np.append(nt_price, (val1*nt_factor))
            print(nt_new_year)
            print(nt_new_price)
            # plotting(ht_new_year, ht_new_price, "HT Price", "Year", "Price", "images/HT Price.png")
            plotting(nt_new_year, nt_new_price, "NT Price", "Year", "Price", "images/NT Price.png")


    elif (val == 2):
        ht_industrie_prices_without_VAT = mid_industrie_prices
        ht_industrie_prices_without_VAT["year"] = ht_industrie_prices_without_VAT["year"].astype(int)
        ht_year = ht_industrie_prices_without_VAT["year"]
        ht_price = ht_industrie_prices_without_VAT["price"]
        f = interpolate.interp1d(ht_year, ht_price, fill_value = "extrapolate")
        p_2021 = f(2021)

        ht_new_year = np.append(ht_year, 2021)
        ht_new_price = np.append(ht_price, (f(2021)*ht_factor))
        print(ht_new_year)
        print(ht_new_price)
        plotting(ht_new_year, ht_new_price, "HT Price", "Year", "Price", "images/HT Price.png")
        # plotting(nt_new_year, nt_new_price, "NT Price", "Year", "Price", "images/NT Price.png")

        nt_industrie_prices_without_VAT = mid_industrie_prices
        nt_industrie_prices_without_VAT["year"] = nt_industrie_prices_without_VAT["year"].astype(int)
        nt_year = nt_industrie_prices_without_VAT["year"]
        nt_price = nt_industrie_prices_without_VAT["price"]
        
        f = interpolate.interp1d(nt_year, nt_price, fill_value = "extrapolate")
        p_2021 = f(2021)

        nt_new_year = np.append(nt_year, 2021)
        nt_new_price = np.append(nt_price, (f(2021)*nt_factor))
        print(nt_new_year)
        print(nt_new_price)
        # plotting(ht_new_year, ht_new_price, "HT Price", "Year", "Price", "images/HT Price.png")
        plotting(nt_new_year, nt_new_price, "NT Price", "Year", "Price", "images/NT Price.png")

elif ((val_yearly_demand > 70000) & (val_yearly_demand <= 150000)):
    print("Do you already know your electricty price?")
    print("Yes = 1 / No = 2")
    #choose = 0
    val = input("Enter your value: ")
    val = int(val)
    if (val == 1):
        print("Do you have a yearly mean or HT/NT electricity price structure?")
        val_ht_nt = input("Enter 0 (zero) for yearly mean price and Enter 1 for HT/NT price structure: ")
        val_ht_nt = int(val_ht_nt)
        if (val_ht_nt == 1):
            val1 = input("Enter HT value: ")
            val1 = float(val1)
            val2 = input("Enter NT value: ")
            val2 = float(val2)
            ht_industrie_prices_without_VAT = big_industrial_prices_BDEW
            ht_industrie_prices_without_VAT["year"] = ht_industrie_prices_without_VAT["year"].astype(int)
            ht_year = ht_industrie_prices_without_VAT["year"]
            ht_price = ht_industrie_prices_without_VAT["price"]

            ht_new_year = np.append(ht_year, 2021)
            ht_new_price = np.append(ht_price, val1)
            print(ht_new_year)
            print(ht_new_price)
            plotting(ht_new_year, ht_new_price, "HT Price", "Year", "Price", "images/HT Price.png")
            # plotting(nt_new_year, nt_new_price, "NT Price", "Year", "Price", "images/NT Price.png")

            nt_industrie_prices_without_VAT = big_industrial_prices_BDEW
            nt_industrie_prices_without_VAT["year"] = nt_industrie_prices_without_VAT["year"].astype(int)
            nt_year = nt_industrie_prices_without_VAT["year"]
            nt_price = nt_industrie_prices_without_VAT["price"]

            nt_new_year = np.append(nt_year, 2021)
            nt_new_price = np.append(nt_price, val2)
            print(nt_new_year)
            print(nt_new_price)
            plotting(nt_new_year, nt_new_price, "NT Price", "Year", "Price", "images/NT Price.png")

        elif (val_ht_nt == 0):
            val1 = input("Enter yearly mean price for electricity: ")
            val1 = float(val1)
            ht_industrie_prices_without_VAT = big_industrial_prices_BDEW
            ht_industrie_prices_without_VAT["year"] = ht_industrie_prices_without_VAT["year"].astype(int)
            ht_year = ht_industrie_prices_without_VAT["year"]
            ht_price = ht_industrie_prices_without_VAT["price"]

            ht_new_year = np.append(ht_year, 2021)
            ht_new_price = np.append(ht_price, (val1*ht_factor))
            print(ht_new_year)
            print(ht_new_price)
            plotting(ht_new_year, ht_new_price, "HT Price", "Year", "Price", "images/HT Price.png")
            # plotting(nt_new_year, nt_new_price, "NT Price", "Year", "Price", "images/NT Price.png")


            nt_industrie_prices_without_VAT = big_industrial_prices_BDEW
            nt_industrie_prices_without_VAT["year"] = nt_industrie_prices_without_VAT["year"].astype(int)
            nt_year = nt_industrie_prices_without_VAT["year"]
            nt_price = nt_industrie_prices_without_VAT["price"]

            nt_new_year = np.append(nt_year, 2021)
            nt_new_price = np.append(nt_price, (val1*nt_factor))
            print(nt_new_year)
            print(nt_new_price)
            # plotting(ht_new_year, ht_new_price, "HT Price", "Year", "Price", "images/HT Price.png")
            plotting(nt_new_year, nt_new_price, "NT Price", "Year", "Price", "images/NT Price.png")


    elif (val == 2):
        ht_industrie_prices_without_VAT = big_industrial_prices_BDEW
        ht_industrie_prices_without_VAT["year"] = ht_industrie_prices_without_VAT["year"].astype(int)
        ht_year = ht_industrie_prices_without_VAT["year"]
        ht_price = ht_industrie_prices_without_VAT["price"]
        f = interpolate.interp1d(ht_year, ht_price, fill_value = "extrapolate")
        p_2021 = f(2021)

        ht_new_year = np.append(ht_year, 2021)
        ht_new_price = np.append(ht_price, (f(2021)*ht_factor))
        print(ht_new_year)
        print(ht_new_price)
        plotting(ht_new_year, ht_new_price, "HT Price", "Year", "Price", "images/HT Price.png")
        # plotting(nt_new_year, nt_new_price, "NT Price", "Year", "Price", "images/NT Price.png")

        nt_industrie_prices_without_VAT = big_industrial_prices_BDEW
        nt_industrie_prices_without_VAT["year"] = nt_industrie_prices_without_VAT["year"].astype(int)
        nt_year = nt_industrie_prices_without_VAT["year"]
        nt_price = nt_industrie_prices_without_VAT["price"]
        
        f = interpolate.interp1d(nt_year, nt_price, fill_value = "extrapolate")
        p_2021 = f(2021)

        nt_new_year = np.append(nt_year, 2021)
        nt_new_price = np.append(nt_price, (f(2021)*nt_factor))
        print(nt_new_year)
        print(nt_new_price)
        # plotting(ht_new_year, ht_new_price, "HT Price", "Year", "Price", "images/HT Price.png")
        plotting(nt_new_year, nt_new_price, "NT Price", "Year", "Price", "images/NT Price.png")

elif ((val_yearly_demand > 150000)):
    print("Do you already know your electricty price?")
    print("Yes = 1 / No = 2")
    #choose = 0
    val = input("Enter your value: ")
    val = int(val)
    if (val == 1):
        print("Do you have a yearly mean or HT/NT electricity price structure?")
        val_ht_nt = input("Enter 0 (zero) for yearly mean price and Enter 1 for HT/NT price structure: ")
        val_ht_nt = int(val_ht_nt)
        if (val_ht_nt == 1):
            val1 = input("Enter HT value: ")
            val1 = float(val1)
            val2 = input("Enter NT value: ")
            val2 = float(val2)
            ht_industrie_prices_without_VAT = v_big_industrial_prices_BDEW
            ht_industrie_prices_without_VAT["year"] = ht_industrie_prices_without_VAT["year"].astype(int)
            ht_year = ht_industrie_prices_without_VAT["year"]
            ht_price = ht_industrie_prices_without_VAT["price"]

            ht_new_year = np.append(ht_year, 2021)
            ht_new_price = np.append(ht_price, val1)
            print(ht_new_year)
            print(ht_new_price)
            plotting(ht_new_year, ht_new_price, "HT Price", "Year", "Price", "images/HT Price.png")
            # plotting(nt_new_year, nt_new_price, "NT Price", "Year", "Price", "images/NT Price.png")

            nt_industrie_prices_without_VAT = v_big_industrial_prices_BDEW
            nt_industrie_prices_without_VAT["year"] = nt_industrie_prices_without_VAT["year"].astype(int)
            nt_year = nt_industrie_prices_without_VAT["year"]
            nt_price = nt_industrie_prices_without_VAT["price"]

            nt_new_year = np.append(nt_year, 2021)
            nt_new_price = np.append(nt_price, val2)
            print(nt_new_year)
            print(nt_new_price)
            plotting(nt_new_year, nt_new_price, "NT Price", "Year", "Price", "images/NT Price.png")

        elif (val_ht_nt == 0):
            val1 = input("Enter yearly mean price for electricity: ")
            val1 = float(val1)
            ht_industrie_prices_without_VAT = v_big_industrial_prices_BDEW
            ht_industrie_prices_without_VAT["year"] = ht_industrie_prices_without_VAT["year"].astype(int)
            ht_year = ht_industrie_prices_without_VAT["year"]
            ht_price = ht_industrie_prices_without_VAT["price"]

            ht_new_year = np.append(ht_year, 2021)
            ht_new_price = np.append(ht_price, (val1*ht_factor))
            print(ht_new_year)
            print(ht_new_price)
            plotting(ht_new_year, ht_new_price, "HT Price", "Year", "Price", "images/HT Price.png")
            # plotting(nt_new_year, nt_new_price, "NT Price", "Year", "Price", "images/NT Price.png")


            nt_industrie_prices_without_VAT = v_big_industrial_prices_BDEW
            nt_industrie_prices_without_VAT["year"] = nt_industrie_prices_without_VAT["year"].astype(int)
            nt_year = nt_industrie_prices_without_VAT["year"]
            nt_price = nt_industrie_prices_without_VAT["price"]

            nt_new_year = np.append(nt_year, 2021)
            nt_new_price = np.append(nt_price, (val1*nt_factor))
            print(nt_new_year)
            print(nt_new_price)
            # plotting(ht_new_year, ht_new_price, "HT Price", "Year", "Price", "images/HT Price.png")
            plotting(nt_new_year, nt_new_price, "NT Price", "Year", "Price", "images/NT Price.png")


    elif (val == 2):
        ht_industrie_prices_without_VAT = v_big_industrial_prices_BDEW
        ht_industrie_prices_without_VAT["year"] = ht_industrie_prices_without_VAT["year"].astype(int)
        ht_year = ht_industrie_prices_without_VAT["year"]
        ht_price = ht_industrie_prices_without_VAT["price"]
        f = interpolate.interp1d(ht_year, ht_price, fill_value = "extrapolate")
        p_2021 = f(2021)

        ht_new_year = np.append(ht_year, 2021)
        ht_new_price = np.append(ht_price, (f(2021)*ht_factor))
        print(ht_new_year)
        print(ht_new_price)
        plotting(ht_new_year, ht_new_price, "HT Price", "Year", "Price", "images/HT Price.png")
        # plotting(nt_new_year, nt_new_price, "NT Price", "Year", "Price", "images/NT Price.png")

        nt_industrie_prices_without_VAT = v_big_industrial_prices_BDEW
        nt_industrie_prices_without_VAT["year"] = nt_industrie_prices_without_VAT["year"].astype(int)
        nt_year = nt_industrie_prices_without_VAT["year"]
        nt_price = nt_industrie_prices_without_VAT["price"]
        
        f = interpolate.interp1d(nt_year, nt_price, fill_value = "extrapolate")
        p_2021 = f(2021)

        nt_new_year = np.append(nt_year, 2021)
        nt_new_price = np.append(nt_price, (f(2021)*nt_factor))
        print(nt_new_year)
        print(nt_new_price)
        # plotting(nt_new_year, nt_new_price, "NT Price", "Year", "Price", "images/NT Price.png")

        plotting(nt_new_year, nt_new_price, "NT Price", "Year", "Price", "images/NT Price.png")
