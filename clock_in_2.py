#-------------------------Import-------------------------#
import datetime as tm
import os
import sys
import time
import logging
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as tkm
from inspect import currentframe
from calendar import month, monthrange, week
from datetime import datetime, timedelta

try:
    from github import Github
except ImportError:
    os.system('pip install PyGithub')
    from github import Github

f = open("token.txt","r")
token = f.read()
f.close()

g = Github(token)
repo = g.get_repo("sensetraining/Clock-In-2")

f = open("options.txt", "r")
optionData = f.readlines()
lastLog = optionData[1]

try:
    f = open(f"logs/{lastLog}.txt", "r")
    file_contents = f.read()
    f.close()

    file_path = f"logs/{lastLog}.txt"
    repo.create_file(file_path, "commit message", file_contents)
except:
    pass

x = tm.datetime.now()
time_str = str(x.strftime("%Y-%m-%d %H.%M.%S"))

f = open("options.txt", "r")
optionData = f.readlines()
f.close()
optionData[1] = (time_str)
f = open("options.txt","w")
f.writelines(optionData)
f.close()

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
    
logger.info(f"[{time_str}] Running Program")
print(f"[{time_str}] Running Program")
    
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

try:
    import requests
except ImportError:
    lineNum(f"Installing Requests")
    os.system('pip install requests')
    import requests

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
    lineNum("weekEnd Function")
    Letters = ["B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]

    total = ["Week Total"]
    lineNum("Adding Week Total to each column")
    for k in range(25):
        d1 = datetime.strftime(datetime.now() - timedelta(0), '%d/%m/%Y')
        lineNum(f"Date 1: {d1}")
        d2 = datetime.strftime(datetime.now() - timedelta(i), '%d/%m/%Y')
        lineNum(f"Date 2: {d2}")
        num = i + i // 7 + 1 + (int(d1[6:9])-int(d2[6:9]))*12+int(d1[3:5])-int(d2[3:5])
        lineNum(f"Num variable: {num}")
        column = "=SUM("
        lineNum("Checking for end of month in week")
        for j in range(7):
            if datetime.strftime(datetime.now() - timedelta(i+j), '%d') == "01":
                lineNum("End of month found")
                num += 1
                lineNum(f"Adding 1 to Num: {num}")
            column += f"{Letters[k]}{10+j+num}+"
        lineNum(f"")
        column = column[:-1] + ")"
        lineNum("Appending column to total")
        total.append(column)
    lineNum("All columns appended returning total")
    return total

def monthEnd(i):
    lineNum("monthEnd function")
    Letters = ["B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]

    total = ["Month Total"]
    lineNum("Adding Month Total to each column")
    for k in range(25):
        d1 = datetime.strftime(datetime.now() - timedelta(0), '%d/%m/%Y')
        d2 = datetime.strftime(datetime.now() - timedelta(i), '%d/%m/%Y')
        num = i + i // 7 + 1 + (((int(d1[6:10]) - int(d2[6:10])) * 12 + int(d1[3:5]) - int(d2[3:5]))*2)
        lineNum(f"Num variable: {num}")
        column = "=SUM("
        lineNum("Checking for end of week in month")
        for j in range(monthrange(int(datetime.strftime(datetime.now() - timedelta(0), '%Y')), int(datetime.strftime(datetime.now() - timedelta(i+1), '%m')))[1]):
            if datetime.strftime(datetime.now() - timedelta(i+j+1), '%a') == "Sun":
                lineNum("End of week found")
                num += 1
                lineNum(f"Adding 1 to Num: {num}")
            column += f"{Letters[k]}{10+j+num}+"
        column = column[:-1] + ")"
        lineNum("Appending column to total")
        total.append(column)
    lineNum("All columns appended returning total")
    return total

def dayCheck():
    lineNum("dayCheck Function")
    currentDate = str(x.strftime("%a - %d/%m/%y"))
    lineNum(f"Current Date: {currentDate}")
    values_list = sheet.col_values(1)
    diff = (datetime.strptime(values_list[8][6:14], "%d/%m/%y") - datetime.strptime(currentDate[6:14], "%d/%m/%y")).days
    if diff <0:
        diff = diff * -1
    values = []
    lineNum(f"Difference between last date and current date: {diff}")
    if diff >=1:
        lineNum(f"Difference {diff} is more than 1, filling in dates")
        for i in range(diff):
            lineNum("Adding black row")
            values.append([datetime.strftime(datetime.now() - timedelta(i), '%a - %d/%m/%y'),'00:00:00.000','00:00:00.000','00:00:00.000','00:00:00.000','00:00:00.000','00:00:00.000','00:00:00.000','00:00:00.000','00:00:00.000','00:00:00.000','00:00:00.000','00:00:00.000','00:00:00.000','00:00:00.000','00:00:00.000','00:00:00.000','00:00:00.000','00:00:00.000','00:00:00.000','00:00:00.000','00:00:00.000','00:00:00.000','00:00:00.000','00:00:00.000','00:00:00.000'])
            lineNum("Checking for end of month")
            if datetime.strftime(datetime.now() - timedelta(i), '%d') == "01":
                lineNum("End of month found, running monthEnd function")
                values.append(monthEnd(i))
                lineNum("Appending returned total from monthEnd")
            lineNum("Checking for end of week")
            if datetime.strftime(datetime.now() - timedelta(i+1), '%a') == "Sun":
                lineNum("End of week found running weekEnd function")
                values.append(weekEnd(i))
                lineNum("Appending returned total from weekEnd")
        lineNum("All rows appended to values variable, adding to sheets")
        sheet.insert_rows(values, row=9, value_input_option='USER_ENTERED', inherit_from_before=True)
    lineNum("Sheets all up to date, returning from dayCheck function")
    return

def updateCheck():
    lineNum("Running updateCheck")
    lineNum("Getting version from GitHub")
    version = requests.get("https://raw.githubusercontent.com/sensetraining/Clock-In-2/main/version.txt").text
    lineNum(f"GitHub version: {version}")

    lineNum("Opening 'version.txt' file")
    cver = open("version.txt","r").read()

    lineNum(f"Installed version: {cver}")

    if cver == version:
        lineNum("Program up to date")
        return

    else:
        lineNum("Update is available, displaying message")
        updateMsg = tkm.showerror(title="Warning", message=f"Update available, please reopen application")
        lineNum("Closing application")
        sys.exit()

def login(enteredUsername,enteredPassword,loginBox,checkState):
    lineNum("Login button presses, attempting login")
    lineNum("Getting all values from sheets")
    allValues = sheet.get_all_values()

    lineNum(f"Checking for entered username: {enteredUsername} in the sheets")
    if enteredUsername in allValues[0]:
        userPos = allValues[0].index(enteredUsername)
        lineNum(f"Username is valid at position {userPos}")
    else:
        lineNum(f"Username not found, displaying error message and returning to loginPage")
        incorrectEntry = tkm.showerror(title="Incorrect", message="You entered an incorrect Username or Password")
        return

    lineNum("Checking if entered password matches password on sheets")
    if enteredPassword != allValues[1][userPos]:
        lineNum("Passwords don't match, displaying error message and returning to loginPage")
        incorrectEntry = tkm.showerror(title="Incorrect", message="You entered an incorrect Username or Password")
        return
    else:
        lineNum("Passwords match")

    lineNum("Checking is Remember me? button was checked")
    if checkState == ("selected",):
        lineNum("Button was checked setting remember to True")
        remember = "True"
    else:
        lineNum("Button not checked setting remember to false")
        remember = "False"

    lineNum("Opening 'options.txt' file")
    f = open("options.txt", "r")
    optionData = f.readlines()
    f.close()
    lineNum("Setting the remmeber and userPos variables")
    optionData[0] = (f"{remember} {userPos}\n")
    f = open("options.txt","w")
    f.writelines(optionData)
    f.close()
    lineNum("Closing file")

    lineNum("Destroying loginPage and running mainPage")
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
    mainBox.destroy()
    loginPage()
    return

def noClockOut(userPos,allValues,date,mainBox):
    lineNum("noClockOut")

    x = tm.datetime.now()
    lineNum("Getting dates from sheet")
    dates = sheet.col_values(1)
    clockInTime = allValues[3][userPos]
    lineNum(f"Last clock in time: {clockInTime}")

    lineNum(f"Checking for {date} in dates column")
    if date in dates:
        lineNum(f"Date found, add clocked in time at specific date and setting clock status to FALSE")
        datePos = dates.index(date)

        cell_list = [
        sheet.cell(datePos, userPos+1),
        sheet.cell(3, userPos+1)]

        cell_list[0].value = f"R{clockInTime}"
        cell_list[1].value = "FALSE"
        sheet.update_cells(cell_list,value_input_option='USER_ENTERED')
    
    else:
        lineNum("Date not found, setting clock status to FALSE")
        sheet.update_cell(3,userPos+1,"FALSE")

    lineNum("Displaying warning message")
    clockOutMsg = tkm.showerror(title="Warning", message=f"You didn't clock out on {date} so no hours were saved")
    mainBox.destroy()
    lineNum("Destroying mainBox and going back to mainPage")

    mainPage(userPos)
    return

def clockIn(userPos,mainBox):
    lineNum("Running clockIn function")
    dayCheck()
    updateCheck()
    
    letters = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
    lineNum("Getting current time and current date")
    x = tm.datetime.now()
    currentTime = (x.strftime("%X"))
    currentDate = str(x.strftime("%a - %d/%m/%y"))

    lineNum("Setting the last clock in date and time and setting clock status to TRUE")
    sheet.update(f"{letters[userPos]}3:{letters[userPos]}5",[["TRUE"],[currentTime],[currentDate]])

    lineNum("Destroying mainBox and going back to mainPage")
    mainBox.destroy()
    mainPage(userPos)
    return

def clockOut(userPos,mainBox):
    lineNum("Running clockOut function")
    dayCheck()
    updateCheck()

    letters = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
    lineNum("Getting current time and current dates")
    x = tm.datetime.now()
    currentTime = (x.strftime("%X"))
    currentDate = str(x.strftime("%a - %d/%m/%y"))

    lineNum("Getting column data for the user")
    column = sheet.col_values(userPos+1)
    lastClocked = column[3]
    lineNum(f"Last clock in time: {lastClocked}")
    clockedTime = column[8]
    lineNum(f"Clocked time: {clockedTime}")

    currentTime = tm.datetime.strptime(currentTime,"%X")
    lastClocked = tm.datetime.strptime(lastClocked,"%X")
    clockedTime = tm.datetime.strptime(clockedTime,"%X")

    timeDiff = currentTime - lastClocked
    totalClocked = timeDiff + clockedTime

    lineNum(f"Total clocked time: {totalClocked}")
    lineNum("Setting clocked status to False, adding total time and setting last clock out time and date")

    column[2] = "False"
    column[5] = (currentTime.strftime("%X"))
    column[6] = (currentDate)
    column[8] = (totalClocked.strftime("%X"))

    lineNum("Updating sheet")
    sheet.update(f"{letters[userPos]}1:{letters[userPos]}9",[[x] for x in column[0:9]],value_input_option='USER_ENTERED')

    lineNum("Destroing mainBox and returning to mainPage")
    mainBox.destroy()
    mainPage(userPos)
    return

def loginPage():
    lineNum("Login Page")
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

def hoursPage(userPos,page,adminBox,mainBox,usernames,selectedUsers):
    lineNum("Running hoursPage function")
    lineNum("Setting page to 'hours")
    page = "hours"
    adminBox.destroy()
    settingsPage(userPos,mainBox,page,usernames,selectedUsers)
    return

def accountPage(userPos,page,adminBox,mainBox,usernames,selectedUsers):
    lineNum("Running accountPage function")
    lineNum("Setting page to 'accounts")
    page = "accounts"
    adminBox.destroy()
    settingsPage(userPos,mainBox,page,usernames,selectedUsers)
    return

def developmentPage(userPos,page,adminBox,mainBox,usernames,selectedUsers):
    lineNum("Running developmentPage function")
    lineNum("Setting page to 'development")
    page = "development"
    adminBox.destroy()
    lineNum("Returning to settingsPage")
    settingsPage(userPos,mainBox,page,usernames,selectedUsers)
    return

def mainPageBack(userPos,adminBox):
    lineNum("Running mainPageBack function")
    lineNum("Destroing adminBox")
    adminBox.destroy()
    lineNum("Returning to mainPage")
    mainPage(userPos)
    return

def addUser(userPos,mainBox,page,usernames,selectedUsers,adminBox,value):
    lineNum("Running addUser function")
    lineNum(f"Removing {value} from {usernames}")
    usernames.remove(value)
    lineNum(f"Adding {value} to {selectedUsers}")
    selectedUsers.append(value)
    adminBox.destroy()
    lineNum("Returning to settingsPage")
    settingsPage(userPos,mainBox,page,usernames,selectedUsers)
    return

def removeUser(userPos,mainBox,page,usernames,selectedUsers,adminBox,value):
    lineNum("Running removeUser function")
    lineNum(f"Removing {value} from {selectedUsers}")
    selectedUsers.remove(value)
    lineNum(f"Adding {value} to {usernames}")
    usernames.append(value)
    adminBox.destroy()
    lineNum("Returning to settingsPage")
    settingsPage(userPos,mainBox,page,usernames,selectedUsers)
    return

def searchHours(day1,month1,year1,day2,month2,year2,selectedUsers):
    lineNum("Running searchHours function")

    lineNum("Checking if entered date is valid")
    try:
        day1,month1,year1,day2,month2,year2 = int(day1),int(month1),int(year1),int(day2),int(month2),int(year2)
        date = datetime(day=day1, month=month1, year=year1)
        formattedDate1 = date.strftime("%d/%m/%Y")
        date2 = datetime(day=day2, month=month2, year=year2)
        formattedDate2 = date2.strftime("%d/%m/%Y")  
    except Exception as error:
        lineNum("Date is invalid")
        lineNum(f"Error: {error}")
        lineNum("Displaying invalid date popup")
        invalidDate = tkm.showerror(title="Warning", message=f"Not a valid date")
        return
    lineNum("Date is valid")
    
    x = tm.datetime.now()
    year = int(x.strftime("%Y"))

    date1Year = int(datetime.strptime(formattedDate1, "%d/%m/%Y").strftime("%Y"))
    date2Year = int(datetime.strptime(formattedDate2, "%d/%m/%Y").strftime("%Y"))

    print(type(date1Year),type(date2Year))

    lineNum("Checking if year is valid")
    if date1Year < 2022 or date1Year > year or date2Year < 2022 or date2Year > year:
        lineNum("Invalid year, displaying error popup message")
        invalidYear = tkm.showerror(title="Error", message=f"You entered an invalid year")
        return

    date1 = datetime.strptime(formattedDate1, "%d/%m/%Y")
    date2 = datetime.strptime(formattedDate2, "%d/%m/%Y")

    lineNum("Getting the difference between the 2 dates")
    diff = (date2 - date1).days
    if diff <0:
        diff = (diff*-1)+1
    lineNum(f"Difference is: {diff}")

    date1Full = (datetime.strptime(formattedDate1, "%d/%m/%Y").strftime('%a - %d/%m/%y'))
    date2Full = (datetime.strptime(formattedDate2, "%d/%m/%Y").strftime('%a - %d/%m/%y'))

    lineNum("Getting all values from sheet")
    allValues = sheet.get_all_values()
    
    column = [row[0] for row in allValues]

    lineNum("Getting all positions where there is a Month or Week Total")
    skipPos = [i for i, x in enumerate(column) if x in ["Month Total", "Week Total"]]
    lineNum(f"Skip positions: {skipPos}")

    lineNum(f"Check if date 1: {date1Full} is in date column")
    if date1Full in column:
        position1 = column.index(date1Full)
        lineNum(f"TRUE at postion {position1}")
    else:
        lineNum("Displaying error popup message")
        noDate = tkm.showerror(title="Error", message=f"Date does not exist within spreadsheet")
        return

    lineNum(f"Check if date 2: {date2Full} is in date column")
    if date2Full in column:
        position2 = column.index(date2Full)
        lineNum(f"TRUE at postion {position2}")
    else:
        lineNum("Displaying error popup message")
        noDate = tkm.showerror(title="Error", message=f"Date does not exist within spreadsheet")
        return

    if position1 > position2:
        startPos = position2
    else:
        startPos = position1

    lineNum("Creating new window")
    rootHours = tk.Tk()
    rootHours.title("Hours")
    rootHours.minsize(365,340)
    rootHours.geometry("290x340")
    rootHours['bg'] = "#f27420"

    style = ttk.Style()
    style.theme_use('default')

    x_cordinate = int((rootHours.winfo_screenwidth() / 2) - 365/2)
    y_cordinate = int((rootHours.winfo_screenheight() / 2) - 340/2)
    rootHours.geometry("+{}+{}".format(x_cordinate-50, y_cordinate-30))

    blueBox = tk.Label(rootHours,bg="#113f8c",relief="solid")
    blueBox.place(relx=0.5,rely=0.5,height=260,width=285,anchor="center")

    nameText = tk.Text(blueBox,font=("Helvetica",12),relief="flat")
    nameText.place(height=200,width=75,x=30,y=30)

    hoursText = tk.Text(blueBox,font=("Helvetica",12),relief="flat")
    hoursText.place(height=200,width=75,x=105,y=30)

    NCOText = tk.Text(blueBox,font=("Helvetica",12),relief="flat")
    NCOText.place(height=200,width=75,x=180,y=30)

    nameText.insert(tk.END, "Name:\n")
    hoursText.insert(tk.END, "Hours:\n")
    NCOText.insert(tk.END, "No. NCO:\n")

    allUserHours = 0
    failTotal = 0

    lineNum("Getting hours for each user inside specified date range")
    for user in selectedUsers:
        startPosi = startPos
        userTotalMin = 0
        userFail = 0
        userPos = allValues[0].index(user)
        userColumn = [row[userPos] for row in allValues]
        for i in range (diff):
            if startPosi+i in skipPos:
                startPosi += 1
            cell = userColumn[startPosi+i]
            try:
                cellHour = int(cell[0:2])
                cellMin = int(cell[3:5])
                userTotalMin += (cellHour*60)+cellMin
            except Exception as error:
                try:
                    cellHour = int(cell[0:1])
                    cellMin = int(cell[2:4])
                    userTotalMin += (cellHour*60)+cellMin
                except Exception as error:
                    userFail += 1
        lineNum(f"User: {user}")
        lineNum(f"Total Min: {userTotalMin}")
        userTotalHour = userTotalMin/60
        lineNum(f"Total Hour: {userTotalHour}")
        lineNum(f"Total Fail: {userFail}")
        failTotal += userFail
        allUserHours += userTotalHour
        lineNum(f"All Hours: {allUserHours}")

        lineNum("Inserting user hours into text box")
        nameText.insert(tk.END, f"{user}\n")
        hoursText.insert(tk.END, f"{round(userTotalHour,1)}\n")
        NCOText.insert(tk.END,f"{userFail}\n")
    lineNum("Inserting total hours into text box")
    nameText.insert(tk.END, "Total:\n")
    hoursText.insert(tk.END, f"{round(allUserHours,1)}\n")
    NCOText.insert(tk.END, f"{failTotal}\n")

    rootHours.mainloop()
    return

def makeAdmin(userPos,mainBox,page,usernames,selectedUsers,adminBox,staff):
    lineNum("Running makeAdmin function")
    lineNum("Displaying popup option")
    response = tkm.askquestion("Warning", f"Are you sure you want to make {staff} an admin?")
    lineNum(f"Response was: {response}")
    if response == "yes":
        lineNum("Setting admin to TRUE on sheet")
        allStaff = sheet.row_values(1)
        staffPos = allStaff.index(staff)
        sheet.update_cell(8, staffPos+1, 'TRUE')
    adminBox.destroy()
    lineNum("Returning to settingsPage")
    settingsPage(userPos,mainBox,page,usernames,selectedUsers,staff)
    return

def removeAdmin(userPos,mainBox,page,usernames,selectedUsers,adminBox,staff):
    lineNum("Running removeAdmin function")
    lineNum("Displaying popup option")
    response = tkm.askquestion("Warning", f"Are you sure you want to remove admin from {staff}?")
    lineNum(f"Reponse was: {response}")
    if response == "yes":
        lineNum("Setting admin to FALSE on sheet")
        allStaff = sheet.row_values(1)
        staffPos = allStaff.index(staff)
        sheet.update_cell(8, staffPos+1, 'False')
    adminBox.destroy()
    lineNum("Returning to settingsPage")
    settingsPage(userPos,mainBox,page,usernames,selectedUsers,staff)
    return

def deleteUser(userPos,mainBox,page,usernames,selectedUsers,adminBox,staff):
    lineNum("Running deleteUser function")
    lineNum("Displaying popup option")
    response = tkm.askquestion("Warning", f"Are you sure you want to remove {staff} as a user? This cannot be undone!")
    lineNum(f"Response was: {response}")
    if response == "yes":
        lineNum("Setting username and pass to EMPTY o sheets")
        allStaff = sheet.row_values(1)
        staffPos = allStaff.index(staff)
        sheet.update_cell(1, staffPos+1, 'EMPTY')
        sheet.update_cell(2, staffPos+1, 'EMPTY')
        lineNum("Display popup message")
        response = tkm.showinfo("User Added", f"{staff} has been removed")
    adminBox.destroy()
    lineNum("Returning to settingsPage")
    settingsPage(userPos,mainBox,page,usernames,selectedUsers)
    return

def staffSelection(userPos,mainBox,page,usernames,selectedUsers,adminBox,staff):
    lineNum("Running staffSelection function")
    lineNum("Destroying adminBox")
    adminBox.destroy()
    lineNum("Returning to settingsPage")
    settingsPage(userPos,mainBox,page,usernames,selectedUsers,staff)
    return

def developmentSelection(userPos,mainBox,page,usernames,selectedUsers,adminBox,staff,value):
    lineNum("Running developmentSelection function")
    lineNum("Destroying adminBox")
    adminBox.destroy()
    lineNum("Returning to settignsPage")
    settingsPage(userPos,mainBox,page,usernames,selectedUsers,staff,value)
    return

def editUser(userPos,mainBox,page,usernames,selectedUsers,adminBox,staff):
    lineNum("Runnning editUser page")
    adminBox.destroy()

    lineNum("Getting column of user from sheet")
    allStaff = sheet.row_values(1)
    staffPos = allStaff.index(staff)
    staffCol = sheet.col_values(staffPos+1)


    editBox = ttk.Label(root,style="blueBox.TLabel")
    editBox.place(height=280,width=480,relx=0.5,rely=0.5,anchor="center")

    editLabel = ttk.Label(editBox,text=f"Edit {staff}'s login details",style="label.TLabel")
    editLabel.place(relx=0.5,y=30,anchor="center")

    usernameLabel = ttk.Label(editBox, text="Username:",style="label.TLabel")
    usernameLabel.place(x=20, y=60)

    usernameEntry = ttk.Entry(editBox,style="Custom.TEntry",font=("Helvetica", 14))
    usernameEntry.insert(0,staff)
    usernameEntry.place(height=31,width=290,x=150, y=60)

    passwordLabel = ttk.Label(editBox, text="Password:",style="label.TLabel")
    passwordLabel.place(x=20, y=100)

    passwordEntry = ttk.Entry(editBox,show="*",style="Custom.TEntry",font=("Helvetica", 14))
    passwordEntry.insert(0,staffCol[1])
    passwordEntry.place(height=31,width=290,x=150, y=100)

    submitButton = ttk.Button(editBox, text="Submit",style="LoginButton.TButton",command=lambda:userUpdate(userPos,mainBox,page,usernames,selectedUsers,adminBox,staff,staffCol,editBox,usernameEntry.get(),passwordEntry.get()))
    submitButton.place(height=40,relx=0.5, rely=0.65, anchor="center")

    backButton = ttk.Button(editBox, text="Back",style="LoginButton.TButton",command=lambda:editBack(userPos,mainBox,page,usernames,selectedUsers,adminBox,staff,editBox))
    backButton.place(height=40,relx=0.5, rely=0.85, anchor="center")
    return

def editBack(userPos,mainBox,page,usernames,selectedUsers,adminBox,staff,editBox):
    lineNum("Running editBack function")
    lineNum("Destroying editBox")
    editBox.destroy()
    lineNum("Returning to settingsPage")
    settingsPage(userPos,mainBox,page,usernames,selectedUsers,staff)
    return

def userUpdate(userPos,mainBox,page,usernames,selectedUsers,adminBox,staff,staffCol,editBox,enteredUser,EnteredPass):
    lineNum("Running userUpdate function")
    editBox.destroy()

    letters = ["B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]

    staffCol[0] = enteredUser
    staffCol[1] = EnteredPass

    lineNum("Updating sheets with entered username and pass")
    sheet.update(f"{letters[userPos-1]}1:{letters[userPos-1]}2",[[x] for x in staffCol[0:2]],value_input_option='USER_ENTERED')
    lineNum("Displaying popup message")
    response = tkm.showinfo("User Updated", f"{staff} login details have been updated")
    lineNum("Returning to settingsPage")
    settingsPage(userPos,mainBox,page,usernames,selectedUsers,enteredUser)
    return

def addAccount(userPos,mainBox,page,usernames,selectedUsers,adminBox,username,password,allStaff):
    lineNum("Running addAccount function")
    adminBox.destroy()

    lineNum("Finding a free position")
    freePos = allStaff.index("EMPTY")

    lineNum("Adding new user details to sheet")
    sheet.update_cell(1, freePos+1, username)
    sheet.update_cell(2, freePos+1, password)

    lineNum("Displaying popup message")
    response = tkm.showinfo("User Added", f"{username} has been added as a user")

    lineNum("Returning to settings page")
    settingsPage(userPos,mainBox,page,usernames,selectedUsers,username)
    return

def submitBug(userPos,mainBox,page,usernames,selectedUsers,adminBox,selectedStaff,selectedOption,input):
    lineNum("Runninng submitBug function")
    adminBox.destroy()

    lineNum("Getting GitHub token from 'token.txt' file")
    f = open("token.txt","r")
    token = f.read()
    f.close()

    lineNum("Connecting to repo")
    g = Github(token)
    repo = g.get_repo("sensetraining/Clock-In-2")

    name = sheet.cell(1,userPos+1).value

    lineNum("Gettinng current date and time")
    x = tm.datetime.now()
    time_str = str(x.strftime("%Y-%m-%d %H.%M.%S"))

    lineNum("Pushing bug report to the GitHub")
    file_path = f"Bug_Report/{name}|Bug_Report|{time_str}.txt"
    repo.create_file(file_path, "commit message", input)
    lineNum("Displaying popup message")
    response = tkm.showinfo("Bug Report", f"Thank you. Your bug report has been submitted")
    lineNum("Returning to settinngsPage")
    settingsPage(userPos,mainBox,page,usernames,selectedUsers,selectedStaff,selectedOption)
    return

def submitSuggest(userPos,mainBox,page,usernames,selectedUsers,adminBox,selectedStaff,selectedOption,input):
    lineNum("Running submitSuggest function")
    adminBox.destroy()

    lineNum("Getting GitHub token from 'token.txt' file")
    f = open("token.txt","r")
    token = f.read()
    f.close()

    lineNum("Connecting to repo")
    g = Github(token)
    repo = g.get_repo("sensetraining/Clock-In-2")

    name = sheet.cell(1,userPos+1).value

    lineNum("Gettinng current date and time")
    x = tm.datetime.now()
    time_str = str(x.strftime("%Y-%m-%d %H.%M.%S"))

    lineNum("Pushing suggestion to the GitHub")
    file_path = f"Suggestions/{name}|Suggestion|{time_str}.txt"
    repo.create_file(file_path, "commit message", input)
    lineNum("Displaying popup message")
    response = tkm.showinfo("Suggestion", f"Thank you. Your suggestion has been submitted")
    lineNum("Returning to settinngsPage")
    settingsPage(userPos,mainBox,page,usernames,selectedUsers,selectedStaff,selectedOption)
    return

def settingsPage(userPos,mainBox,page,usernames,selectedUsers,selectedStaff="Accounts",selectedOption="Report Bug"):
    lineNum("Running settings page")
    lineNum("Destroying mainBox")
    mainBox.destroy()

    allStaff = sheet.row_values(1)
    staff = [item for item in allStaff if item != "EMPTY"]
    staff.pop(0)

    lineNum("Checking if user has admin")
    if sheet.cell(8,userPos+1).value == "TRUE":
        lineNum("TRUE")
        admin = True
    else:
        lineNum("FALSE")
        admin = False

    adminBox = ttk.Label(root,style="blueBox.TLabel")
    adminBox.place(height=280,width=480,relx=0.5,rely=0.5,anchor="center")

    if page == "hours" and admin == True:
        lineNum("Loading hours page")
        hoursButton = ttk.Button(adminBox,text="Hours",style="tabSunken.TButton",command=lambda:hoursPage(userPos,page,adminBox,mainBox,usernames,selectedUsers))
        hoursButton.place(height=29,width=159,x=1,y=1)
        hoursButton.state(["disabled"])

        accountButton = ttk.Button(adminBox,text="Accounts",style="tabFlat.TButton",command=lambda:accountPage(userPos,page,adminBox,mainBox,usernames,selectedUsers))
        accountButton.place(height=29,width=160,x=160,y=1)

        developmentButton = ttk.Button(adminBox,text="Development",style="tabFlat.TButton",command=lambda:developmentPage(userPos,page,adminBox,mainBox,usernames,selectedUsers))
        developmentButton.place(height=29,width=159,x=320,y=1)

        value = tk.StringVar(adminBox)
        value.set("Staff")

        staffSelect = ttk.OptionMenu(adminBox, value, "Staff",*usernames)
        staffSelect["menu"].config(background="white",font=('Helvetica', 12))
        staffSelect.place(x=5,y=35,width=200,height=40)

        addButon = ttk.Button(adminBox,text="+",style="addBtn.TButton",command=lambda:addUser(userPos,mainBox,page,usernames,selectedUsers,adminBox,value.get()))
        addButon.place(x=210,y=35,height=40,width=40)

        if len(selectedUsers) != 0:
            lineNum("Displaying selected staff box")
            value2 = tk.StringVar(adminBox)
            value2.set("Selected")

            staffSelected = ttk.OptionMenu(adminBox, value2, "Selected",*selectedUsers)
            staffSelected["menu"].config(background="white",font=('Helvetica', 12))
            staffSelected.place(x=5,y=80,width=200,height=40)

            minusButon = ttk.Button(adminBox,text="-",style="removeBtn.TButton",command=lambda:removeUser(userPos,mainBox,page,usernames,selectedUsers,adminBox,value2.get()))
            minusButon.place(x=210,y=80,height=40,width=40)

            firstDateLabel = ttk.Label(adminBox,text="First Date",style="label2.TLabel")
            firstDateLabel.place(x=253,y=30)

            dmyLabel =ttk.Label(adminBox,text="Day:       Month:    Year:",style="label3.TLabel")
            dmyLabel.place(x=253,y=53)

            days = list(range(1, 32))
            months = list(range(1, 13))
            years = list(range(2022, 2101))

            selected_day = tk.StringVar()
            selected_month = tk.StringVar()
            selected_year = tk.StringVar()

            selected_day2 = tk.StringVar()
            selected_month2 = tk.StringVar()
            selected_year2 = tk.StringVar()

            dayCombobox = ttk.Combobox(adminBox, textvariable=selected_day, values=days, width=5)
            dayCombobox.place(x=255,y=75)
            monthCombobox = ttk.Combobox(adminBox, textvariable=selected_month, values=months, width=5)
            monthCombobox.place(x=315,y=75)
            yearCombobox = ttk.Combobox(adminBox, textvariable=selected_year, values=years, width=10)
            yearCombobox.place(x=377,y=75)

            secondDateLabel = ttk.Label(adminBox,text="Second Date",style="label2.TLabel")
            secondDateLabel.place(x=253,y=100)

            dmyLabel =ttk.Label(adminBox,text="Day:       Month:    Year:",style="label3.TLabel")
            dmyLabel.place(x=253,y=123)

            dayCombobox2 = ttk.Combobox(adminBox, textvariable=selected_day2, values=days, width=5)
            dayCombobox2.place(x=255,y=145)
            monthCombobox2 = ttk.Combobox(adminBox, textvariable=selected_month2, values=months, width=5)
            monthCombobox2.place(x=315,y=145)
            yearCombobox2 = ttk.Combobox(adminBox, textvariable=selected_year2, values=years, width=10)
            yearCombobox2.place(x=377,y=145)

            searchHoursButton = ttk.Button(adminBox,text="Search Hours",style="MediumButton.TButton",command=lambda:searchHours(dayCombobox.get(),monthCombobox.get(),yearCombobox.get(),dayCombobox2.get(),monthCombobox2.get(),yearCombobox2.get(),selectedUsers))
            searchHoursButton.place(x=255,y=175,height=28,width=201)

            today = datetime.today()
            last_week = today - timedelta(days=7)

            start_date = last_week - timedelta(days=last_week.weekday())
            end_date = start_date + timedelta(days=6)

            weekStartDay = start_date.strftime('%d')
            weekStartMonth = start_date.strftime('%m')
            weekStartYear = start_date.strftime('%Y')

            weekEndDay = end_date.strftime('%d')
            weekEndMonth = end_date.strftime('%m')
            weekEndYear = end_date.strftime('%Y')

            last_month = today.replace(day=1) - timedelta(days=1)
            start_date = last_month.replace(day=1)
            end_date = last_month

            monthStartDay = start_date.strftime('%d')
            monthStartMonth = start_date.strftime('%m')
            monthStartYear = start_date.strftime('%Y')
            
            monthEndDay = end_date.strftime('%d')
            monthEndMonth    = end_date.strftime('%m')
            monthEndYear = end_date.strftime('%Y')

            searchLabel = ttk.Label(adminBox,text="Search Hours For:",style="label3.TLabel")
            searchLabel.place(x=5,y=122)

            lastWeekButton = ttk.Button(adminBox,text=f"Last Week {weekStartDay}/{weekStartMonth} - {weekEndDay}/{weekEndMonth}",style="MediumButton.TButton",command=lambda:searchHours(weekStartDay,weekStartMonth,weekStartYear,weekEndDay,weekEndMonth,weekEndYear,selectedUsers))
            lastWeekButton.place(x=5,y=146,height=26,width=245)

            lastMonthButton = ttk.Button(adminBox,text=f"Last Month {monthStartDay}/{monthStartMonth} - {monthEndDay}/{monthEndMonth}",style="MediumButton.TButton",command=lambda:searchHours(monthStartDay,monthStartMonth,monthStartYear,monthEndDay,monthEndMonth,monthEndYear,selectedUsers))
            lastMonthButton.place(x=5,y=177,height=26,width=245)

    elif page == "accounts" and admin == True:
        lineNum("Displaying accounts page")
        hoursButton = ttk.Button(adminBox,text="Hours",style="tabFlat.TButton",command=lambda:hoursPage(userPos,page,adminBox,mainBox,usernames,selectedUsers))
        hoursButton.place(height=29,width=159,x=1,y=1)

        accountButton = ttk.Button(adminBox,text="Accounts",style="tabSunken.TButton",command=lambda:accountPage(userPos,page,adminBox,mainBox,usernames,selectedUsers))
        accountButton.place(height=29,width=160,x=160,y=1)
        accountButton.state(["disabled"])

        developmentButton = ttk.Button(adminBox,text="Development",style="tabFlat.TButton",command=lambda:developmentPage(userPos,page,adminBox,mainBox,usernames,selectedUsers))
        developmentButton.place(height=29,width=159,x=320,y=1)

        editLabel = ttk.Label(adminBox,text="Edit Accounts",style="label.TLabel")
        editLabel.place(x=5,y=35)

        value = tk.StringVar(adminBox)
        value.set("Accounts")

        staffSelect = ttk.OptionMenu(adminBox, value, selectedStaff,*staff,command=lambda event, val=value :staffSelection(userPos,mainBox,page,usernames,selectedUsers,adminBox,value.get()))
        staffSelect["menu"].config(background="white",font=('Helvetica', 12))
        staffSelect.place(x=5,y=70,width=200,height=40)

        if selectedStaff != "Accounts":
            lineNum("Displaying account buttons")
            staffPos = allStaff.index(selectedStaff)

            if sheet.cell(8,staffPos+1).value == "FALSE":
                adminButton = ttk.Button(adminBox,text="Make Admin",style="MediumButton.TButton",command=lambda:makeAdmin(userPos,mainBox,page,usernames,selectedUsers,adminBox,value.get()))
                adminButton.place(x=210,y=70,height=28,width=130)
            else:
                adminButton = ttk.Button(adminBox,text="Remove Admin",style="MediumButton.TButton",command=lambda:removeAdmin(userPos,mainBox,page,usernames,selectedUsers,adminBox,value.get()))
                adminButton.place(x=210,y=70,height=28,width=130)

            editButton = ttk.Button(adminBox,text="Edit Login",style="MediumButton.TButton",command=lambda:editUser(userPos,mainBox,page,usernames,selectedUsers,adminBox,value.get()))
            editButton.place(x=345,y=70,height=28,width=130)

            deleteButton = ttk.Button(adminBox,text="Delete",style="DeleteButton.TButton",command=lambda:deleteUser(userPos,mainBox,page,usernames,selectedUsers,adminBox,value.get()))
            deleteButton.place(x=210,y=105,height=28,width=130)


        addLabel = ttk.Label(adminBox,text="Add Account",style="label.TLabel")
        addLabel.place(x=5,y=125)

        usernameLabel = ttk.Label(adminBox, text="Username:",style="label2.TLabel")
        usernameLabel.place(x=5, y=165)

        usernameEntry = ttk.Entry(adminBox,style="Custom.TEntry",font=("Helvetica", 12))
        usernameEntry.place(height=24,width=180,x=110, y=165)

        passwordLabel = ttk.Label(adminBox, text="Password:",style="label2.TLabel")
        passwordLabel.place(x=5, y=195)

        passwordEntry = ttk.Entry(adminBox,show="*",style="Custom.TEntry",font=("Helvetica", 12))
        passwordEntry.place(height=24,width=180,x=110, y=195)

        submitButton = ttk.Button(adminBox,text="Submit",style="MediumButton.TButton",command=lambda:addAccount(userPos,mainBox,page,usernames,selectedUsers,adminBox,usernameEntry.get(),passwordEntry.get(),allStaff))
        submitButton.place(x=5,y=234,height=28,width=285)

    else:
        if admin == True:
            hoursButton = ttk.Button(adminBox,text="Hours",style="tabFlat.TButton",command=lambda:hoursPage(userPos,page,adminBox,mainBox,usernames,selectedUsers))
            hoursButton.place(height=29,width=159,x=1,y=1)

            accountButton = ttk.Button(adminBox,text="Accounts",style="tabFlat.TButton",command=lambda:accountPage(userPos,page,adminBox,mainBox,usernames,selectedUsers))
            accountButton.place(height=29,width=160,x=160,y=1)

            developmentButton = ttk.Button(adminBox,text="Development",style="tabSunken.TButton",command=lambda:developmentPage(userPos,page,adminBox,mainBox,usernames,selectedUsers))
            developmentButton.place(height=29,width=159,x=320,y=1)
            developmentButton.state(["disabled"])
        else:
            developmentButton = ttk.Button(adminBox,text="Development",style="tabSunken.TButton",command=lambda:developmentPage(userPos,page,adminBox,mainBox,usernames,selectedUsers))
            developmentButton.place(height=29,width=478,x=1,y=1)
            developmentButton.state(["disabled"])
        lineNum("Displaying development page")

        value = tk.StringVar(adminBox)
        value.set("Report Bug")

        options = ["Report Bug","Suggest Feature"]

        staffSelect = ttk.OptionMenu(adminBox, value, selectedOption,*options,command=lambda event, val=value :developmentSelection(userPos,mainBox,page,usernames,selectedUsers,adminBox,selectedStaff,value.get()))
        staffSelect["menu"].config(background="white",font=('Helvetica', 12))
        staffSelect.place(x=120,y=35,width=240,height=40)

        if selectedOption == "Report Bug":
            bugLabel = ttk.Label(adminBox, text="Explain the bug:",style="label2.TLabel")
            bugLabel.place(x=24, y=80)

            submitButton = ttk.Button(adminBox,text="Submit",style="LoginButton.TButton",command=lambda:submitBug(userPos,mainBox,page,usernames,selectedUsers,adminBox,selectedStaff,selectedOption,developInput.get("1.0", tk.END)))
            submitButton.place(height=48,width=110,y=214,x=185)
        else:
            featureLabel = ttk.Label(adminBox, text="Explain the feature:",style="label2.TLabel")
            featureLabel.place(x=24, y=80)

            submitButton = ttk.Button(adminBox,text="Submit",style="LoginButton.TButton",command=lambda:submitSuggest(userPos,mainBox,page,usernames,selectedUsers,adminBox,selectedStaff,selectedOption,developInput.get("1.0", tk.END)))
            submitButton.place(height=48,width=110,y=214,x=185)

        developInput = tk.Text(adminBox,font=("Helvetica",12),relief="solid")
        developInput.place(width=432,height=98,x=24,y=110)


    settingsButton = ttk.Button(adminBox,style="setting.TButton",compound="center",command=lambda:mainPageBack(userPos,adminBox))
    settingsButton.place(width=48,height=48,relx=0.9,rely=.85,anchor="center")
    return

def mainPage(userPos):
    lineNum("Main Page")
    lineNum("Getting current time and current day")
    x = tm.datetime.now()
    currentDay = x.strftime("%a")
    allValues = sheet.get_all_values()
    username = allValues[0][userPos]

    lineNum("Resizing the window")
    root.minsize(484, 284)
    root.geometry("600x400")

    mainBox = ttk.Label(root,style="blueBox.TLabel")
    mainBox.place(height=280,width=480,relx=0.5,rely=0.5,anchor="center")

    welcomeLabel = ttk.Label(mainBox,text=f"Hello {username}!",style="label.TLabel")
    welcomeLabel.place(x=20,y=20)

    currentLabel = ttk.Label(mainBox,text=f"You are currently ",style="label.TLabel")
    currentLabel.place(x=20,y=55)

    lineNum("Checking if user is current clocked in")
    if allValues[2][userPos] == "FALSE":
        lineNum("User is clocked out, displayed relevant info")
        clockOutLabel = ttk.Label(mainBox,text="Clocked Out",style="label.TLabel",foreground="Red")
        clockOutLabel.place(x=223,y=55)

        clockInButton = ttk.Button(mainBox,text="Clock In",style='clockIn.TButton',command=lambda:clockIn(userPos,mainBox))
        clockInButton.place(height=48,relx=0.5,rely=0.6,anchor="center")
    else:
        lineNum("User is clocked in, displayed relevant info")
        clockInLabel = ttk.Label(mainBox,text="Clocked In",style="label.TLabel",foreground="Lime")
        clockInLabel.place(x=223,y=55)
        
        lineNum("Getting the clocked time")
        x = tm.datetime.now()
        currentTime = (x.strftime("%X"))
        currentTime = tm.datetime.strptime(currentTime,"%X")
        lastClockedTime = allValues[3][userPos]
        lastClockedTime = tm.datetime.strptime(lastClockedTime,"%X")
        clockedTime = allValues[8][userPos]
        clockedTime = tm.datetime.strptime(clockedTime,"%X")

        timeDiff = currentTime - lastClockedTime + clockedTime
        timeDiff = timeDiff.strftime("%X")
        lineNum(f"Clocked time is {timeDiff}")

        clockTime = ttk.Label(mainBox,text=f"Clocked Time: {timeDiff}",style="label.TLabel")
        clockTime.place(x=20,y=90)

        clockOutButton = ttk.Button(mainBox,text="Clock Out",style='clockOut.TButton',command=lambda:clockOut(userPos,mainBox))
        clockOutButton.place(height=48,relx=0.5,rely=0.6,anchor="center")

    logoutButton = ttk.Button(mainBox,text="Logout",style="LoginButton.TButton",command=lambda:logout(mainBox))
    logoutButton.place(height=48,relx=0.5,rely=0.85,anchor="center")

    lineNum("Getting the usernames from allValues and removing any EMPTY")
    usernames = allValues[0]
    usernames = [item for item in usernames if item != "EMPTY"]
    usernames.pop(0)
    page = "hours"
    selectedUsers = []

    settingsButton = ttk.Button(mainBox,style="setting.TButton",compound="center",command=lambda:settingsPage(userPos,mainBox,page,usernames,selectedUsers))
    settingsButton.place(width=48,height=48,relx=0.9,rely=.85,anchor="center")

    lineNum("Checking that if the user is clocked in, it was from a different day")
    if allValues[2][userPos] == "TRUE" and allValues[4][userPos][0:3] != currentDay:
        lineNum("TRUE, running noClockOut function")
        noClockOut(userPos,allValues,allValues[4][userPos],mainBox)
    return

###################### MAIN ######################
lineNum(f"Running TKinter")
root = tk.Tk()
root['bg'] = "#f27420"
width = 600
height = 350
root.minsize(464, 214)
root.geometry("600x350")
root.title("Clock In")
x_cordinate = int((root.winfo_screenwidth() / 2) - width/2)
y_cordinate = int((root.winfo_screenheight() / 2) - height/2)
root.geometry("+{}+{}".format(x_cordinate, y_cordinate-20))

lineNum(f"Loading Styles")
CheckVar = tk.IntVar(value=0)
settingsIcon = tk.PhotoImage(file="setting_icon.png")
style = ttk.Style()
style.theme_use('default')
style.configure("blueBox.TLabel", relief="solid", background="#113f8c")
style.configure("label.TLabel", background="#113f8c", foreground="white", font=("Helvetica", 18, "bold"))
style.configure("label2.TLabel", background="#113f8c", foreground="white", font=("Helvetica", 14, "bold"))
style.configure("label3.TLabel", background="#113f8c", foreground="white", font=("Helvetica", 12))
style.configure("Custom.TEntry", background="#113f8c")
style.map("SmallButton.TButton",
    background=[('pressed', '#cce4f7'), ('active', '#e0eef9'), ('!active', '#FFFFFF')],
    relief=[('pressed', 'flat'), ('active', 'flat'),('!active','flat')],)
style.configure("SmallButton.TButton", foreground="black", font=("Helvetica", 10,"bold"),padding=(0, -1, 0, 0))
style.map("MediumButton.TButton",
    background=[('pressed', '#cce4f7'), ('active', '#e0eef9'), ('!active', '#FFFFFF')],
    relief=[('pressed', 'flat'), ('active', 'flat'),('!active','flat')],)
style.configure("MediumButton.TButton", foreground="black", font=("Helvetica", 12, "bold"))
style.map("DeleteButton.TButton",
    background=[('pressed', '#c46a64'), ('active', '#f29a94'), ('!active', '#f5877f')],
    relief=[('pressed', 'flat'), ('active', 'flat'),('!active','flat')],)
style.configure("DeleteButton.TButton", foreground="black", font=("Helvetica", 12, "bold"))
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
style.configure('TMenubutton',font=("Helvetica", 14, "bold"),background="white")
style.map("addBtn.TButton",
    background=[('pressed', '#cce4f7'), ('active', '#e0eef9'), ('!active', '#FFFFFF')],
    relief=[('pressed', 'flat'), ('active', 'flat'),('!active','flat')],)
style.configure('addBtn.TButton', background="white",font=("Helvetica", 32, "bold"),padding=(0, -7, 0, 0))
style.map("removeBtn.TButton",
    background=[('pressed', '#cce4f7'), ('active', '#e0eef9'), ('!active', '#FFFFFF')],
    relief=[('pressed', 'flat'), ('active', 'flat'),('!active','flat')],)
style.configure('removeBtn.TButton', background="white",font=("Helvetica", 32, "bold"),padding=(0, -10, 0, 0))
style.configure('TCombobox',background="#e0eef9",arrowsize=15, relief="flat", font=('Helvetica', 14))
style.configure('TScrollbar', background = "white",troughcolor ="white")

lineNum("Running dayCheck function")
dayCheck()

lineNum("Opening 'options.txt' file")
f = open("options.txt", "r")
optionData = f.readlines()
f.close()
lineNum(f"Stored info: {optionData}")

autoLogin = optionData[0].rstrip().split(" ")
lineNum(f"Getting line 1: {autoLogin}")

lineNum(f"Check if autoLogin is True")
if autoLogin[0] == "True":
    lineNum("autoLogin is True, going straight to mainPage")
    mainPage(int(autoLogin[1]))

else:
    lineNum("autoLogin is False, running loginPage")
    loginPage()

root.mainloop()
