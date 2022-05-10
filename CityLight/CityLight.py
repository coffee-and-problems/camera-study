from statsmodels.graphics.tsaplots import plot_pacf
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from statsmodels.tsa.stattools import adfuller
import matplotlib.pyplot as plt
from tqdm import tqdm_notebook
import numpy as np
import pandas as pd
from itertools import product
# This module allows us to use LINQ syntaxis to operate the collections
from py_linq import Enumerable
import warnings
warnings.filterwarnings('ignore')
from statsmodels.tsa.seasonal import seasonal_decompose
import datetime

data = pd.read_csv('CityLight.csv')
#I hate python so much because of this:
data.reset_index(inplace=True)
data['date'] = pd.to_datetime(data['date']).dt.date
data = data.sort_values('date')
data = data.set_index('date')

def get_min(data):
    data = Enumerable(data)
    return data.order_by_descending(lambda x: x[1])[0]

data = pd.read_csv('CityLight.csv')
data[['date_only', 'time']] = data['date'].str.split('T', 1, expand=True)
data = data.loc[(data['time'] >= '21:00:00') | (data['time'] <= '02:00:00')]
#data['date'] = pd.to_datetime(data['date'])
data = data.sort_values('date')

start_date = datetime.datetime.strptime(data.iloc[0]['date_only'], "%Y-%m-%d")
i=0

temp = []
x = []
y = []
while True:
    if i == len(data):
        if len(temp) > 0:
            minimum = get_min(temp)
            x.append(minimum[0])
            y.append(minimum[1])
        break
    end_date = start_date + datetime.timedelta(days=7)
    current_date = datetime.datetime.strptime(data.iloc[i]['date_only'], "%Y-%m-%d")
    if current_date > end_date:
        if len(temp) > 0:
            minimum = get_min(temp)
            x.append(minimum[0])
            y.append(minimum[1])
        start_date = current_date
        temp = []
    else:
        temp.append( (current_date, data.iloc[i]['background_magnitude']) )
    i += 1


decompose_result_mult = seasonal_decompose(y, model="additive", freq=9)

#figure = decompose_result_mult.plot()
#figure.axes[0].invert_yaxis()
#figure.axes[1].invert_yaxis()

#fig, axis = plt.subplots(4)
plt.gca().invert_yaxis()
#axis[0].plot(x, decompose_result_mult.observed)#.set_title('Observed')
#axis[1].plot(x, decompose_result_mult.trend)#.set_title('Trend')
#axis[2].plot(x, decompose_result_mult.seasonal)#.set_title('Seasonal')
#axis[3].plot(x, decompose_result_mult.resid)#.set_title('Residuals')

decompose_result_mult.plot();
#plt.plot(x,decompose_result_mult.trend)
plt.show()



#data['date']= data['date'].dt.year
#data = data.sort_values('date')

#print(data.groupby(['date']).mean())