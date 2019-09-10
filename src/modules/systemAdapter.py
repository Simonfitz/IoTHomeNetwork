import csv
import os
import sys
import subprocess
import time
from subprocess import Popen
import zipfile
import constants

def readFile(filename):
    try:
        with open(filename, 'r') as file:
            data = file.read()
        print(data)
        return data
        print("Successfully read in file")
    except:
        print("ERROR: Could not read file")

def writeFile(filename, data):
    with open(filename, 'w') as file:
        if not data:
            file.close()
            print('file close()')
        # write data to a file
        file.write(data)

def runApplication(filename):
    print("Starting Application")
    subprocess.Popen(['bash', filename])
    print("terminating current process")
    sys.exit()
    print("Did not close")

def restartDevice():
    os.system("sudo /sbin/shutdown -r now")

def unzip(filename):
    print("Extracting " + filename)
    with zipfile.ZipFile(filename, "r") as zip_ref:
        zip_ref.extractall("../newestVersion")
    print("Successfully extracted " + filename)

def printOut(message):
    print(message)

def functionSelect(module, data):
    switcher = {
        'unzip': unzip,
        'restart': restartDevice,
        'run': runApplication,
        'writefile': writeFile,
        'readfile': readFile,
        'message' : printOut
    }
    # Get the function from switcher dictionary
    func = switcher.get(module, lambda: "Invalid")
    func(data)

def handlerSystem(commandDetails):
    print("Alarm Command:" + commandDetails)
    commandDetails = commandDetails.split(' ', 1)
    # make sure command is in correct format
    if len(commandDetails) == 2:
        module = commandDetails[0]
        data = commandDetails[1]
        functionSelect(module, data)

# unzip("../newestVersion.zip")
# runApplication("./../../run.sh")