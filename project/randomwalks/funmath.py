
import numpy as np
import random
import subprocess
import math
import os
import matplotlib.mlab as mlab
import math
import matplotlib.pyplot as plt

#import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
"""this file contains all the function in the main code.
It is meant to allow the main function to read more easily/like
pseudocode."""

def getnormval(distance, expectedlength, codesize, strength, variance):
    """takes an input value for a mahatten distance, and returns a reduced
    distance if the distance is close to the correlation dist. Strength of
    falloff is proportional to normal distribution."""
    val = mlab.normpdf(distance, expectedlength, math.sqrt(variance))
    maxval = mlab.normpdf(expectedlength, expectedlength, math.sqrt(variance))
    val = -val*strength/maxval+1
    return(val*distance)

def adjustmatrix(zM, expectedlength, codesize, strength, variance):
    """This function takes a matrix as input and performs funmath.getnormval()
    on each element. """
    for i in range(zM.shape[0]):
        for j in range(zM.shape[1]):
            zM[i,j] = getnormval(zM[i,j], expectedlength, codesize, strength, variance)
    return(zM)


def randik(L):
    """randomized the value of Ri or Rj on a grid of dim L"""
    return(int(round(random.random()*L)) -1)
def randj():#could be combined with randik
    """randomized the value of Rj"""
    return(int(round(random.random()*1)))


def ApplyXErrors( ErrorNum,array,type,L,CorrLen):
    """Applies X-Errors to the an array for various error models"""

    if type == 1:
            #run across every element in the array
        for i in range(len(array[:,0,0])):
            for j in range(2):
                for k in range(len(array[0,0,:])):
                    if random.random() >1- 1.*ErrorNum/(L*L): #rand chance of bitflip
                        array[i,j,k] = -1*array[i,j,k] #apply bitflip if true
        return(array)

    elif type == 2:
        """creates a number of errors on the grid. rather than having a chance of
        getting a certain number of errors, this one doesnt stop generating errors
        until you get a specified number of error.
        Two flips on the one qubit is counted as one error. This model may need to
        be changed to count it as no error. But this isnt necessilarly needed."""
        numerrsLeft =  ErrorNum
        while numerrsLeft != 0:
            Ri =  int(round(random.random()*L)) -1
            Rj =  int(round(random.random()*1)) -1 #int(r.rand()*2)
            Rk =  int(round(random.random()*L)) -1
            if int(array[Ri,Rj,Rk]) == 1:
                array[Ri,Rj,Rk] = -1*array[Ri,Rj,Rk] #apply bitflip if true
                numerrsLeft += -1
        return(array)

    elif type == 4:
            """creates a random walk with a set walk length"""
            ErrorChains =  ErrorNum
            movements = []
            distances=[]
            while ErrorChains != 0: #this loop creates 1 chain
                Ri =  randik(L)#create start location of walk
                Rj =  randj()
                Rk =  randik(L)
                walk=[] #this will be a list of tuples
                walk += [[Ri,Rk]] #create anyon
                i = 0 #set walk len counter-> could apply gauss dist here
                while i != CorrLen: #here we will just create the walk.
                    nextstep=[]
                    dice = int(4*random.random()) #randomly choose move direction
                    if dice==0:
                        #if its intersecting the walk;
                        nextstep = [[walk[i][0],modpos(walk[i][1],L,-1)]]
                        walk += nextstep

                    if dice ==1 :
                        nextstep = [[walk[i][0],modpos(walk[i][1],L,+1)]]
                        walk += nextstep

                    if dice == 2:
                        nextstep = [[modpos(walk[i][0],L,-1),walk[i][1]]]
                        walk += nextstep

                    if dice == 3:
                        nextstep = [[modpos(walk[i][0],L,-1),walk[i][1]]]
                        walk += nextstep
                    i+=1
                ErrorChains += -1
                movements += [walk] #combine all walks
            return(GetFlippedPoints(movements,array))

    elif type == 5:
            """Self avoiding version of 4 (with self intersections)"""
            ErrorChains =  ErrorNum
            movements = []
            distances=[]
            while ErrorChains != 0: #this loop creates 1 chain
                Ri =  randik(L)
                Rj =  ()
                Rk =  randik(L)
                walk=[] #this will be a list of tuples
                walk += [[Ri,Rk]] #create anyon
                i = 0 #set walk len counter-> could apply gauss dist here
                while i != CorrLen: #here we will just create the walk.
                    nextstep=[]
                    dice = int(4*random.random()) #randomly choose move direction
                    if dice == 0:
                        #if its intersecting the walk;
                        nextstep = [[walk[i][0],modpos(walk[i][1],L,-1)]]
                        try:#if next step in walk:
                            if nextstep[0] in walk:
                                continue#try again.
                        except:#if not in walk:
                            pass#add to walk.
                        walk += nextstep

                    if dice == 1:
                        nextstep = [[walk[i][0],modpos(walk[i][1],L,+1)]]
                        try:
                            if nextstep[0] in walk:
                                continue
                        except:
                            pass
                        walk += nextstep

                    if dice == 2:
                        nextstep = [[modpos(walk[i][0],L,-1),walk[i][1]]]
                        try:
                            if nextstep[0] in walk:
                                continue
                        except:
                            pass
                        walk += nextstep

                    if dice == 3:
                        nextstep = [[modpos(walk[i][0],L,-1),walk[i][1]]]
                        try:
                            if nextstep[0] in walk:
                                continue
                        except:
                            pass
                        walk += nextstep
                    i+=1
                ErrorChains += -1
                movements += [walk] #combine all walks
            return(GetFlippedPoints(movements,array))
    elif type == 6:
            """fixed version of 4
            a walk of set length, with self intersections. this one also doesnt 'cancel itself out' when it crosses over itself NOT IMPLEMENTED YET"""
            ErrorChains =  ErrorNum
            movements = []
            distances=[]
            while ErrorChains != 0: #this loop creates 1 chain
                Ri =  randik(L)#create start location of walk
                Rj =  randj()
                Rk =  randik(L)
                walk=[] #this will be a list of tuples
                walk += [[Ri,Rj,Rk]] #create anyon
                i = 0 #set walk len counter-> could apply gauss dist here
                while i != CorrLen: #here we will just create the walk.

                    nextstep=[]
                    dice = int(4*random.random()) #randomly choose move direction
                    if dice==0:
                        if Rj == 0:
                            nextstep = [walk[i][0], walk[i][1]^1, modpos(walk[i][2],L,-1)]#removed extra bracket
                        if Rj == 1:
                            nextstep = [modpos(walk[i][0],L,-1), walk[i][1]^1, walk[i][2]]

                    if dice ==1 :
                        if Rj == 0:
                            nextstep = [modpos(walk[i][0],L,1), walk[i][1]^1, walk[i][2]]
                        if Rj == 1:
                            nextstep = [walk[i][0], walk[i][1]^1, walk[i][2]]

                    if dice == 2:
                        if Rj == 0:
                            nextstep = [modpos(walk[i][0],L,1), walk[i][1]^1, walk[i][2]]
                        if Rj == 1:
                            nextstep = [walk[i][0], walk[i][1]^1, modpos(walk[i][2],L,1)]

                    if dice == 3:
                        if Rj == 0:
                            nextstep = [walk[i][0], walk[i][1]^1, walk[i][2]]
                        if Rj == 1:
                            nextstep = [modpos(walk[i][0], L, -1) , walk[i][1]^1, modpos(walk[i][2],L,1)]
                    walk += [nextstep]
                    i+=1
                ErrorChains += -1
                movements += [walk] #combine all walk
            return(GetFlippedPoints3(movements,array))

def modpos(pos,L,move):
    """very similar to modcoord, but only for a LxL.
    takes as input walk[i][0] or walk[i][1]
    returns the pos modified with the move, accounting for PBCs."""
    pos += move
    if pos == L: #moved off right or bottom
        return(0)
    if pos == -1:#moved off top or left
        return(L-1)
    return(pos) #in the middle

'''
def plot(numsamples,LRange,errormode):
    """This just plots the data - not the graphical grid"""
    fig = plt.figure()
    ax = plt.subplot(111)

    for i in LRange:
        rawdata = np.loadtxt('data/'+'a'+str(numsamples)+'b'+str(i)+'c'+str(errormode)+'d'+str(errormode)+'.txt' , delimiter=',', skiprows=0, unpack=False)
        x = rawdata[:,0]plt
        plot8 = plt.plot(x,rawdata[:,1], label='size = '+str(i) )

    #plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.ylabel('Success Rate')
    if errormode ==1:
        plt.xlabel('Error Rate')
    elif errormode ==2:
        plt.xlabel('Average Number of errors')
    elif errormode == 3:
        plt.xlabel('Exact Number of errors')
    #funky legend stuff
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
    plt.legend(bbox_to_anchor=(1.05, 1),loc=2, borderaxespad=0.)

    plt.title('Success Rate of the Toric Code for various error rates')
    plt.grid(True)
    plt.savefig('figs/'+str(numsamples)+'.eps')
    plt.show()
'''
def CustomShortestPath(p1,p2,m,n):
    """This should be a faster way to find the shorest path, as we only have a
    cartesian grid. So Dijkstra might be overkill

    This function takes p1 and p2 in cartesian coords, and returns a simple
    path between them by correcting x pos. then y pos.

    this will not navigate around loss errors
q    --- returns a lst of the end points(stabilizer locations), along with all the
        stabilizers in the shortest path between them.
    """
    L = [m,n]
    custompath=[]
    custompath.append(list(p1)) #add the start positon
    randnum1 = int(random.random()*2)#generate a random order to correct in
    randnum2 = 0
    if randnum1 == 0:
        randnum2 = 1
    for i in [randnum1,randnum2]:
        while p1[i] != p2[i]: #havent reached end of path
            if p1[i] - p2[i]>0: #p1 to the right or below of p2
                if abs(p1[i]-p2[i]) > L[i] - abs(p1[i]-p2[i]):#if its faster to jump
                    if p1[i] == L[i]-1: #reached edge
                        p1[i] = 0
                    else:
                        p1[i] = p1[i]+1 #move closer to edge

                else: #if direct is faster
                    p1[i] = p1[i]-1 #move right or down
                custompath.append(list(p1))

            else: #p1 to the left or above of
                if abs(p1[i]-p2[i]) > L[i] - abs(p1[i]-p2[i]):#if faster to jump
                    if p1[i] == 0: #reached edge
                        p1[i] = L[i]-1
                    else:
                        p1[i] = p1[i]-1 #move closer to edge

                else:#if direct is faster
                    p1[i] = p1[i]+1 #move right or down
                custompath.append(list(p1))
    return(custompath)

def Measure_Syndrome(blankarray,m,n):
    """returns the syndrome of a qubits array of eigenvalues with errors"""
    #Generate syndrome
    PSyndrome = np.ones((m,n))
    h=0 #k
    w=0 #l
    for i in range(len(PSyndrome[:,0])):
        h=i
        if i ==len(PSyndrome[:,0])-1:#test for bottom row
                h = -1
        for j in range(len(PSyndrome[0,:])): #this counts across the first row, then down to the next [[1,2,3],[4,5,6]]
            w=j
            if j ==len(PSyndrome[0,:])-1:#test for bottom row
                    w=-1
            PSyndrome[i,j] = blankarray[h,0,w]*blankarray[h+1,0,w]*blankarray[h,1,w]*blankarray[h,1,w+1]
    return(PSyndrome)

def Manhatten_Distance(vertices,m,n):
    """This function takes a list of vertices and returns the manhatten
    distance between each pair of points in a 2D array"""
    vert =  np.array(vertices) #convert vertices into matrix #is this necessary?
    #this code gets the manhatten distance; taking into account periodic boundaries
    zM = np.zeros((len(vertices),len(vertices)))
    for i in range(len(vertices)):
        for j in range(len(vertices)):
            #need to test if distance over boundary is shorter than ~not
            x1 = vert[i][0]
            x2 = vert[j][0]
            y1 = vert[i][1]
            y2 = vert[j][1]
            xd1 = abs(x1 - x2)
            xd2 = abs(m - abs(x1 - x2))
            yd1 = abs(y1 - y2)
            yd2 = abs(n - abs(y1 - y2))
            d1 = min(xd1, xd2)#xdist
            d2 = min(yd1, yd2)#ydist

            zM[i,j] = d1 + d2
    return(zM)

def Degenerate_Distance(vertices,m,n):
    """This function takes a list of vertices and returns d_m-ln(Dm)"""
    vert =  np.array(vertices) #convert vertices into matrix #is this necessary?
    #this code gets the manhatten distance; taking into account periodic boundaries
    zM = np.zeros((len(vertices),len(vertices)))
    for i in range(len(vertices)):
        for j in range(len(vertices)):
            #need to test if distance over boundary is shorter than ~not
            x1 = vert[i][0]
            x2 = vert[j][0]
            y1 = vert[i][1]
            y2 = vert[j][1]
            xd1 = abs(x1 - x2)
            xd2 = abs(m - abs(x1 - x2))
            yd1 = abs(y1 - y2)
            yd2 = abs(n - abs(y1 - y2))
            d1 = min(xd1, xd2)#xdist
            d2 = min(yd1, yd2)#ydist

            Dm = math.factorial(d1+d2)/(math.factorial(d1)*math.factorial(d2))
            zM[i,j] = 2*(d1 + d2)-math.log(Dm) #`2' comes from eq 14 TOM.S

    return(zM)

def FindDefects(PSyndrome):
    """This code takes a syndrom measurement and adds the cartesian location
    of any -1 eigenvalues to a list"""
    vertices =[] #error locations
    for i in range(len(PSyndrome[:,0])):
        for j in range(len(PSyndrome[0,:])):
            if PSyndrome[i,j] == -1:
                vertices.append((i,j))
    return(vertices)

def GetFlippedPoints(paths,array):
    """This code takes the shortest paths and outputs the qubits that are in them
    this allows me to tell which qubits to flip.

    Neatly returns the bits that need to be flipped in the same form as the
    matrix they were generated on

    **this has been updated to work for 3D paths for the 3D array"""
    #this may not work for double ups?

    for i in paths:
        jprev = i[0]
        for j in i[1:]:
            if abs(j[0] - jprev[0])>1:#top/bottom edge jump
                array[jprev[0]][j[1]][jprev[1]] *=-1
            elif abs(j[2] - jprev[2])>1:#left/right edge jumps
                if (j[2] - jprev[2])<0:#off right edge
                    array[j[0]][j[1]][j[2]] *=-1
                elif j[2] - jprev[2]>0:#off left edge
                    array[jprev[0]][j[1]][jprev[2]] *=-1
            elif j[0] - jprev[0]==1:#vertical down movement
                array[j[0]][j[1]][j[2]] *=-1
            elif j[0] - jprev[0]==-1:#vertical up movement
                array[jprev[0]][j[1]][jprev[2]] *=-1
            elif j[2] - jprev[2]==1:#right movement
                array[j[0]][j[1]][j[2]] *=-1
            elif j[2] - jprev[2]==-1:#left movement #Edoesnt get called? int/float error?
                array[jprev[0]][j[1]][jprev[2]] *=-1
            jprev=j
    return(array)

def GetFlippedPoints2(paths,blankarray):
    """THIS ONE IS FOR TAKING A 2D GRID OF POINTS. 2D PATHS. 2D ARRAY"""
    #this may not work for double ups?
    for i in paths:
        jprev = i[0]
        for j in i[1:]:
            if abs(j[0] - jprev[0])>1:#top edge jump
                blankarray[jprev[0]][0][jprev[1]] =-1
            elif abs(j[1] - jprev[1])>1:#left/right edge jumps
                if (j[1] - jprev[1])<0:#off right edge
                    blankarray[j[0]][1][j[1]] =-1
                elif j[1] - jprev[1]>0:#off left edge
                    blankarray[jprev[0]][1][jprev[1]] =-1
            elif j[0] - jprev[0]==1:#vertical down movement
                blankarray[j[0]][0][j[1]] =-1
            elif j[0] - jprev[0]==-1:#vertical up movement
                blankarray[jprev[0]][0][jprev[1]] =-1
            elif j[1] - jprev[1]==1:#right movement
                blankarray[j[0]][1][j[1]] =-1
            elif j[1] - jprev[1]==-1:#left movement #Edoesnt get called? int/float error?
                blankarray[jprev[0]][1][jprev[1]] =-1
            jprev=j
    return(blankarray)

def GetFlippedPoints3(paths,array):
    """same as first version, but doesnt flip locations: just sets to -1
    used for random walks with self intersections - err type 6"""
    #this may not work for double ups?

    for i in paths:
        jprev = i[0]
        for j in i[1:]:
            if abs(j[0] - jprev[0])>1:#top/bottom edge jump
                array[jprev[0]][j[1]][jprev[1]] =-1
            elif abs(j[2] - jprev[2])>1:#left/right edge jumps
                if (j[2] - jprev[2])<0:#off right edge
                    array[j[0]][j[1]][j[2]] =-1
                elif j[2] - jprev[2]>0:#off left edge
                    array[jprev[0]][j[1]][jprev[2]] =-1
            elif j[0] - jprev[0]==1:#vertical down movement
                array[j[0]][j[1]][j[2]] =-1
            elif j[0] - jprev[0]==-1:#vertical up movement
                array[jprev[0]][j[1]][jprev[2]] =-1
            elif j[2] - jprev[2]==1:#right movement
                array[j[0]][j[1]][j[2]] =-1
            elif j[2] - jprev[2]==-1:#left movement #Edoesnt get called? int/float error?
                array[jprev[0]][j[1]][jprev[2]] =-1
            jprev=j
    return(array)
##
## beyond here is misc.
#dijkstra shortest paths
def FindShortestPath(graph, start, end, path=[]):
    """This is code I found online to find shortest paths. It should take all
    edge weights as 1? I thik this is dijkstra. I had trouble implementing
    other dijkstra code

    From website:
    Note that while the user calls find_graph() with three arguments, it calls
    itself with a fourth argument: the path that has already been traversed.
    The default value for this argument is the empty list, '[]', meaning no
     nodes have been traversed yet. This argument is used to avoid cycles

     This is slow and should only be used when losses are present"""
    path = path + [start]
    if start == end:
        return path
    if start not in graph:
        return None
    shortest = None
    for node in graph[start]:
        if node not in path:
            newpath = FindShortestPath(graph, node, end, path)
            if newpath:
                if not shortest or len(newpath) < len(shortest):
                    shortest = newpath
    return shortest

def ploterror(ErrorArray,PSyndrome,paths,vertices,CorrectionArray):
    """Given an error array, this will graphically plot which qubits have error"""
    height = len(ErrorArray[:,0,0])
    width = len(ErrorArray[0,0,:])
    scale = 100
    radius = 5
    image = Image.new('RGB', (width*scale, height*scale ))
    draw = ImageDraw.Draw(image)
    draw.rectangle((0,0, width*scale-1,height*scale-1), outline = 'white')
    l=3
    #draw qubits
    for i in range(len(ErrorArray[:,0,0])):
        for j in range(2):
            for k in range(len(ErrorArray[0,0,:])):
                #draw qubits with error
                if ErrorArray[i,j,k] == -1:
                    if j ==0:#vertical lines
                        draw.ellipse(((k+0.75)*scale-radius,(i+0.25)*scale-radius,(k+0.75)*scale+radius,(i+0.25)*scale+radius), fill = 'red', outline ='red')
                        draw.line(((k+0.75)*scale-l,(i+0.25-0.5)*scale,(k+0.75)*scale-l,(i+0.25+0.5)*scale), fill = 'red',width = 2)
                        if i == 0 :
                            draw.line(((k+0.75)*scale-l,height*scale,(k+0.75)*scale-l,height*scale-0.25*scale), fill = 'red',width = 2)
                    else:#horizontal lines
                        draw.ellipse(((k+0.25)*scale-radius,(i+0.75)*scale-radius,(k+0.25)*scale+radius,(i+0.75)*scale+radius), fill = 'red', outline ='red')
                        draw.line(((k+0.25-0.5)*scale,(i+0.75)*scale-l,(k+0.25+0.5)*scale,(i+0.75)*scale-l), fill = 'red',width = 2)
                        if k == 0 :
                            draw.line((width*scale,(i+0.75)*scale-l,width*scale - 0.2*scale,(i+0.75)*scale-l), fill = 'red',width = 2)
                #draw qubits free of error
                else:
                    if j ==0:
                        draw.ellipse(((k+0.75)*scale-radius,(i+0.25)*scale-radius,(k+0.75)*scale+radius,(i+0.25)*scale+radius), fill = 'blue', outline ='blue')
                    else:
                        draw.ellipse(((k+0.25)*scale-radius,(i+0.75)*scale-radius,(k+0.25)*scale+radius,(i+0.75)*scale+radius), fill = 'blue', outline ='blue')

    #draw line between matching points
        #doesnt yet draw matches over boundaries correctly
    for i in paths:
        list2=[]
        for x in i:
            for y in x:
                list2.append((y+(0.75))*scale)
        #test if the distance moved is larger than 1 -> jumpes over the edge

            #need to run for all pairs of points
        list3=list(list2)
        part1=[]
        part2=[]
        colour = randcolour()

    #draw corrections
    for i in range(len(CorrectionArray[:,0,0])):
        for j in range(2):
            for k in range(len(CorrectionArray[0,0,:])):
                #draw qubits with error
                if CorrectionArray[i,j,k] == -1:
                    if j ==0:#vertical lines
                        draw.line(((k+0.75)*scale+l,(i+0.25-0.5)*scale,(k+0.75)*scale+l,(i+0.25+0.5)*scale), fill = 'yellow',width = 2)
                        if i == 0 :
                            draw.line(((k+0.75)*scale+l,height*scale,(k+0.75)*scale+l,height*scale-0.25*scale), fill = 'yellow',width = 2)
                    else:#horizontal lines
                        draw.line(((k+0.25-0.5)*scale,(i+0.75)*scale+l,(k+0.25+0.5)*scale,(i+0.75)*scale+l), fill = 'yellow',width = 2)
                        if k == 0 :
                            draw.line((width*scale,(i+0.75)*scale+l,width*scale - 0.2*scale,(i+0.75)*scale+l), fill = 'yellow',width = 2)
    #draw stabilizers
    for i in range(len(PSyndrome[:,0])):
        for j in range(len(PSyndrome[0,:])):
            if PSyndrome[i,j] == -1:
                draw.rectangle(((j+0.75)*scale-radius,(i+0.75)*scale-radius,(j+0.75)*scale+radius,(i+0.75)*scale+radius), fill = 'green', outline = 'green')
                #draw.text(((j+0.75)*scale,(i+0.75)*scale),'-')
            else:
                draw.text(((j+0.75)*scale,(i+0.75)*scale),'+')
            draw.text(((j+0.6)*scale,(i+0.85)*scale),'('+str(i)+','+str(j)+')')

    image.save('graphicaloutput.png')   #Keep at the end!

def clear_all():
    """Clears all the variables from the workspace of the spyder application."""
    gl = globals().copy()
    for var in gl:
        if var[0] == '_': continue
        if 'func' in str(globals()[var]): continue
        if 'module' in str(globals()[var]): continue

        del globals()[var]

#timers for code
def tic():
    """Homemade version of matlab tic and toc functions"""
    import time
    global startTime_for_tictoc
    startTime_for_tictoc = time.time()

def toc():
    import time
    if 'startTime_for_tictoc' in globals():
        print("Elapsed time is " + str(time.time() - startTime_for_tictoc) + " seconds.")
    else:
        print("Toc: start time not set")


def createarray(m,n):
    """ creates a 3D array with dimensions m*2*n. This is done to because qubits
    are offset in the toric grid. So a 2D grid gets logically messy. This is a
    way to absorb the odd and even rows into the same row/position. This also
    makes calculating stabilizers easier.
    ex:
    |    q       q       q       q  | 0
    |q   s   q   s   q   s   q   s  | 1
    |    q       q       q       q  | 0
    |q   s   q   s   q   s   q   s  | 1
    """
    return( np.ones((m,2,n)) )

def FindAllPaths(graph, start, end, path=[]):
    """finds all paths of all lengths, but only visiting each node a maximum
    of 1 time. I could compute this, and look for all paths with the same length
    as the shortest path, to find how degenerate it is.

    This is likely super slow. So be careful with useage """
    path = path + [start]
    if start == end:
        return [path]
    if start not in graph:
        return None
    paths = []
    for node in graph[start]:
        if node not in path:
            newpaths = find_all_paths(graph, node, end, path)
            for newpath in newpaths:
                paths.append(newpath)
    return paths

def randcolour():
    """creates a random 3-tuple of integers between 0-255. If the total
    brightness isnt high enough, it tries again"""
    colour = [0,0,0]
    while sum(colour)<450:
        for i in range(3):
            colour[i] = int(random.random()*255)
    return(tuple(colour))

def CreateGraph(m,n,refarray):
    """create a dict for the dijkstra algoirthm. each point is connected to the
    4 adjacent. This is where i include the edges over the periodic boundary

    nearest neighbours for each point"""
    IDs = list(range(1,m*n+1))
    for i in range(len(IDs)):
        IDs[i] = str(IDs[i])
    dict1 = {}#init dict
    # create an array of m*n, counting up (reference matrix)
    # refarray = np.zeros((m,n))
    # counter = 1
    # for i in range(len(refarray[:,0])):
    #     for j in range(len(refarray[0,:])):
    #         refarray[i,j] = counter
    #         counter +=1

    counter = 0
    for i in range(m): #height
        for j in range(n): #width

            dict2 = {}#init dict
            #will need to include distances over edges
                    #cases: edges (4), middle(1), corners(4)
                        #9 if statements? or easier way?

            if i != 0 and i != m-1 and j != 0 and j != n-1: #any point not on edge or middle

                above = refarray[i-1,j]
                below = refarray[i+1,j]
                left =  refarray[i,j-1]
                right = refarray[i,j+1]

            #keep corners above edges!
            elif i==0 and j==0: #top left corner
                above = refarray[m-1,j]
                below = refarray[i+1,j]
                left =  refarray[i,n-1]
                right = refarray[i,j+1]
            elif i==0 and j==n-1: #top right corner
                above = refarray[m-1,j]
                below = refarray[i+1,j]
                left =  refarray[i,j-1]
                right = refarray[i,0]
            elif i==m-1 and j==0: #bottom left corner
                above = refarray[i-1,j]
                below = refarray[0,j]
                left =  refarray[i,n-1]
                right = refarray[i,j+1]
            elif i==m-1 and j==n-1: #bottom right corner
                above = refarray[i-1,j]
                below = refarray[0,j]
                left =  refarray[i,j-1]
                right = refarray[i,0]

            elif i == 0: #top edge ~corners
                above = refarray[m-1,j] #[row,col]
                below = refarray[i+1,j]
                left =  refarray[i,j-1]
                right = refarray[i,j+1]
            elif i==m-1: #bottom edge ~corners
                above = refarray[i-1,j]
                below = refarray[0,j]

                left =  refarray[i,j-1]
                right = refarray[i,j+1]
            elif j==0: #left edge ~corners
                above = refarray[i-1,j]
                below = refarray[i+1,j]
                left =  refarray[i,n-1]
                right = refarray[i,j+1]
            elif j==n-1: #right edge ~corners
                above = refarray[i-1,j]
                below = refarray[i+1,j]
                left =  refarray[i,j-1]
                right = refarray[i,0]

            dict1[IDs[counter]] = [str(int(above)),str(int(below)),str(int(right)),str(int(left))]
            counter+=1
    return(dict1)


if __name__ == '__main__':
    """if you put something in 'main' it will only run if the file
    is run; and not when the file is imported. """
    normdist()
