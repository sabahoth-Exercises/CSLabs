import socket
import time
import random


def send_data(a, b, c):
    sock = socket.socket()
    try:
        sock.connect(('127.0.0.1', port))
    except socket.error as e:
        print(str(e))

    mes = str(str(a) + '_' + str(b) + '_' + str(c))
    sock.send(mes.encode())
    print(mes)

    sock.close


id = 'T2'
battery = 100
port = 9090
while battery > 0:
    temp = random.randint(-10, 100)
    p = random.random()
    if p >= 0.45:
        send_data(id, temp, battery)
        battery -= 10
        time.sleep(2)
