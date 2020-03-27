
'''DBG_agent.py
by Russell Kook and Jia-Jia (Jay) Lin
UWNetIDs:russkook, jia18
Student Numbers:1620672,1820474

Assignment 3, in CSE 415, Winter 2020
This file contains our problem formulation of Deterministic
Simplified Backgammon (DSBG).
'''

from backgState import *
#from gameMaster import *

class DSBG:
    # Initializes the Agent
    def __init__(self, old=None):
        self.num_states = 0
        self.cutoffs = 0
        self.prune = False
        self.max_depth = 1
        self.function = None
        self.best_state = None
        self.state_dict = None
        #self.move_dict = None

    # Turns on and off AlphaBeta, and resets counters
    # Ask what this is? prune = False
    def useAlphaBetaPruning(self, prune = False):
        self.num_states = 0
        self.cutoffs = 0
        self.prune = not self.prune

    # this method returns a tuple (number of states and cutoffs)
    def statesAndCutoffsCounts(self):
        return (self.num_states, self.cutoffs)

    # Sets a specific limit on the depth of agent's searches
    def setMaxPly(self, maxply=-1):
        self.max_depth = maxply

    # Use the special static eval. function
    def useSpecialStaticEval(self, func):
        self.function = func

    # The Static Evaluation itself, apply to state
    # Count all whites moved out of start corner (positive)
    # vs red moved out of its start corner (negative)
    def staticEval(self, someState):
        #w = state.whose_move
        red = 0
        white = 0
        '''
        # how many whites are in its goal corner (triangles 19-24)
        for triangle in someState.pointLists[19:25]:
            for pieces in triangle:
                if pieces == 0: # if the value is white (W=0)
                    white += 100
        # how many reds are in its goal corner (triangles 1-6)
        for triangle in someState.pointLists[1:7]:
            for pieces in triangle:
                if pieces == 1: # if the value is red (R=1)
                    red += 100
        '''
                    
        for i in range(len(someState.pointLists)):
            for checker in someState.pointLists[i]:
                if(checker == W):
                    white += i
                else:
                    red += (24 - i)

        '''
        for i in range(24):
            if(W in someState.pointLists[i]):
                white += 5*(i + 1)
            elif(R in someState.pointLists[i]):
                red += 5*(24 - i)
        '''
        bar_value = 0
        '''
        for checker in someState.bar:
            if(checker == W):
                bar_value = bar_value - 100
            else:
                bar_value = bar_value + 100
        '''
        bear_off_value = (1000 * len(someState.white_off)) - (1000 * len(someState.red_off))
        
        return white - red + bar_value + bear_off_value
    
    # Minimax algorithm with OPTIONAL alpha-beta pruning
    # board = current state of the board
    # alpha and beta = only matters if self.prune = True
    # plyLeft = number of plays left
    # if the length of stack == maxDepth
    def minimax(self, board, alpha, beta, whoseMove, plyLeft, die1, die2):
      # provisional value of search
      #provisional = 0
      # If there are no more plays left (game ended)
      if(plyLeft == 0): #might need to change if plyLeft is -1
        if not (self.function == None):
          # Use TA's static eval function
          return self.function(board)
        else:
          #print(str(self.staticEval(board)))
          return self.staticEval(board)
        
      # if currently the maximizing player (White) 
      if(whoseMove == 0): 
        maxEval = -100000
        # for each child state 's' in a list 'successors'
        #print("hello0000O")
        for s in self.successors(board, whoseMove, die1, die2,plyLeft): 
          #print("helloOO")
          newVal = self.minimax(s,alpha,beta,self.other(whoseMove), plyLeft-1,die1,die2)
          #print("hello")
          if(newVal > maxEval):
              maxEval = newVal
          if(plyLeft == self.max_depth and newVal == maxEval):
              self.best_state = s
          #maxEval = max(provisional, newVal)
          # only check for alpha beta if self.prune = True
          if (self.prune):
            alpha = max(alpha,newVal)
            if beta <= alpha:
              self.cutoffs = self.cutoffs + 1
              #print("AB")
              break
        return maxEval
      # if currently the minimizing player (Red)
      
      else:
        minEval = 100000           
        for s in self.successors(board, whoseMove, die1, die2,plyLeft):
          newVal = self.minimax(s,alpha,beta,self.other(whoseMove), plyLeft-1, die1, die2)
          if(newVal < minEval):
              minEval = newVal
          if(plyLeft == self.max_depth and newVal == minEval):
              self.best_state = s
          #minEval = min(minEval,newVal)
          # only check for alpha beta if self.prune = True
          if (self.prune):
            beta = min(beta,newVal)
            if beta <= alpha:
              self.cutoffs = self.cutoffs + 1
              #print("AC")
              break
        return minEval

    def other(self, whoseMove):
        return 1 - whoseMove

    def successors(self, board, whose_move, die1, die2,plyLeft):
        original_state = board
        state_list = []
        #self.state_dict = {}
        #a = -1
        #while (a < 25):
        for a in range(26):
            #a = a + 1
            for j in range(26):
                current_state = original_state
                new_state = None
                #print(get_color(whose_move)+' to play...')
                #die1,die2 = toss(deterministic)
                #if deterministic: print("The result of the 'heavily biased' dice roll gives "+
                #       str(die1)+', '+str(die2))
                #else: print("The dice roll gives: "+str(die1)+', '+str(die2))

                # Moves the Piece
                #move is what gets returned by the user. Comma separated list?
                #2,2
                move = ""
                '''
                if(whose_move in board.bar):
                    move = "0,"
                    if(j == 25):
                        move = move + "p"
                    else:
                        move = move + str(j)
                    a = 26
                elif(a == 25):
                    move = "P"
                    if(j == 25):
                        move = move
                    else:
                        move = move +","+str(j)
                elif(j == 25):
                    move = str(a) + ",p"
                else:   
                    move= ""+str(a)+","+str(j)
                '''
                if((not a == 25) and (not j == 25)):
                    move = str(a) +","+ str(j)
                elif((not a == 25) and (j == 25)):
                    move = str(a) +",p"
                elif((a == 25) and (not j == 25)):
                    move = "p," + str(j)
                    #print(move)
                else:
                    move = "P"
                #print(get_color(whose_move), "moves from: ", move)
                if move in ["Q", "q"]:
                  #print('Agent '+get_color(whose_move)+' resigns. Game OVER!')
                  #forfeit(whose_move)
                  #break;
                  continue
                if move in ["P", "p"]:
                  #print(str(move))
                  #if "P" in move or "p" in move:
                  #print("true")  
                  #print('Agent '+get_color(whose_move)+' passes.')
                  if self.moves_exist(current_state, whose_move, die1, die2):
                    #print("Moves exist. Passing is not allowed!")
                    #forfeit(whose_move)
                    #break;
                    continue
                  else:
                    #print("OK. Pass is accepted for this turn.")
                    #a = 26
                    new_state = bgstate(current_state)
                    new_state.whose_move=1-whose_move
                    current_state = new_state
                    self.num_states = self.num_states + 1
                    if(plyLeft == self.max_depth):
                        self.state_dict[current_state] = move
                    yield current_state
                    #state_list.append(current_state)
                    #self.state_dict[current_state] = ""+str(a)+","+str(j)
                    #self.num_states = self.num_states + 1
                    #print(len(self.state_dict))
                    #a = 26
                    continue
                else:
                  #print("i am here")
                  try:
                    move_list = move.split(',')
                    if len(move_list)==3 and move_list[2] in ['R','r']:
                      dice_list = [die2, die1]
                    else:
                      dice_list = [die1, die2]
                    checker1, checker2 = move_list[:2]
                  except:
                    #print("Invalid type of move: ", move)
                    #forfeit(whose_move)
                    #break
                    continue
                  for i in range(2):
                    # Just in case the player wants to pass after the first checker is moved:
                    #print(i)
                    if i==1 and checker2 in ['P','p']:
                      #print(str(move))
                      #print("OK. Pass is accepted for the other die.")
                      new_state = bgstate(current_state)
                      new_state.whose_move=1-whose_move
                      current_state = new_state
                      self.num_states = self.num_states + 1
                      if(plyLeft == self.max_depth):
                          self.state_dict[current_state] = move
                      yield current_state
                      break
                    if checker1 == "p" or checker1 == "P":
                        continue
                    
                    pt = int([checker1, checker2][i])
                    #print(pt)
                    # Check first for a move from the bar:
                    if pt==0:
                      # Player must have a checker on the bar.
                      if not whose_move in current_state.bar:
                        #print("You don't have any checkers on the bar.")
                        #forfeit(whose_move)
                        #print("AD")
                        break
                        #continue
                      new_state = self.handle_move_from_bar(current_state, whose_move, dice_list[i])
                      if not new_state:
                        #print("Move from bar is illegal.")
                        #forfeit(whose_move)
                        break
                        #continue
                      current_state = new_state
                      continue
                    # Now make sure player does NOT have a checker on the bar.
                    if self.any_on_bar(current_state, whose_move):
                      #print("Illegal to move a checker from a point, when you have one on the bar.")
                      #forfeit(whose_move)
                      break
                      #continue
                    # Is checker available on point pt?
                    if pt < 1 or pt > 24:
                      #print(pt, "is not a valid point number.")
                      #forfeit(whose_move)
                      break
                      #continue
                    if not whose_move in current_state.pointLists[pt-1]:
                      #print("No "+get_color(whose_move)+" checker available at point "+str(pt))
                      #forfeit(whose_move)
                      break
                      #continue
                    # Determine whether destination is legal.
                    die = dice_list[i]
                    if whose_move==W:
                      dest_pt = pt + die
                    else:
                      dest_pt = pt - die
                    if dest_pt > 24 or dest_pt < 1:
                      born_off_state = self.bear_off(current_state, pt, dest_pt, whose_move)
                      if born_off_state:
                        current_state = born_off_state
                        if(i == 1):
                            self.num_states = self.num_states + 1
                            if(plyLeft == self.max_depth):
                                self.state_dict[current_state] = move
                            yield current_state
                        continue
                      #print("Cannot bear off this way.")
                      #forfeit(whose_move)
                      break
                      #continue
                   
                    dest_pt_list = current_state.pointLists[dest_pt-1]
                    if len(dest_pt_list) > 1 and dest_pt_list[0]!=whose_move:
                      #print("Point "+str(dest_pt)+" is blocked. You can't move there.")
                      #forfeit(whose_move)
                      break
                      #continue
                    # So this checker's move is legal. Update the state.
                    if not new_state:
                      new_state = bgstate(current_state)
                    # Remove checker from its starting point.
                    new_state.pointLists[pt-1].pop()
                    # If the destination point contains a single opponent, it's hit.
                    new_state = self.hit(new_state, dest_pt_list, dest_pt)
                    # Now move the checker into the destination point.
                    new_state.pointLists[dest_pt-1].append(whose_move)
                    current_state = new_state

                    #replace this with yield???
                    #state_list.append(current_state)
                    if(i == 1):
                        self.num_states = self.num_states + 1
                        if(plyLeft == self.max_depth):
                            self.state_dict[current_state] = move
                        yield current_state

                    
                    

                    #print(len(self.state_dict))
                    #self.num_states = self.num_states + 1
                    #state_dict[current_state] = ''+i+','+j
                    
        #return state_list
        #return state_dict.keys()      
                
    def move(self, state, die1, die2):
        #print("in move")
        self.state_dict = {}
        #self.move_dict = {}
        #self.setMaxPly(3)
        #self.useAlphaBetaPruning()
        #self.minimax(state, state.whose_move, self.max_depth, die1, die2)
        self.minimax(state, -1000000, 1000000, state.whose_move, self.max_depth, die1, die2)
        #print(str(self.state_dict[self.best_state]))
        #print(str(self.statesAndCutoffsCounts()))
        return self.state_dict[self.best_state]

        
        #ans = input("or enter Q to quit: ")
        #return ans
        #return "Q" # quit































    
    def hit(self, new_state, dest_pt_list, dest_pt):
      opponent = 1-new_state.whose_move
      if len(dest_pt_list)==1 and dest_pt_list[0]==opponent:
        if opponent==W:
          new_state.bar.insert(W, 0) # Whites at front of bar
        else:
          new_state.bar.append(R) # Reds at end of bar
        new_state.pointLists[dest_pt-1]=[]
      return new_state

    def bear_off(self, state, src_pt, dest_pt, who):
      # Return False if 'who' is not allowed to bear off this way.
      # Otherwise, create the new state showing the result of bearing
      # this one checker off, and return the new state.

      # First of all, is bearing off allowed, regardless of the dice roll?
      if not self.bearing_off_allowed(state, who): return False
      # Direct bear-off, if possible:
      pl = state.pointLists[src_pt-1]
      if pl==[] or pl[0]!=who:
        #print("Cannot bear off from point "+src(src_pt))
        return False
      # So there is a checker to possibly bear off.
      # If it does not go exactly off, then there must be
      # no pieces of the same color behind it, and dest
      # can only be one further away.
      good = False
      if who==W:
        if dest_pt==25:
           good = True
        elif dest_pt==26:
           for point in range(18,src_pt-1):
             if W in state.pointLists[point]: return False
           good = True
      elif who==R:
        if dest_pt==0:
           good = True
        elif dest_pt== -1:
           for point in range(src_pt, 6):
             if R in state.pointLists[point]: return False
           good = True
      if not good: return False 
      born_off_state = bgstate(state)
      born_off_state.pointLists[src_pt-1].pop()
      if who==W: born_off_state.white_off.append(W)
      else:  born_off_state.red_off.append(R)
      return born_off_state

    def forfeit(self, who):
      global DONE
      #print("Player "+get_color(who)+" forfeits the game and loses.")
      DONE = True

    def moves_exist(self, state, die1, die2, who):
      return False  # placeholder.

    def any_on_bar(self, state, who):
      return who in state.bar

    def remove_from_bar(self, new_state, who):
      #removes a white from start of bar list,
      # or a red from the end of the bar list.
      if who==W:
        del new_state.bar[0]
      else:
        new_state.bar.pop()
      #print("After removing a "+get_color(who)+" from the bar,")
      #print("  the bar is now: "+str(new_state.bar))

    def handle_move_from_bar(self, state, who, die):
      # We assume there is a piece of this color available on the bar.
      if who==W: target_point=die
      else: target_point=25-die
      pointList = state.pointLists[target_point-1]
      if pointList!=[] and pointList[0]!=who and len(pointList)>1:
         #print("Cannot move checker from bar to point "+str(target_point)+" (blocked).")
         return False
      new_state = bgstate(state)
      new_state = self.hit(new_state, pointList, target_point)
      self.remove_from_bar(new_state, who)
      new_state.pointLists[target_point-1].append(who)
      return new_state

    def bearing_off_allowed(self, state, who):
      # True provided no checkers of this color on the bar or in
      # first three quadrants.
      if self.any_on_bar(state, who): return False
      if who==W: point_range=range(0,18)
      else: point_range=range(6,24)
      pl = state.pointLists
      for i in point_range:
        if pl[i]==[]: continue
        if pl[i][0]==who: return False
      return True

    
      


    
