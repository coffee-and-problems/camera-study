from numpy import datetime64
import pandas as pd
import matplotlib.pyplot as plt
import re
import datetime
import astropy.units as u
from astropy.coordinates import SkyCoord
from astropy.coordinates import FK5

def dms2dd(s):
    degrees, minutes, seconds = re.split(' ', s)
    dd = float(degrees) + float(minutes)/60 + float(seconds)/(60*60)
    return dd

def dms2dd2(s):
    degrees, minutes, seconds = re.split(' ', s)
    dd = float(degrees)*60*60 + float(minutes)*60 + float(seconds)
    return dd

def to_time(s):
    return datetime.datetime.strptime(s, "%H:%M:%S")

def to_time2(s):
    return datetime.datetime.strptime(s, "%H:%M")

tab = pd.read_fwf("TABOB.TXT")
coords = {}

for index, row in tab.iterrows():
    ra = float(row[1])*15 + float(row[2])*0.25 + float(row[3])*1/240
    dec = float(row[4]) + float(row[5])/60 + float(row[6])/60/60

    fk5c = SkyCoord(ra*u.degree, dec*u.degree, frame='fk5')
    fk5_2022 = FK5(equinox='B2022')
    coords[row[0]] = fk5c.transform_to(fk5_2022)

data = pd.read_csv("pointing.dat", header=None, delimiter=' ')

x_a = []
x_d = []
y_a = []
y_d = []
for index, row in data.iterrows():
    try:
        x_a.append(coords[row[2]].ra.degree)
        x_d.append(coords[row[2]].dec.degree)
        y_a.append(coords[row[2]].ra.degree*60 - float(row[3])*60)
        y_d.append(coords[row[2]].dec.degree*60 - float(row[4])*60)
    except:
        continue

df = pd.DataFrame({'x_a': x_a,
                  'y_a': y_a})

df = df.sort_values(by=['x_a'])
plt.grid(True)
plt.grid(linestyle=':')
plt.scatter(df['x_a'], df['y_a'], color='b', marker='o', s=8)
plt.xticks(rotation=90, ha='right')
plt.xlabel('прямое восхождение, градусы')
plt.ylabel('поправка, угловые минуты')
plt.show()

plt.grid(True)
plt.grid(linestyle=':')
plt.scatter(x_d, y_d, c='b', marker='o', s=8)
plt.xlabel('склонение, градусы')
plt.ylabel('поправка, угловые минуты')
plt.show()

