# PyAgent.py

import Action
import Orientation
import random

#  global arrow
global gold
global location
global direction  # 0-r, 1-u, 2-l, 3-d, same as in Orientation
global size
global unsize

#  creat a new global variable to save the Action
#  since we can only return one action
global ActionSet

global PathSet  # Set for saving path
global Dangers  # Set for dangerous locations
global CheckDangers  # A state for whether need to check dangers
global safe


def PyAgent_Constructor():
    print("PyAgent_Constructor")


def PyAgent_Destructor():
    print("PyAgent_Destructor")


def PyAgent_Initialize():
    """
        Initial the state of agent
    """
    #  global arrow
    global location
    global gold
    global direction
    global ActionSet
    global PathSet
    global Dangers
    global CheckDangers
    global size
    global unsize
    global safe
    #  arrow = 1
    location = [1, 1]
    gold = 0
    direction = Orientation.RIGHT
    ActionSet = []
    PathSet = []
    Dangers = []
    CheckDangers = 0
    size = 10
    safe = 0
    unsize = 1
    print("PyAgent_Initialize")


def PyAgent_Process(stench, breeze, glitter, bump, scream):
    #  global arrow
    global gold
    global location
    global direction
    global ActionSet
    global Dangers
    global CheckDangers
    global size
    global safe
    global unsize
    print("location:", location)
    perceptStr = ""
    #  RecordPath(location)
    #  Test whether need to climb
    if (glitter == 1):
        # Glitter percept, GRAB
        perceptStr += "Glitter=True,"
        gold += 1
        TravelToInit()
        return Action.GRAB
    else:
        perceptStr += "Glitter=False,"
    if location == [1, 1] and gold == 1:
        return Action.CLIMB
    #  Try to do the remaining actions
    if ActionSet:
        actions = ActionSet.pop()
        if actions == Action.GOFORWARD:
            if Dangers:
                return testwumpus()
            else:
                return UpdateLocation(actions)
        elif actions == Action.SHOOT:
            safe = 1
            return Action.SHOOT
        else:
            return UpdateDirection(actions)
    #  If still in the process of checking wumpus.
    if gold:
        TravelToInit()
        return Action.GRAB
    if CheckDangers:
        if stench:
            ActionSet.append(Action.TURNLEFT)
            ActionSet.append(Action.GOFORWARD)
            ActionSet.append(Action.TURNRIGHT)
            ActionSet.append(Action.SHOOT)
            CheckDangers = 0
            return UpdateDirection(Action.TURNRIGHT)
        else:
            CheckDangers = 0
            ActionSet.append(Action.SHOOT)
            ActionSet.append(Action.TURNLEFT)
            ActionSet.append(Action.GOFORWARD)
            ActionSet.append(Action.TURNRIGHT)
            return UpdateDirection(Action.TURNRIGHT)
    #  Check whether the wumpus is on the next location.
    if (stench == 1):
        perceptStr += "Stench=True,"
        if safe:
            pass
        else:
            if Dangers:
                return testwumpus()
            else:
                if location[1] == 1 and bump != 1:
                    return WumpusLocation(location)
                else:
                    if location[0] == 1:
                        for i in range(direction-Orientation.RIGHT):
                            ActionSet.insert(0, Action.TURNLEFT)
                        ActionSet.insert(0, Action.GOFORWARD)
                        ActionSet.insert(0, Action.TURNLEFT)
                        ActionSet.insert(0, Action.GOFORWARD)
                        ActionSet.insert(0, Action.TURNLEFT)
                        ActionSet.insert(0, Action.SHOOT)
                        ActionSet.insert(0, Action.TURNLEFT)
                        ActionSet.insert(0, Action.GOFORWARD)
                        if direction == Orientation.LEFT:
                            ActionSet.insert(0, Action.TURNRIGHT)
                        else:
                            ActionSet.insert(0, Action.TURNLEFT)
                    else:
                        if direction == Orientation.DOWN:
                            ActionSet.insert(0, Action.TURNRIGHT)
                        else:
                            for i in range(Orientation.LEFT-direction):
                                ActionSet.insert(0, Action.TURNLEFT)
                            ActionSet.insert(0, Action.GOFORWARD)
                            ActionSet.insert(0, Action.TURNRIGHT)
                            ActionSet.insert(0, Action.GOFORWARD)
                            ActionSet.insert(0, Action.TURNRIGHT)
                            ActionSet.insert(0, Action.SHOOT)
                            ActionSet.insert(0, Action.TURNRIGHT)
                            ActionSet.insert(0, Action.GOFORWARD)
                            if direction == Orientation.LEFT:
                                ActionSet.insert(0, Action.TURNRIGHT)
                            else:
                                ActionSet.insert(0, Action.TURNLEFT)
                    actions = ActionSet.pop()
                    if actions == Action.GOFORWARD:
                        return UpdateLocation(actions)
                    else:
                        return UpdateDirection(actions)
    else:
        perceptStr += "Stench=False,"
    if (breeze == 1):
        perceptStr += "Breeze=True,"
    else:
        perceptStr += "Breeze=False,"
    if (bump == 1):
        # Bump percept, randomly turn LEFT or RIGHT
        perceptStr += "Bump=True,"
        if unsize:
            location[0] = max(1, location[0]-1)
            size = location[0]
            unsize = 0
        else:
            size = max(size, location[0], location[1])
        return ChangeDirection()
    else:
        perceptStr += "Bump=False,"
    if (scream == 1):
        perceptStr += "Scream=True"
    else:
        perceptStr += "Scream=False"
    print("PyAgent_Process: " + perceptStr)
    return UpdateLocation(Action.GOFORWARD)


def PyAgent_GameOver(score):
    print("PyAgent_GameOver: score = " + str(score))


def UpdateLocation(action):
    global direction
    global location
    if direction == Orientation.RIGHT:
        location[0] = min(location[0]+1, size)
    elif direction == Orientation.DOWN:
        location[1] = max(location[1]-1, 1)
    elif direction == Orientation.LEFT:
        location[0] = max(location[0]-1, 1)
    elif direction == Orientation.UP:
        location[1] = min(location[1]+1, size)
    return action


def UpdateDirection(actions):
    global direction
    if actions == Action.TURNLEFT:
        direction += 1
        if direction > 3:
            direction = 0
        return actions
    if actions == Action.TURNRIGHT:
        direction -= 1
        if direction < 0:
            direction = 3
        return actions


def ChangeDirection():
    '''
        When facing with bump, will use this function.
    '''
    global direction
    global ActionSet
    global location
    global size
    if location == (size, size):
        if random.randint(0, 1):
            return UpdateDirection(Action.TURNRIGHT)
        else:
            return UpdateDirection(Action.TURNLEFT)
    if direction == 0:
        ActionSet.append(Action.TURNLEFT)
        ActionSet.append(Action.GOFORWARD)
        return UpdateDirection(Action.TURNLEFT)
    elif direction == 2:
        ActionSet.append(Action.TURNRIGHT)
        ActionSet.append(Action.GOFORWARD)
        return UpdateDirection(Action.TURNRIGHT)
    else:
        if random.randint(0, 1):
            return UpdateDirection(Action.TURNRIGHT)
        else:
            return UpdateDirection(Action.TURNLEFT)


def RecordPath(Locat):
    """
        Used to remember the agent's path
    """
    global PathSet
    if Locat not in PathSet:
        PathSet.append(Locat)


def TravelToInit():
    """
        function used for travel to init,
        consider optimal and safety.
    """
    global location
    global direction
    global Dangers
    global ActionSet
    ActionSet.clear()
    way = 0
    if Dangers:
        if Dangers[0][0] == location[0] or Dangers[0][1] == 1:
            way = 1
        elif Dangers[0][0] == 1 or Dangers[0][1] == location[1]:
            way = 0
        else:
            way = 1
    else:
        way = 1
    if way:
        #  if we can choose way 1, we will go left until the bump
        #  then go down until the init.
        if direction != Orientation.LEFT:
            if direction == Orientation.DOWN:
                ActionSet.append(Action.TURNRIGHT)
            else:
                for i in range(Orientation.LEFT-direction):
                    ActionSet.append(Action.TURNLEFT)
        for i in range(location[0]-1):
            ActionSet.insert(0, Action.GOFORWARD)
        ActionSet.insert(0, Action.TURNLEFT)
        for i in range(location[1]-1):
            ActionSet.insert(0, Action.GOFORWARD)
    else:
        for i in range(Orientation.DOWN-direction):
            ActionSet.append(Action.TURNLEFT)
        for i in range(location[1]-1):
            ActionSet.insert(0, Action.GOFORWARD)
        ActionSet.insert(0, Action.TURNRIGHT)
        for i in range(location[0]-1):
            ActionSet.insert(0, Action.GOFORWARD)


def WumpusLocation(locat):
    """
        Once feeling the stench, the agent will try to confirm
        the location of the wumpus.
    """
    global ActionSet
    global CheckDangers
    CheckDangers = 1
    ActionSet.append(Action.GOFORWARD)
    ActionSet.append(Action.TURNRIGHT)
    ActionSet.append(Action.GOFORWARD)
    ActionSet.append(Action.TURNLEFT)
    return UpdateDirection(Action.TURNLEFT)


def testwumpus():
    global direction
    global location
    global Dangers
    if direction == Orientation.RIGHT:
        if (location[0]+1, location[1]) == Dangers[0]:
            if Dangers[0][0] == size:
                ActionSet.append(Action.TURNLEFT)
                ActionSet.append(Action.TURNLEFT)
                ActionSet.append(Action.GOFORWARD)
                ActionSet.append(Action.TURNRIGHT)
                ActionSet.append(Action.GOFORWARD)
                return UpdateDirection(Action.TURNLEFT)
            else:
                ActionSet.append(Action.TURNRIGHT)
                ActionSet.append(Action.GOFORWARD)
                ActionSet.append(Action.TURNLEFT)
                ActionSet.append(Action.GOFORWARD)
                ActionSet.append(Action.GOFORWARD)
                ActionSet.append(Action.TURNLEFT)
                return UpdateDirection(Action.TURNRIGHT)
    if direction == Orientation.LEFT:
        if (location[0]-1, location[1]) == Dangers[0]:
            if Dangers[0][0] == 1:
                ActionSet.append(Action.TURNRIGHT)
                ActionSet.append(Action.TURNRIGHT)
                ActionSet.append(Action.GOFORWARD)
                ActionSet.append(Action.TURNLEFT)
                ActionSet.append(Action.GOFORWARD)
                return UpdateDirection(Action.TURNRIGHT)
            else:
                ActionSet.append(Action.TURNLEFT)
                ActionSet.append(Action.GOFORWARD)
                ActionSet.append(Action.TURNRIGHT)
                ActionSet.append(Action.GOFORWARD)
                ActionSet.append(Action.GOFORWARD)
                ActionSet.append(Action.TURNRIGHT)
                return UpdateDirection(Action.TURNLEFT)
    if direction == Orientation.UP:
        if (location[0], location[1]+1) == Dangers[0]:
            ActionSet.clear()
            if Dangers[0] == 1:
                ActionSet.append(Action.TURNRIGHT)
                ActionSet.append(Action.GOFORWARD)
                ActionSet.append(Action.TURNLEFT)
                ActionSet.append(Action.GOFORWARD)
                return UpdateDirection(Action.TURNRIGHT)
            if Dangers[0] == size:
                ActionSet.append(Action.TURNLEFT)
                ActionSet.append(Action.GOFORWARD)
                ActionSet.append(Action.TURNRIGHT)
                ActionSet.append(Action.GOFORWARD)
                return UpdateDirection(Action.TURNLEFT)
    return UpdateLocation(Action.GOFORWARD)
