import json
from tkinter import *
import os
import time

os.chdir(r'C:\Users\matthew.shum\Documents\GitHub\Account-Manager')

#--LIST-FUNCTIONS-------------------------------------------------
"""
def close_window(root) -- takes in tkinter obj and closes window via destruction
def getUserInfo() -- retrieves user info and stores into global vars
def depositCheck() -- prompts user for check 
"""
def close_window():
    main.destroy()

def getUserInfo():
    global user_first
    global user_last
    global balance
    global debt
    with open('info.txt','r') as json_file:
        data = json.load(json_file)
        user_first = data['user_info']['first_name']
        user_last = data['user_info']['last_name']
        balance = data['account_info']['balance']
        debt = data['account_info']['debt']



#---VARIABLES-------------------------------------------
user_first = "John"
user_last = "Doe"
welcome = 'Welcome back ' + user_first + ' ' + user_last + '! \n Your account is as following:'
balance = 0
debt = 0
time_string = time.strftime('%H:%M:%S')


#--Main Loop tKinter------------------------------------------------
main = Tk()
main.title('ACCOUNT INFO')

getUserInfo()

Label(main, text=('Welcome back ' + user_first + ' ' + user_last + '!')).grid(row=0, column=0)
Label(main, text=('Your account is as following:')).grid(row=1,column=0)
Label(main, text=('Balance: ' + str(balance))).grid(row=2,column=0)
Label(main, text=('Debt: ' + str(debt))).grid(row=3,column=0)
Label(main, text=time_string).grid(row=0,column=5)

logout_button = Button(main, text='Logout', command=close_window, fg='red').grid(row=5,column=0)

main.mainloop()