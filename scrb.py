import sys
import datetime
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64

def generateKey(seed):
    seed_bytes = str(seed).encode()  # Convert seed to bytes
    kdf = PBKDF2HMAC(
        algorithm = hashes.SHA256(),
        length = 32,
        salt = b"mmm... salty",
        iterations=5,
    )
    return base64.urlsafe_b64encode(kdf.derive(seed_bytes))

def getData():
    return eval(Fernet(globalKey).decrypt(open(globalDir + "/" + "scarabData", "rb").read()).decode())

def setData(data):
    open(globalDir + "/" + "scarabData", "wb").write(Fernet(globalKey).encrypt(str(data).encode()))

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
    print(f'Deleted note with title {title}\n')

def wipeProcedure():
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
    print("Continue? Y/N")
    inp = input(">> ")
    if inp == 'y' or inp == 'Y':
        for file in os.listdir(globalDir):
            os.remove(globalDir + "/" + file)
        os.rmdir(globalDir)
        os.remove(os.getcwd() + "/scrb.exe")
        os.remove(os.getcwd() + "/scrb.py")
        sys.exit()
    else:
        print()
        return

###########################################################################

globalDir = os.path.expanduser("~")+"/AppData/Local/Scarab"
globalKey = "PjUYNENTBSGja15yQdPSzwNls-PKBWPRBrHDyxCdsFY="

#first time setup, create the directory and all the things in it, if havent.
try:
    os.mkdir(globalDir)
    status = "N"
    empty = {
        "exists" : True,
        "notes" : []
    }
    emptyStr = str(empty)
    open(globalDir + "/" + "scarabData", "wb").write(Fernet(globalKey).encrypt(emptyStr.encode()))
    open(globalDir + "/" + "scarabStatus", "w").write(status)
except:
    pass
#check if password is required. get input and generate the key for now.
passRequired = (open(globalDir + "/" + "scarabStatus", "r").read() == "Y")
if passRequired:
    inp = input("Enter password: ")
    globalKey = generateKey(inp)

try:
    trying = getData()['exists']
except:
    print("Wrong password.")

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
    elif inp == 'lock':
        pass
        #lockProcedure()
    elif inp == 'e':
        sys.exit()
    elif inp == 'show':
        showNotes()
    else:
        print('Unknown command. \n')
    if noArgs:
        continue
    else:
        sys.exit()