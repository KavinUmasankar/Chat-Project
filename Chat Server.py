import socket
from _thread import *
import threading
import time

currentDate = ""
currentTime = ""

host = '192.168.1.96'
port = 5353
threadCount = 0
lastUser = ""

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client1 = ""
client2 = ""

clientnames = {}
clients = []


class App(threading.Thread):
    
    def __init__(self):
        threading.Thread.__init__(self)
        self.start()
        
    def run(self):
        while True:
            try:
                counter = 0
                for client in clients:
                    if client:
                        counter += 1
                time.sleep(3)
                for client in clients:
                    if client:
                        client.sendall(str.encode("usernum" + str(counter)))
                        time.sleep(0.25)
            except:
                continue

def threaded_client(connection, client):
    global currentDate
    global currentTime
    global lastUser
    new = True
    while True:
        try:
            data = connection.recv(2048)
            if data:
                if data.decode("utf-8").strip():
                    data = data.decode("utf-8").strip()
                    
                    parse = list(data)
                    parse.append("")
                    for x in range(len(parse)):
                        if parse[x] == "\n":
                            parse.insert(x + 1, "    ")
                    
                    data = ""
                    for char in parse:
                        data += char
                    
                    if len(data) > 5 and data[0:4] == "name" and new:
                        print(data)
                        if data[4:] in clientnames.values():
                            connection.sendall(str.encode("No"))
                        else:
                            clientnames[client] = data[4:]
                            new = False
                            connection.sendall(str.encode("Yes"))
                    else:
                        if lastUser == clientnames[client]:
                            reply = "    " + data + "\n"
                        else:
                            reply = clientnames[client] + ": \n    " + data + "\n"
                            lastUser = clientnames[client]
                        for user in clients:
                            if user:
                                user.sendall(str.encode(reply))
                #print(clients)
            else:
                clients[client] = ""
                clientnames[client] = ""
                break
        except:
            clients[client] = ""
            clientnames[client] = ""
            break
    connection.close()

try:
    server.bind((host, port))
except socket.error as e:
    print(str(e))

server.listen()

app = App()

while True:
    conn, addr = server.accept()
    clients.append(conn)
    print('Connected to: ', addr)
    start_new_thread(threaded_client, (conn, threadCount))
    threadCount += 1
server.close()
