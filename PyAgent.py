# PyAgent.py

import Action
import Orientation
import Random

global size
global location
global direction
global gold
global arrow

def PyAgent_Constructor ():
    print("PyAgent_Constructor")

def PyAgent_Destructor ():
    print("PyAgent_Destructor")

def PyAgent_Initialize ():
    global size
    global location
    global direction
    global gold
    global arrow
    location = [1,1]
    direction = Orientation.RIGHT
    gold = 0
    arrow = 1
    print("PyAgent_Initialize")
    
def PyAgent_Process (stench,breeze,glitter,bump,scream):
    global size
    global location
    global direction
    global gold
    global arrow
    perceptStr = ""
    if (stench == 1):
        perceptStr += "Stench=True,"
        if arrow == 1:
            arrow -=1
            return Action.SHOOT
    else:
        perceptStr += "Stench=False,"
    if (breeze == 1):
        perceptStr += "Breeze=True,"
    else:
        perceptStr += "Breeze=False,"
    if (glitter == 1):
        perceptStr += "Glitter=True,"
        gold += 1
        return Action.GRAB
    else:
        perceptStr += "Glitter=False,"
    if (bump == 1):
        perceptStr += "Bump=True,"
        if random.randint(0,1):
            direction += 1
                if direction > 3:
                    direction = 0
                else:
                    direction -= 1
                        if direction < 0:
                            direction = 2
    else:
        perceptStr += "Bump=False,"
    if (scream == 1):
        perceptStr += "Scream=True"
    else:
        perceptStr += "Scream=False"
    print("PyAgent_Process: " + perceptStr)
    if direction == 0:
        lacation[0] = min(location[0]+1,size)
    return Action.GOFORWARD

def PyAgent_GameOver (score):
    print("PyAgent_GameOver: score = " + str(score))
