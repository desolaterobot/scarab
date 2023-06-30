import sys
import datetime
import os
from cryptography.fernet import Fernet

globalKey = "PjUYNENTBSGja15yQdPSzwNls-PKBWPRBrHDyxCdsFY="

###########################################################################

def deleteNote(index):
    dat = getData()
    del dat['notes'][index]
    setData(dat)

def getData():
    return eval(Fernet(globalKey).decrypt(open(os.getcwd() + "/" + "scarabData", "rb").read()).decode())

def setData(data):
    open(os.getcwd() + "/" + "scarabData", "wb").write(Fernet(globalKey).encrypt(str(data).encode()))

def addNote(title, body, tags):
    note = {
        "title" : title,
        "body" : body,
        "tags" : tags,
        "datetime" : datetime.datetime.now(),
    }
    dat = getData()
    dat["notes"].append(note)
    setData(dat)

def encrypt(key, data):
    return Fernet(key).encrypt(data)

def decrypt(key, data):
    return Fernet(key).decrypt(data)

def showNotes():
    dat = getData()
    i = 1
    if dat['notes'] == []:
        print("No notes saved.")
        return
    print("----------------ALL-NOTES------------------\n")
    for note in dat["notes"]:
        print(f"{i}. {note['title']}")
        print(note['datetime'])
        print(note['body'])
        print(f"TAGS: {note['tags']}")
        print()
        i+=1
    print("----------------ALL-NOTES------------------")

###########################################################################

# current directory
currentdir = os.getcwd()
# list of the current directory
listdir = os.listdir(currentdir)
# list of arguments
args = sys.argv[1:]
# empty starter data dictionary
empty = {
    "passcode" : None,
    "username" : None,
    "password" : None,
    "notes" : []
}
# if no data file, create one.
if 'scarabData' not in listdir:
    byt = str(empty)
    open(os.getcwd() + "/" + "scarabData", "wb").write(Fernet(globalKey).encrypt(byt.encode()))

###########################################################################

givenPass = getData()['passcode']
if givenPass != None:
    while True:
        enteredPass = input('Enter passcode: ')
        if enteredPass == givenPass:
            break
        print('Wrong password.')
        sys.exit()

if len(args) == 0:
    showNotes()
else:
    firstArg = args[0]
    if firstArg == "add":
        print("Adding a note. Enter the title of this note.")
        name = input(">> ")
        print("Enter the contents of this note.")
        body = input(">> ")
        print("Enter note tags, seperated by spaces.")
        tags = input(">> ").split(sep=" ")
        addNote(name, body, tags)
    elif firstArg == "remove":
        print("Removing a note. Enter the note index you wish to remove.")
        ind = None
        while True:
            ind = input(">> ")
            try:
                int(ind)
            except:
                print("That was not an integer.")
                continue
            ind = int(ind)
            if ind > len(getData()['notes']):
                print("Index is out of range.")
                continue
            break
        deleteNote(ind+1)
    elif firstArg == 'wipe':
        print('Are you sure you want to clear all your notes? (y/n)')
        ans = input('>> ')
        while True:
            if ans == 'y' or ans == 'Y':
                dat = getData()
                dat['notes'] = []
                setData(dat)
                break
            elif ans == 'n' or ans == 'N':
                break
    elif firstArg == 'lock':
        passs = input('Enter your choice of passcode: ')
        dat = getData()
        dat['passcode'] = passs
        setData(dat)
        print(f'Using Scarab now requires a passcode: {passs}')