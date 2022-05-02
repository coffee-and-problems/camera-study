from numpy import datetime64
import pandas as pd
import matplotlib.pyplot as plt
import re
import datetime

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
ra = {}
dec = {}

for index, row in tab.iterrows():
    ra[row[0]] = row[2]
    dec[row[0]] = f"{row[3]} {row[4]}"

a = pd.read_csv("pointing.dat", header=None, delimiter=' ')
names = a.iloc[:,2]

def sub(a):
    split1 = a.split(' ')
    h = float(split1[0])*60*60 + float(split1[1])*60 + float(split1[2])
    hours, remainder = divmod(h, 3600)
    minutes, seconds = divmod(remainder, 60)
    return hours*15 + minutes*0.25 + seconds*1/240

def sub2(a, b, c):
    split1 = a.split(' ')
    split_time = c.split(':')
    h = float(split1[0])*15 + float(split1[1])*0.25 + float(split1[2])*1/240 - b #+ float(split_time[0])*15 + float(split_time[1])*0.25 + float(split_time[2])*1/240
    return h

x_a = []
x_d = []
y_a = []
y_d = []
for index, row in a.iterrows():
    try:
        x_a.append(sub(ra[row[2]]))
        x_d.append(dms2dd(dec[row[2]]))
        y_a.append(sub2(ra[row[2]], float(row[3]), row[0].split(";")[-1]))
        y_d.append(dms2dd2(dec[row[2]]) - float(row[4])*60*60)
    except:
        continue

a = pd.DataFrame({'x_a': x_a,
                  'y_a': y_a})

a = a.sort_values(by=['x_a'])
plt.grid(True)
plt.grid(linestyle=':')
plt.scatter(a['x_a'], a['y_a'], color='b', marker='o', s=8)
plt.xticks(rotation=90, ha='right')
plt.xlabel('прямое восхождение, градусы')
plt.ylabel('поправка, градусы')
plt.show()

plt.grid(True)
plt.grid(linestyle=':')
plt.scatter(x_d, y_d, c='b', marker='o', s=8)
plt.xlabel('склонение, градусы')
plt.ylabel('поправка, угловые секунды')
plt.show()

