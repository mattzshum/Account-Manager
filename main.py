import json
from tkinter import *
import os
import time
import csv

os.chdir(r'C:\Users\matthew.shum\Documents\GitHub\Account-Manager')

#--LIST-FUNCTIONS-----------------------------------------------------------------------------
"""
def getCheck() ------- retrieves check amount entered by user
def close_login() ---- retrieves user first and last name and then stores them in local variables
def close_window() --- closes the main window (main)
def getUserInfo() ---- retrieves user info and stores into global vars
def depositCheck() --- prompts user for check 
"""
def close_login():
    global user_first
    global user_last

    user_first = first_name_entry.get()
    user_last = last_name_entry.get()
    login.destroy()

def close_window():
    main.destroy()

def getUserInfo(user):
    global user_first
    global user_last
    global balance
    global debt
    global savings
    global wants
    global needs

    global transaction_log

    print('retrieving user info')

    data2 = json.load(user)
    user_first = data2['user_info'][0]['user_first']
    print(user_first)
    user_last = data2['user_info'][0]['user_last']
    print(user_last)
    balance = data2['account_info'][0]['balance']
    print(balance)
    debt = data2['account_info'][0]['debt']
    print(debt)
    needs = data2['division_of_check'][0]['needs']
    print(needs)
    wants = data2['division_of_check'][0]['wants']
    print(wants)
    savings = data2['division_of_check'][0]['savings']
    print(savings)

    transaction_log = data2['transaction_log'][0]


    data['user_info'][0]['user_first'] = user_first
    data['user_info'][0]['user_last'] = user_last
    data['account_info'][0]['balance'] = balance
    data['account_info'][0]['debt'] = debt
    data['division_of_check'][0]['needs'] = needs
    data['division_of_check'][0]['wants'] = wants
    data['division_of_check'][0]['savings'] = savings
    data['transaction_log'][0] = transaction_log

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
    savings = .2 * float(check_amount)
    needs = .6 * float(check_amount)
    wants = .2 * float(check_amount)
    data['account_info'][0]['balance'] = balance

    data['division_of_check'][0]['savings'] += savings
    data['division_of_check'][0]['needs'] += needs
    data['division_of_check'][0]['wants'] += wants
    #updateUserInfo()

def getDebt():
    global debt
    global debt_retrieval

    debt_retrieval = debt_amount_entry.get()
    debt -= float(debt_retrieval)
    item_purchased = debt_item_entry.get()
    data['account_info'][0]['debt'] = debt
    print(debt_retrieval, item_purchased)

    #load this into the transaction log as a transaction item_purchased:debt
    if item_purchased in transaction_log:
        transaction_log[item_purchased + 'r'] = debt_retrieval
    else:
        transaction_log[item_purchased] = debt_retrieval
    data['transaction_log'][0] = transaction_log
    #updateUserInfo()




#---VARIABLES--------------------------------------------------------------------------------
all_users = []#----------instantiated in LOAD ALL USERS
user_first = "John"#-----instantiated in login
user_last = "Doe"#-------instantiated in login
balance = 0.0#-----------instantiated in def getUserInfo
debt = 0.0#--------------instantiated in def getUserInfo
file_name_combo = ''#----instantiated in CREATE USER FILE
user_file = ''#----------instantiated in CREATE USER FILE as a combination of file_name_combo + '.txt'
check_amount = 0#--------instantiated in depositCheck()
time_string = time.strftime('%H:%M:%S')# import datetime
deposit_check = False#---instantiated in MAIN LOOP
debt_retrieval = 0.0#----instantiated in getDebt()
needs = 0.0#-------------instantiated in getUserInfo and updateUserInfo
wants = 0.0#-------------instantiated in getUserInfo and updateUserInfo
savings=0.0#-------------instantiated in getUserInfo and updateUserInfo
compressed_transaction_log=''#---instantiated in main_loop

transaction_log={}

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
data['division_of_check'] = []
data['division_of_check'].append({
        'needs': 60,
        'wants': 20,
        'savings': 20
})
data['transaction_log'] = []
data['transaction_log'].append({
        'item_purchased': 'the cost of the item'
})

#-LOAD ALL USERS-----------------------------------------------------------------------------
#utilize all_users to login. Need to deal with runtime later. NOTE::use dictionary instead of arr
with open('users.csv','r') as f:
    z = csv.reader(f, delimiter=',')
    for row in f:
            all_users.append(str(row).replace(',','').replace('\n',''))

#--LOGIN LOOP--------------------------------------------------------------------------------
#takes in users first namd and last name. Uses this as login. We can deal with pswd later
login = Tk()
login.title('-----Sign In-----')

Label(login,text='Welcome to the BETA for account_manager.\nPlease log in using your first and last names').grid(row=0)
Label(login,text='First Name').grid(row=1)
Label(login,text='Last Name').grid(row=2)
first_name_entry = Entry(login)
last_name_entry = Entry(login)
first_name_entry.grid(row=1,column=1)
last_name_entry.grid(row=2,column=1)
Label(login, text=time_string).grid(row=0,column=10)

login_button = Button(login, text='Login', command=close_login, fg='red').grid(row=5,column=0)

login.mainloop()
#--CREATE USER FILE IF DNE, OR PULL UP EXISTING FILE------------------------------------------
#if the user is a new one create a new 'account for them' and add to the user file
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
#This is where all the transaction occurs. Need to find a way to destroy main loop and reinstantiate
#--it when some data is updated. Like real time changing balance from 0 -> 4
main = Tk()
main.title('ACCOUNT INFO')

#...TEXT ON PAGE...
Label(main, text=('Welcome back ' + user_first + ' ' + user_last + '!')).grid(row=0, column=0)
Label(main, text=('Your account is as following:')).grid(row=1,column=0)
Label(main, text=('Balance: ' + str(round(balance,2))) ).grid(row=2,column=0)
Label(main, text=('Debt: ' + str(round(debt,2))) ).grid(row=3,column=0)
Label(main, text=('Running Total: ' + str(round((balance+debt),2))) ).grid(row=4, column=0)
Label(main, text=time_string).grid(row=0,column=10)

print(savings, needs, wants)
Label(main, text='Savings [recommended]: ' + str(round(savings,2))).grid(row=2, column=4)
Label(main, text='Needs [recommended]: ' + str(round(needs,2))).grid(row=3, column=4)
Label(main, text='Wants [recommended]: ' + str(round(wants,2))).grid(row=4, column=4)

for key, element in transaction_log.items():
    print(key, element)
    compressed_transaction_log += (key + ' ----------------------------------> ' + element + '\n')
Label(main, text=compressed_transaction_log).grid(row=15)

#..Deposit Check Button...
Label(main, text='Enter the amount you are depositing').grid(row=6, column=0)
check_amount_entry = Entry(main)
check_amount_entry.grid(row=6, column=1)
deposit_button = Button(main,\
                        text='Deposit',\
                        command=getCheck).grid(row=6,column=2)

#..Input any "debt Costs".....
Label(main, text='Enter the purchases [cost],[item]').grid(row=7,column=0)
debt_amount_entry = Entry(main)
debt_amount_entry.grid(row=7, column=1)
debt_item_entry = Entry(main)
debt_item_entry.grid(row=7, column=3)
debt_button = Button(main,\
                     text='Debt Entry',\
                     command=getDebt).grid(row=7, column=2)
                     
#..Log out and exit program button.....
logout_button = Button(main,\
                       text='Logout',\
                       command=close_window,\
                       fg='red').grid(row=10,column=0)
main.mainloop()
updateUserInfo()

# file1.close()