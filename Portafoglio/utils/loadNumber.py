from utils.display import display
from utils.getdatas import getdatas
from colors import bcolors

def loadNumber():
    total = getdatas()
    if (int(total) > 0):
        print(bcolors.OKGREEN + str(total))
        display(str(total))
    else:
        print(bcolors.FAIL + str(total))
        display(str(total))