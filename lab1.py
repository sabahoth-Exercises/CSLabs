# 1 import

import numpy as npy
from numpy import linalg as lng
from matplotlib import pyplot as ppt

# 2 loading data and separate each value(time, voltage, current)

data_from_variant = npy.genfromtxt('testLab1Var19.csv', delimiter=',')

time = data_from_variant[:, 0]
current = data_from_variant[:, 1]
voltage = data_from_variant[:, 2]
positive_voltage = npy.where(voltage > 0, voltage, 0)
positive_voltage = positive_voltage[:, npy.newaxis]

time = time[:, npy.newaxis]
voltage = voltage[:, npy.newaxis]
current = current[:, npy.newaxis]

# 3
T_per = 0.1
fig, (ay1, ay2) = ppt.subplots(2, 1, sharex=True)
ay1.plot(time[time < 2 * T_per], voltage[time < 2 * T_per])
ay1.grid()
ay1.set_xlabel('time,s')
ay1.set_ylabel('voltage,V')

ay2.plot(time[time < 2 * T_per], current[time < 2 * T_per])
ay2.grid()
ay2.set_xlabel('time,s')
ay2.set_ylabel('current,A')
ppt.show()
fig.savefig('Data (part)')

# 4
Td = 0.001
X = npy.concatenate([voltage[0:len(voltage) - 2], current[0:len(current) - 2]], axis=1)
Y = current[1:len(current) - 1]
K = npy.dot(npy.dot(lng.inv(npy.dot(X.T, X)), X.T), Y)

R = 1 / K[0] * (1 - K[1])
T = -Td / npy.log(K[1])
L = T * R

current_est = X.dot(K)
fig, ax = ppt.subplots(1, 1)
ppt.plot(time[time < T_per], current[time < T_per])
ppt.plot(time[time < T_per], current_est[time[0:len(current) - 2] < T_per])
ax.grid()
ax.set_xlabel('time,s')
ax.set_ylabel('current, A')
ppt.show()
fig.savefig('Compared data(part')

#  5 Calculation of estimated values of parameters L and R.
R_est = []
L_est = []
n = 1000

for i in range(0, n - 1, 1):
    ind = (time >= T_per * i) & (time <= T_per * (i + 1))
    new_current = current[ind]
    new_current = new_current[:, npy.newaxis]
    new_voltage = voltage[ind]
    # new_voltage = positive_voltage[ind]
    new_voltage = new_voltage[:, npy.newaxis]
    X = npy.concatenate([new_voltage[0:len(new_voltage) - 2], new_current[0:len(new_current) - 2]], axis=1)
    Y = new_current[1:len(new_current) - 1]
    K = npy.dot(npy.dot(lng.inv(npy.dot(X.T, X)), X.T), Y)

    if K[1] > 0:
        R = 1 / K[0] * (1 - K[1])
        T = -Td / npy.log(K[1])
        L = T * R
        R_est.append(R)
        L_est.append(T * R)

print('Mean value of R: ', npy.mean(R_est), 'Ohms')
print('Standart deviation of R: ', npy.std(R_est))
print('Mean value of L: ', npy.mean(L_est), 'H')
print('Standart deviation of L: ', npy.std(L_est))

