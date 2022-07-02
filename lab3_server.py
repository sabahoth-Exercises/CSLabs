import socket
from _thread import *

sock = socket.socket()

port = 9090
try:
    sock.bind(('127.0.0.1', port))
except socket.error as e:
    print(str(e))

sock.listen(2)


def check_value(t, d):
    if d == 'W':
        if t < 30:
            print("warning! low wetness near", d)
        if t > 60:
            print("warning! hight wetness near", d)
        if t < 15:
            print("warning! low temperature near", d)
        if t > 25:
            print("warning! hight temperature near", d)


def check_battery(bat, d):
    if bat <= 20:
        print("warning! low charge in sensor", d)


def threaded_client(connection):
    while True:
        data = connection.recv(1024)
        if not data:
            break
        mes = str(data.decode('utf-8'))
        conn.sendall(str(data).encode())
        print('Received: ', mes)
        mes_split = data.split('-')
        type = mes_split[0]
        battery = mes_split[2]
        value = int(mes_split[1])
        check_value(value, type)
        check_battery(battery, type)
    connection.close


while True:
    conn, addr = sock.accept()
    start_new_thread(threaded_client, (conn,))
    conn.close()
