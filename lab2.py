# 1
import pandas as pds
import numpy as npy
import matplotlib.pyplot as ppt
from scipy.special import expit as function_act
from xlsxwriter import Workbook

file = 'CPSLab2.xlsx'

"""
Function to set basic network parameters
 2 => 28x28=784 input signals
 0-9 => 10 output signals
"""


def init_net():
    input_nodes = 784
    print('Input the number of hidden neurons:')
    hidden_nodes = int(input())
    out_nodes = 10
    print('Input the training speed (0.5):')
    learn_speed = float(input())
    return input_nodes, hidden_nodes, out_nodes, learn_speed


# 3
def create_net_rand(input_nodes, hidden_nodes, out_nodes):
    w_in2hidden = npy.random.uniform(-0.5, 0.5, (hidden_nodes, input_nodes))
    w_hidden2out = npy.random.uniform(-0.5, 0.5, (out_nodes, hidden_nodes))
    return w_in2hidden, w_hidden2out


def create_net_fix(input_nodes, hidden_nodes, out_nodes):
    w_in2hidden = npy.zeros([hidden_nodes, input_nodes], dtype=float) + 0.5
    w_hidden2out = npy.zeros([out_nodes, hidden_nodes], dtype=float) + 0.5
    return w_in2hidden, w_hidden2out


# 4
def net_output(w_in2hidden, w_hidden2out, input_signal, return_hidden):
    inputs = npy.array(input_signal, ndmin=2).T
    hidden_in = npy.dot(w_in2hidden, inputs)
    hidden_out = function_act(hidden_in)
    final_in = npy.dot(w_hidden2out, hidden_out)
    final_out = function_act(final_in)
    if return_hidden == 0:
        return final_out
    else:
        return final_out, hidden_out


# 5
def net_train(target_list, input_signal, w_in2hidden, w_hidden2out, learn_speed):
    targets = npy.array(target_list, ndmin=2).T
    inputs = npy.array(input_signal, ndmin=2).T
    final_out, hidden_out = net_output(w_in2hidden, w_hidden2out, input_signal, 1)
    out_errors = targets - final_out
    hidden_errors = npy.dot(w_hidden2out.T, out_errors)
    w_hidden2out += learn_speed * npy.dot((out_errors * final_out * (1 - final_out)), hidden_out.T)
    w_in2hidden += learn_speed * npy.dot((hidden_errors * hidden_out * (1 - hidden_out)), inputs.T)
    return w_in2hidden, w_hidden2out


# 6
def train_set(w_in2hidden, w_hidden2out, learn_speed):
    data_file = open('mnist_train.csv', 'r')
    training_list = data_file.readlines()
    data_file.close()
    for record in training_list:
        all_values = record.split(',')
        # the range of pixel values is [0,255]
        # we will scale it to [0.001;1] not to [0;1]
        inputs = (npy.asfarray(all_values[1:]) / 255.0 * 0.999) + 0.001
        # 0-9
        targets = npy.zeros(10) + 0.001
        targets[int(all_values[0])] = 1.0
        w_in2hidden, w_hidden2out = net_train(targets, inputs, w_in2hidden, w_hidden2out, learn_speed)
    return w_in2hidden, w_hidden2out


# 7
def test_set(w_in2hidden, w_hidden2out):
    data_file = open('mnist_test.csv', 'r')
    test_list = data_file.readlines()
    data_file.close()
    test = []
    for record in test_list:
        all_values = record.split(',')
        inputs = (npy.asfarray(all_values[1:]) / 255.0 * 0.999) + 0.001
        out_session = net_output(w_in2hidden, w_hidden2out, inputs, 0)

        if int(all_values[0]) == npy.argmax(out_session):
            test.append(1)
        else:
            test.append(0)
    test = npy.asarray(test)
    print('Net efficient,% =', (test.sum() / test.size) * 100)
    #print('Dependence of efficiency on number of hidden neurons = ', ((test.sum() / test.size) / hidden_nodes))


def plot_image(pixels: npy.array):
    ppt.imshow(pixels.reshape((28, 28)), cmap='gray')
    ppt.show()


input_nodes, hidden_nodes, out_nodes, learn_speed = init_net()
w_in2hidden, w_hidden2out = create_net_rand(input_nodes, hidden_nodes, out_nodes)

for i in range(1):
    print('Test#', i + 1)
    w_in2hidden, w_hidden2out = train_set(w_in2hidden, w_hidden2out, learn_speed)
    test_set(w_in2hidden, w_hidden2out)

data_file = open('mnist_test.csv', 'r')
test_list = data_file.readlines()
data_file.close()

columns = ['Q1', 'Q2']
ind = list(range(0, 100))
frame_data = pds.DataFrame(index=ind, columns=columns)

for i in range(0, 100, 1):
    all_values = test_list[i].split(',')
    inputs = (npy.asfarray(all_values[1:]) / 255.0 * 0.999) + 0.001
    out_session = net_output(w_in2hidden, w_hidden2out, inputs, 0)
    frame_data.loc[i, 'Q1'] = npy.argmax(out_session)
    frame_data.loc[i, 'Q2'] = all_values[0]

writer = pds.ExcelWriter(file, engine='xlsxwriter')
frame_data.to_excel(writer, 'Sheet1')
writer.save()

all_values = test_list[int(npy.random.uniform(0, 9999))].split(',')
inputs = (npy.asfarray(all_values[1:]) / 255.0 * 0.999) + 0.001
out_session = net_output(w_in2hidden, w_hidden2out, inputs, 0)
print(npy.argmax(out_session))
plot_image(npy.asfarray(all_values[1:]))
