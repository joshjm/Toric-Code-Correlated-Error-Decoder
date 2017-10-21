import random

def type4(array,L,CorrLen):
    """creates a random walk with a set walk length"""
    movements = []
    Ri =  int(L/2) #with integer division, this should be the centre of an odd grid
    Rk =  int(L/2)
    walk=[] #this will be a list of tuples
    walk += [[Ri,Rk]] #create anyon
    i = 0 #set walk len counter-> could apply gauss dist here
    while i != CorrLen: #here we will just create the walk.

        dice = int(4*random.random()) #randomly choose move direction

        if dice==0:
            nextstep = [walk[i][0],walk[i][1] - 1]
            walk += [nextstep]

        if dice ==1 :
            nextstep = [walk[i][0],walk[i][1]+1]
            walk += [nextstep]

        if dice == 2:
            nextstep = [walk[i][0]-1,walk[i][1]]
            walk += [nextstep]

        if dice == 3:
            nextstep = [walk[i][0]+1,walk[i][1]]
            walk += [nextstep]

        i+=1
    return([walk[-1][0] - walk[0][0],walk[-1][1] - walk[0][1],walk[-1][0],walk[-1][1]])#return final position


def modpos(pos,L,move):
    """very similar to modcoord, but only for a LxL.
    takes as input walk[i][0] or walk[i][1]
    returns the pos modified with the move, accounting for PBCs."""
    pos += move
    # if pos == L: #moved off right or bottom
    #     return(0)
    # if pos == -1:#moved off top or left
    #     return(L-1)
    return(pos) #in the middle
