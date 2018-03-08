#!/usr/bin/python3
import subprocess
import linecache
import os
def stripend(strip):
    mod = strip.replace('\n','')
    return mod
def ynchoice(user_input):
    while ((user_input is 'y' == False) or (user_input is 'n' == False)):
        print("The character you entered could not be recognized!")
        user_input = input("Please try again! (y/n) ")
def setpath(old_path, new_path):
    print("You may choose a work directory where the list of your devices can be found.")
    print("The work directory is also the place where the backup process files will be stored.")
    print("If you haven't done this already - name your list 'pclist', or else the program WON'T recognize it!")
    yn = input("Would you like to set a new work directory? (y/n) ")
    ynchoice(yn)
    if (yn == 'y'):
        print("Remember: as of right now this only works with '/' paths!")
        new_path = input("Define the path: ")
        while ((os.path.exists(new_path + "pclist") == False)):
            if ((new_path[-1:] != '/')):
                print("The path was not set correctly!")
                print("Did you put a '/' at the end? Or missed a space from the end?")
                new_path = input("Define the path again: ")
                continue
            else:
                print("New path exists!")
                print("The 'pclist' file was not found!")
                newlist = input ("Would you like to copy the current 'pclist' to the new path? (y/n) ")
                ynchoice(newlist)
                if (newlist is 'y'):
                    while (os.path.exists(new_path) == False):
                        print("The new path could not be found! Please try again!")
                        new_path = input ("Define an existing path: ")
                    cmd = "cp pclist "+new_path+"pclist"
                    subprocess.call(cmd, shell=True)
                    print("Success! 'pclist' copy completed!")
                else:
                    new_path = input("OK! Define the path again: ")
        if (old_path == new_path):
            print("The new path that was defined is the same as the current one!")
            print("No changes occured!")
        else:
            cmd = "echo $(date) >> old_paths"
            subprocess.call(cmd, shell=True)
            open("old_paths", 'a').write(old_path)
            open("path_file", 'w').write(new_path)
            print("The given path is compatible and the new path is set:" + new_path)
    else:
        print("The path remained the main folder of the program!")
    return new_path
def createlist(path):
    open(path+"queue", 'w').close()
    open(path+"finished", 'w').close()
    print("Define the devices with their position in the list file!")
    print("Press <ENTER> to finish the list!te")
    var = 0
    while (var is not None):
        with open(path+"queue", 'a') as w:
            w.write(linecache.getline(path+"pclist", var))
        try:
            var = int(input("Device that needs backup: "))
        except ValueError:
            var = None
    print("Backup list complete!")
def backup(path):
    crash = ''
    with open(path+"queue", 'r') as f:
        for i in f:
                open(path+"finished", 'a').write(i)
                with open(path+"queue", 'r') as get:
                    data = get.read().splitlines(True)
                with open(path + "queue", 'w') as rem:
                    rem.writelines(data[1:])
                if (crash is not 'x'):
                    crash = input("Would you like to interrupt the process now? (y/n) ")
                    ynchoice(crash)
                    if (crash == 'y'):
                        print("Backup process interrupted!")
                        return
                    else:
                        crash = input("Should the process finish without interruption? (y/n) ")
                        ynchoice(crash)
                        if (crash == 'y'):
                            crash = 'x'
                        else:
                            continue
                else:
                    continue
    open(path + "queue", 'w').close()
    print("Backup process successful!")
    return
def start(def_path):
    def_path = setpath(def_path, def_path)
    createlist(def_path)
    yn = input("Would you like to run the backup process? (y/n) ")
    ynchoice(yn)
    if (yn == 'y'):
        open(def_path + "finished", 'w').close()
        backup(def_path)
    else:
        print("Backup process denied!")
    return

print("Welcome to the early stage of this experimental backup sytem!")
if ((os.path.exists("backup_system.py")) == False):
    print("You are not in the program's main folder.")
    print("Please navigate to the folder where 'backup_system.py' is located!")
else:
    org_path = linecache.getline("path_file",1)
    org_path = stripend(org_path)
    if (os.path.exists(org_path+"queue")):
        if (os.stat(org_path+"queue").st_size != 0):
            yn = input("You have an unfinished backup process! Would you like to continue? (y/n) ")
            ynchoice(yn)
            if (yn == 'y'):
                backup(org_path)
            else:
                start(org_path)
        else:
            start(org_path)
    else:
        start(org_path)
