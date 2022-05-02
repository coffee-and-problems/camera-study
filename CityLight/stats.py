from numpy import datetime64
import pandas as pd
import matplotlib.pyplot as plt
import re
import datetime

def dms2dd(s):
    degrees, minutes, seconds = re.split('[:]+', s)
    dd = float(degrees) + float(minutes)/60 + float(seconds)/(60*60)
    return dd

def dms2dd2(s):
    degrees, minutes, seconds = re.split('[:]+', s)
    dd = float(degrees)*60*60 + float(minutes)*60 + float(seconds)
    return dd

def to_time(s):
    return datetime.datetime.strptime(s, "%H:%M:%S")

def to_time2(s):
    return datetime.datetime.strptime(s, "%H:%M")

a = pd.read_fwf("coords.dat")
q = a.iloc[:,5]

def sub(a, b):
    x = []
    for i in range(len(a)):
        split1 = a[i].split(':')
        split2 = b[i].split(':')
        h = float(split1[0])*60*60 + float(split1[1])*60 + float(split1[2]) - float(split2[0])*60*60 - float(split2[1])*60
        if h < 0:
            s = h + 24*60*60
            hours, remainder = divmod(s, 3600)
            minutes, seconds = divmod(remainder, 60)
            x.append('{:02}:{:02}:{:02}'.format(int(hours), int(minutes), int(seconds)))
        else: 
            hours, remainder = divmod(h, 3600)
            minutes, seconds = divmod(remainder, 60)
            x.append('{:02}:{:02}:{:02}'.format(int(hours), int(minutes), int(seconds)))
    return x

def sub2(a, b):
    y = []
    for i in range(len(a)):
        split1 = a[i].split(':')
        split2 = b[i].split(':')
        h = (float(split1[0])*15 + float(split1[1])*0.25 + float(split1[2])*1/240 - float(split2[0])*15 - float(split2[1])*0.25 - float(split2[2])*1/240)*60*60
        y.append(h)
    return y

x_a = sub(a.iloc[:,2], a.iloc[:,1])
x_d = a.iloc[:,3].apply(dms2dd)

y_a = sub2(a.iloc[:,2], a.iloc[:,4])
y_d = a.iloc[:,3].apply(dms2dd2) - a.iloc[:,5].apply(dms2dd2)

a = pd.DataFrame({'x_a': x_a,
                  'y_a': y_a})

a = a.sort_values(by=['x_a'])
plt.grid(True)
plt.grid(linestyle=':')
plt.scatter(a['x_a'], a['y_a'], color='b', marker='o', s=8)
plt.xticks(rotation=90, ha='right')
plt.xlabel('часовой угол, h:m:s')
plt.ylabel('поправка, угловые секунды')
plt.show()

plt.grid(True)
plt.grid(linestyle=':')
plt.scatter(x_d, y_d, c='b', marker='o', s=8)
plt.xlabel('склонение, градусы')
plt.ylabel('поправка, угловые секунды')
plt.show()
