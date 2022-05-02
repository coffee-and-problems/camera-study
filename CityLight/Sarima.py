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

def get_min(data):
    data = Enumerable(data)
    return data.order_by_descending(lambda x: x[1])[0]

data = pd.read_csv('CityLight.csv')
data[['date_only', 'time']] = data['date'].str.split(' ', 1, expand=True)
data = data.loc[(data['time'] >= '21:00:00') | (data['time'] <= '02:00:00')]
#data['date'] = pd.to_datetime(data['date'])
data = data.sort_values('date')

start_date = datetime.datetime.strptime(data.iloc[0]['date'], "%Y-%m-%d %H:%M:%S")
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
    current_date = datetime.datetime.strptime(data.iloc[i]['date'], "%Y-%m-%d %H:%M:%S")
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


plt.figure()
plt.scatter(x, y, s=4)
plt.title('Фон неба (в звездных величинах с квадратной секунды) в зависимости от времени')
plt.ylabel('m/"')
plt.xlabel('Год')
plt.xticks(rotation=90)
plt.grid(True)
plt.gca().invert_yaxis()
plt.show()

#ad_fuller_result = adfuller(data['background_magnitude'])
#print(f'ADF Statistic: {ad_fuller_result[0]}')
#print(f'p-value: {ad_fuller_result[1]}') #1e-7, будто ряд стационарный...

##data['background_magnitude'] = np.log(data['background_magnitude'])
##data['background_magnitude'] = data['background_magnitude'].diff()
##data = data.drop(data.index[0])
##data['background_magnitude'] = data['background_magnitude'].diff(12)
##data = data.drop([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], axis=0).reset_index(drop=True)
##plt.figure()
##plt.plot(data['background_magnitude'])
##plt.show()

#def optimize_SARIMA(parameters_list, d, D, s, exog):
#    """
#        Return dataframe with parameters, corresponding AIC and SSE
        
#        parameters_list - list with (p, q, P, Q) tuples
#        d - integration order
#        D - seasonal integration order
#        s - length of season
#        exog - the exogenous variable
#    """
    
#    results = []
    
#    for param in tqdm_notebook(parameters_list):
#        try: 
#            model = SARIMAX(exog, order=(param[0], d, param[1]), seasonal_order=(param[2], D, param[3], s)).fit(disp=-1)
#        except:
#            continue
            
#        aic = model.aic
#        results.append([param, aic])
        
#    result_df = pd.DataFrame(results)
#    result_df.columns = ['(p,q)x(P,Q)', 'AIC']
#    #Чем AIC меньше, тем лучше
#    result_df = result_df.sort_values(by='AIC', ascending=True).reset_index(drop=True)
    
#    return result_df

p = range(0, 4, 1)
d = 1
q = range(0, 4, 1)
P = range(0, 4, 1)
D = 1
Q = range(0, 4, 1)
s = 12
##parameters = product(p, q, P, Q)
##parameters_list = list(parameters) #256 вариантов параметров
##result_df = optimize_SARIMA(parameters_list, d, D, s, data['background_magnitude'])
##print(result_df)

best_model = SARIMAX(y, order=(2, d, 3), seasonal_order=(0, D, 2, s)).fit(dis=-1)
print(best_model.summary())
best_model.plot_diagnostics()

arima = best_model.fittedvalues
#forecast = best_model.predict(start=data.shape[0], end=data.shape[0]+20)
#forecast = data['arima_model'].append(forecast)
plt.figure()
plt.scatter(x, arima, color='r', s=3, label='model')
#plt.axvspan(data.index[-1], forecast.index[-1], alpha=0.5, color='lightgrey')
plt.scatter(x, y, s=3, label='actual')
plt.xticks(rotation=90)
plt.gca().invert_yaxis()
plt.legend()
plt.show()
