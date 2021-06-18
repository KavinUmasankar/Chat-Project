import socket
from _thread import *
import threading
from datetime import datetime
import time

currentDate = ""
currentTime = ""

host = '192.168.1.96'
port = 5353
threadCount = 0

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
                for client in clients:
                    if client:
                        client.sendall(str.encode("usernum" + str(counter)))
                        time.sleep(0.25)
            except:
                continue

def threaded_client(connection, client):
    connection.sendall(str.encode(str(client)))
    global currentDate
    global currentTime
    while True:
        try:
            data = connection.recv(2048)
            if data:
                if data.decode("utf-8").strip():
                    data = data.decode("utf-8").strip()                
                    if len(data) > 5 and data[0:4] == "name":
                        clientnames[client] = data[4:]
                    else:
                        reply = clientnames[client] + ": \n    " + data + "\n"
                        today = datetime.today().strftime("%B, %d, %Y")
                        now = datetime.now().strftime("%I:%M %p")
                        for user in clients:
                            if user:
                                if currentDate != today:
                                    user.sendall(str.encode(today + "\n"))
                                    currentDate = today
                                if currentTime != now:
                                    user.sendall(str.encode(now + "\n"))
                                    currentTime = now
                                user.sendall(str.encode(reply))
                print(clients)
            else:
                clients[client] = ""
                break
        except:
            clients[client] = ""
            break
    connection.close()

try:
    server.bind((host, port))
except socket.error as e:
    print(str(e))

server.listen(2)

app = App()

while True:
    conn, addr = server.accept()
    clients.append(conn)
    print('Connected to: ', addr)
    start_new_thread(threaded_client, (conn, threadCount))
    threadCount += 1
server.close()
