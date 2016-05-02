from game import Agent
from game import Directions
from game import Actions
from game import ghosts_in_action
from game import ghosts_at_rest
import random
from util import manhattanDistance
from util import euclidianDistance
import util
import layout
from layout import Layout

class MouseAgent(Agent):
    """
    An agent controlled by the mouse.
    """
    def __init__( self, index = 0 ):

        self.lastMove = Directions.STOP
        self.index = index		

    def getAction( self, state):
        #getAction gets the action for a given index given the object state of gamestatedata class. 
        legal = state.getLegalActions(self.index)
        #print legal
        ghost_indices = [1,2,3,4]
        #print self.index
        if self.index == 0:
            decision_index = 0 
            conf = state.getPacmanState().configuration
            reverse = Actions.reverseDirection( conf.direction )
            for i in ghost_indices:
                if manhattanDistance(state.getPacmanPosition(),state.getGhostPosition(i)) < 3:
                    decision_index+=1
            if decision_index > 0:
                legal = state.getLegalActions(self.index)
            else:
                if reverse in legal and len(legal)>1:
                    legal.remove(reverse)
            depth = 6
            cost_dict = {}
            ghost_successor_dict = {} # 1:state of ghost 1 at depth i
            for i in ghost_indices:
                ghost_successor_dict[i] = [state.getGhostPosition(i)]            
            pacman_dict = {}  # direction:state of pacman with that direciton at depth i
            for i in legal:
                pacman_dict[i] = [(Actions.getSuccessor(state.getPacmanPosition(),i),i)]
            
            for d in range(depth):
                for ghost in ghost_indices: 
                    temp_list = []
                    for stat in ghost_successor_dict[ghost]:
                        temp_list.append(self.getSuccessors_g(stat,state))
                    ghost_successor_dict[ghost] = []
                    for x in temp_list:
                       for y in x:
                           ghost_successor_dict[ghost].append(y)
                break_value = 0
                if d == 1:
                    for t in pacman_dict.keys():
                        for u in pacman_dict[t]:
                            for ghost in ghost_indices:
                                if u[0] in ghost_successor_dict[ghost]:
                                    break_value =1
                                    cost_dict[t] = d
                                    del pacman_dict[t]
                                    break
                            if break_value == 1:
                                break_value = 0
                                break
                    if len(pacman_dict.keys()) == 1:
                        #print '1111'
                        return pacman_dict.keys()[0]
                else:               
                   for i in pacman_dict.keys():
                        temp_list = []  
                        for tupl in pacman_dict[i]:    #tupl = ((2,3),prev_action)
                            temp_list.append(self.getSuccessors_indexo(tupl,state))
                        pacman_dict[i] = []
                        for x in temp_list:
                            for y in x:
                                pacman_dict[i].append(y)
    
                   for i in pacman_dict.keys():
                       for j in pacman_dict[i]:
                           for ghost in ghost_indices:
                               if j[0] in ghost_successor_dict[ghost]:
                                   cost_dict[i] = d
                                   del pacman_dict[i]
                                   break_value =1
                                   break
                           if break_value == 1:
                               break_vlaue = 0
                               break
                   if len(pacman_dict.keys()) == 1:
                       #print '23234'
                       return pacman_dict.keys()[0]
            #print 'returning random'
            return random.choice(legal)
        distance = {}
        from graphicsUtils import click_pos
        from graphicsUtils import del_leftclick_loc
        #print click_pos(),'mouseagent' 
             
        if self.index in ghosts_in_action.keys():
            #print ghosts_in_action
            #print self.index, ghosts_in_action
            a = ghosts_in_action[self.index][0]            
            del ghosts_in_action[self.index][0]
            if len(ghosts_in_action[self.index]) == 0:
                del ghosts_in_action[self.index]
                ghosts_at_rest.append(self.index)
                return a
            else:
                return a
        else:
            if click_pos() != None:
                goal_state = click_pos()
                del_leftclick_loc()
                if state.hasWall(goal_state[0],goal_state[1]):
                    temp_a = 0
                    for acti in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
                        actual_state = (int(Actions.getSuccessor(goal_state,acti)[0]),int(Actions.getSuccessor(goal_state,acti)[1]))
                        if not(state.hasWall(actual_state[0],actual_state[1])):
                            goal_state = actual_state
                            temp_a = 1
                            break
                    if temp_a == 0:
                        print "Please provide valid co-ordinates"
                        return Directions.STOP
                for i in ghosts_at_rest:
                    distance[i] = euclidianDistance(goal_state, state.getGhostPosition(i))
                assigned_ghost = min(distance.items(), key=lambda x: x[1])[0]
                start_state = state.getGhostPosition(assigned_ghost)
                dist_list = self.uniformCostSearch(start_state, goal_state,state,self.index)
                ghosts_in_action[assigned_ghost] = dist_list
                ghosts_at_rest.remove(assigned_ghost)
                if assigned_ghost == self.index:
                    a = ghosts_in_action[assigned_ghost][0]
                    del ghosts_in_action[assigned_ghost][0]
                    if len(ghosts_in_action[self.index]) == 0:
                        del ghosts_in_action[self.index]
                        ghosts_at_rest.append(self.index)
                    return a
                else:
                    return Directions.STOP
            else:
                return Directions.STOP

    def uniformCostSearch(self,start_state, goal_state,objj,index):
        """Search the node of least total cost first."""
        closed = set()
        fringe = util.PriorityQueue()
        from game import Directions
        South = Directions.SOUTH
        West = Directions.WEST
        North = Directions.NORTH
        East = Directions.EAST
        Stop = Directions.STOP
        l=[start_state,[]]
        fringe.push(l,0)
        if start_state == goal_state:
            return [Directions.STOP]
        while (not(fringe.isEmpty())):
            n = fringe.heap[0]
            b = fringe.pop()[1]
            if len(b) != 0: 
                prev_action = b[-1]
            else:
                prev_action = None
            if n[2][0] == goal_state:
                return n[2][1]
               
            if n[2][0] not in closed :
                closed.add(n[2][0])
                n[2][1]= tuple(n[2][1])
                s =self.getSuccessors(n[2][0],objj,prev_action)
                for i in s:
                    li = []
                    li.append(i[0])
                    li.append(list(n[2][1]))
                    li[1].append(i[1])
                    cost = n[0] +i[2]
                    fringe.push(li,cost)

    def getSuccessors(self,state_pos,obj,act):     
        successors = []
        d = ['North','South','East','West']
        new_d = []
        direction_list = []
        reverse = Actions.reverseDirection(act)
        if reverse == None:
            direction_list = d
        elif reverse in d:
            for di in d:
                if di != reverse:
                    new_d.append(di)
            direction_list = new_d
        for action in direction_list:
            x,y = state_pos
            dx, dy = Actions.directionToVector(action)
            nextx, nexty = int(x + dx), int(y + dy)
            if not obj.hasWall(nextx,nexty):
                nextState = (nextx, nexty)
                cost = 1
                successors.append( ( nextState, action, cost) )
        return successors

    def getSuccessors_indexo(self,tupl,obj):     
        successors = []
        d = [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]
        prevact = Actions.reverseDirection(tupl[1])
        action_list = []
        for k in d:
            if k != prevact:
                action_list.append(k)
        #print state_pos, 'successor fn state'
        for action in action_list:
            x,y = tupl[0]
            dx, dy = Actions.directionToVector(action)
            nextx, nexty = int(x + dx), int(y + dy)
            if not obj.hasWall(nextx,nexty):
                nextState = (nextx, nexty)
                successors.append( ( nextState, action) )
        #print successors, 'successors'
        return successors

    def getSuccessors_g(self,state_pos,obj):     
        successors = []
        for action in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
            x,y = state_pos
            dx, dy = Actions.directionToVector(action)
            nextx, nexty = int(x + dx), int(y + dy)
            if not obj.hasWall(nextx,nexty):
            	nextState = (nextx, nexty)
            	successors.append(nextState)
        successors.append(state_pos)
        #print successors, 'successors'Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]
        return successors

    def getSuccessors_indexo2(self,tupl,obj):     
        successors = []
        d = [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]
        for action in d:
            x,y = tupl[0]
            dx, dy = Actions.directionToVector(action)
            nextx, nexty = int(x + dx), int(y + dy)
            if not obj.hasWall(nextx,nexty):
                nextState = (nextx, nexty)
                successors.append( ( nextState, action) )
        return successors


    def depthFirstSearch(self,start_state, goal_state,objj):    
        closed = set()
        fringe = util.Stack()
        from game import Directions
        South = Directions.SOUTH
        West = Directions.WEST
        North = Directions.NORTH
        East = Directions.EAST
        South = Directions.STOP
        l=[start_state,[]]
        fringe.push(l) 
        while (not(fringe.isEmpty())):        
            fringe.pop()	
            if (n[0] == goal_state):
                return n[1]
            if n[0] not in closed :
                closed.add(n[0])
                n[1]= tuple(n[1])
                s =self.getSuccessors(n[0],objj)
                for successor in s:
                    li = []
                    li.append(successor[0])
                    li.append(list(n[1]))
                    li[1].append(successor[1])
                    fringe.push(li)

'''
def getSuccessors(state_pos):     
    successors = []
    for action in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
        x,y = state_pos
        dx, dy = Actions.directionToVector(action)
        nextx, nexty = int(x + dx), int(y + dy)
        #print state.getWalls(), 'walls'
        if not (([nextx],[nexty])):
        	nextState = (nextx, nexty)
        	cost = 1
        	successors.append( ( nextState, action, cost) )
    return successors


def depthFirstSearch(start_state, goal_state):    
    closed = set()
    fringe = util.Stack()
    from game import Directions
    South = Directions.SOUTH
    West = Directions.WEST
    North = Directions.NORTH
    East = Directions.EAST
    l=[start_state,[]]
    fringe.push(l)
    while (not(fringe.isEmpty())):
        n = fringe.list[-1]
        fringe.pop()	
        if (n[0] == goal_state):
            print n[1], 'ini'
            return n[1]
        if n[0] not in closed :
            closed.add(n[0])
            n[1]= tuple(n[1])
            s =getSuccessors(n[0])
            for i in s:
            	li = []
            	li.append(i[0])
            	li.append(list(n[1]))
            	li[1].append(i[1])
            	fringe.push(li)
		
'''
                     
''' 
    def getMove(self, legal):
        move = Directions.STOP
        if   (self.WEST_KEY in self.keys or 'Left' in self.keys) and Directions.WEST in legal:  move = Directions.WEST
        if   (self.EAST_KEY in self.keys or 'Right' in self.keys) and Directions.EAST in legal: move = Directions.EAST
        if   (self.NORTH_KEY in self.keys or 'Up' in self.keys) and Directions.NORTH in legal:   move = Directions.NORTH
        if   (self.SOUTH_KEY in self.keys or 'Down' in self.keys) and Directions.SOUTH in legal: move = Directions.SOUTH
        return move

class KeyboardAgent2(KeyboardAgent):
    """
    A second agent controlled by the keyboard.
    """
    # NOTE: Arrow keys also work.
    WEST_KEY  = 'j'
    EAST_KEY  = "l"
    NORTH_KEY = 'i'
    SOUTH_KEY = 'k'
    STOP_KEY = 'u'

    def getMove(self, legal):
        move = Directions.STOP
        if   (self.WEST_KEY in self.keys) and Directions.WEST in legal:  move = Directions.WEST
        if   (self.EAST_KEY in self.keys) and Directions.EAST in legal: move = Directions.EAST
        if   (self.NORTH_KEY in self.keys) and Directions.NORTH in legal:   move = Directions.NORTH
        return move


        if move == Directions.STOP:     #when keys = [] (keys is empty, i.e no input from the user)
            # Try to move in the same direction as before
            if self.lastMove in legal:
                move = self.lastMove

        if (self.STOP_KEY in self.keys) and Directions.STOP in legal: move = Directions.STOP

        if move not in legal:
            move = random.choice(legal)

        self.lastMove = move
        return move
'''
