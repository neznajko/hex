#! /usr/bin/env python3
import numpy as np
from math import inf
from itertools import product
########################################################
########################################################
###o....o....o....:....o### = i,j ######################
###.   ..   ..   ..   ..################################
###.  . .  . .  . .  . .### % i-1,j ####################
###. .  . .  . .  . .  .################# : i-2,j+1 ####
###..   ..   ..   ..   .### < i-1,j+1 ##################
###o....)....%....<....|################# | i-1,j+2 ####
###.   ..   ..    .   ..### , i,j+1 ####################
###.  . .  . .  . .  . .################# / i+1,j+1 ####
###. .  . .  . .  . .  .### > i+1,j ####################
###..   ..   ..   ..   .################# * i+2,j-1 ####
###o....@....=....,....o### \ i+1,j-1 ##################
###.   ..   ..   ..   ..################# ? i+1,j-2 ####
###.  . .  . .  . .  . .### @ i,j-1 ####################
###. .  . .  . .  . .  .################# ) i-1,j-1 ####
###..   ..   ..   ..   .################################
###?....\....>..../....o################################
###.   ..   ..   ..   ..### near nbors \\ far nbors ####
###.  . .  . .  . .  . .################################
###. .  . .  . .  . .  .################################
###..   ..   ..   ..   .################################
###o....*....o....o....o################################
################################ ck V ######## ck V ####
########################################################
# moowing clockwise 
near=((-1,-0), # %
      (-1,+1), # <
      (+0,+1), # ,
      (+1,-0), # >
      (+1,-1), # \ 
      (-0,-1)) # @
far=((-2,+1), # : 0,1 near nbors
     (-1,+2), # | 1,2
     (+1,+1), # / 2,3
     (+2,-1), # * 3,4
     (+1,-2), # ? 4,5
     (-1,-1)) # ) 5,0
# convert to numpy array so we can use addition
near = tuple(map(np.array,near))
far  = tuple(map(np.array,far))
# Python Enum jst sucks
BLACK=0
WHITE=1
EMPTY=2
def makeframe(board):
# Ok so we represent hex board as 2D numpy array
# plus additional borders colored accordingly to
# players, so we can thread connectivity exactly.
    pos = len(board), 0
    for j in BLACK, WHITE:
        for p in pos:
            board = np.insert(board, p, j, axis=j)
    for i in 0,-1:
      for j in 0,-1:
        board[i,j] = EMPTY
    return board

def newboard(size):
    board = np.full((size,)*2, EMPTY)
    return makeframe(board)

def load(filename):
# Load position from filename. 
    board = np.loadtxt(filename, dtype=int)
    return makeframe(board)

NOFDIR=6 # Number of Directions

def getnbors(v, board, diR):
# Return nbors in the given direction, that have
# same colour as v. If near nbors (left, ryte) are
# EMPTY ck the far nbor.
    left = diR
    # cycle
    if left < NOFDIR - 1:
        ryte = left + 1
    else:
        ryte = 0
    nearnbors = [tuple(v + near[j]) for j in (left, ryte)]
    e = 0 # empty counter
    ls = []
    for u in nearnbors:
        if board[u] == board[v]:
            ls.append(u)
        elif board[u] == EMPTY:
            e += 1
    if e == 2:
        u = tuple(v + far[diR])
        if board[u] == board[v]: 
            ls.append(u)
    return ls

def engarde(v, board):
# ck vhether v is a border vertex
    if min(v) == 0: return True
    if max(v) == len(board) - 1: return True
    return False
  
def explore(v, board, x, cc):
    x[v] = True # mark as visited
    c = board[v] # colour
    cc[-1].append(v[c]) # append only one componend
    if engarde(v, board): return
    for diR in range(NOFDIR):
        for u in getnbors(v, board, diR):
            if x[u] == False: explore(u, board, x, cc)

def dfs(board, colour):
    x = np.full(board.shape, False) # visited
    cc = [] # connect counter
    for v, c in np.ndenumerate(board): # vertex, board colour
        if engarde(v, board): continue
        if x[v] == False and c == colour:
            cc.append([])
            explore(v, board, x, cc)
    return cc

def getrange(path):
    path.sort()
    return path[-1] - path[0]

def maxrange(cc):
    if cc:
        return max(map(getrange, cc))
    else: return 0

diCt = {} # lookup of known positions
def key(a): return hash(a.tobytes())

def evaluate(board):
    ccw = dfs(board, WHITE)
    ccb = dfs(board, BLACK)
    value = maxrange(ccw) - maxrange(ccb)
    diCt[key(board)] = value
    return value

def maxi(board, depth):
    if depth == 0: return evaluate(board)
    maxscore = -inf
    R = range(1, len(board) - 1)
    # loop over all possible moos
    for v in product(R, R):
        if board[v] != EMPTY: continue
        # make a moo
        board[v] = WHITE
        # ck vhether it's known position
        k = key(board)
        if k in diCt:
            score = diCt[k]
        else:
            score = mini(board, depth-1)
            diCt[k] = score
        if score > maxscore: maxscore = score
        # undo moo
        board[v] = EMPTY
    return maxscore

def mini(board, depth):
# This is a bit of repetition, but for first blood it's OK.
    if depth == 0: return evaluate(board)
    minscore = inf
    R = range(1, len(board) - 1)
    # loop over all possible moos
    for v in product(R, R):
        if board[v] != EMPTY: continue
        # make a moo
        board[v] = BLACK
        # ck vhether it's known position
        k = key(board)
        if k in diCt:
            score = diCt[k]
        else:
            score = maxi(board, depth-1)
            diCt[k] = score
        if score < minscore: minscore = score
        # undo moo
        board[v] = EMPTY
    return minscore

if __name__ == '__main__':
    board = load('NPUT') 
    print(board)
    if 0: import pdb; pdb.set_trace()
    u = (-1, -1)
    maxscore = -inf
    depth = 3
    R = range(1, len(board) - 1)
    for v in product(R, R):
        if board[v] != EMPTY: continue
        board[v] = WHITE
        score = mini(board, depth)
        if score > maxscore:
            maxscore = score
            u = v
        board[v] = EMPTY
    print(u, maxscore)
      
# log:
