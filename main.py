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

def calculate_mean_price(customer_type, val_yearly_demand):
    """
    
    Parameters
    ----------
    customer_type : Type of customer, differentiated between household and industrial customers
    total_demand : yearly electricity demand for household customers in KWh/y and for industrial customers in MWh/y
    
    Returns
    -------
    mean_price: average price for the customer for the next year in cents/kWh

    """
   

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


    #industrial 2000 - 20000 MWh
    industrie_prices_without_VAT = pd.read_excel(r'Energiepreisentwicklung.xlsx',sheet_name='5.8.3 Strom - € - Industrie', skiprows = 5, nrows = 26, index_col = 0)
    industrie_prices_without_VAT = industrie_prices_without_VAT.iloc[:,0]
    industrie_prices_without_VAT = industrie_prices_without_VAT.reset_index()
    industrie_prices_without_VAT["index"]= industrie_prices_without_VAT["index"].str.slice(start = 5)
    industrie_prices_without_VAT.columns = ["year","price"]
    industrie_prices_without_VAT = industrie_prices_without_VAT.set_index("year")
    industrie_prices_without_VAT.index = industrie_prices_without_VAT.index.astype(str)
    industrie_prices_without_VAT.index =  pd.to_datetime(industrie_prices_without_VAT.index, errors='ignore')
    industrie_prices_without_VAT = industrie_prices_without_VAT.astype(float)
    industrie_prices_without_VAT = industrie_prices_without_VAT.resample('12M').mean()
    industrie_prices_without_VAT.index = industrie_prices_without_VAT.index.astype(str)
    industrie_prices_without_VAT.index= industrie_prices_without_VAT.index.str.slice(start = 0, stop = -6)
    ht_industrie_prices_without_VAT = industrie_prices_without_VAT.price * ht_factor
    nt_industrie_prices_without_VAT = industrie_prices_without_VAT.price * nt_factor
    ht_industrie_prices_without_VAT = ht_industrie_prices_without_VAT.reset_index()
    nt_industrie_prices_without_VAT = nt_industrie_prices_without_VAT.reset_index()
    industrie_prices_without_VAT = industrie_prices_without_VAT.reset_index()
    industrie_prices_without_VAT = industrie_prices_without_VAT[industrie_prices_without_VAT.year >= str(2016)]


    #industrial prices > 150000 MWh/y
    v_big_industrial_prices_BDEW = {'year': range(2019,2021), 'price': [3.77,3.05]}
    v_big_industrial_prices_BDEW = pd.DataFrame(data=v_big_industrial_prices_BDEW)
    v_big_industrial_prices_BDEW

    #industrial prices between 70000-150000 MWh/y
    big_industrial_prices_BDEW = {'year': range(2016,2021), 'price': [8.37, 9.96, 8.96, 9.28, 10.07]}
    big_industrial_prices_BDEW = pd.DataFrame(data=big_industrial_prices_BDEW)
    big_industrial_prices_BDEW


    #industrial prices between 20000-70000 MWh/y
    mid_industrie_prices = pd.read_excel(r'mid_size_industrial_prices.xlsx')
    mid_industrie_prices.columns = ['year', 'price']
    mid_industrie_prices


    #household electricity prices between 2500-5000 KWh/y
    
    household_prices_without_VAT = pd.read_excel(r'Energiepreisentwicklung.xlsx',sheet_name='5.8.2 Strom - € - Haushalte', skiprows = 5, nrows = 26, index_col = 0)
    household_prices_without_VAT = household_prices_without_VAT.iloc[:,0]
    household_prices_without_VAT = household_prices_without_VAT.reset_index()
    household_prices_without_VAT["index"]= household_prices_without_VAT["index"].str.slice(start = 5)
    household_prices_without_VAT.columns = ["year","price"]
    household_prices_without_VAT = household_prices_without_VAT.set_index("year")
    household_prices_without_VAT.index = household_prices_without_VAT.index.astype(str)
    household_prices_without_VAT.index =  pd.to_datetime(household_prices_without_VAT.index, errors='ignore')
    household_prices_without_VAT = household_prices_without_VAT.astype(float)
    household_prices_without_VAT = household_prices_without_VAT.resample('12M').mean()
    household_prices_without_VAT.index = household_prices_without_VAT.index.astype(str)
    household_prices_without_VAT.index= household_prices_without_VAT.index.str.slice(start = 0, stop = -6)
    household_prices_without_VAT = household_prices_without_VAT[6:].reset_index()
    household_prices_without_VAT = household_prices_without_VAT[household_prices_without_VAT.year >= str(2016)]
    household_prices_without_VAT


    if ((customer_type == 0) & ((val_yearly_demand >= 2500) & (val_yearly_demand <= 5000))):
        print("Do you already know your electricty price?")
        #print("Yes = 1 / No = 2")
        print("Yes = 0 / No = 1")
        #choose = 0
        val = input("Enter your value: ")
        val = int(val)
        if (val == 0):
            print("Do you have a fixed electricity price or HT/NT price structure?")
            val_ht_nt = input("Enter 0 (zero) for yearly mean price and Enter 1 for HT/NT price structure: ")
            val_ht_nt = int(val_ht_nt)
            if (val_ht_nt == 1):
                val1 = input("Enter HT value: ")
                val1 = float(val1)
                val2 = input("Enter NT value: ")
                val2 = float(val2)
               
                """# ht_industrie_prices_without_VAT = household_prices
                ht_industrie_prices_without_VAT = household_prices_without_VAT
                ht_industrie_prices_without_VAT["year"] = ht_industrie_prices_without_VAT["year"].astype(int)
                ht_year = ht_industrie_prices_without_VAT["year"]
                ht_price = ht_industrie_prices_without_VAT["price"] * ht_factor

                ht_new_year = np.append(ht_year, 2021)
                ht_new_price = np.append(ht_price, val1 * ht_factor)
                print(ht_new_year)
                print(ht_new_price)
                plotting(ht_new_year, ht_new_price, "HT Price", "Year", "Price", "images/HT Price.png")
                # plotting(nt_new_year, nt_new_price, "NT Price", "Year", "Price", "images/NT Price.png")

                nt_industrie_prices_without_VAT = household_prices_without_VAT
                nt_industrie_prices_without_VAT["year"] = nt_industrie_prices_without_VAT["year"].astype(int)
                nt_year = nt_industrie_prices_without_VAT["year"]
                nt_price = nt_industrie_prices_without_VAT["price"] * nt_factor

                nt_new_year = np.append(nt_year, 2021)
                nt_new_price = np.append(nt_price, val2 * nt_factor)
                print(nt_new_year)
                print(nt_new_price)
                plotting(nt_new_year, nt_new_price, "NT Price", "Year", "Price", "images/NT Price.png")"""
                
                # ht_industrie_prices_without_VAT = household_prices
                ht_household_prices_without_VAT = household_prices_without_VAT
                ht_household_prices_without_VAT["year"] = ht_household_prices_without_VAT["year"].astype(int)
                ht_year = ht_household_prices_without_VAT["year"]
                ht_price = ht_household_prices_without_VAT["price"] * ht_factor

                ht_new_year = np.append(ht_year, 2021)
                ht_new_price = np.append(ht_price, val1 * ht_factor)
                print(ht_new_year)
                print(ht_new_price)
                plotting(ht_new_year, ht_new_price, "HT Price", "Year", "Price", "images/HT Price.png")
                # plotting(nt_new_year, nt_new_price, "NT Price", "Year", "Price", "images/NT Price.png")

                nt_household_prices_without_VAT = household_prices_without_VAT
                nt_household_prices_without_VAT["year"] = nt_household_prices_without_VAT["year"].astype(int)
                nt_year = nt_household_prices_without_VAT["year"]
                nt_price = nt_household_prices_without_VAT["price"] * nt_factor

                nt_new_year = np.append(nt_year, 2021)
                nt_new_price = np.append(nt_price, val2 * nt_factor)
                print(nt_new_year)
                print(nt_new_price)
                plotting(nt_new_year, nt_new_price, "NT Price", "Year", "Price", "images/NT Price.png")
                
                

            elif (val_ht_nt == 0):
                val1 = input("Enter yearly mean price for electricity: ")
                val1 = float(val1)
                yt_household_prices_without_VAT = household_prices_without_VAT
                yt_household_prices_without_VAT["year"] = yt_household_prices_without_VAT["year"].astype(int)
                yt_year = yt_household_prices_without_VAT["year"]
                yt_price = yt_household_prices_without_VAT["price"]

                yt_new_year = np.append(yt_year, 2021)
                yt_new_price = np.append(yt_price, (val1))
                print(yt_new_year)
                print(yt_new_price)
                plotting(yt_new_year, yt_new_price, "Price", "Year", "Price", "images/Price.png")
                # plotting(nt_new_year, nt_new_price, "NT Price", "Year", "Price", "images/NT Price.png")



        elif (val == 1):
            yt_household_prices_without_VAT = household_prices_without_VAT
            yt_household_prices_without_VAT["year"] = yt_household_prices_without_VAT["year"].astype(int)
            yt_year = yt_household_prices_without_VAT["year"]
            yt_price = yt_household_prices_without_VAT["price"]
            f = interpolate.interp1d(ht_year, ht_price, fill_value = "extrapolate")
            p_2021 = f(2021)

            yt_new_year = np.append(yt_year, 2021)
            yt_new_price = np.append(yt_price, (f(2021)))
            # ht_new_price = ht_new_price * ht_factor
            print(yt_new_year)
            print(yt_new_price)
            plotting(yt_new_year, yt_new_price, "Price", "Year", "Price", "images/Price.png")
            # plotting(nt_new_year, nt_new_price, "NT Price", "Year", "Price", "images/NT Price.png")

           

    elif ((customer_type == 1) & (val_yearly_demand >= 2000) & (val_yearly_demand <= 20000)):
        print("Do you already know your electricty price?")
        #print("Yes = 1 / No = 2")
        print("Yes = 0 / No = 1")
        #choose = 0
        val = input("Enter your value: ")
        val = int(val)
        if (val == 0):
            print("Do you have a fixed electricity price or HT/NT price structure?")
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
                ht_new_price = np.append(ht_price, val1 * ht_factor)
                print(ht_new_year)
                print(ht_new_price)
                plotting(ht_new_year, ht_new_price, "HT Price", "Year", "Price", "images/HT Price.png")
                # plotting(nt_new_year, nt_new_price, "NT Price", "Year", "Price", "images/NT Price.png")

                nt_industrie_prices_without_VAT["year"] = nt_industrie_prices_without_VAT["year"].astype(int)
                nt_year = nt_industrie_prices_without_VAT["year"]
                nt_price = nt_industrie_prices_without_VAT["price"]

                nt_new_year = np.append(nt_year, 2021)
                nt_new_price = np.append(nt_price, val2 * nt_factor)
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
                ht_new_price = np.append(ht_price, (val1))
                print(ht_new_year)
                print(ht_new_price)
                plotting(ht_new_year, ht_new_price, "Price", "Year", "Price", "images/Price.png")
                # plotting(nt_new_year, nt_new_price, "NT Price", "Year", "Price", "images/NT Price.png")


        elif (val == 1):
            # val1 = input("Enter your preferred price: ")
            # val1 = float(val1)
            ht_industrie_prices_without_VAT = industrie_prices_without_VAT
            ht_industrie_prices_without_VAT["year"] = ht_industrie_prices_without_VAT["year"].astype(int)
            ht_year = ht_industrie_prices_without_VAT["year"]
            ht_price = ht_industrie_prices_without_VAT["price"]
            f = interpolate.interp1d(ht_year, ht_price, fill_value = "extrapolate")
            p_2021 = f(2021)

            ht_new_year = np.append(ht_year, 2021)
            ht_new_price = np.append(ht_price, (f(2021)))
            ht_new_price = ht_new_price
            print(ht_new_year)
            print(ht_new_price)
            plotting(ht_new_year, ht_new_price, "Price", "Year", "Price", "images/Price.png")
            # plotting(nt_new_year, nt_new_price, "NT Price", "Year", "Price", "images/NT Price.png")

        

    elif ((customer_type == 1) & (val_yearly_demand > 20000) & (val_yearly_demand <= 70000)):
        print("Do you already know your electricty price?")
        #print("Yes = 1 / No = 2")
        print("Yes = 0 / No = 1")
        #choose = 0
        val = input("Enter your value: ")
        val = int(val)
        if (val == 0):
            print("Do you have a fixed electricity price or HT/NT price structure?")
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
                ht_price = ht_industrie_prices_without_VAT["price"] * ht_factor

                ht_new_year = np.append(ht_year, 2021)
                ht_new_price = np.append(ht_price, val1 * ht_factor)
                print(ht_new_year)
                print(ht_new_price)
                plotting(ht_new_year, ht_new_price, "HT Price", "Year", "Price", "images/HT Price.png")
                # plotting(nt_new_year, nt_new_price, "NT Price", "Year", "Price", "images/NT Price.png")

                nt_industrie_prices_without_VAT = mid_industrie_prices
                nt_industrie_prices_without_VAT["year"] = nt_industrie_prices_without_VAT["year"].astype(int)
                nt_year = nt_industrie_prices_without_VAT["year"]
                nt_price = nt_industrie_prices_without_VAT["price"] * nt_factor

                nt_new_year = np.append(nt_year, 2021)
                nt_new_price = np.append(nt_price, val2 * nt_factor)
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
                ht_new_price = np.append(ht_price, (val1))
                print(ht_new_year)
                print(ht_new_price)
                plotting(ht_new_year, ht_new_price, "Price", "Year", "Price", "images/Price.png")
                # plotting(nt_new_year, nt_new_price, "NT Price", "Year", "Price", "images/NT Price.png")
             

        elif (val == 1):
            ht_industrie_prices_without_VAT = mid_industrie_prices
            ht_industrie_prices_without_VAT["year"] = ht_industrie_prices_without_VAT["year"].astype(int)
            ht_year = ht_industrie_prices_without_VAT["year"]
            ht_price = ht_industrie_prices_without_VAT["price"]
            f = interpolate.interp1d(ht_year, ht_price, fill_value = "extrapolate")
            p_2021 = f(2021)

            ht_new_year = np.append(ht_year, 2021)
            ht_new_price = np.append(ht_price, (f(2021)))
            ht_new_price = ht_new_price

            print(ht_new_year)
            print(ht_new_price)
            plotting(ht_new_year, ht_new_price, "Price", "Year", "Price", "images/Price.png")
            # plotting(nt_new_year, nt_new_price, "NT Price", "Year", "Price", "images/NT Price.png")

    elif ((customer_type == 1) & (val_yearly_demand > 70000) & (val_yearly_demand <= 150000)):
        print("Do you already know your electricty price?")
        #print("Yes = 1 / No = 2")
        print("Yes = 0 / No = 1")
        #choose = 0
        val = input("Enter your value: ")
        val = int(val)
        if (val == 0):
            print("Do you have a fixed electricity price or HT/NT price structure?")
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
                ht_price = ht_industrie_prices_without_VAT["price"] * ht_factor

                ht_new_year = np.append(ht_year, 2021)
                ht_new_price = np.append(ht_price, val1 * ht_factor)
                print(ht_new_year)
                print(ht_new_price)
                plotting(ht_new_year, ht_new_price, "HT Price", "Year", "Price", "images/HT Price.png")
                # plotting(nt_new_year, nt_new_price, "NT Price", "Year", "Price", "images/NT Price.png")

                nt_industrie_prices_without_VAT = big_industrial_prices_BDEW
                nt_industrie_prices_without_VAT["year"] = nt_industrie_prices_without_VAT["year"].astype(int)
                nt_year = nt_industrie_prices_without_VAT["year"]
                nt_price = nt_industrie_prices_without_VAT["price"] * nt_factor

                nt_new_year = np.append(nt_year, 2021)
                nt_new_price = np.append(nt_price, val2 * nt_factor)
                print(nt_new_year)
                print(nt_new_price)
                plotting(nt_new_year, nt_new_price, "NT Price", "Year", "Price", "images/NT Price.png")

            elif (val_ht_nt == 0):
                val1 = input("Enter yearly mean price for electricity: ")
                val1 = float(val1)
                ht_industrie_prices_without_VAT = big_industrial_prices_BDEW
                ht_industrie_prices_without_VAT["year"] = ht_industrie_prices_without_VAT["year"].astype(int)
                ht_year = ht_industrie_prices_without_VAT["year"]
                ht_price = ht_industrie_prices_without_VAT["price"] * ht_factor

                ht_new_year = np.append(ht_year, 2021)
                ht_new_price = np.append(ht_price, (val1*ht_factor))
                print(ht_new_year)
                print(ht_new_price)
                plotting(ht_new_year, ht_new_price, "HT Price", "Year", "Price", "images/HT Price.png")
                # plotting(nt_new_year, nt_new_price, "NT Price", "Year", "Price", "images/NT Price.png")


                nt_industrie_prices_without_VAT = big_industrial_prices_BDEW
                nt_industrie_prices_without_VAT["year"] = nt_industrie_prices_without_VAT["year"].astype(int)
                nt_year = nt_industrie_prices_without_VAT["year"]
                nt_price = nt_industrie_prices_without_VAT["price"] * nt_factor

                nt_new_year = np.append(nt_year, 2021)
                nt_new_price = np.append(nt_price, (val1*nt_factor))
                print(nt_new_year)
                print(nt_new_price)
                # plotting(ht_new_year, ht_new_price, "HT Price", "Year", "Price", "images/HT Price.png")
                plotting(nt_new_year, nt_new_price, "NT Price", "Year", "Price", "images/NT Price.png")


        elif (val == 1):
            ht_industrie_prices_without_VAT = big_industrial_prices_BDEW
            ht_industrie_prices_without_VAT["year"] = ht_industrie_prices_without_VAT["year"].astype(int)
            ht_year = ht_industrie_prices_without_VAT["year"]
            ht_price = ht_industrie_prices_without_VAT["price"]
            f = interpolate.interp1d(ht_year, ht_price, fill_value = "extrapolate")
            p_2021 = f(2021)

            ht_new_year = np.append(ht_year, 2021)
            ht_new_price = np.append(ht_price, (f(2021)))
            ht_new_price = ht_new_price

            print(ht_new_year)
            print(ht_new_price)
            plotting(ht_new_year, ht_new_price, "Price", "Year", "Price", "images/Price.png")
            # plotting(nt_new_year, nt_new_price, "NT Price", "Year", "Price", "images/NT Price.png")

        

    elif ((customer_type == 1) & (val_yearly_demand > 150000)):
        print("Do you already know your electricty price?")
        #print("Yes = 1 / No = 2")
        print("Yes = 0 / No = 1")
        #choose = 0
        val = input("Enter your value: ")
        val = int(val)
        if (val == 0):
            print("Do you have a fixed electricity price or HT/NT price structure?")
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
                ht_price = ht_industrie_prices_without_VAT["price"] * ht_factor

                ht_new_year = np.append(ht_year, 2021)
                ht_new_price = np.append(ht_price, val1 * ht_factor)
                print(ht_new_year)
                print(ht_new_price)
                plotting(ht_new_year, ht_new_price, "HT Price", "Year", "Price", "images/HT Price.png")
                # plotting(nt_new_year, nt_new_price, "NT Price", "Year", "Price", "images/NT Price.png")

                nt_industrie_prices_without_VAT = v_big_industrial_prices_BDEW
                nt_industrie_prices_without_VAT["year"] = nt_industrie_prices_without_VAT["year"].astype(int)
                nt_year = nt_industrie_prices_without_VAT["year"]
                nt_price = nt_industrie_prices_without_VAT["price"] * nt_factor

                nt_new_year = np.append(nt_year, 2021)
                nt_new_price = np.append(nt_price, val2 * nt_factor)
                print(nt_new_year)
                print(nt_new_price)
                plotting(nt_new_year, nt_new_price, "NT Price", "Year", "Price", "images/NT Price.png")

            elif (val_ht_nt == 0):
                val1 = input("Enter yearly mean price for electricity: ")
                val1 = float(val1)
                ht_industrie_prices_without_VAT = v_big_industrial_prices_BDEW
                ht_industrie_prices_without_VAT["year"] = ht_industrie_prices_without_VAT["year"].astype(int)
                ht_year = ht_industrie_prices_without_VAT["year"]
                ht_price = ht_industrie_prices_without_VAT["price"] * ht_factor

                ht_new_year = np.append(ht_year, 2021)
                ht_new_price = np.append(ht_price, (val1*ht_factor))
                print(ht_new_year)
                print(ht_new_price)
                plotting(ht_new_year, ht_new_price, "HT Price", "Year", "Price", "images/HT Price.png")
                # plotting(nt_new_year, nt_new_price, "NT Price", "Year", "Price", "images/NT Price.png")


                nt_industrie_prices_without_VAT = v_big_industrial_prices_BDEW
                nt_industrie_prices_without_VAT["year"] = nt_industrie_prices_without_VAT["year"].astype(int)
                nt_year = nt_industrie_prices_without_VAT["year"]
                nt_price = nt_industrie_prices_without_VAT["price"] * nt_factor

                nt_new_year = np.append(nt_year, 2021)
                nt_new_price = np.append(nt_price, (val1*nt_factor))
                print(nt_new_year)
                print(nt_new_price)
                # plotting(ht_new_year, ht_new_price, "HT Price", "Year", "Price", "images/HT Price.png")
                plotting(nt_new_year, nt_new_price, "NT Price", "Year", "Price", "images/NT Price.png")


        elif (val == 1):
            ht_industrie_prices_without_VAT = v_big_industrial_prices_BDEW
            ht_industrie_prices_without_VAT["year"] = ht_industrie_prices_without_VAT["year"].astype(int)
            ht_year = ht_industrie_prices_without_VAT["year"]
            ht_price = ht_industrie_prices_without_VAT["price"]
            f = interpolate.interp1d(ht_year, ht_price, fill_value = "extrapolate")
            p_2021 = f(2021)

            ht_new_year = np.append(ht_year, 2021)
            ht_new_price = np.append(ht_price, (f(2021)))
            ht_new_price = ht_new_price

            print(ht_new_year)
            print(ht_new_price)
            plotting(ht_new_year, ht_new_price, "Price", "Year", "Price", "images/Price.png")
            # plotting(nt_new_year, nt_new_price, "NT Price", "Year", "Price", "images/NT Price.png")

           

print("Which type of Customer category you have?")
print("Enter 0 (zero) for Household customers and 1 (one) for Industrial customers.")        
val1 = input("Please enter your value: ")
val1 = int(val1)
if (val1 == 0):
    print("What is your yearly electricty demand (in KWh/y)?")
    val2 =input("Please enter your value: ")
    val2 = float(val2)
elif(val1 == 1):
    val2 = input("What is your yearly electricty demand in (MWh/y)? ")
    val2 = float(val2)
    
calculate_mean_price(val1,val2)

