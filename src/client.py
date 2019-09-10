import sys
import os

def addPythonPaths():
    print(f"Current Working Dir : {os.getcwd()}")
    for i, j, y in os.walk(os.getcwd()):
        if (str(i).find('__pycache__') == -1 and str(i).find('.vscode') == -1):
            sys.path.append(i)
            print(f"Added {i} to python path")

    sys.path.append('../Logging')
    print(f'Final PYTHONPATH :: {sys.path}')

addPythonPaths()

from Networking import netTest
from Networking import main as netMain

netTest.tester()

