'''Farmer_Fox.py
by Russell Kook
UWNetID: Russkook
Student number: 1620672

Assignment 2, in CSE 415, Winter 2020.
 
This file contains my problem formulation for the problem of
the Farmer, Fox, Chicken, and Grain.
'''

#<METADATA>
SOLUZION_VERSION = "1.0"
PROBLEM_NAME = "Farmer, Fox, Chicken, and Grain"
PROBLEM_VERSION = "1.0"
PROBLEM_AUTHORS = ['R. Kook']
PROBLEM_CREATION_DATE = "13-JAN-2020"

#<COMMON_CODE>
Fa=0  # array index to access Farmer
Fo=1  # index for Fox 
C=2   # index for Chicken
G=3   # index for Grain  
LEFT=0 # same idea for left side of river
RIGHT=1 # etc.

class State():

  def __init__(self, d=None):
    if d==None:
#                     Fa    Fo     C     G
      d = {'people':[[0,0],[0,0],[0,0],[0,0]],
#                     L,R   L,R   L,R   L,R
           'boat':LEFT}
    self.d = d

  def __eq__(self,s2):
    for prop in ['people', 'boat']:
      if self.d[prop] != s2.d[prop]: return False
    return True

  def __str__(self):
    # Produces a textual description of a state.
    p = self.d['people']
    txt = "\n Fa on left:"+str(p[Fa][LEFT])+"\n"
    txt += " Fo on left:"+str(p[Fo][LEFT])+"\n"
    txt += " C on left:"+str(p[C][LEFT])+"\n"
    txt += " G on left:"+str(p[G][LEFT])+"\n"
    txt += "   Fa on right:"+str(p[Fa][RIGHT])+"\n"
    txt += "   Fo on right:"+str(p[Fo][RIGHT])+"\n"
    txt += "   C on right:"+str(p[C][RIGHT])+"\n"
    txt += "   G on right:"+str(p[G][RIGHT])+"\n"
    side='left'
    if self.d['boat']==1: side='right'
    txt += " boat is on the "+side+".\n"
    return txt

  def __hash__(self):
    return (self.__str__()).__hash__()

  def copy(self):
    # Performs an appropriately deep copy of a state,
    # for use by operators in creating new states.
    news = State({})
    news.d['people']=[self.d['people'][Fa_or_Fo_or_C_or_G][:] for Fa_or_Fo_or_C_or_G in [Fa, Fo, C, G]]
    news.d['boat'] = self.d['boat']
    return news 

#inputs fa, fo, c, g are what you want to move
#X_available is whats avaliable at said side of river
  def can_move(self,fa,fo,c,g):
    '''Tests whether it's legal to move the boat and take
     m missionaries and c cannibals.'''
    side = self.d['boat'] # Where the boat is.
    p = self.d['people']

    ##checking that you arn't taking zero of animal
    #Farmer present check
    if fa<1: return False # Need an fa to steer boat.
    fa_available = p[Fa][side] 
    if fa_available < fa: return False # Can't take more fa's than available
    #Fox present check
    fo_available = p[Fo][side]    
    if fo_available < fo: return False # Can't take more fo's than available
    #Chicken present check
    c_available = p[C][side]    
    if c_available < c: return False # Can't take more c's than available
    #Grain present check
    g_available = p[G][side]    
    if g_available < g: return False # Can't take more g's than available    

    ##calculating remaining animals after requested move
    #remaining = available - what youre taking 
    fa_remaining = fa_available - fa
    fo_remaining = fo_available - fo
    c_remaining = c_available - c
    g_remaining = g_available - g
    #amount of animals on arriving side
    fa_at_arrival = p[Fa][1-side]+fa
    fo_at_arrival = p[Fo][1-side]+fo
    c_at_arrival = p[C][1-side]+c
    g_at_arrival = p[G][1-side]+g


    ##fox and chicken cannot be left alone on either side
    #current side
    if (fa_remaining == 0 and g_remaining == 0 and c_remaining > 0
        and fo_remaining == c_remaining): return False
    #next side
    if (fa_at_arrival == 0 and g_at_arrival == 0 and c_at_arrival > 0
        and fo_at_arrival == c_at_arrival): return False
    ##chicken and grain cannot be left alone on either side
    #current side
    if (fa_remaining == 0 and fo_remaining == 0 and c_remaining > 0
        and g_remaining == c_remaining): return False
    #next side
    if (fa_at_arrival == 0 and fo_at_arrival == 0 and c_at_arrival > 0
        and g_at_arrival == c_at_arrival): return False

    return True


  def move(self,fa,fo,c,g):
    '''Assuming it's legal to make the move, this computes
     the new state resulting from moving the boat carrying
     m missionaries and c cannibals.'''
    news = self.copy()      # start with a deep copy.
    side = self.d['boat']         # where is the boat?
    p = news.d['people']          # get the array of arrays of people.
    p[Fa][side] = p[Fa][side]-fa     # Remove people from the current side.
    p[Fo][side] = p[Fo][side]-fo
    p[C][side] = p[C][side]-c
    p[G][side] = p[G][side]-g
    p[Fa][1-side] = p[Fa][1-side]+fa # Add them at the other side.
    p[Fo][1-side] = p[Fo][1-side]+fo
    p[C][1-side] = p[C][1-side]+c
    p[G][1-side] = p[G][1-side]+g
    news.d['boat'] = 1-side       # Move the boat itself.
    return news

def goal_test(s):
  '''If Fa,Fo,C,G are on the right, then s is a goal state.'''
  p = s.d['people']
  return (p[Fa][RIGHT] == 1 and p[Fo][RIGHT] == 1 and
          p[C][RIGHT] == 1 and p[G][RIGHT] == 1)
   

def goal_message(s):
  return "Congratulations on successfully guiding the farmer, fox, chicken and grain across the river!"


class Operator:
  def __init__(self, name, precond, state_transf):
    self.name = name
    self.precond = precond
    self.state_transf = state_transf
    
  def is_applicable(self, s):
    return self.precond(s)

  def apply(self, s):
    return self.state_transf(s)

#<INITIAL_STATE>
CREATE_INITIAL_STATE = lambda : State(d={'people':[[1, 0], [1, 0], [1, 0], [1, 0]], 'boat':LEFT })
#</INITIAL_STATE>

#Combinations in the boat
#<OPERATORS>
combinations = [(1,0,0,0),(1,1,0,0),(1,0,1,0),(1,0,0,1)]

OPERATORS = [Operator(
  "Cross the river with "+str(fa)+" farmer and "+str(fo)+" fox and "+str(c)+" chicken and "+str(g)+" grain",
  lambda s, fa1=fa, fo1=fo, c1=c, g1=g: s.can_move(fa1,fo1,c1,g1),
  lambda s, fa1=fa, fo1=fo, c1=c, g1=g: s.move(fa1,fo1,c1,g1) )
  for (fa,fo,c,g) in combinations]
#</OPERATORS>

#<GOAL_TEST> (optional)
GOAL_TEST = lambda s: goal_test(s)
#</GOAL_TEST>

#<GOAL_MESSAGE_FUNCTION> (optional)
GOAL_MESSAGE_FUNCTION = lambda s: goal_message(s)
#</GOAL_MESSAGE_FUNCTION>

# Put your formulation of the Farmer-Fox-Chicken-and-Grain problem here.
# Be sure your name, uwnetid, and 7-digit student number are given above in 
# the format shown.

