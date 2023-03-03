#-------------------------Import-------------------------#
import datetime as tm
import os
import time
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
        print(error)
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

def login(enteredUsername,enteredPassword,loginBox,checkState):
    
    allValues = sheet.get_all_values()

    if enteredUsername in allValues[0]:
        userPos = allValues[0].index(enteredUsername)
    else:
        incorrectEntry = tkm.showerror(title="Incorrect", message="You entered an incorrect Username or Password")
        return

    if enteredPassword in allValues[1]:
        passPos = allValues[1].index(enteredPassword)
    else:
        incorrectEntry = tkm.showerror(title="Incorrect", message="You entered an incorrect Username or Password")
        return

    if checkState == ("selected",):
        remember = "True"

    else:
        remember = "False"

    f = open("options.txt", "r")
    optionData = f.readlines()
    f.close()
    optionData[0] = (f"{remember} {userPos}\n")
    f = open("options.txt","w")
    f.writelines(optionData)
    f.close()

    if userPos == passPos:
        loginBox.destroy()
        mainPage(userPos)
    return

def logout(mainBox):
    f = open("options.txt", "r")
    optionData = f.readlines()
    f.close()
    optionData[0] = ("False 0\n")
    f = open("options.txt","w")
    f.writelines(optionData)
    f.close()
    print("Logout")
    mainBox.destroy()
    loginPage()
    return

def noClockOut(userPos,allValues,date,mainBox):
    x = tm.datetime.now()
    dates = sheet.col_values(1)
    clockInTime = allValues[3][userPos]

    if date in dates:
        datePos = dates.index(date)

        cell_list = [
        sheet.cell(datePos, userPos+1),
        sheet.cell(3, userPos+1)]

        cell_list[0].value = f"R{clockInTime}"
        cell_list[1].value = "FALSE"
        sheet.update_cells(cell_list,value_input_option='USER_ENTERED')
    
    else:
        sheet.update_cell(3,userPos+1,"FALSE")

    clockOutMsg = tkm.showerror(title="Warning", message=f"You didn't clock out on {date} so no hours were saved")
    mainBox.destroy()

    mainPage(userPos)
    return

def clockIn(userPos,mainBox):
    letters = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
    x = tm.datetime.now()
    currentTime = (x.strftime("%X"))
    currentDate = str(x.strftime("%a - %d/%m/%y"))

    sheet.update(f"{letters[userPos]}3:{letters[userPos]}5",[["TRUE"],[currentTime],[currentDate]])

    mainBox.destroy()
    mainPage(userPos)
    return

def clockOut(userPos,mainBox):
    letters = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
    x = tm.datetime.now()
    currentTime = (x.strftime("%X"))
    currentDate = str(x.strftime("%a - %d/%m/%y"))

    column = sheet.col_values(userPos+1)
    lastClocked = column[3]
    clockedTime = column[8]

    currentTime = tm.datetime.strptime(currentTime,"%X")
    lastClocked = tm.datetime.strptime(lastClocked,"%X")
    clockedTime = tm.datetime.strptime(clockedTime,"%X")

    timeDiff = currentTime - lastClocked
    totalClocked = timeDiff + clockedTime

    column[2] = "False"
    column[5] = (currentTime.strftime("%X"))
    column[6] = (currentDate)
    column[8] = (totalClocked.strftime("%X"))

    sheet.update(f"{letters[userPos]}1:{letters[userPos]}9",[[x] for x in column[0:9]],value_input_option='USER_ENTERED')

    mainBox.destroy()
    mainPage(userPos)
    return

def loginPage():
    root['bg'] = "#f27420"
    root.minsize(464, 214)
    loginBox = ttk.Label(root,style="blueBox.TLabel")
    loginBox.place(height=(height-140),width=(width-140),relx=0.5,rely=0.5,anchor="center")

    # Label height = 31px
    username_label = ttk.Label(loginBox, text="Username:",style="label.TLabel")
    username_label.place(x=20, y=20)

    username_entry = ttk.Entry(loginBox,style="Custom.TEntry",font=("Helvetica", 14))
    username_entry.place(height=31,width=290,x=150, y=20)

    password_label = ttk.Label(loginBox, text="Password:",style="label.TLabel")
    password_label.place(x=20, y=60)

    password_entry = ttk.Entry(loginBox,show="*",style="Custom.TEntry",font=("Helvetica", 14))
    password_entry.place(height=31,width=290,x=150, y=60)

    # CheckVar = tk.IntVar(value=0)
    checkButton = ttk.Checkbutton(loginBox,text="Remember me",style="Check.TCheckbutton",variable=CheckVar)
    checkButton.place(x=20,y=100)

    login_button = ttk.Button(loginBox, text="Login",style="LoginButton.TButton",command=lambda:login(username_entry.get(),password_entry.get(),loginBox,checkState = checkButton.state()))
    login_button.place(height=48,relx=0.5, rely=0.8, anchor="center")
    return

def hoursPage(userPos,hours,adminBox,mainBox):
    hours = True
    adminBox.destroy()
    adminPage(userPos,mainBox,hours)
    return

def accountPage(userPos,hours,adminBox,mainBox):
    hours = False
    adminBox.destroy()
    adminPage(userPos,mainBox,hours)
    return

def mainPageBack(userPos,adminBox):
    adminBox.destroy()
    mainPage(userPos)
    return

def adminPage(userPos,mainBox,hours):
    mainBox.destroy()
    usernames = sheet.row_values(1)
    print(usernames)

    usernames = [item for item in usernames if item != "EMPTY"]
    usernames.pop(0)

    print(usernames)

    adminBox = ttk.Label(root,style="blueBox.TLabel")
    adminBox.place(height=280,width=480,relx=0.5,rely=0.5,anchor="center")

    if hours == True:
        hoursButton = ttk.Button(adminBox,text="Hours",style="tabSunken.TButton",command=lambda:hoursPage(userPos,hours,adminBox,mainBox))
        hoursButton.place(height=29,width=238,x=1,y=1)
        hoursButton.state(["disabled"])

        accountButton = ttk.Button(adminBox,text="Accounts",style="tabFlat.TButton",command=lambda:accountPage(userPos,hours,adminBox,mainBox))
        accountButton.place(height=29,width=238,relx=0.5,x=-1,y=1)

    
        value = tk.StringVar()
        value.set("Staff")


        # optionmenu_var = tk.StringVar(root, optionmenu_var, "Select greeting", "Hi", "Hello", "Bye")
        optionMenu = ttk.OptionMenu(adminBox, value, "Staff",*usernames)
        optionMenu["menu"].config(background="white")
        optionMenu.place(x=5,y=35,width=200,height=40)

        addButon = ttk.Button(adminBox,text="+",style="staffBtn.TButton")
        addButon.place(x=210,y=35,height=40,width=40)

    else:
        hoursButton = ttk.Button(adminBox,text="Hours",style="tabFlat.TButton",command=lambda:hoursPage(userPos,hours,adminBox,mainBox))
        hoursButton.place(height=29,width=238,x=1,y=1)

        accountButton = ttk.Button(adminBox,text="Accounts",style="tabSunken.TButton",command=lambda:accountPage(userPos,hours,adminBox,mainBox))
        accountButton.place(height=29,width=238,relx=0.5,x=-1,y=1)
        accountButton.state(["disabled"])
    
    settingsButton = ttk.Button(adminBox,style="setting.TButton",compound="center",command=lambda:mainPageBack(userPos,adminBox))
    settingsButton.place(width=48,height=48,relx=0.9,rely=.85,anchor="center")

    return

def mainPage(userPos):
    x = tm.datetime.now()
    currentDay = x.strftime("%a")
    allValues = sheet.get_all_values()
    username = allValues[0][userPos]

    height=400
    root.minsize(484, 284)
    root.geometry("600x400")

    mainBox = ttk.Label(root,style="blueBox.TLabel")
    mainBox.place(height=280,width=480,relx=0.5,rely=0.5,anchor="center")

    welcomeLabel = ttk.Label(mainBox,text=f"Hello {username}!",style="label.TLabel")
    welcomeLabel.place(x=20,y=20)

    currentLabel = ttk.Label(mainBox,text=f"You are currently ",style="label.TLabel")
    currentLabel.place(x=20,y=55)

    if allValues[2][userPos] == "FALSE":
        clockOutLabel = ttk.Label(mainBox,text="Clocked Out",style="label.TLabel",foreground="Red")
        clockOutLabel.place(x=223,y=55)

        clockInButton = ttk.Button(mainBox,text="Clock In",style='clockIn.TButton',command=lambda:clockIn(userPos,mainBox))
        clockInButton.place(height=48,relx=0.5,rely=0.6,anchor="center")
    else:
        clockInLabel = ttk.Label(mainBox,text="Clocked In",style="label.TLabel",foreground="Lime")
        clockInLabel.place(x=223,y=55)
        
        x = tm.datetime.now()
        currentTime = (x.strftime("%X"))
        currentTime = tm.datetime.strptime(currentTime,"%X")
        lastClockedTime = allValues[3][userPos]
        lastClockedTime = tm.datetime.strptime(lastClockedTime,"%X")
        clockedTime = allValues[8][userPos]
        clockedTime = tm.datetime.strptime(clockedTime,"%X")

        timeDiff = currentTime - lastClockedTime + clockedTime
        timeDiff = timeDiff.strftime("%X")

        clockTime = ttk.Label(mainBox,text=f"Clocked Time: {timeDiff}",style="label.TLabel")
        clockTime.place(x=20,y=90)

        clockOutButton = ttk.Button(mainBox,text="Clock Out",style='clockOut.TButton',command=lambda:clockOut(userPos,mainBox))
        clockOutButton.place(height=48,relx=0.5,rely=0.6,anchor="center")

    logoutButton = ttk.Button(mainBox,text="Logout",style="LoginButton.TButton",command=lambda:logout(mainBox))
    logoutButton.place(height=48,relx=0.5,rely=0.85,anchor="center")


    settingsButton = ttk.Button(mainBox,style="setting.TButton",compound="center",command=lambda:adminPage(userPos,mainBox,hours=True))
    settingsButton.place(width=48,height=48,relx=0.9,rely=.85,anchor="center")

    if allValues[2][userPos] == "TRUE" and allValues[4][userPos][0:3] != currentDay:
        noClockOut(userPos,allValues,allValues[4][userPos],mainBox)
    return

###################### MAIN ######################
root = tk.Tk()
root['bg'] = "#f27420"
width = 600
height = 350
root.minsize(464, 214)
root.geometry("600x350")
x_cordinate = int((root.winfo_screenwidth() / 2) - width/2)
y_cordinate = int((root.winfo_screenheight() / 2) - height/2)
root.geometry("+{}+{}".format(x_cordinate, y_cordinate-20))

CheckVar = tk.IntVar(value=0)
settingsIcon = tk.PhotoImage(file="setting_icon.png")
style = ttk.Style()
style.theme_use('default')
style.configure("blueBox.TLabel", relief="solid", background="#113f8c")
style.configure("label.TLabel", background="#113f8c", foreground="white", font=("Helvetica", 18, "bold"))
style.configure("Custom.TEntry", background="#113f8c")
style.map("LoginButton.TButton",
    background=[('pressed', '#cce4f7'), ('active', '#e0eef9'), ('!active', '#FFFFFF')],
    relief=[('pressed', 'flat'), ('active', 'flat'),('!active','flat')],)
style.configure("LoginButton.TButton", foreground="black", font=("Helvetica", 18, "bold"), width=14)
style.map("Check.TCheckbutton",
    background=[('pressed', '#113f8c'), ('active', '#113f8c'), ('!active', '#113f8c')],)
style.configure("Check.TCheckbutton", background="#113f8c", foreground="white", font=("Helvetica", 12))
style.map("clockIn.TButton",
    background=[('pressed', '#cce4f7'), ('active', '#e0eef9'), ('!active', '#FFFFFF')],
    relief=[('pressed', 'flat'), ('active', 'flat'),('!active','flat')],)
style.configure('clockIn.TButton', background="white", foreground="#2bd900", font=("Helvetica", 18, "bold"), width=14)
style.map("clockOut.TButton",
    background=[('pressed', '#cce4f7'), ('active', '#e0eef9'), ('!active', '#FFFFFF')],
    relief=[('pressed', 'flat'), ('active', 'flat'),('!active','flat')],)
style.configure('clockOut.TButton', background="white", foreground="Red", font=("Helvetica", 18, "bold"), width=14)
style.map("setting.TButton",
    background=[('pressed', '#cce4f7'), ('active', '#e0eef9'), ('!active', '#FFFFFF')],
    relief=[('pressed', 'flat'), ('active', 'flat'),('!active','flat')],)
style.configure('setting.TButton', background="white", image=settingsIcon)
style.map("tabFlat.TButton",
    background=[('pressed', '#1651b5'), ('active', '#1651b5'), ('!active', '#0e3373')],
    foreground=[('pressed', '#e6e6e6'), ('active', '#e6e6e6'), ('!active', '#878787')],
    relief=[('pressed', 'flat'), ('active', 'flat'),('!active','flat')],)
style.configure('tabFlat.TButton',background="white",font=("Helvetica", 10, "bold"))
style.map("tabSunken.TButton",
    background=[('pressed', '#cce4f7'), ('active', '#e0eef9'), ('!active', '#113f8c')],
    foreground=[('pressed', '#FFFFFF'), ('active', '#FFFFFF'), ('!active', '#FFFFFF')],
    relief=[('pressed', 'flat'), ('active', 'flat'),('!active','flat')],)
style.configure('tabSunken.TButton',font=("Helvetica", 10, "bold"))
style.map("TMenubutton",
    background=[('pressed', '#cce4f7'), ('active', '#e0eef9'), ('!active', '#FFFFFF')],
    relief=[('pressed', 'flat'), ('active', 'flat'),('!active','flat')],)
style.configure('TMenubutton',font=("Helvetica", 14, "bold"),background="white",activebackground='red')
style.map("staffBtn.TButton",
    background=[('pressed', '#cce4f7'), ('active', '#e0eef9'), ('!active', '#FFFFFF')],
    relief=[('pressed', 'flat'), ('active', 'flat'),('!active','flat')],)
style.configure('staffBtn.TButton', background="white",font=("Helvetica", 32, "bold"))
style.configure('TCombobox',background="red")


#dayCheck()

f = open("options.txt", "r")
optionData = f.readlines()

autoLogin = optionData[0].rstrip().split(" ")

if autoLogin[0] == "True":
    mainPage(int(autoLogin[1]))

else:
    loginPage()

root.mainloop()
