# -*- coding: utf-8 -*-
"""
Functions for estimating electricity prices, eeg levies, remunerations and other components, based on customer type and annual demand

@author: Christian
"""
from typing import ValuesView
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import interpolate
from scipy.interpolate import InterpolatedUnivariateSpline
# some historical prices as reference

#ct/kWh prices from the "Daten zur Energiepreisentwicklung" by Destatis (monthly published https://www.destatis.de/DE/Themen/Wirtschaft/Preise/Publikationen/Energiepreise/energiepreisentwicklung-pdf-5619001.html)
#household 2500-5000 kWh
household_prices_without_VAT = pd.read_excel(r'Energiepreisentwicklung.xlsx',sheet_name='5.8.2 Strom - € - Haushalte', skiprows = 5, nrows = 26, index_col = 0)
household_prices_without_VAT = household_prices_without_VAT.iloc[:,0]

#industrial 2000-20000 MWh
industrial_prices_without_VAT = pd.read_excel(r'Energiepreisentwicklung.xlsx',sheet_name='5.8.3 Strom - € - Industrie', skiprows = 5, nrows = 26, index_col = 0)
industrial_prices_without_VAT = industrial_prices_without_VAT.iloc[:,0]

#BDEW Strompreisanalyse: https://www.bdew.de/media/documents/BDEW-Strompreisanalyse_no_halbjaehrlich_Ba_online_28012021.pdf
#industrial 160-20000 MWh 
industrial_prices_BDEW = {'Jahr': range(1998,2022), 'Preis': [9.34, 8.86, 6.05, 6.47, 6.86, 7.98, 8.92, 9.73, 11.53, 11.41, 13.25, 11.4, 12.07, 14.04, 14.33, 15.11, 15.32, 15.23, 15.55, 17.09, 17.96, 18.43, 17.76, 18.25]}
industrial_prices_BDEW = pd.DataFrame(data=industrial_prices_BDEW)

#industrial 70000-150000 MWh
big_industrial_prices_BDEW = {'Jahr': range(2007,2021), 'Preis': [7.91, 8.56, 8.69, 8.63, 10.07, 9.26, 10.18, 10.48, 9.76, 8.37, 9.96, 8.96, 9.28, 10.07]}
big_industrial_prices_BDEW = pd.DataFrame(data=big_industrial_prices_BDEW)

#VAT
vat = 0.19 # 19% VAT 2021

# possible tax deductibles for large scale companies
stromsteuer_full = 2.05
stromsteuer_reduced = 0.75*stromsteuer_full # some production process are exempted completely (§9a Stromsteuergesetz, z.B. Glas, Zement, Metallerzeugung, chemische Reduktionsverfahren)

konzessionsabgabe_ind = 0.11
konzessionsabgabe_hh = 1.66
konzessionsabgabe_reduced = 0

# EEG-Umlage, needs to be maintained manually (new values each October): https://www.netztransparenz.de/EEG/EEG-Umlagen-Uebersicht/EEG-Umlage-2021
eeg_umlage = 6.5 # 2021
eeg_umlage_red = 0.15*eeg_umlage # für stromkostenintensive Unternehmen gemäß Anlage 4 EEG 2021 für Produktion über 1 GWh, auf erste GWh volle EEG-Umlage
eeg_umlage_min_a = 0.05 # Aluminium, Blei, Zink- und Zinnerzeugung
eeg_umlage_min_b = 0.1 # andere stromkostenintensive Unternehmen gemäß Anlage 4 EEG 2021, auch Elektrolyse

#KWKG-Umlage, needs to be maintained manually (new values each October): https://www.netztransparenz.de/KWKG/KWKG-Umlagen-Uebersicht/KWKG-Umlage-2021
kwkg_umlage = 0.254 # 2021
kwkg_umlage_red = 0.15 * kwkg_umlage # für stromkostenintensive Unternehmen gemäß Anlage 4 EEG 2021 für Produktion über 1 GWh, auf erste GWh volle KWKG-Umlage
kwkg_umlage_min = 0.03

# Offshore-Netzumlage, needs to be maintained manually (new values each October): https://www.netztransparenz.de/EnWG/Offshore-Netzumlage/Offshore-Netzumlagen-Uebersicht/Offshore-Netzumlage-2021
off_umlage = 0.395 # 2021
off_umlage_red = 0.15 * off_umlage # für stromkostenintensive Unternehmen gemäß Anlage 4 EEG 2021 für Produktion über 1 GWh, auf erste GWh volle Offshore-Netzumlage
off_umlage_min = 0.03

# Umlage nach § 19 Abs. 2 StromNEV, needs to be maintained manually (new values each October): https://www.netztransparenz.de/EnWG/-19-StromNEV-Umlage/-19-StromNEV-Umlagen-Uebersicht/-19-StromNEV-Umlage-2021 
nev19_umlage_a = 0.432 # 2021, for the first GWh
nev19_umlage_b = 0.05 # 2021, for all remaining GWh
nev19_umlage_c = 0.025 # 2021, for all electricity cost-heavy producers, for all remaining GWh, also atypical grid usage

nev19_discount_a = 0.8 # only 20% are demmanded if using hours surpass 7000 h
nev19_discount_b = 0.85 # only 15% are demmanded if using hours surpass 7500 h
nev19_discount_c = 0.9 # only 10% are demmanded if using hours surpass 8000 h

def calculate_mean_price(customer_type, total_demand):
    """
    
    Parameters
    ----------
    customer_type : Type of customer, differentiated between household, industrial and GHD
    total_demand : yearly electricity demand in kWh/y
    
    Returns
    -------
    mean_price: average price for the customer in the given year in €/kWh

    """
   
        
    
    
    
    # mean_price=14

    # return mean_price


def calculate_mean_price(customer_type, val_yearly_demand):
    """
    
    Parameters
    ----------
    customer_type : Type of customer, differentiated between household, industrial and GHD
    total_demand : yearly electricity demand in kWh/y
    
    Returns
    -------
    mean_price: average price for the customer in the given year in €/kWh

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

    industrie_prices_without_VAT = pd.read_excel(r'/Users/shakhawathossainturag/Downloads/Energiepreisentwicklung.xlsx',sheet_name='5.8.3 Strom - € - Industrie', skiprows = 5, nrows = 26, index_col = 0)
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

    #industrie_prices_without_VAT = industrie_prices_without_VAT[6:].reset_index()
    ht_industrie_prices_without_VAT = ht_industrie_prices_without_VAT.reset_index()
    nt_industrie_prices_without_VAT = nt_industrie_prices_without_VAT.reset_index()

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
    household_prices_without_VAT = pd.read_excel(r'/Users/shakhawathossainturag/Downloads/Energiepreisentwicklung.xlsx',sheet_name='5.8.2 Strom - € - Haushalte', skiprows = 5, nrows = 26, index_col = 0)
    household_prices_without_VAT = household_prices_without_VAT.iloc[:,0]
    #household_prices_without_VAT.columns = ["year","price"]
    household_prices_without_VAT = household_prices_without_VAT.reset_index()
    household_prices_without_VAT["index"]= household_prices_without_VAT["index"].str.slice(start = 5)
    household_prices_without_VAT.columns = ["year","price"]
    # household_prices_without_VAT
    household_prices_without_VAT = household_prices_without_VAT.set_index("year")

    household_prices_without_VAT.index = household_prices_without_VAT.index.astype(str)
    household_prices_without_VAT.index =  pd.to_datetime(household_prices_without_VAT.index, errors='ignore')
    household_prices_without_VAT = household_prices_without_VAT.astype(float)
    household_prices_without_VAT = household_prices_without_VAT.resample('12M').mean()
    household_prices_without_VAT.index = household_prices_without_VAT.index.astype(str)
    # household_prices_without_VAT
    household_prices_without_VAT.index= household_prices_without_VAT.index.str.slice(start = 0, stop = -6)
    # household_prices_without_VAT
    household_prices_without_VAT = household_prices_without_VAT[6:].reset_index()





    # household_prices = pd.read_excel(r'households_price.xlsx')
    # household_prices.columns = ['year', 'price']
    # household_prices

    # print("Whats your yearly electricity demand?")
    # val_yearly_demand = input("Please Input Demand:")
    # val_yearly_demand = float(val_yearly_demand)

    # print("Whats your customer type?")
    # print("For households enter 1 and for industrial enter 2.")
    # customer_type = input("Enter your value:")
    # customer_type = int(val_yearly_demand)


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
                # ht_industrie_prices_without_VAT = household_prices
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
                plotting(nt_new_year, nt_new_price, "NT Price", "Year", "Price", "images/NT Price.png")

            elif (val_ht_nt == 0):
                val1 = input("Enter yearly mean price for electricity: ")
                val1 = float(val1)
                ht_industrie_prices_without_VAT = household_prices_without_VAT
                ht_industrie_prices_without_VAT["year"] = ht_industrie_prices_without_VAT["year"].astype(int)
                ht_year = ht_industrie_prices_without_VAT["year"]
                ht_price = ht_industrie_prices_without_VAT["price"]

                ht_new_year = np.append(ht_year, 2021)
                ht_new_price = np.append(ht_price, (val1))
                print(ht_new_year)
                print(ht_new_price)
                plotting(ht_new_year, ht_new_price, "Price", "Year", "Price", "images/Price.png")
                # plotting(nt_new_year, nt_new_price, "NT Price", "Year", "Price", "images/NT Price.png")


                # nt_industrie_prices_without_VAT = household_prices_without_VAT
                # nt_industrie_prices_without_VAT["year"] = nt_industrie_prices_without_VAT["year"].astype(int)
                # nt_year = nt_industrie_prices_without_VAT["year"]
                # nt_price = nt_industrie_prices_without_VAT["price"] * nt_factor

                # nt_new_year = np.append(nt_year, 2021)
                # nt_new_price = np.append(nt_price, (val1*nt_factor))
                # print(nt_new_year)
                # print(nt_new_price)
                # # plotting(ht_new_year, ht_new_price, "HT Price", "Year", "Price", "images/HT Price.png")
                # plotting(nt_new_year, nt_new_price, "NT Price", "Year", "Price", "images/NT Price.png")


        elif (val == 1):
            ht_industrie_prices_without_VAT = household_prices_without_VAT
            ht_industrie_prices_without_VAT["year"] = ht_industrie_prices_without_VAT["year"].astype(int)
            ht_year = ht_industrie_prices_without_VAT["year"]
            ht_price = ht_industrie_prices_without_VAT["price"]
            f = interpolate.interp1d(ht_year, ht_price, fill_value = "extrapolate")
            p_2021 = f(2021)

            ht_new_year = np.append(ht_year, 2021)
            ht_new_price = np.append(ht_price, (f(2021)))
            # ht_new_price = ht_new_price * ht_factor
            print(ht_new_year)
            print(ht_new_price)
            plotting(ht_new_year, ht_new_price, "Price", "Year", "Price", "images/Price.png")
            # plotting(nt_new_year, nt_new_price, "NT Price", "Year", "Price", "images/NT Price.png")

            # nt_industrie_prices_without_VAT = household_prices_without_VAT
            # nt_industrie_prices_without_VAT["year"] = nt_industrie_prices_without_VAT["year"].astype(int)
            # nt_year = nt_industrie_prices_without_VAT["year"]
            # nt_price = nt_industrie_prices_without_VAT["price"]
            
            # f = interpolate.interp1d(nt_year, nt_price, fill_value = "extrapolate")
            # p_2021 = f(2021)

            # nt_new_year = np.append(nt_year, 2021)
            # nt_new_price = np.append(nt_price, (f(2021)))
            # nt_new_price = nt_new_price * nt_factor
            # print(nt_new_year)
            # print(nt_new_price)
            # # plotting(ht_new_year, ht_new_price, "HT Price", "Year", "Price", "images/HT Price.png")
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


                # nt_industrie_prices_without_VAT = industrie_prices_without_VAT
                # nt_industrie_prices_without_VAT["year"] = nt_industrie_prices_without_VAT["year"].astype(int)
                # nt_year = nt_industrie_prices_without_VAT["year"]
                # nt_price = nt_industrie_prices_without_VAT["price"] * nt_factor

                # nt_new_year = np.append(nt_year, 2021)
                # nt_new_price = np.append(nt_price, (val1*nt_factor))
                # print(nt_new_year)
                # print(nt_new_price)
                # # plotting(ht_new_year, ht_new_price, "HT Price", "Year", "Price", "images/HT Price.png")
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

            # nt_industrie_prices_without_VAT = industrie_prices_without_VAT
            # nt_industrie_prices_without_VAT["year"] = nt_industrie_prices_without_VAT["year"].astype(int)
            # nt_year = nt_industrie_prices_without_VAT["year"]
            # nt_price = nt_industrie_prices_without_VAT["price"]
            
            # f = interpolate.interp1d(nt_year, nt_price, fill_value = "extrapolate")
            # p_2021 = f(2021)

            # nt_new_year = np.append(nt_year, 2021)
            # nt_new_price = np.append(nt_price, (f(2021)))
            # nt_new_price = nt_new_price * nt_factor

            # print(nt_new_year)
            # print(nt_new_price)
            # # plotting(ht_new_year, ht_new_price, "HT Price", "Year", "Price", "images/HT Price.png")
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


                # nt_industrie_prices_without_VAT = mid_industrie_prices
                # nt_industrie_prices_without_VAT["year"] = nt_industrie_prices_without_VAT["year"].astype(int)
                # nt_year = nt_industrie_prices_without_VAT["year"]
                # nt_price = nt_industrie_prices_without_VAT["price"] * nt_factor

                # nt_new_year = np.append(nt_year, 2021)
                # nt_new_price = np.append(nt_price, (val1*nt_factor))
                # print(nt_new_year)
                # print(nt_new_price)
                # # plotting(ht_new_year, ht_new_price, "HT Price", "Year", "Price", "images/HT Price.png")
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

            # nt_industrie_prices_without_VAT = mid_industrie_prices
            # nt_industrie_prices_without_VAT["year"] = nt_industrie_prices_without_VAT["year"].astype(int)
            # nt_year = nt_industrie_prices_without_VAT["year"]
            # nt_price = nt_industrie_prices_without_VAT["price"]
            
            # f = interpolate.interp1d(nt_year, nt_price, fill_value = "extrapolate")
            # p_2021 = f(2021)

            # nt_new_year = np.append(nt_year, 2021)
            # nt_new_price = np.append(nt_price, (f(2021)))
            # nt_new_price = nt_new_price * nt_factor

            # print(nt_new_year)
            # print(nt_new_price)
            # # plotting(ht_new_year, ht_new_price, "HT Price", "Year", "Price", "images/HT Price.png")
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

            # nt_industrie_prices_without_VAT = big_industrial_prices_BDEW
            # nt_industrie_prices_without_VAT["year"] = nt_industrie_prices_without_VAT["year"].astype(int)
            # nt_year = nt_industrie_prices_without_VAT["year"]
            # nt_price = nt_industrie_prices_without_VAT["price"]
            
            # f = interpolate.interp1d(nt_year, nt_price, fill_value = "extrapolate")
            # p_2021 = f(2021)

            # nt_new_year = np.append(nt_year, 2021)
            # nt_new_price = np.append(nt_price, (f(2021)))
            # nt_new_price = nt_new_price * nt_factor

            # print(nt_new_year)
            # print(nt_new_price)
            # # plotting(ht_new_year, ht_new_price, "HT Price", "Year", "Price", "images/HT Price.png")
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

            # nt_industrie_prices_without_VAT = v_big_industrial_prices_BDEW
            # nt_industrie_prices_without_VAT["year"] = nt_industrie_prices_without_VAT["year"].astype(int)
            # nt_year = nt_industrie_prices_without_VAT["year"]
            # nt_price = nt_industrie_prices_without_VAT["price"]
            
            # f = interpolate.interp1d(nt_year, nt_price, fill_value = "extrapolate")
            # p_2021 = f(2021)

            # nt_new_year = np.append(nt_year, 2021)
            # nt_new_price = np.append(nt_price, (f(2021)))
            # nt_new_price = nt_new_price * nt_factor

            # print(nt_new_year)
            # print(nt_new_price)
            # # plotting(nt_new_year, nt_new_price, "NT Price", "Year", "Price", "images/NT Price.png")

            # plotting(nt_new_year, nt_new_price, "NT Price", "Year", "Price", "images/NT Price.png")

            
        
        
        
        # mean_price=14

        # return mean_price


# Please input customer type in first parameter and total demand as 2nd parameter
# For Customer type 0: Household and 1: Industrial 
calculate_mean_price(0,2500)
