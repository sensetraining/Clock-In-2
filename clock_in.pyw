#-------------------------Import-------------------------#
# pip install gspread oauth2client
import datetime as tm
import os
import time
import requests
import urllib
import logging
import tkinter as tk
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
def delete(box):
    lineNum(f"Destroying box, going to login page")
    box.destroy()
    login()

def login():
    lineNum(f"Running login page")
    plainBox1 = tk.Label(bg="#113F8C",relief="solid")
    #plainBox1.place(height=180,width=400,x=50,y=50)
    plainBox1.place(height=180,width=400,relx=0.5,rely=0.5,anchor="center")

    # helvetica, 18, bold height = 35

    nameLabel = tk.Label(plainBox1,text="Name:",fg="white",bg="#113F8C",font=("Helvetica", 18, "bold"))
    nameLabel.place(x=20,y=20,height=35)

    passLabel = tk.Label(plainBox1,text="Password:",fg="white",bg="#113F8C",font=("Helvetica", 18, "bold"))
    passLabel.place(x=20,y=60,height=35)

    nameInput = tk.Entry(plainBox1,font=("Helvetica", 18, "bold"))
    nameInput.place(x=150,y=20,width=230,height=35)

    passInput = tk.Entry(plainBox1,font=("Helvetica",18, "bold"),show="*")
    passInput.place(x=150,y=60,width=230,height=35)

    submitButton = tk.Button(plainBox1,text="Submit",command=lambda:loginCheck(nameInput.get(),passInput.get(),plainBox1),bg="white",fg="black",font=("Helvetica", 12, "bold"))
    submitButton.place(x=125,y=115,height=40,width=150)

def loginCheck(userName,userPass,box):
    lineNum(f"loginCheck")
    position = 0
    correctLogin = False

    while True:
        try:
            lineNum(f"Collecting names and passwords from the sheets")
            data = sheet.get_all_values()
            sheetNames = data[0]
            passwords = data[1]
            break
        except:
            lineNum(f"Waiting 1")
            time.sleep(5)

    lineNum(f"Checking for a name matching {userName}")
    for i in range (len(sheetNames)-1):
        if userName.capitalize() == (sheetNames[i+1]):
            position = i+1
            correctLogin = True

    lineNum(f"Checking if intputted password, {userPass} matches saved password, {passwords[position]} ")
    if passwords[position] != userPass:
        correctLogin = False

    if correctLogin == False:
        lineNum(f"Incorrect name or password was entered")
        inputError = tkm.showerror(title="Error", message="You entered an invalid name or password")
        delete(box)
        login()
        window.mainloop()

    position += 1

    letters=["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]

    x = tm.datetime.now()
    currentDate = str(x.strftime("%a - %d/%m/%y"))

    lineNum(f"Checking clocked status")
    while True:
            try:
                col = sheet.col_values(position)

                clockedStatus = (col[2])
                if col[5] != currentDate and clockedStatus == "TRUE":
                    lineNum(f"Clocked status TRUE, last clocked date {col[5]} does not match current date {currentDate}")
                    datesCol = sheet.col_values(1)
                    i = 9
                    lineNum(f"Searching for the clocked date")
                    while datesCol[i] != col[5] and i < len(datesCol)-1:
                        i += 1

                    if i < len(datesCol)-1:
                        lineNum(f"Clocked date found on row {i+1}")
                        sheet.update_cell(i+1,position,f"R{col[3]}")
                        lineNum(f"Adding clocked in time and highlighting red")
                        column = letters[position-1]
                        fmt = cellFormat(
                            backgroundColor=color(1, 0.5, 0.5),
                            )

                        lineNum(f"Formating {column}{i+1}:{column}{i+1}")
                        format_cell_range(sheet, f'{column}{i+1}:{column}{i+1}', fmt)
                    else:
                        lineNum(f"Clocked date not found")
                    lineNum(f"Setting clocked status to FALSE")
                    sheet.update_cell(3,position,"FALSE")
                break
            except Exception as error:
                print(error)
                lineNum(error)
                lineNum(f"Waiting 4")
                time.sleep(5)

    main(userName.capitalize(),position,box)

def clockIn(name,position,box):
    lineNum(f"Running day check for clock In")
    dayCheck()
    lineNum(f"Clocking In")
    x = tm.datetime.now()
    currentTime = str(x.strftime("%X"))
    currentDate = str(x.strftime("%a - %d/%m/%y"))
    while True:
        try:
            lineNum(f"Setting clocked status to TRUE, updating clock in time and date on sheets")
            sheet.update_cell(3,position,"TRUE")
            sheet.update_cell(4,position,currentTime)
            sheet.update_cell(6,position,currentDate)

            break
        except:
            lineNum(f"Waiting 2")
            time.sleep(5)

    main(name,position,box)

def clockOut(name,position,box):
    lineNum(f"Clocking out")
    x = tm.datetime.now()
    currentTime = str(x.strftime("%X"))

    while True:
        try:
            lineNum(f"Calculating clocked time")
            clockInTime = sheet.cell(4,position).value
    
            clockInTime = clockInTime.split(":")

            clockInHour = int(clockInTime[0])
            clockInMin = int(clockInTime[1])
            clockInSec = int(clockInTime[2])

            currentHour = int(currentTime[0:2])
            currentMin = int(currentTime[3:5])
            currentSec = int(currentTime[6:8])

            clockedHour = currentHour - clockInHour
            clockedMin = currentMin - clockInMin
            clockedSec = currentSec - clockInSec

            clockedTime = (f"{clockedHour}:{clockedMin}:{clockedSec}")
            lineNum(f"Clocked time, {clockedTime}")

            cellNine = sheet.cell(9,position).value
            lineNum(f"Grabbing value of cell 9, {cellNine}")
            cellNine = cellNine.split(":")
            if cellNine is not None:
                
                cellNineHour = int(cellNine[0])
                cellNineMin = int(cellNine[1])
                cellNineSec = int(cellNine[2])

                cellNineHourAdd = cellNineHour + clockedHour
                cellNineMinAdd = cellNineMin + clockedMin
                cellNineSecAdd = cellNineSec + clockedSec

                cellTotal = (f"{cellNineHourAdd}:{cellNineMinAdd}:{cellNineSecAdd}")
                lineNum(f"Adding previous clocked time to new clocked time, {':'.join(cellNine)} + {clockedTime} = {cellTotal}")

                lineNum(f"Replacing cell 9 with new total")
                sheet.update_cell(9,position,cellTotal)

            else:
                lineNum(f"Cell 9 is empty, inputting clocked time")
                sheet.update_cell(9,position,clockedTime)
            
            lineNum(f"Updating last clocked out time to current time, {currentTime}")
            sheet.update_cell(5,position,currentTime)

            break
        except Exception as error:
            print(error)
            logger.info(f"error")
            lineNum(f"Waiting 3")
            time.sleep(5)

    lineNum(f"Updating clocked status to false")
    sheet.update_cell(3,position,"FALSE")
    main(name,position,box)

def adminPage(name,position,box,selected,unselected,option1,option2):
    lineNum(f"Running Admin page")

    lineNum(f"option1 is {option1}")

    lineNum(f"option2 is {option2}")

    box.destroy()

    plainBox1 = tk.Label(bg="#113F8C",relief="solid")
    plainBox1.place(height=225,width=440,relx=0.5,rely=0.5,anchor="center")

    backButton = tk.Button(plainBox1,command=lambda:main(name,position,plainBox1),text="Back",fg="white",bg="#ff4747",font=("Helvetica", 14,"bold"),activebackground="#f04343",activeforeground="#f0f0f0")
    backButton.place(x=380,y=200,height=30,width=100,anchor="center")

    try:   
        userImage = tk.PhotoImage(file = r"settings.png")
    except:
        lineNum(f"Image not found, download from github")
        img = "https://raw.githubusercontent.com/sensetraining/Work-hours/main/settings.png"
        urllib.request.urlretrieve(img, "settings.png")
        userImage = tk.PhotoImage(file = r"settings.png")

    editButton = tk.Button(plainBox1,command=lambda:editUser(),image = userImage,bg="white")
    editButton.place(x=310,y=200,height=30,width=30,anchor="center")

    progressLabel = tk.Label(plainBox1,text="In Progress",fg="white",bg="#113F8C",font=("Helvetica", 16,"bold"))
    progressLabel.place(x=5,y=185)

    dateLabel = tk.Label(plainBox1,text="Date range (dd/mm/yy):",bg="#113F8C",fg="white",wraplength=177,justify="left",font=("Helvetica", 11,"bold"))  
    dateLabel.place(x=255,y=5,height=25)

    date1Input = tk.Entry(plainBox1,font=("Helvetica", 12,"bold"))
    date1Input.place(x=255,y=35,width=177,height=25)

    date2Input = tk.Entry(plainBox1,font=("Helvetica", 12,"bold"))
    date2Input.place(x=255,y=65,width=177,height=25)
    if option1 == True:
        lineNum(f"Displaying select staff menu")
        value = tk.StringVar(plainBox1)
        value.set("Select a staff member")
        staffOptions = tk.OptionMenu(plainBox1,value, *unselected)
        staffOptions.config(bg="white",fg="black",font=("Helvetica", 12,"bold"),activebackground='white')
        staffOptions["menu"].config(bg="white",fg="black",font=("Helvetica", 11,"bold"))
        staffOptions["highlightthickness"]=0
        #staffOptions["borderwidth"] = 0
        staffOptions.place(x=5,y=5,height=40,width=200)

        plusButton = tk.Button(plainBox1,text="+",command=lambda:addSelected(name,position,value.get(),plainBox1,selected,unselected,option1,option2),bg="white",fg="black",font=("Helvetica", 26))
        plusButton.place(x=210,y=5,height=40,width=40)  

    if option2 == True:
        if option1 == False:
            yValue = 5
        else:
            yValue = 50
        lineNum(f"Displaying selected staff menu at y={yValue}")
        value2 = tk.StringVar(plainBox1)
        value2.set("Selected staff               ")
        Options = tk.OptionMenu(plainBox1,value2, *selected)
        Options.config(bg="white",fg="black",font=("Helvetica", 12,"bold"),activebackground='white')
        Options["menu"].config(bg="white",fg="black",font=("Helvetica", 11,"bold"))
        Options["highlightthickness"]=0
        #Options["borderwidth"] = 0
        Options.place(x=5,y=yValue,height=40,width=200)

        minusButton = tk.Button(plainBox1,text="-",command=lambda:minusSelected(name,position,value2.get(),plainBox1,selected,unselected,option1,option2),bg="white",fg="black",font=("Helvetica", 26))
        minusButton.place(x=210,y=yValue,height=40,width=40)   

        searchButton = tk.Button(plainBox1,text="Search",command=lambda:searchDate(date1Input.get(),date2Input.get(),selected),bg="white",fg="black",font=("Helvetica", 12,"bold"))
        searchButton.place(x=255,y=95,width=177,height=25)
    
def searchDate(date1,date2,selected):
    if not selected:
        inputError = tkm.showerror(title="Error", message="No staff selected")
        return
    
    try:
        date1 = datetime.strptime(date1, "%d/%m/%y")
        date2 = datetime.strptime(date2, "%d/%m/%y")
    except Exception as error:
        print(error)
        inputError = tkm.showerror(title="Error", message="Date entered incorrectly")
        return

    diff = (date2 - date1).days
    if diff <0:
        diff = diff * -1
    print("👤")
    
    return


def addSelected(name,position,value,box,selected,unselected,option1,option2):
    lineNum(f"Running addSelected function")
    box.destroy()
    if value in unselected:
        lineNum(f"Adding selected staff {value}")
        selected.append(value)
        unselected.remove(value)
        lineNum(f"Setting option2 to True")
        option2 = True
    if len(unselected) == 0:
        lineNum(f"Setting option1 to False")
        option1 = False

    adminPage(name,position,box,selected,unselected,option1,option2)

def minusSelected(name,position,value,box,selected,unselected,option1,option2):
    lineNum(f"Running minusSelected function")
    box.destroy
    if value in selected:
        lineNum(f"Removing selected staff {value}")
        unselected.append(value)
        selected.remove(value)
        lineNum(f"Setting option1 to True")
        option1 = True
    if len(selected) == 0:
        lineNum(f"Setting option2 to False")
        option2 = False
    
    adminPage(name,position,box,selected,unselected,option1,option2)

def editUser():

    return

def main(name,position,box):
    admins = ["Bruce","Emily","Test"]
    admin = False
    

    lineNum(f"Admin check")
    if name in admins:
        lineNum(f"{name} is Admin")
        admin = True
    else:
        lineNum(f"{name} is not Admin")

    box.destroy()
    lineNum(f"Running main")

    plainBox1 = tk.Label(bg="#113F8C",relief="solid")
    plainBox1.place(height=205,width=400,relx=0.5,rely=0.5,anchor="center")

    welcomeLabel = tk.Label(plainBox1,text=f"Hello, {name}!",fg="white",bg="#113F8C",font=("Helvetica", 16, "bold"))
    welcomeLabel.place(x=20,y=15)

    textLabel = tk.Label(plainBox1,text="You are currently ",fg="white",bg="#113F8C",font=("Helvetica", 16, "bold"))
    textLabel.place(x=20,y=45)
    lineNum(f"Checking clocked status")
    col = sheet.col_values(position)
    clockedStatus = (col[2])

    if clockedStatus == "FALSE":
        lineNum(f"Clocked status FALSE, displaying appropriate text")
        clockedLabel = tk.Label(plainBox1,text="not clocked in.",fg="red2",bg="#113F8C",font=("Helvetica", 16, "bold"))
        clockedLabel.place(x=200,y=45)

        clockInButton = tk.Button(plainBox1,text="Clock in",command=lambda:clockIn(name,position,plainBox1),fg="lime green",bg="white",font=("Helvetica", 16, "bold"))
        clockInButton.place(x=125,y=90,height=40,width=150)

    else:
        lineNum(f"Clocked status TRUE, displaying appropriate text")
        clockedLabel = tk.Label(plainBox1,text="clocked in.",fg="lime green",bg="#113F8C",font=("Helvetica", 16, "bold"))
        clockedLabel.place(x=200,y=45)

        clockOutButton = tk.Button(plainBox1,text="Clock out",command=lambda:clockOut(name,position,plainBox1),fg="red2",bg="white",font=("Helvetica", 16, "bold"))
        clockOutButton.place(x=125,y=90,height=40,width=150)

    logoutButton = tk.Button(plainBox1,text="Logout",command=lambda:delete(plainBox1),bg="white",fg="black",font=("Helvetica", 16, "bold"))
    logoutButton.place(x=125,y=145,height=40,width=150)

    if admin == True:
        lineNum(f"Retrieving names from sheets")
        while True:
            try:
                names = sheet.row_values(1)
                break
            except:
                lineNum(f"Waiting 14")
                time.sleep(5)
        o = ""
        lineNum(f"Removing filler names")
        for i in range(len(names)):
            try:
                names.remove(f"Name{o}")
            except:
                pass
            o = i + 1

        unselected = names
        lineNum(f"Setting unselected to name ({names})")
        selected = []
        lineNum(f"Setting selected to nothing")
        option1 = True
        option2 = False

        adminButton = tk.Button(plainBox1,command=lambda:adminPage(name,position,plainBox1,selected,unselected,option1,option2),text="🖳",fg="black",bg="#ffbd03",font=("Helvetica", 26,"bold"),activebackground="#f0b102")
        adminButton.place(x=340,y=145,height=40,width=40)

    return

def endWeek():
    lineNum(f"Running end of week function")
    addSUM1 = [10,11,12,13,14,15,16]
    for j in range (7):
        while True:
            try:
                check = sheet.cell(9+j,1).value
                lineNum(f"Checking if {check} is Month Total")
                if sheet.cell(9+j,1).value == "Month Total":
                    lineNum(f"Month Total found, skipping over it")
                    for k in range (j,7):
                        addSUM1[k] = addSUM1[k] + 1
                break
            except:
                lineNum(f"Waiting 5")
                time.sleep(5)

    weekTotal = ["Week Total",
    f"=SUM(B{addSUM1[0]}+B{addSUM1[1]}+B{addSUM1[2]}+B{addSUM1[3]}+B{addSUM1[4]}+B{addSUM1[5]}+B{addSUM1[6]})",
    f"=SUM(C{addSUM1[0]}+C{addSUM1[1]}+C{addSUM1[2]}+C{addSUM1[3]}+C{addSUM1[4]}+C{addSUM1[5]}+C{addSUM1[6]})",
    f"=SUM(D{addSUM1[0]}+D{addSUM1[1]}+D{addSUM1[2]}+D{addSUM1[3]}+D{addSUM1[4]}+D{addSUM1[5]}+D{addSUM1[6]})",
    f"=SUM(E{addSUM1[0]}+E{addSUM1[1]}+E{addSUM1[2]}+E{addSUM1[3]}+E{addSUM1[4]}+E{addSUM1[5]}+E{addSUM1[6]})",
    f"=SUM(F{addSUM1[0]}+F{addSUM1[1]}+F{addSUM1[2]}+F{addSUM1[3]}+F{addSUM1[4]}+F{addSUM1[5]}+F{addSUM1[6]})",
    f"=SUM(G{addSUM1[0]}+G{addSUM1[1]}+G{addSUM1[2]}+G{addSUM1[3]}+G{addSUM1[4]}+G{addSUM1[5]}+G{addSUM1[6]})",
    f"=SUM(H{addSUM1[0]}+H{addSUM1[1]}+H{addSUM1[2]}+H{addSUM1[3]}+H{addSUM1[4]}+H{addSUM1[5]}+H{addSUM1[6]})",
    f"=SUM(I{addSUM1[0]}+I{addSUM1[1]}+I{addSUM1[2]}+I{addSUM1[3]}+I{addSUM1[4]}+I{addSUM1[5]}+I{addSUM1[6]})",
    f"=SUM(J{addSUM1[0]}+J{addSUM1[1]}+J{addSUM1[2]}+J{addSUM1[3]}+J{addSUM1[4]}+J{addSUM1[5]}+J{addSUM1[6]})",
    f"=SUM(K{addSUM1[0]}+K{addSUM1[1]}+K{addSUM1[2]}+K{addSUM1[3]}+K{addSUM1[4]}+K{addSUM1[5]}+K{addSUM1[6]})",
    f"=SUM(L{addSUM1[0]}+L{addSUM1[1]}+L{addSUM1[2]}+L{addSUM1[3]}+L{addSUM1[4]}+L{addSUM1[5]}+L{addSUM1[6]})",
    f"=SUM(M{addSUM1[0]}+M{addSUM1[1]}+M{addSUM1[2]}+M{addSUM1[3]}+M{addSUM1[4]}+M{addSUM1[5]}+M{addSUM1[6]})",
    f"=SUM(N{addSUM1[0]}+N{addSUM1[1]}+N{addSUM1[2]}+N{addSUM1[3]}+N{addSUM1[4]}+N{addSUM1[5]}+N{addSUM1[6]})",
    f"=SUM(O{addSUM1[0]}+O{addSUM1[1]}+O{addSUM1[2]}+O{addSUM1[3]}+O{addSUM1[4]}+B{addSUM1[5]}+O{addSUM1[6]})",
    f"=SUM(P{addSUM1[0]}+P{addSUM1[1]}+P{addSUM1[2]}+P{addSUM1[3]}+P{addSUM1[4]}+P{addSUM1[5]}+P{addSUM1[6]})",
    f"=SUM(Q{addSUM1[0]}+Q{addSUM1[1]}+Q{addSUM1[2]}+Q{addSUM1[3]}+Q{addSUM1[4]}+Q{addSUM1[5]}+Q{addSUM1[6]})",
    f"=SUM(R{addSUM1[0]}+R{addSUM1[1]}+R{addSUM1[2]}+R{addSUM1[3]}+R{addSUM1[4]}+R{addSUM1[5]}+R{addSUM1[6]})",
    f"=SUM(S{addSUM1[0]}+S{addSUM1[1]}+S{addSUM1[2]}+S{addSUM1[3]}+S{addSUM1[4]}+S{addSUM1[5]}+S{addSUM1[6]})",
    f"=SUM(T{addSUM1[0]}+T{addSUM1[1]}+T{addSUM1[2]}+T{addSUM1[3]}+T{addSUM1[4]}+T{addSUM1[5]}+T{addSUM1[6]})",
    f"=SUM(U{addSUM1[0]}+U{addSUM1[1]}+U{addSUM1[2]}+U{addSUM1[3]}+U{addSUM1[4]}+U{addSUM1[5]}+U{addSUM1[6]})",
    f"=SUM(V{addSUM1[0]}+V{addSUM1[1]}+V{addSUM1[2]}+V{addSUM1[3]}+V{addSUM1[4]}+V{addSUM1[5]}+V{addSUM1[6]})",
    f"=SUM(W{addSUM1[0]}+W{addSUM1[1]}+W{addSUM1[2]}+W{addSUM1[3]}+W{addSUM1[4]}+W{addSUM1[5]}+W{addSUM1[6]})",
    f"=SUM(X{addSUM1[0]}+X{addSUM1[1]}+X{addSUM1[2]}+X{addSUM1[3]}+X{addSUM1[4]}+X{addSUM1[5]}+X{addSUM1[6]})",
    f"=SUM(Y{addSUM1[0]}+Y{addSUM1[1]}+Y{addSUM1[2]}+Y{addSUM1[3]}+Y{addSUM1[4]}+Y{addSUM1[5]}+Y{addSUM1[6]})",
    f"=SUM(Z{addSUM1[0]}+Z{addSUM1[1]}+Z{addSUM1[2]}+Z{addSUM1[3]}+Z{addSUM1[4]}+Z{addSUM1[5]}+Z{addSUM1[6]})"]
    while True:
        try:
            lineNum(f"Adding week total to sheets")
            sheet.insert_row(weekTotal,9,value_input_option="USER_ENTERED")
            break
        except:
            sheet.delete_row(9)
            lineNum(f"Waiting 6")
            time.sleep(5)

def endMonth():
    lineNum(f"Running end of month function")
    lastMonth = int(datetime.strftime(datetime.now() - timedelta(1), '%m'))
    addMonth = []
    monthLength = (monthrange(2022, lastMonth)[1])
    monthLength1 = monthLength
    q = 0
    lineNum(f"Last month was {lastMonth}")
    lineNum(f"Last month had {monthLength} days")
    for l in range (monthLength):
        addMonth.append(10+l)
    for m in range (monthLength):
        while True:
            try:
                check = sheet.cell(9+m,1).value
                lineNum(f"Checking if {check} is Week Total")
                if check == "Week Total":
                    lineNum(f"{check} is Week Total")
                    lineNum(f"Skipping over Week Total")
                    for n in range(m,monthLength1):
                        addMonth[n-q] = addMonth[n-q] + 1
                    q += 1
                    monthLength1 += 1
                break
            except:
                lineNum(f"Waiting 7")
                time.sleep(5)
    
    monthTotal = ["Month Total"]
    monthRow = ["=SUM("]
    Letters = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
    for p in range (25):
        for o in range(monthLength):
            monthRow.append(f"{Letters[p+1]}{addMonth[o]}")
            monthRow.append("+")

        monthRow.pop()
        monthRow.append(")")
        combine = "".join(monthRow)
        monthRow = ["=SUM("]
        monthTotal.append(combine)
        lineNum(f"Month total, {monthTotal}")

    while True:
        try:
            lineNum(f"Adding month total to sheets")
            sheet.insert_row(monthTotal,9,value_input_option="USER_ENTERED")
            break
        except:
            lineNum(f"Waiting 8")
            time.sleep(15)

def weekCheck():
    lineNum(f"Running week check function")
    yesterday = datetime.strftime(datetime.now() - timedelta(1), '%a - %d/%m/%y')
    while True:
        try:
            rowNine2 = sheet.cell(9,1).value
            lineNum(f"Check if row nine, {rowNine2} is yesterday date, {yesterday}")
            if rowNine2 != yesterday:
                lineNum(f"Dates do not match, running while loop")
                i=16
                while i != 0:
                    i-=1
                    lineNum(f"i value is, {i}")
                    yesterdayDate = datetime.strftime(datetime.now() - timedelta(i), '%a - %d/%m/%y')
                    aYesterdayDate = [yesterdayDate]
                    while True:
                        try:
                            skipCell = 0
                            rowNine = sheet.cell(9,1).value
                            rowTen = sheet.cell(10,1).value
                            lineNum(f"Check for Month Total or Week Total on row 9 - {rowNine} and row 10 - {rowTen}")
                            if rowNine == "Month Total" or rowNine == "Week Total":
                                if rowTen == "Week Total" or rowTen == "Month Total":
                                    skipCell = 2
                                    lineNum(f"Both Week Total and Month Total found, skipCell is {skipCell}")
                                else:
                                    skipCell = 1
                                    lineNum(f"Either Week Total or Month Total found, skipCell is {skipCell}")
                            else:
                                lineNum(f"No total found, skipCell is {skipCell}")
                            cell9Skip = sheet.cell(9+skipCell,1).value
                            lineNum(f"Check if {cell9Skip} and {yesterdayDate} match")
                            if cell9Skip == yesterdayDate:
                                lineNum(f"Match found")
                                i-=1
                                lineNum(f"i value is, {i}")
                                while i != 0:
                                    yesterdayDate = datetime.strftime(datetime.now() - timedelta(i), '%a - %d/%m/%y')
                                    aYesterdayDate = [yesterdayDate,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
                                    yesterdayDay = datetime.strftime(datetime.now() - timedelta(i+1), '%a')
                                    yesterdayMonth = datetime.strftime(datetime.now() - timedelta(i), '%d')
                                    lineNum(f"Date check, {yesterdayDate}")
                                    if yesterdayDay == "Sun" and skipCell == 0:
                                        lineNum(f"End of week found")
                                        endWeek()
                                    if yesterdayMonth == "01" and skipCell == 0:
                                        lineNum(f"End of month found")
                                        endMonth()

                                    while True:
                                        try:
                                            lineNum(f"Inserting date, {yesterday} into sheets")
                                            sheet.insert_row(aYesterdayDate,9)
                                            skipCell = 0
                                            i-=1
                                            lineNum(f"i value is, {i}")
                                            break
                                        except:
                                            lineNum(f"Waiting 9")
                                            time.sleep(15)
                                while True:
                                    try:
                                        currentDate = str(x.strftime("%a - %d/%m/%y"))

                                        rowNine = sheet.cell(9,1).value

                                        lineNum(f"Checking for end of week or end of month on final insert")
                                        if rowNine != currentDate:
                                            lineNum(f"Row 9, {rowNine} does not match current date, {currentDate}")
                                            if rowNine == datetime.strftime(datetime.now() - timedelta(1), '%a - %d/%m/%y'):
                                                if datetime.strftime(datetime.now() - timedelta(1), '%a') == "Sun":
                                                    lineNum(f"End of week found")
                                                    endWeek()
                                                elif datetime.strftime(datetime.now() - timedelta(0), '%d') == "01":
                                                    lineNum(f"End of month found")
                                                    endMonth()

                                        lineNum(f"Inserting current date. {currentDate}")
                                        date = [currentDate,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
                                        sheet.insert_row(date,9)
                                        break
                                    except:
                                        lineNum(f"Waiting 10")
                                        time.sleep(15)
                                break
                            else:
                                lineNum(f"Match not")
                            break
                        except:
                            lineNum(f"Waiting 11")
                            time.sleep(5)
            while True:
                try:
                    if cell9Skip != yesterdayDate and sheet.cell(9,1).value != currentDate:
                        print(cell9Skip,yesterdayDate)
                        lineNum(f"Previous date not found")
                        lineNum(f"Adding current date")
                        date = [currentDate,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
                        sheet.insert_row(date,9)
                    break
                except Exception as error:
                    lineNum(f"Waiting, {error}")
                    time.sleep(5)
            lineNum(f"Dates match, breaking loop")
            break
        except:
            lineNum(f"Waiting 12")
            time.sleep(5)

def dayCheck():
    rowNine = sheet.cell(9,1).value

    lineNum(f"Current date is {currentDate}")
    lineNum(f"Row 9 date is {rowNine}")

    if rowNine != currentDate:
        lineNum(f"Current date and row 9 date do not match")
        if rowNine == datetime.strftime(datetime.now() - timedelta(1), '%a - %d/%m/%y'):
            lineNum(f"Row 9 is yesterdays date, {datetime.strftime(datetime.now() - timedelta(1), '%a - %d/%m/%y')}")
            if datetime.strftime(datetime.now() - timedelta(1), '%a') == "Sun":
                lineNum(f"Yesterday day was sunday")
                endWeek()
            elif datetime.strftime(datetime.now() - timedelta(0), '%d') == "01":
                lineNum(f"Today is the beginning of the month")
                endMonth()
            while True:
                try:
                    lineNum(f"Adding todays date to the sheets")
                    sheet.insert_row(date,9)
                    break
                except:
                    lineNum(f"Waiting 13")
                    time.sleep(5)
        else:
            weekCheck()

#--------------------------Main--------------------------#
x = tm.datetime.now()
currentDate = str(x.strftime("%a - %d/%m/%y"))
date = [currentDate,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

#dayCheck()

window = tk.Tk()
window.title("Hour tracker")
window.geometry("520x300")
window['bg']="#F57A22"

login()

window.mainloop()