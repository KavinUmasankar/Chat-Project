import socket
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
import threading

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

chat = ttk.Entry(win, width = 50)
chat.grid(column = 0, row = 1)

text_area.configure(state = "disabled")

def enter():
    if len(chat.get()):
        client.send(str.encode(chat.get()))
        chat.delete(0, len(chat.get()))

ttk.Button(win, text = "Enter", command = enter).grid(column = 0, row = 2)

class App(threading.Thread):
    
    def __init__(self, person, box):
        self.person = person
        self.box = box
        threading.Thread.__init__(self)
        self.start()
    
    def run(self):
        while True:
            data = self.person.recv(2048)
            if data:
                data = data.decode()
                self.box.configure(state = "normal")
                self.box.insert(tk.INSERT, data)
                self.box.configure(state = "disabled")

app = App(client, text_area)
win.mainloop()
