import numpy as np
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FormatStrFormatter
import os

#T_E = np.genfromtxt('T_E.csv', delimiter=',')
#fig = plt.figure()
#ax = fig.add_subplot(1, 2, 1)
#plt.grid(True)
#plt.grid(linestyle=':')
#t = T_E[:,1]
#e = T_E[:,2]
#plt.scatter(t, e, color='b', marker='*', s=3)
#plt.title(f'Зависимость интегральной интенсивности от температуры')
#plt.xlabel('T')
#plt.ylabel('E')
##plt.xlabel(r'${\lambda},{\mu m}$')

##это самая нечитаемая группировка и усреднение, которые я писала
#means = {}
#for i in np.unique(T_E[:,1]):
#    tmp = T_E[np.where(T_E[:,1] == i)]
#    means[i] = np.mean(tmp[:,2])

#lists = sorted(means.items())
#x, y = zip(*lists)
#ax = fig.add_subplot(1, 2, 2)
#plt.grid(True)
#plt.grid(linestyle=':')
#plt.scatter(x, y, color='b', marker='*', s=3)
#plt.xlabel('T')
#plt.ylabel('E')
#plt.show()

fig = plt.figure()
for subdir, dirs, files in os.walk('parts'):
    for (part,n) in zip(files, range(1,26)):
        T_E = np.genfromtxt(os.path.join(subdir, part), delimiter=',')
        means = {}
        for i in np.unique(T_E[:,1]):
            tmp = T_E[np.where(T_E[:,1] == i)]
            means[i] = np.mean(tmp[:,2])

        lists = sorted(means.items())
        x, y = zip(*lists)
        ax = fig.add_subplot(5, 5, n)
        plt.grid(True)
        plt.grid(linestyle=':')
        plt.scatter(x, y, color='b', marker='*', s=3)
        plt.xlabel('T')
        plt.ylabel('E')
plt.show()