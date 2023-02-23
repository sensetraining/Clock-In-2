#-------------------------Import-------------------------#
import datetime as tm
import os
import time
import requests
import urllib
import logging
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as tkm
from inspect import currentframe
from calendar import month, monthrange, week
from datetime import datetime, timedelta

x = tm.datetime.now()
time_str = str(x.strftime("%Y-%m-%d %H.%M.%S"))


try:
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    fh = logging.FileHandler(f'logs\{time_str}.txt')
    fh.setLevel(logging.INFO)
    logger.addHandler(fh)
except:
    os.mkdir('logs')
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    fh = logging.FileHandler(f'logs\{time_str}.txt')
    fh.setLevel(logging.INFO)
    logger.addHandler(fh)
    
def lineNum(text):
    x = tm.datetime.now()
    time_str = str(x.strftime("[%X-%x]"))
    cf = currentframe()
    logger.info(f"{time_str} Line {cf.f_back.f_lineno}: {text}")
    print(f"{time_str} Line {cf.f_back.f_lineno}: {text}")

try:
    import gspread
except ImportError:
    lineNum(f"Installing gspread oauth2client")
    os.system('pip install gspread oauth2client')
    import gspread

try:
    from gspread_formatting import *
except ImportError:
    lineNum(f"Installing gspread_formatting")
    os.system('pip install gspread_formatting')
    from gspread_formatting import *

from gspread.cell import Cell
from oauth2client.service_account import ServiceAccountCredentials

scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)

while True:
    try:
        lineNum(f"Opening Staff Hours sheet")
        sheet = client.open("Staff Hours").sheet1
        break
    except Exception as error:
        lineNum(f"Waiting 0")
        time.sleep(5)

#-----------------------Functions------------------------#

def weekEnd(i):
    Letters = ["B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]

    total = ["Week Total"]
    for k in range(25):
        d1 = datetime.strftime(datetime.now() - timedelta(0), '%d/%m/%Y')
        d2 = datetime.strftime(datetime.now() - timedelta(i), '%d/%m/%Y')
        num = i + i // 7 + 1 + (int(d1[6:9])-int(d2[6:9]))*12+int(d1[3:5])-int(d2[3:5])
        column = "=SUM("
        for j in range(7):
            if datetime.strftime(datetime.now() - timedelta(i+j), '%d') == "01":
                num += 1
            column += f"{Letters[k]}{10+j+num}+"
        column = column[:-1] + ")"
        total.append(column)

    return total

def monthEnd(i):
    Letters = ["B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]

    total = ["Month Total"]
    for k in range(25):
        d1 = datetime.strftime(datetime.now() - timedelta(0), '%d/%m/%Y')
        d2 = datetime.strftime(datetime.now() - timedelta(i), '%d/%m/%Y')
        num = i + i // 7 + 1 + (((int(d1[6:10]) - int(d2[6:10])) * 12 + int(d1[3:5]) - int(d2[3:5]))*2)
        column = "=SUM("
        for j in range(monthrange(int(datetime.strftime(datetime.now() - timedelta(0), '%Y')), int(datetime.strftime(datetime.now() - timedelta(i+1), '%m')))[1]):
            if datetime.strftime(datetime.now() - timedelta(i+j+1), '%a') == "Sun":
                num += 1
            column += f"{Letters[k]}{10+j+num}+"
        column = column[:-1] + ")"
        total.append(column)

    return total

def dayCheck():
    currentDate = str(x.strftime("%a - %d/%m/%y"))
    values_list = sheet.col_values(1)
    diff = (datetime.strptime(values_list[8][6:14], "%d/%m/%y") - datetime.strptime(currentDate[6:14], "%d/%m/%y")).days
    if diff <0:
        diff = diff * -1
    values = []
    if diff >=1:
        for i in range(diff):
            values.append([datetime.strftime(datetime.now() - timedelta(i), '%a - %d/%m/%y'),0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
            if datetime.strftime(datetime.now() - timedelta(i), '%d') == "01":
                values.append(monthEnd(i))
            if datetime.strftime(datetime.now() - timedelta(i+1), '%a') == "Sun":
                values.append(weekEnd(i))
        #sheet.insert_rows(values, row=9, value_input_option='USER_ENTERED', inherit_from_before=True)
    return

###################### MAIN ######################
root = tk.Tk()
root['bg'] = "#f27420"
width = 600
height = 400
root.minsize(width, height)
x_cordinate = int((root.winfo_screenwidth() / 2) - width/2)
y_cordinate = int((root.winfo_screenheight() / 2) - height/2)
root.geometry("+{}+{}".format(x_cordinate, y_cordinate-20))

style = ttk.Style()
style.configure("blueBox.TLabel", relief="solid", background="#113f8c")
style.configure("label.TLabel", background="#113f8c",foreground="white",font=("Helvetica", 18, "bold"))
style.configure("Custom.TEntry", background="#113f8c")
style.configure("LoginButton.TButton", background="#113f8c", foreground="black", font=("Helvetica", 18, "bold"), width=10)
style.configure("Check.TCheckbutton", background="#113f8c", foreground="white", font=("Helvetica", 12), height=3, rememberVar=False)

#dayCheck()

loginBox = ttk.Label(root,style="blueBox.TLabel")
loginBox.place(height=f"{height-140}",width=f"{width-140}",relx=0.5,rely=0.5,anchor="center")

# Label height = 31px
# Create a Username label with an entry box to the right of it
username_label = ttk.Label(loginBox, text="Username:",style="label.TLabel")
username_label.place(x=20, y=20)

username_entry = ttk.Entry(loginBox,style="Custom.TEntry",font=("Helvetica", 14))
username_entry.place(height=31,width=290,x=150, y=20)

# Create a Password label with an entry box to the right of it
password_label = ttk.Label(loginBox, text="Password:",style="label.TLabel")
password_label.place(x=20, y=60)

password_entry = ttk.Entry(loginBox,show="*",style="Custom.TEntry",font=("Helvetica", 14))
password_entry.place(height=31,width=290,x=150, y=60)

checkButton = ttk.Checkbutton(loginBox,text="Remember me?",style="Check.TCheckbutton")
checkButton.place(x=20,y=100)

# Create a login button centered
login_button = ttk.Button(loginBox, text="Login",style="LoginButton.TButton")
login_button.place(relx=0.5, rely=0.7, anchor="center")

root.mainloop()