# PyAgent.py

import Action
import Orientation
import random

#  global arrow
global gold
global location
global direction  # 0-r, 1-u, 2-l, 3-d, same as in Orientation
global ActionSet


def PyAgent_Constructor():
    print("PyAgent_Constructor")


def PyAgent_Destructor():
    print("PyAgent_Destructor")


def PyAgent_Initialize():
    global arrow
    global location
    global gold
    global direction
    global ActionSet
    arrow = 1
    location = [1, 1]
    gold = 0
    direction = Orientation.RIGHT
    ActionSet = []
    print("PyAgent_Initialize")


def PyAgent_Process(stench, breeze, glitter, bump, scream):
    #  global arrow
    global gold
    global location
    global direction
    perceptStr = ""
    if location == [1, 1] and gold == 1:
        return Action.CLIMB
    if not ActionSet:
        return ActionSet.pop
    if (stench == 1):
        # Stench percept, if has an arrow, SHOOT
        perceptStr += "Stench=True,"
        # if arrow:
        #    arrow -= 1
        #    return Action.SHOOT
    else:
        perceptStr += "Stench=False,"
    if (breeze == 1):
        perceptStr += "Breeze=True,"
    else:
        perceptStr += "Breeze=False,"
    if (glitter == 1):
        # Glitter percept, GRAB
        perceptStr += "Glitter=True,"
        gold += 1
        return Action.GRAB
    else:
        perceptStr += "Glitter=False,"
    if (bump == 1):
        # Bump percept, randomly turn LEFT or RIGHT
        perceptStr += "Bump=True,"
        return ChangeDirection('bump')
    else:
        perceptStr += "Bump=False,"
    if (scream == 1):
        perceptStr += "Scream=True"
    else:
        perceptStr += "Scream=False"
    print("PyAgent_Process: " + perceptStr)
    return Action.GOFORWARD


def PyAgent_GameOver(score):
    print("PyAgent_GameOver: score = " + str(score))


def UpdateLocation():
    global direction
    global location
    if direction == Orientation.RIGHT:
        location[0] += 1
    elif direction == Orientation.DOWN:
        location[1] -= 1
    elif direction == Orientation.LEFT:
        location[0] -= 1
    elif direction == Orientation.UP:
        location[1] += 1


def ChangeDirection(state):
    global direction
    if state == 'bump':
        if random.randint(0, 1):  # If random get 1, turn left.
            direction += 1
            if direction > 3:
                direction = 0
            return Action.TURNLEFT
        else:  # Else, turn right
            direction -= 1
            if direction < 0:
                direction = 3
            return Action.TURNRIGHT
    if state == 'stench':  # If face with stench, turn back
        direction += 2
        if direction > 3:
            direction -= 2
        ActionSet.append(Action.TURNLEFT)
        return Action.TURNLEFT



