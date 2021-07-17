from utils.display import display
from utils.getdatas import getdatas

def loadNumber():
    total = getdatas()
    if (int(total) > 0):
        print(str(total))
        display(str(total))
    else:
        print(str(total))
        display(str(total))