import socket
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
import threading
import time
import sys

client = socket.socket()
host = '192.168.1.96'
port = 5353

user = ""

form = tk.Tk()
form.title("Welcome")
ttk.Label(form, text = "Username: ", font = ("Arial", 30)).grid(column = 0, row = 0)
name = ttk.Entry(form, font = ("Arial", 30))
name.insert(0, "Anonymous User")
name.grid(column = 1, row = 0)

def submit():
    global user
    user = name.get()
    form.destroy()

ttk.Button(form, text = "Enter!", command = submit).grid(column = 0, row = 1)

form.mainloop()

try:
    client.connect((host, port))
except socket.error as e:
    print(str(e))
    
userid = client.recv(2048).decode("utf-8")

client.send(str.encode("name" + user))

win = tk.Tk()
win.title("Chat Project")

text_area = scrolledtext.ScrolledText(win, wrap = tk.WORD, width = 40, height = 10, font = ("Times New Roman", 15))
text_area.grid(column = 0, row = 0, padx = 10, pady = 10)

chat = scrolledtext.ScrolledText(win, wrap = tk.WORD, width = 40, height = 1, font = ("Times New Roman", 15))

chat.grid(column = 0, row = 1)

text_area.configure(state = "disabled")

ttk.Label(win, text = "When leaving, please click the 'Exit' button and not the red X!").grid(column = 0, row = 5)

def enter():
    if len(chat.get("1.0", tk.END)):
        client.send(str.encode(chat.get("1.0", tk.END)))
        chat.delete("1.0", tk.END)

ttk.Button(win, text = "Enter", command = enter).grid(column = 0, row = 2)

def leave():
    client.close()
    win.destroy()
    time.sleep(3)
    sys.exit()

ttk.Button(win, text = "Exit", command = leave).grid(column = 0, row = 3)
usernum = ttk.Label(win, text = "Users: 0", font = ("Arial", 12))
usernum.grid(column = 0, row = 4)

class App(threading.Thread):
    
    def __init__(self, person, box, label):
        self.person = person
        self.box = box
        self.label = label
        threading.Thread.__init__(self)
        self.start()
    
    def run(self):
        data = self.person.recv(2048)
        while True:
            try:
                data = self.person.recv(2048)
                if data: 
                    data = data.decode()
                    if data[0:7] == "usernum":
                        self.label.config(text = "Users: " + data[7:])
                    else:
                        self.box.configure(state = "normal")
                        self.box.insert(tk.INSERT, data)
                        self.box.configure(state = "disabled")
            except:
                break
            
app = App(client, text_area, usernum)
win.mainloop()
