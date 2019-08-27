import json
from tkinter import *
import os
import time
import csv

os.chdir(r'C:\Users\matthew.shum\Documents\GitHub\Account-Manager')

#--LIST-FUNCTIONS-----------------------------------------------------------------------------
"""
def getCheck() -- retrieves check amount entered by user
def close_login() -- retrieves user first and last name and then stores them in local variables
def close_window() -- closes the main window (main)
def getUserInfo() -- retrieves user info and stores into global vars
def depositCheck() -- prompts user for check 
"""
def close_login():
    global user_first
    global user_last

    user_first = first_name_entry.get()
    user_last = last_name_entry.get()
#     print(user_first,user_last,first_name_entry.get(),last_name_entry.get())
    login.destroy()

def close_window():
    main.destroy()

def getUserInfo(user):
    global user_first
    global user_last
    global balance
    global debt
    data = json.load(user)
    user_first = data['user_info'][0]['user_first']
    user_last = data['user_info'][0]['user_last']
    balance = data['account_info'][0]['balance']
    debt = data['account_info'][0]['debt']

def updateUserInfo():
    global data
    global user_file
    print('opening up and running test file')
    with open(user_file,'w') as outfile:
        json.dump(data,outfile)

def getCheck():
    global check_amount
    global balance
    check_amount = check_amount_entry.get()
    balance += float(check_amount)
    data['account_info'][0]['balance'] += balance
    updateUserInfo()
#     try:
#         data['account_info'][0]['balance'] += int(check_amount)
#         updateUserInfo()
#     except:
#         print("WTF")
#         print("error ")




#---VARIABLES--------------------------------------------------------------------------------
all_users = []#--------instantiated in LOAD ALL USERS
user_first = "John"#---instantiated in login
user_last = "Doe"#-----instantiated in login
balance = 0.0#-----------instantiated in def getUserInfo
debt = 0#--------------instantiated in def getUserInfo
file_name_combo = ''#--instantiated in CREATE USER FILE
user_file = ''#--------instantiated in CREATE USER FILE as a combination of file_name_combo + '.txt'
check_amount = 0#------instantiated in depositCheck()
time_string = time.strftime('%H:%M:%S')
deposit_check = False#--instantiated in MAIN LOOP

#--LOAD VARIABLES INTO CORRESPONDING DICTIONARIES--------------------------------------------
data = {}
data['user_info'] = []
data['user_info'].append({
        'user_first': user_first,
        'user_last': user_last
})
data['account_info'] = []
data['account_info'].append({
        'balance': balance,
        'debt': debt
})

#-LOAD ALL USERS-----------------------------------------------------------------------------
with open('users.csv','r') as f:
    z = csv.reader(f, delimiter=',')
    for row in f:
            all_users.append(str(row).replace(',','').replace('\n',''))

#--LOGIN LOOP--------------------------------------------------------------------------------
login = Tk()
login.title('-----Sign In-----')

Label(login,text='First Name').grid(row=0)
Label(login,text='Last Name').grid(row=1)
first_name_entry = Entry(login)
last_name_entry = Entry(login)
first_name_entry.grid(row=0,column=1)
last_name_entry.grid(row=1,column=1)
Label(login, text=time_string).grid(row=0,column=10)

login_button = Button(login, text='Login', command=close_login, fg='red').grid(row=5,column=0)

login.mainloop()
#--CREATE USER FILE IF DNE, OR PULL UP EXISTING FILE------------------------------------------
file_name_combo = user_first + "_" + user_last
user_file = "%s.txt" % file_name_combo
if file_name_combo in all_users:
    print("found existing user")
    with open(user_file,'r') as user:
        getUserInfo(user)
else:
    #create a new user
    print('Creating new user')
    with open(user_file,'w') as outfile:
        data['user_info'][0]['user_first'] = user_first
        data['user_info'][0]['user_last'] = user_last
        json.dump(data, outfile)
    with open('users.csv','a') as appender:
        appender = csv.writer(appender,lineterminator='\n')
        appender.writerow(file_name_combo)

#--MAIN LOOP----------------------------------------------------------------------------------
main = Tk()
main.title('ACCOUNT INFO')

#...TEXT ON PAGE...
Label(main, text=('Welcome back ' + user_first + ' ' + user_last + '!')).grid(row=0, column=0)
Label(main, text=('Your account is as following:')).grid(row=1,column=0)
Label(main, text=('Balance: ' + str(balance))).grid(row=2,column=0)
Label(main, text=('Debt: ' + str(debt))).grid(row=3,column=0)
Label(main, text=time_string).grid(row=0,column=10)

#...BUTTON ON PAGE...
Label(main, text='Enter the amount you are depositing').grid(row=6, column=0)
check_amount_entry = Entry(main)
check_amount_entry.grid(row=6, column=1)
deposit_button = Button(main, text='Deposit',command=getCheck).grid(row=6,column=2)

logout_button = Button(main, text='Logout', command=close_window, fg='red').grid(row=10,column=0)
main.mainloop()

# file1.close()