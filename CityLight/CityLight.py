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

data = pd.read_csv('CityLight.csv')
#I hate python so much because of this:
data.reset_index(inplace=True)
data['date'] = pd.to_datetime(data['date']).dt.date
data = data.sort_values('date')
data = data.set_index('date')

decompose_result_mult = seasonal_decompose(data['background_magnitude'], model="additive", freq=120)

trend = decompose_result_mult.trend
seasonal = decompose_result_mult.seasonal
residual = decompose_result_mult.resid

decompose_result_mult.plot();
plt.show()

#data['date']= data['date'].dt.year
#data = data.sort_values('date')

#print(data.groupby(['date']).mean())