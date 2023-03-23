import os
import sys
try:
    import requests
except ImportError:
    os.system('pip install requests')
    import requests
import subprocess
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

def update():
    file = requests.get("https://raw.githubusercontent.com/sensetraining/Clock-In-2/main/clock_in_2.py").content

    f = open("clock_in_2.pyw","wb")
    f.write(file)
    f.close()

    f = open("version.txt","w")
    f.write(version)
    f.close()

    window.destroy()

def cancel():
    response = messagebox.askquestion("Warning", "Are you sure you want to cancel?")
    if response == "yes":
        window.destroy()
    sys.exit()

def install():
    print("installing")
    os.system('winget install python.python.3.10')
    window.destroy()

version = requests.get("https://raw.githubusercontent.com/sensetraining/Clock-In-2/main/version.txt").text

f = open("version.txt","r").read()

print(f"Latest version: {version}")
print(f"Installed version: {f}")

try:
    subprocess.run(['python', '--version'], check=True, capture_output=True)
except subprocess.CalledProcessError:
    # Python is not installed
    print('Python is not installed')
    window = tk.Tk()
    window.title("Python Installer")
    window.geometry("395x265")
    window["bg"] = "#F57A22"
    window.minsize(329, 199)
    x_cordinate = int((window.winfo_screenwidth() / 2) - 400/2)
    y_cordinate = int((window.winfo_screenheight() / 2) - 270/2)
    window.geometry("+{}+{}".format(x_cordinate, y_cordinate-20))

    style = ttk.Style()
    style.theme_use('default')
    style.configure("blueBox.TLabel", relief="solid", background="#113f8c")
    style.configure("label.TLabel", background="#113f8c", foreground="white", font=("Helvetica", 18, "bold"))
    style.configure("UpdateButton.TButton", foreground="black", font=("Helvetica", 14, "bold"), width=14)
    style.map("UpdateButton.TButton",
    background=[('pressed', '#cce4f7'), ('active', '#e0eef9'), ('!active', '#FFFFFF')],
    relief=[('pressed', 'flat'), ('active', 'flat'),('!active','flat')],)
    style.configure("CancelButton.TButton", foreground="white", font=("Helvetica", 14, "bold"), width=14)
    style.map("CancelButton.TButton",
    background=[('pressed', '#b33d3d'), ('active', '#c94242'), ('!active', '#ff4747')],
    relief=[('pressed', 'flat'), ('active', 'flat'),('!active','flat')],)

    plainBox1 = tk.Label(style="blueBox.TLabel")
    plainBox1.place(height=195,width=325,relx=0.5,rely=0.5,anchor="center")

    nameLabel = tk.Label(plainBox1,text="Python needs installing to run",style="label.TLabel",wraplength=205)
    nameLabel.place(relx=0.5,y=40,height=60,anchor="center")

    updateButton = tk.Button(plainBox1,text="Install",command=install,style="UpdateButton.TButton")
    updateButton.place(relx=0.5,y=105,height=40,width=150,anchor="center")

    cancelButton = tk.Button(plainBox1,text="Cancel",command=cancel,style="CancelButton.TButton")
    cancelButton.place(relx=0.5,y=155,height=40,width=150,anchor="center")

    window.mainloop()
else:
    print('Python is installed')


if f == version:
    print("Up to date")

else:
    print("Available update")

    window = tk.Tk()
    window.title("Updater")
    window.geometry("395x245")
    window["bg"] = "#F57A22"
    window.minsize(329, 179)
    x_cordinate = int((window.winfo_screenwidth() / 2) - 400/2)
    y_cordinate = int((window.winfo_screenheight() / 2) - 270/2)
    window.geometry("+{}+{}".format(x_cordinate, y_cordinate-20))

    style = ttk.Style()
    style.theme_use('default')
    style.configure("blueBox.TLabel", relief="solid", background="#113f8c")
    style.configure("label.TLabel", background="#113f8c", foreground="white", font=("Helvetica", 18, "bold"))
    style.configure("UpdateButton.TButton", foreground="black", font=("Helvetica", 14, "bold"), width=14)
    style.map("UpdateButton.TButton",
    background=[('pressed', '#cce4f7'), ('active', '#e0eef9'), ('!active', '#FFFFFF')],
    relief=[('pressed', 'flat'), ('active', 'flat'),('!active','flat')],)
    style.configure("CancelButton.TButton", foreground="white", font=("Helvetica", 14, "bold"), width=14)
    style.map("CancelButton.TButton",
    background=[('pressed', '#b33d3d'), ('active', '#c94242'), ('!active', '#ff4747')],
    relief=[('pressed', 'flat'), ('active', 'flat'),('!active','flat')],)

    plainBox1 = ttk.Label(style="blueBox.TLabel")
    plainBox1.place(height=175,width=325,relx=0.5,rely=0.5,anchor="center")

    nameLabel = ttk.Label(plainBox1,text="Update available!",style="label.TLabel")
    nameLabel.place(relx=0.5,y=30,height=35,anchor="center")

    updateButton = ttk.Button(plainBox1,text="Update",command=update,style="UpdateButton.TButton")
    updateButton.place(relx=0.5,y=85,height=40,width=150,anchor="center")

    cancelButton = ttk.Button(plainBox1,text="Cancel",command=cancel,style="CancelButton.TButton")
    cancelButton.place(relx=0.5,y=135,height=40,width=150,anchor="center")

    window.mainloop()

import clock_in_2

