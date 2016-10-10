#!/usr/bin/python

# v1.0 by Arijit Basu

import os
import subprocess
import re
import sys

# Configure -----------------------

if os.name == "nt":
    editor = "notepad"  # if windows
else:
    editor = "vi"       # other than windows

notesDir = os.path.expanduser("~") + "/notes"

#----------------------------------

def hr(c):
    rows, columns = os.popen('stty size', 'r').read().split()
    for j in range(0, int(columns) / 2):
        print c,
    print


def clr():
    os.system('cls' if os.name == 'nt' else 'clear')

def center(line):
    rows, columns = os.popen('stty size', 'r').read().split()
    space = (int(columns) - len(line))/2
    for j in range(0, int(space) / 2):
        print " ",
    print line

def createNote(words):
    filename = re.sub("[^a-zA-Z0-9]","_",words)
    filepath = notesDir + "/" + filename

    clr()
    while os.path.exists(filepath):
        clr()
        print "Note \'" +re.sub("[^a-zA-Z0-9]", " ",filename) + "\' already exists !"
        newname = raw_input("Try another name: ")
        filename = re.sub("[^a-zA-Z0-9]","_",newname)
        filepath = notesDir + "/" + filename

    subprocess.call([editor, filepath])
    clr()

    if os.path.isfile(filepath):
        displayNote(filename)
    else:
        words = "search " + re.sub("[^a-zA-Z0-9]"," ",words)
        interact(words.split())


def displayNote(filename):
    filepath = notesDir + "/" + filename

    clr()
    center("* " + re.sub('[^a-zA-Z0-9]', ' ',filename) + " *")
    hr("*")
    print
    with open(filepath) as f:
        content = f.read()
        print str(content)
        f.close()
    hr("=")
    print "o) open in editor \t r) rename \t d) delete \t s) search again"
    hr("=")
    ans = raw_input("> ")

    if ans in ["o","O"]:
        clr()
        subprocess.call([editor, filepath])
        displayNote(filename)
    elif ans in ["r","R"]:
        clr()
        print "Note \'" + re.sub("[^a-zA-Z0-9]", "_", filename) + "\' already exists !"
        newname = re.sub('[^a-zA-Z0-9]', '_', str(raw_input("Enter new name \t: ")))
        while os.path.exists(notesDir+"/"+newname):
            clr()
            print "Note \'" + re.sub("[^a-zA-Z0-9]", "_",newname) + "\' already exists !"
            newname = raw_input("Try another name: ")
            newname = re.sub("[^a-zA-Z0-9]", "_", newname)

        os.rename(filepath, notesDir+"/"+newname)
        displayNote(newname)
    elif ans in ["d","D"]:
        clr()
        ans = raw_input("Delete file \'"+filepath+"\' [ y/N ] ? ")
        clr()
        if ans in ["y","Y"]:
            os.remove(filepath)
        if not os.path.isfile(filepath):
            print "Deleted file \'"+filepath+"\'"
        else:
            print "File not deleted"
    elif ans in ["s", "S"]:
        clr()
        words = "search "
        words = words + raw_input("Search for: ")
        clr()
        interact(words.split())

    return 0


def initDir():
    if not os.path.isdir(notesDir):
        if os.makedirs(notesDir):
            print "Created directory: " + notesDir
        else:
            print "Error: Could\'nt create directory: " + notesDir
            exit(1)
    return 0


def printHelp():
    print
    print "Usage:\t\t./note.py KEYWORDS [e.g. ./note.py patching rhel kernel]"
    print
    return 0


def search(args):
    print "Searching for \t: " + str(args)
    filenames = os.listdir(notesDir)
    searched = os.listdir(notesDir)

    for filename in filenames:
        for word in args:
            if word in filename.split("_"):
                continue
            else:
                filepath = notesDir + "/" + filename
                with open(filepath) as f:
                    content = f.read()
                    f.close()
                if word in content:
                    continue
                elif filename in searched:
                    searched.remove(str(filename))

    return searched


def interact(args):
    del args[0]

    words = " ".join(args)

    filenames = search(args)
    clr()
    i = 1
    opts = ["1"]
    if len(filenames) > 0:
        print str(len(filenames)) + " note(s) found"
        hr("-")
        print
        for filename in filenames:
            print " \t" + str(i) + ") " + re.sub("[^a-zA-Z0-9]"," ",filename)
            i = i+1
            opts.append(str(i))
        print

    hr("=")
    print "n) new note \t s) search again"
    hr("=")
    ans = raw_input("> ")

    if ans in opts:
        clr()
        displayNote(str(filenames[int(ans)-1]))
        exit(1)
    elif ans in ["n", "N"]:
        clr()
        createNote(words)
        exit(1)
    elif ans in ["s", "S"]:
        clr()
        words = "search "
        words = words + raw_input("Search for: ")
        clr()
        interact(words.split())
    else:
        exit(0)


# Call
interact(sys.argv)


