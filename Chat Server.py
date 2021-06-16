# -*- coding: utf-8 -*-
"""
Created on Tue Jun 15 17:54:06 2021

@author: kavin
"""
import socket
from _thread import *

host = '192.168.1.96'
port = 5353
threadCount = 0

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client1 = ""
client2 = ""

clients = []

def threaded_client(connection, client):
    global client1
    global client2
    global sendTo0
    global sendTo1
    
    
    
    connection.send(str.encode(str(client)))
    
    while True:
        data = connection.recv(2048)
        if data:
            data = data.decode("utf-8")
            
            if len(data) > 5 and data[0:4] == "name":
                if client == 0:
                    client1 = data[4:]
                if client == 1:
                    client2 = data[4:]
                        
            else:
                if client == 0:
                    reply =  client1 + ": " + data + "\n"
                if client == 1:
                    reply =  client2 + ": " + data + "\n"
                for user in clients:
                    user.sendall(str.encode(reply))
                
        else:
            break

    connection.close()

try:
    server.bind((host, port))
except socket.error as e:
    print(str(e))

server.listen(2)
    
while True:
    conn, addr = server.accept()
    clients.append(conn)
    print('Connected to: ', addr)
    start_new_thread(threaded_client, (conn, threadCount))
    threadCount += 1
server.close()
