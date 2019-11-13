# PyAgent.py

from random import randint
import Action
import Orientation
import itertools as it


class WorldState:
    def __init__(self):
        self.agentLocation = [1, 1]
        self.agentOrientation = Orientation.RIGHT
        self.agentHasArrow = True
        self.agentHasGold = False

        # HW5
        self.goldLocation = [0, 0]
        self.worldSize = 5


class Agent:
    def __init__(self):
        self.worldState = WorldState()
        self.previousAction = Action.CLIMB
        self.previousPercept = 0
        self.actionList = []

        # HW5
        self.firstTry = True
        self.pathToGold = []
        self.possibleWumpusLocations = []
        self.visitedLocations = []
        self.safeLocations = []
        self.stenchLocations = []
        self.clearLocations = []
        self.breezeLocations = []
        self.pitLocations = []
        self.probability = []
        self.randomlr = 0

    def Initialize(self):
        self.worldState.agentLocation = [1, 1]
        self.worldState.agentOrientation = Orientation.RIGHT
        self.worldState.agentHasArrow = True
        self.worldState.agentHasGold = False
        self.previousAction = Action.CLIMB
        self.probability = [[0.20]*5, [0.20]*5, [0.20]*5, [0.20]*5, [0.20]*5]
        self.actionList = []
        self.randomlr = 0

        # HW5
        if (self.firstTry):
            self.worldState.goldLocation = [0, 0]  # unknown
            self.worldState.worldSize = 0  # unknown
            self.pathToGold.append([1, 1])  # path starts in (1,1)
        else:
            if (self.worldState.goldLocation == [0, 0]):
                # Didn't find gold on first try (should never happen,
                # but just in case)
                self.pathToGold = []
                self.pathToGold.append([1, 1])
            else:
                self.AddActionsFromPath(True)
                # forward through path from (1,1) to gold location

    def Process(self, percept):
        self.UpdateState(percept)
        self.ComputeProbability()
        if (not self.actionList):
            if (percept['Glitter']):
                self.actionList.append(Action.GRAB)
                self.AddActionsFromPath(False)
                # HW5: reverse path from (1,1) to gold location
            elif (self.worldState.agentHasGold and \
                  (self.worldState.agentLocation == [1, 1])):
                self.actionList.append(Action.CLIMB)
            else:
                self.actionList.append(self.ChooseAction(percept))  # HW5
        action = self.actionList.pop(0)
        self.previousAction = action
        self.previousPercept = percept
        return action

    def GameOver(self, score):
        # HW5
        if self.previousPercept['Breeze']:
            self.AddNewLocation(self.pitLocations, self.GetGoForward())
        self.firstTry = False

    def UpdateState(self, percept):
        currentOrientation = self.worldState.agentOrientation

        if (self.previousAction == Action.GOFORWARD):
            # HW5
            if (percept['Bump']):
                # Check if we can determine world size
                if (self.worldState.agentOrientation == Orientation.RIGHT):
                    self.worldState.worldSize =\
                        self.worldState.agentLocation[0]
                if (self.worldState.agentOrientation == Orientation.UP):
                    self.worldState.worldSize =\
                        self.worldState.agentLocation[1]
                if (self.worldState.worldSize > 0):
                    self.FilterSafeLocations()
            else:
                self.worldState.agentLocation = self.GetGoForward()
                if (self.worldState.goldLocation == [0, 0]):
                    # If haven't found gold yet,
                    # add this location to the pathToGold
                    self.AddToPath(self.worldState.agentLocation)

        if (self.previousAction == Action.TURNLEFT):
            self.worldState.agentOrientation = (currentOrientation + 1) % 4

        if (self.previousAction == Action.TURNRIGHT):
            currentOrientation -= 1
            if (currentOrientation < 0):
                currentOrientation = 3
            self.worldState.agentOrientation = currentOrientation

        if (self.previousAction == Action.GRAB):
            self.worldState.agentHasGold = True  # Only GRAB when there's gold
            self.worldState.goldLocation = self.worldState.agentLocation  # HW5

        if (self.previousAction == Action.SHOOT):
            self.worldState.agentHasArrow = False

            # HW5
            # The only situation where we shoot is if we start out in (1,1)
            # facing RIGHT, perceive a stench, and don't know the wumpus
            # location. In this case, a SCREAM percept means the wumpus is
            # in (2,1) (and dead), or if no SCREAM, then the wumpus is
            # in (1,2) (and still alive).
            self.possibleWumpusLocations = []
            if (percept['Scream']):
                self.possibleWumpusLocations.append([2, 1])
            else:
                self.possibleWumpusLocations.append([1, 2])

        # Nothing to do for CLIMB
        # HW5
        # Update visited locations, safe locations, stench locations,
        # clear locations, and possible wumpus locations.
        self.AddNewLocation(self.visitedLocations,
                            self.worldState.agentLocation)
        self.AddNewLocation(self.safeLocations, self.worldState.agentLocation)
        if percept['Stench'] and percept['Breeze']:
            self.AddNewLocation(self.stenchLocations,
                                self.worldState.agentLocation)
            self.AddNewLocation(self.breezeLocations,
                                self.worldState.agentLocation)
            self.ComputeProbability()
            for k in self.UDLR(self.worldState.agentLocation):
                if self.probability[k[0]-1][k[1]-1] < 0.5:
                    self.AddNewLocation(self.safeLocations,
                                      self.worldState.agentLocation)
        elif percept['Stench']:
            self.AddNewLocation(self.stenchLocations,
                                self.worldState.agentLocation)
        elif percept['Breeze']:
            self.AddNewLocation(self.breezeLocations,
                                self.worldState.agentLocation)
            for k in self.UDLR(self.worldState.agentLocation):
                if self.probability[k[0]-1][k[1]-1] < 0.5:
                    self.AddNewLocation(self.safeLocations,
                                      self.worldState.agentLocation)
        else:
            self.AddNewLocation(self.clearLocations,
                                self.worldState.agentLocation)
            self.AddAdjacentLocations(self.safeLocations,
                                      self.worldState.agentLocation)
        if (len(self.possibleWumpusLocations) != 1):
            self.UpdatePossibleWumpusLocations()

        self.Output()
    # HW5
    #
    # Update possible wumpus locations based on the current set of stench
    # locations and clear locations.
    #

    def UpdatePossibleWumpusLocations(self):
        self.possibleWumpusLocations = []
        # Determine possible wumpus locations consistent with available
        # stench information
        for location1 in self.stenchLocations:
            # Build list of adjacent locations to this stench location
            adjacentLocations = []
            self.AddAdjacentLocations(adjacentLocations, location1)
            if (not self.possibleWumpusLocations):
                # Must be first stench location in list, so add all
                # adjacent locations
                self.possibleWumpusLocations = adjacentLocations
            else:
                # Eliminate possible wumpus locations not adjacent to this
                # stench location
                tmpLocations = self.possibleWumpusLocations
                self.possibleWumpusLocations = []
                for location2 in tmpLocations:
                    if (location2 in adjacentLocations):
                        self.possibleWumpusLocations.append(location2)
        # Eliminate possible wumpus locations adjacent to a clear location
        for location1 in self.clearLocations:
            # Build list of adjacent locations to this clear location
            adjacentLocations = []
            self.AddAdjacentLocations(adjacentLocations, location1)
            tmpLocations = self.possibleWumpusLocations
            self.possibleWumpusLocations = []
            for location2 in tmpLocations:
                if (location2 not in adjacentLocations):
                    self.possibleWumpusLocations.append(location2)

    # HW5
    #
    # Returns location resulting in a successful GOFORWARD.
    # Replaced Move() method from HW2.
    #
    def GetGoForward(self):
        X = self.worldState.agentLocation[0]
        Y = self.worldState.agentLocation[1]
        if (self.worldState.agentOrientation == Orientation.RIGHT):
            X = X + 1
        if (self.worldState.agentOrientation == Orientation.UP):
            Y = Y + 1
        if (self.worldState.agentOrientation == Orientation.LEFT):
            X = X - 1
        if (self.worldState.agentOrientation == Orientation.DOWN):
            Y = Y - 1
        return [X, Y]

    # HW5
    #
    # Add given location to agent's pathToGold. But if this location is already
    # on the pathToGold, then remove everything after the first occurrence of
    # this location.
    def AddToPath(self, location):
        if (location in self.pathToGold):
            index = self.pathToGold.index(location)
            self.pathToGold = self.pathToGold[:index]
        self.pathToGold.append(location)
    # HW5
    #
    # Choose and return an action when we haven't found the gold yet.
    # Handle special case where we start out in (1,1), perceive a stench, and
    # don't know the wumpus location. In this case, SHOOT. Orientation will be
    # RIGHT, so if SCREAM, then wumpus in (2,1); otherwise in (1,2). This is
    # handled in the UpdateState method.
    #

    def ChooseAction(self, percept):
        forwardLocation = self.GetGoForward()
        if self.randomlr > 20:
            self.randomlr = 0
            action = Action.GOFORWARD
        if (percept['Stench'] and (self.worldState.agentLocation == [1, 1]) and
                (len(self.possibleWumpusLocations) != 1)):
            action = Action.SHOOT
        elif (self.probability[min(forwardLocation[0]-1, 4)]
              [min(forwardLocation[1]-1, 4)] > 0.5):
            action = randint(1, 2)
        elif ((forwardLocation in self.safeLocations)
              and (forwardLocation not in self.visitedLocations)):
            # If happen to be facing safe unvisited location, then move there
            print("GOGOGO")
            action = Action.GOFORWARD
        else:
            if forwardLocation in self.safeLocations:
                action = Action.GOFORWARD
            # Choose randomly from GOFORWARD, TURNLEFT, and TURNRIGHT, but
            # don't GOFORWARD into a possible wumpus location or a wall
            if ((forwardLocation in self.possibleWumpusLocations) or
                    self.OutsideWorld(forwardLocation)):
                action = randint(1, 2)  # TURNLEFT, TURNRIGHT
            else:
                print("randomchoose")
                action = randint(0, 2)  # GOFORWARD, TURNLEFT, TURNRIGHT
        if action == Action.GOFORWARD:
            self.randomlr = 0
        else:
            self.randomlr += 1
        return action
    # HW5
    #
    # Add a sequence of actions to actionList that moves the agent along the
    # pathToGold if forward=true, or the reverse if forward=false. Assumes at
    # least one location is on pathToGold.
    #

    def AddActionsFromPath(self, forward):
        path = list(self.pathToGold)
        if (not forward):
            path = list(reversed(path))
        currentLocation = self.worldState.agentLocation
        currentOrientation = self.worldState.agentOrientation
        for nextLocation in path[1:]:
            if (nextLocation[0] > currentLocation[0]):
                nextOrientation = Orientation.RIGHT
            if (nextLocation[0] < currentLocation[0]):
                nextOrientation = Orientation.LEFT
            if (nextLocation[1] > currentLocation[1]):
                nextOrientation = Orientation.UP
            if (nextLocation[1] < currentLocation[1]):
                nextOrientation = Orientation.DOWN
            # Find shortest turn sequence
            # (assuming RIGHT=0, UP=1, LEFT=2, DOWN=3)
            diff = (currentOrientation - nextOrientation)
            if ((diff == 1) or (diff == -3)):
                self.actionList.append(Action.TURNRIGHT)
            else:
                if (diff != 0):
                    self.actionList.append(Action.TURNLEFT)
                if ((diff == 2) or (diff == -2)):
                    self.actionList.append(Action.TURNLEFT)
            self.actionList.append(Action.GOFORWARD)
            currentLocation = nextLocation
            currentOrientation = nextOrientation

    # HW5
    #
    # Add location to given list, if not already present.
    #
    def AddNewLocation(self, locationList, location):
        if (location not in locationList):
            locationList.append(location)

    # HW5
    #
    # Add locations that are adjacent to the given location to the given
    # location list. Doesn't add locations outside the left and bottom borders
    # of the world, but might add locations outside the top and right borders
    # of the world, if we don't know the world size.
    #
    def AddAdjacentLocations(self, locationList, location):
        worldSize = self.worldState.worldSize
        if ((worldSize == 0) or (location[1] < worldSize)):
            self.AddNewLocation(locationList, [location[0],
                                            location[1] + 1])  # up
        if ((worldSize == 0) or (location[0] < worldSize)):
            self.AddNewLocation(locationList, [location[0] + 1,
                                            location[1]])  # right
        if (location[0] > 1):
            self.AddNewLocation(locationList, [location[0] - 1,
                                            location[1]])  # left
        if (location[1] > 1):
            self.AddNewLocation(locationList, [location[0],
                                            location[1] - 1])  # down
    # HW5
    #
    # Return true if given location is outside known world.
    #

    def OutsideWorld(self, location):
        worldSize = self.worldState.worldSize
        if ((location[0] < 1) or (location[0] < 1)):
            return True
        if ((worldSize > 0) and ((location[0] > worldSize) or
                                 (location[1] > worldSize))):
            return True
        return False
    # HW5
    #
    # Filters from safeLocations any locations that are outside the upper or
    # right borders of the world.
    #

    def FilterSafeLocations(self):
        worldSize = 5
        tmpLocations = list(self.safeLocations)
        self.safeLocations = []
        for location in tmpLocations:
            if ((location[0] < 1) or (location[1] < 1)):
                continue
            if ((worldSize > 0) and ((location[0] > worldSize) or
                                     (location[1] > worldSize))):
                continue
            self.safeLocations.append(location)
    # HW5

    def Output(self):
        print("World Size: " + str(self.worldState.worldSize))
        print("Visited Locations: " + str(self.visitedLocations))
        print("Safe Locations: " + str(self.safeLocations))
        print("Possible Wumpus Locations: " +
              str(self.possibleWumpusLocations))
        print("Possible Pit Location:" + str(self.pitLocations))
        print("Gold Location: " + str(self.worldState.goldLocation))
        print("Breeze Location:" + str(self.breezeLocations))
        print("Path To Gold: " + str(self.pathToGold))
        actionStrList = []
        for action in self.actionList:
            if action == Action.GOFORWARD:
                actionStrList.append('GOFORWARD')
            elif action == Action.TURNLEFT:
                actionStrList.append('TURNLEFT')
            elif action == Action.TURNRIGHT:
                actionStrList.append('TURNRIGHT')
            elif action == Action.GRAB:
                actionStrList.append('GRAB')
            elif action == Action.SHOOT:
                actionStrList.append('SHOOT')
            else:
                actionStrList.append('CLIMB')
        print("Action List: " + str(actionStrList))
        print("")

    # hw9

    def UDLR(self, location):
        up = [location[0], location[1]+1]
        down = [location[0], location[1]-1]
        left = [location[0]-1, location[1]]
        right = [location[0]+1, location[1]]
        return [up, down, left, right]

    # hw9
    def PrintProbability(self):
        print("Probability")
        for j in range(0, 5):
            i = self.probability
            print("%.2f %.2f %.2f %.2f %.2f" % (i[0][4-j], i[1][4-j],
                                        i[2][4-j], i[3][4-j], i[4][4-j]))

    # hw9
    def ComputeProbability(self):
        frontier = []
        size = 5
        # compute frontier
        for locat in self.visitedLocations:
            self.probability[locat[0]-1][locat[1]-1] = 0.00
            up = [locat[0], locat[1]+1 if locat[1]+1 < size else locat[1]]
            down = [locat[0], locat[1]-1 if locat[1]-1 > 0 else locat[1]]
            left = [locat[0]-1 if locat[0]-1 > 0 else locat[0], locat[1]]
            right = [locat[0]+1 if locat[0]+1 < size else locat[0], locat[1]]
            for update in [up, down, left, right]:
                if update not in self.visitedLocations:
                    self.AddNewLocation(frontier, update)
        for pits in self.pitLocations:
            self.probability[pits[0]-1][pits[1]-1] = 1.00
        for safe in self.safeLocations:
            self.probability[min(max(safe[0]-1, 0), 4)]\
                [min(max(safe[1]-1, 0), 4)] = 0.00
        if not self.breezeLocations:
            return self.PrintProbability()
        # compute the probability
        frontier_d = frontier.copy()
        for locat in frontier:
            # initialize
            if locat in self.safeLocations:
                frontier_d.remove(locat)
            if locat in self.pitLocations:
                frontier_d.remove(locat)
        for locat in frontier_d:
            breeze_new = self.breezeLocations.copy()
            for pits in self.pitLocations:
                for k in self.UDLR(pits):
                    if k in breeze_new:
                        breeze_new.remove(k)
            p_true = 0
            p_false = 0
            for i in it.product('01', repeat=len(frontier_d)):
                breeze = breeze_new.copy()
                false = 0
                for j in range(len(i)):
                    if i[j] == '1':
                        for k in self.UDLR(frontier_d[j]):
                            if k in breeze:
                                breeze.remove(k)
                for j in breeze:
                    for k in self.UDLR(j):
                        if k in frontier_d:
                            false += 1
                if not false:
                    t = list(i).count('1')
                    f = len(i) - t
                    if i[frontier_d.index(locat)] == '1':
                        p_true += (0.2**t)*(0.8**f)
                    else:
                        p_false += (0.2**t)*(0.8**f)
            # p_true = p_true*0.2
            # p_false = p_false*0.8
            p_true = p_true/(p_true + p_false)
            self.probability[locat[0]-1][locat[1]-1] = p_true
        self.PrintProbability()


    # hw9

    def GoToSafeLocat(self):
        frontier = []
        size = 5
        # compute frontier
        for locat in self.visitedLocations:
            self.probability[locat[0]-1][locat[1]-1] = 0.00
            up = [locat[0], locat[1]+1 if locat[1]+1 < size else locat[1]]
            down = [locat[0], locat[1]-1 if locat[1]-1 > 0 else locat[1]]
            left = [locat[0]-1 if locat[0]-1 > 0 else locat[0], locat[1]]
            right = [locat[0]+1 if locat[0]+1 < size else locat[0], locat[1]]
            for update in [up, down, left, right]:
                if update not in self.visitedLocations:
                    self.AddNewLocation(frontier, update)
        for locat in frontier:
            # initialize
            if locat in self.safeLocations:
                frontier.remove(locat)
            if locat in self.pitLocations:
                frontier.remove(locat)
        for locat in frontier:
            if self.probability[locat[0]-1][locat[1]-1] < 0.50:
                return self.GoTo(locat)

    # hw9
    def GoTo(self, target):
        print("target:", target)
        path = []
        location = self.worldState.agentLocation
        lr = target[0] - location[0]
        lr_n = abs(target[0] - location[0])
        ud = target[1] - location[1]
        ud_n = abs(target[1] - location[1])
        new_locat = location
        for i in range(lr_n+ud_n):
            if i < ud_n:
                print("UD:", ud, ud_n)
                new_locat[1] = int(new_locat[1] + ud/ud_n)
            else:
                print("LR:", lr, lr_n)
                new_locat[0] = int(new_locat[0] + lr/lr_n)
            lo = new_locat.copy()
            path.append(lo)
        print("path!:", path)
        currentLocation = self.worldState.agentLocation
        currentOrientation = self.worldState.agentOrientation
        for nextLocation in path[1:]:
            if (nextLocation[0] > currentLocation[0]):
                nextOrientation = Orientation.RIGHT
            if (nextLocation[0] < currentLocation[0]):
                nextOrientation = Orientation.LEFT
            if (nextLocation[1] > currentLocation[1]):
                nextOrientation = Orientation.UP
            if (nextLocation[1] < currentLocation[1]):
                nextOrientation = Orientation.DOWN
            # Find shortest turn sequence
            # (assuming RIGHT=0, UP=1, LEFT=2, DOWN=3)
            diff = (currentOrientation - nextOrientation)
            if ((diff == 1) or (diff == -3)):
                self.actionList.append(Action.TURNRIGHT)
            else:
                if (diff != 0):
                    self.actionList.append(Action.TURNLEFT)
                if ((diff == 2) or (diff == -2)):
                    self.actionList.append(Action.TURNLEFT)
            self.actionList.append(Action.GOFORWARD)
            currentLocation = nextLocation
            currentOrientation = nextOrientation
            action = self.actionList.pop(0)
            return action

#  Global agent

myAgent = 0


def PyAgent_Constructor():
    print("PyAgent_Constructor")
    global myAgent
    myAgent = Agent()


def PyAgent_Destructor():
    print("PyAgent_Destructor")


def PyAgent_Initialize():
    print("PyAgent_Initialize")
    global myAgent
    myAgent.Initialize()


def PyAgent_Process(stench, breeze, glitter, bump, scream):
    global myAgent
    percept = {'Stench': bool(stench), 'Breeze': bool(breeze),
               'Glitter': bool(glitter), 'Bump': bool(bump),
               'Scream': bool(scream)}
    # print "PyAgent_Process: percept = " + str(percept)
    return myAgent.Process(percept)


def PyAgent_GameOver(score):
    print("PyAgent_GameOver: score = " + str(score))
    myAgent.GameOver(score)  # HW5
