import socket
from _thread import *

host = '192.168.1.96'
port = 5353
threadCount = 0

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client1 = ""
client2 = ""

clientnames = {}
clients = []

def threaded_client(connection, client):
    
    connection.send(str.encode(str(client)))
    
    while True:
        data = connection.recv(2048)
        if data:
            data = data.decode("utf-8")
            
            if len(data) > 5 and data[0:4] == "name":
                clientnames[client] = data[4:]
            else:
                reply = clientnames[client] + ": " + data + "\n"
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
