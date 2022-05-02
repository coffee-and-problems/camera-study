import numpy as np
import matplotlib.pyplot as plt
import numpy as np
import os

T_E = np.genfromtxt('T_E.csv', delimiter=',')

#это самая нечитаемая группировка и усреднение, которые я писала
means = {}
for i in np.unique(np.around(T_E[:,1])):
    tmp = T_E[np.where(np.around(T_E[:,1]) == i)]
    means[i] = np.mean(tmp[:,2])

lists = sorted(means.items())
x, y = zip(*lists)
(n, p) = np.polyfit(x, np.log(y), 1)
full = np.full(len(x), np.exp(n))
fit = np.exp(p) * np.power(full, np.asarray(x))

plt.grid(True)
plt.grid(linestyle=':')
plt.scatter(x, y, color='b', marker='*', s=3)
#plt.plot(x, fit, c='r')
plt.xlabel('T')
plt.ylabel('E')
plt.show()

fig = plt.figure()
for subdir, dirs, files in os.walk('parts'):
    for (part,n) in zip(files, range(1,26)):
        T_E = np.genfromtxt(os.path.join(subdir, part), delimiter=',')
        means = {}
        for i in np.unique(np.around(T_E[:,1])):
            tmp = T_E[np.where(np.around(T_E[:,1]) == i)]
            means[i] = np.mean(tmp[:,2])

        lists = sorted(means.items())
        x, y = zip(*lists)
        ax = fig.add_subplot(4, 4, n)
        plt.grid(True)
        plt.grid(linestyle=':')
        plt.scatter(x, y, color='b', marker='*', s=3)
        plt.xlabel('T')
        plt.ylabel('E')
plt.show()