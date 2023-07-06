import sys
import datetime
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64

globalDir = os.path.expanduser("~")+"/AppData/Local/Scarab"
globalKey = 'T6B-cbd3e3w1K6Yc2CW9GEk7Iry7L079GGsU9c92-34=' #default key, if no password given.

def generateKey(seed):
    seed_bytes = str(seed).encode()  # Convert seed to bytes
    kdf = PBKDF2HMAC(
        algorithm = hashes.SHA256(),
        length = 32,
        salt = b"mmm... salty",
        iterations=5,
    )
    return base64.urlsafe_b64encode(kdf.derive(seed_bytes))

def getData()->dict:
    return eval(Fernet(globalKey).decrypt(open(globalDir + "/" + "scarabData", "rb").read()).decode())

def setData(data: dict):
    open(globalDir + "/" + "scarabData", "wb").write(Fernet(globalKey).encrypt(str(data).encode()))

def reEncrypt(oldKey, newKey):
    dat = eval(Fernet(oldKey).decrypt(open(globalDir + "/" + "scarabData", "rb").read()).decode())
    open(globalDir + "/" + "scarabData", "wb").write(Fernet(newKey).encrypt(str(dat).encode()))

def showNotes():
    dat = getData()
    i = 1
    if dat['notes'] == []:
        print("No notes saved.\n")
        return
    print("----------------ALL-NOTES------------------\n")
    for note in dat["notes"]:
        print(f"{i}. {note['title']}")
        print(note['datetime'])
        print(note['body'])
        print(f"TAGS: {note['tags']}")
        print()
        i+=1
    print("----------------ALL-NOTES------------------\n")

###########################################################################

def addProcedure():
    print("Adding a note. Enter the title of this note.")
    name = input(">> ")
    print("Enter the contents of this note.")
    body = input(">> ")
    print("Enter note tags, seperated by spaces.")
    tags = input(">> ").split(sep=" ")
    note = {
        "title" : name,
        "body" : body,
        "tags" : tags,
        "datetime" : datetime.datetime.now(),
    }
    dat = getData()
    dat["notes"].append(note)
    setData(dat)
    print("Note added.\n")

def removeProcedure():
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
    dat = getData()
    title = dat['notes'][ind-1]['title']
    del dat['notes'][ind-1]
    setData(dat)
    print(f'Deleted note with title: {title}\n')

def wipeProcedure():
    print('Are you sure you want to clear all your notes? (Y/N)')
    ans = input('>> ')
    while True:
        if ans == 'y' or ans == 'Y':
            dat = getData()
            dat['notes'] = []
            setData(dat)
            break
        elif ans == 'n' or ans == 'N':
            return
    print('Data wiped.\n')

def helpProcedure():
    print("----------------COMMAND-LIST------------------")
    print('show - show all notes')
    print('add - add a note')
    print('remove - remove a note')
    print('wipe - delete all notes')
    #print('lock - lock this program with a passcode')
    #print('uninstall - delete this whole program, along with stored data.')
    print('e - exit')
    print("----------------COMMAND-LIST------------------\n")
    
def uninstallProcedure():
    print("You will uninstall all of Scarab, along with all saved notes.")
    print("Continue? (Y/N)")
    inp = input(">> ")
    if inp == 'y' or inp == 'Y':
        for file in os.listdir(globalDir):
            os.remove(globalDir + "/" + file)
        os.rmdir(globalDir)
        os.remove(os.getcwd() + "/scrb.exe")
        os.remove(os.getcwd() + "/scrb.py")
        sys.exit()
    else:
        return

def lockProcedure():
    global globalKey
    global globalDir
    passw = input("Enter a password to lock your notes: ")
    newKey = generateKey(passw)
    reEncrypt(globalKey, newKey)
    globalKey = newKey
    open(globalDir + "/" + "scarabStatus", "w").write("Y")
    print(f'Data successfully locked with password {passw}\n')

def unlockProcedure():
    global globalKey
    global globalDir
    print('Your notes will no longer by password-protected.')
    print('Are you sure you want to continue? (Y/N)')
    ans = input('>> ')
    while True:
        if ans == 'y' or ans == 'Y':
            newKey = 'T6B-cbd3e3w1K6Yc2CW9GEk7Iry7L079GGsU9c92-34='
            reEncrypt(globalKey, newKey)
            open(globalDir + "/" + "scarabStatus", "w").write("N")
            print("Notes successfully unlocked.")
            return
        else:
            return

###########################################################################

#first time setup, create the directory and all the things in it, if havent.
try:
    os.mkdir(globalDir)
    password = input("First time setup.")
    empty = {
        "notes" : []
    }
    emptyStr = str(empty)
    open(globalDir + "/" + "scarabData", "wb").write(Fernet(globalKey).encrypt(emptyStr.encode())) #creation of data file
    open(globalDir + "/" + "scarabStatus", "w").write("N") #creation of status file, indicates if notebook is password protected.
except:
    pass

#is notes password protected? if so, get the password first.

isPassProtected = open(globalDir+"/"+"scarabStatus", "r").read() == "Y"
if isPassProtected:
    while True:
        #get password from user.
        passw = input("Enter password: ")
        globalKey = generateKey('passw')
        #verify if password is correct.
        try:
            if type(getData()['notes'] == list):
                print('Login successful.')
                break
            else:
                print('Login unsuccessful. Try again.')
        except:
            print('Login unsuccessful. Try again.')

#password protection cleared.

###########################################################################

args = sys.argv[1:]
noArgs = (len(args) == 0)
if noArgs:
    print(
        """
███████╗ ██████╗ █████╗ ██████╗  █████╗ ██████╗ 
██╔════╝██╔════╝██╔══██╗██╔══██╗██╔══██╗██╔══██╗
███████╗██║     ███████║██████╔╝███████║██████╔╝
╚════██║██║     ██╔══██║██╔══██╗██╔══██║██╔══██╗
███████║╚██████╗██║  ██║██║  ██║██║  ██║██████╔╝
╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝  v1.0
Terminal based notetaking - by Dimas Rizky
https://github.com/desolaterobot/scarab
Type 'help' to show the list of commands.
        """
    )
    showNotes()
    
while True:
    noArgs = (len(args) == 0)
    inp = None
    if noArgs:
        inp = input(">> ")
        print()
    else:
        inp = args[0]

    if inp == "add":
        addProcedure()
    elif inp == "remove":
        removeProcedure()
    elif inp == "help":
        helpProcedure()
    elif inp == 'wipe':
        wipeProcedure()
    elif inp == 'e':
        sys.exit()
    elif inp == 'show':
        showNotes()
    elif inp == 'lock':
        lockProcedure()
    else:
        print('Unknown command. \n')
    if noArgs:
        continue
    else:
        sys.exit()