import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import interpolate
from scipy.interpolate import InterpolatedUnivariateSpline
from scipy.interpolate import interp1d

industrie_prices_without_VAT = pd.read_excel(r'Energiepreisentwicklung.xlsx',sheet_name='5.8.3 Strom - € - Industrie', skiprows = 5, nrows = 26, index_col = 0)
industrie_prices_without_VAT = industrie_prices_without_VAT.iloc[:,0]
#household_prices_without_VAT.columns = ["year","price"]
industrie_prices_without_VAT = industrie_prices_without_VAT.reset_index()
industrie_prices_without_VAT.head()

industrie_prices_without_VAT["index"]= industrie_prices_without_VAT["index"].str.slice(start = 5)
industrie_prices_without_VAT.columns = ["year","price"]
industrie_prices_without_VAT.head()

industrie_prices_without_VAT = industrie_prices_without_VAT.set_index("year")

industrie_prices_without_VAT.index = industrie_prices_without_VAT.index.astype(str)
industrie_prices_without_VAT.index =  pd.to_datetime(industrie_prices_without_VAT.index, errors='ignore')
industrie_prices_without_VAT = industrie_prices_without_VAT.astype(float)
industrie_prices_without_VAT = industrie_prices_without_VAT.resample('12M').mean()
industrie_prices_without_VAT.index = industrie_prices_without_VAT.index.astype(str)
industrie_prices_without_VAT.head()

industrie_prices_without_VAT.index= industrie_prices_without_VAT.index.str.slice(start = 0, stop = -6)
industrie_prices_without_VAT.head()

industrie_prices_without_VAT = industrie_prices_without_VAT.reset_index()
industrie_prices_without_VAT

industrie_prices_without_VAT = industrie_prices_without_VAT[industrie_prices_without_VAT.year >= str(2016)]


#industrial 70000-150000 MWh
big_industrial_prices_BDEW = {'year': range(2016,2021), 'price': [8.37, 9.96, 8.96, 9.28, 10.07]}
big_industrial_prices_BDEW = pd.DataFrame(data=big_industrial_prices_BDEW)
# big_industrial_prices_BDEW = big_industrial_prices_BDEW.set_index("year")
big_industrial_prices_BDEW

df = industrie_prices_without_VAT.join(big_industrial_prices_BDEW, lsuffix='_small', rsuffix='_big')
df = df[["year_small","price_small","price_big"]]

df1 = df.set_index("year_small")
df1

df1['price_mid'] = np.nan
df1 = df1[["price_small", "price_mid", "price_big"]]
df1


for i in range(len(df)):
    x = df1.iloc[i].interpolate(method ="linear")
    df1.price_mid[i] = x[1]
df1


x = df1["price_mid"]

x
x.to_excel("mid_size_industrial_prices.xlsx")


# import pandas as pd
# import seaborn as sns

# plt.rcParams["figure.figsize"] = [7.50, 4.50]
# plt.rcParams["figure.autolayout"] = True
# #ax = plt.gca()

# df = df1
# df

# df = df.reset_index().melt('year_small', var_name='cols',  value_name='vals')
# g = sns.catplot(x="year_small", y="vals", hue='cols', data=df, kind='point')