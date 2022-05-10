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
import warnings
import datetime
from py_linq import Enumerable
warnings.filterwarnings('ignore')
import sys
from tqdm import tqdm

from sklearn.metrics import mean_absolute_error, mean_squared_error

import statsmodels.formula.api as smf
import statsmodels.tsa.api as smt
import statsmodels.api as sm
import scipy.stats as scs
from scipy.optimize import minimize

def get_min(data):
    data = Enumerable(data)
    return data.order_by_descending(lambda x: x[1])[0]

data = pd.read_csv('CityLightCopy.csv')
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
        else:
            x.append(end_date)
            y.append(np.NaN)
        start_date = end_date
        temp = []
    else:
        temp.append( (current_date, data.iloc[i]['background_magnitude']) )
        i += 1

#plt.figure()
#plt.scatter(x, y, s=4)
#plt.title('Фон неба (в звездных величинах с квадратной секунды) в зависимости от времени')
#plt.ylabel('m/"')
#plt.xlabel('Год')
#plt.xticks(rotation=90)
#plt.grid(True)
#plt.gca().invert_yaxis()
#plt.show()

#ad_fuller_result = adfuller(np.array(y))
#print(f'ADF Statistic: {ad_fuller_result[0]}')
#print(f'p-value: {ad_fuller_result[1]}') #1e-13, будто ряд стационарный...

#fig = plt.figure()
#layout = (2, 2)
#ts_ax = plt.subplot2grid(layout, (0, 0), colspan=2)
#acf_ax = plt.subplot2grid(layout, (1, 0))
#pacf_ax = plt.subplot2grid(layout, (1, 1))

#ts_ax.set_title('Time Series Analysis Plots')
#smt.graphics.plot_acf(np.array(y), ax=acf_ax, alpha=0.2)
#smt.graphics.plot_pacf(np.array(y), ax=pacf_ax, alpha=0.2)

#plt.tight_layout()
#plt.show()

##data['background_magnitude'] = np.log(data['background_magnitude'])
##data['background_magnitude'] = data['background_magnitude'].diff()
##data = data.drop(data.index[0])
##data['background_magnitude'] = data['background_magnitude'].diff(12)
##data = data.drop([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], axis=0).reset_index(drop=True)
##plt.figure()
##plt.plot(data['background_magnitude'])
##plt.show()

def optimize_SARIMA(parameters_list, s, exog):
    """
        Return dataframe with parameters, corresponding AIC and SSE
        
        parameters_list - list with (p, q, P, Q) tuples
        d - integration order
        D - seasonal integration order
        s - length of season
        exog - the exogenous variable
    """
    
    results = []
    
    for param in tqdm_notebook(parameters_list):
        print(param)
        try: 
            model = SARIMAX(exog, order=(param[0], param[1],  param[2]), seasonal_order=(param[3], param[4], param[5], s)).fit(disp=-1)
        except:
            continue
            
        aic = model.aic
        results.append([param, aic])
        
    result_df = pd.DataFrame(results)
    result_df.columns = ['(p,d,q)x(P,D,Q)', 'AIC']
    #Чем AIC меньше, тем лучше
    result_df = result_df.sort_values(by='AIC', ascending=True).reset_index(drop=True)
    
    return result_df

p = range(3, 4, 1)
d = range(0, 2, 1)
q = range(2, 3, 1)
P = range(0, 4, 1)
D = range(0, 2, 1)
Q = range(0, 4, 1)
s = 52
#parameters = product(p, d, q, P, D, Q)
#parameters_list = list(parameters) #256 вариантов параметров
#result_df = optimize_SARIMA(parameters_list, s, y)
#print(result_df)

best_model = SARIMAX(y, order=(3, 1, 2), seasonal_order=(2, 0, 9, s)).fit(dis=-1)
print(best_model.summary())
best_model.plot_diagnostics()

future = 156
arima = best_model.fittedvalues
forecast = best_model.predict(start = len(y), end = len(y)+future)

x_a = []
for x_i in x:
    x_a.append(x_i)
for x_i in range(future+1):
    x_a.append(x_a[-1]  + datetime.timedelta(days=7))

arima = np.append(arima, forecast)
plt.figure()
plt.scatter(x_a, arima, color='r', s=3, label='model')
#plt.axvspan(data.index[-1], forecast.index[-1], alpha=0.5, color='lightgrey')
plt.scatter(x, y, s=3, label='actual')
plt.xticks(rotation=90)
plt.gca().invert_yaxis()
plt.axvspan(x[-1], x_a[-1], alpha=0.5, color='lightgrey')
plt.legend()
plt.show()
