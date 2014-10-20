#!/usr/bin/python

import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# client.connect(('rpi.local', 1234))
client.connect(('cromartie.local', 1234))

while True:
    s = raw_input('Data: ')
    client.send(str(s))
    data = client.recv(1024)

    if data != s or (data == s and data == '4 0'):
        print('Connection closed.')
        break
    else:
        print(data)

client.close()