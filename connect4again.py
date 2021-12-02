import copy
import random
from matplotlib import pyplot as plt
from matplotlib import animation
from numpy.random import random as rnd
import numpy as np

import mnetworks
import network

# Written for python 3.7


class Gameboard(object):
    '''
    defines the gameboard, its properties and its functionality
    '''
    def __init__(self,dimensionx,dimensiony,show=True):
        '''
        takes the arguments from object creation and impliments them as values within the object
        '''
        self.gameboard = []
        self.height = dimensiony #defines the height of the gameboard
        self.width = dimensionx #defines the width of the board
        self.NoOfMoves = 0
        self.display=show
        for row in range(dimensiony): #generates the correct number of rows
            row = []
            for position in range(dimensionx):
                row.append("") #creates an empty position in the row
            self.gameboard.append(row) #adds the row to the gameboard

        pass

    def insertpiece(self, column, piecesymbol):
        '''
        inserts a specified piece into the board in the specified column in the board
        '''
        column = column - 1
        piece = False #has not been placed yet
        for i in range(self.height-1,-1,-1): #counts up through the column to find the lowest point at which to insert the
                                           #piece
            if piece == False and self.gameboard[i][column]== "": #if piece has not been placed yet and the position is empty
                self.gameboard[i][column] = piecesymbol
                piece = True #Marks piece as placed
        if piece == False:
            return False #only flags for an illegal move
        else:
            self.NoOfMoves += 1 #adds one to the move counter
            self.show(self.display) #shows updated gameboard
            return True
        pass

    def show(self,show=True):
        '''
        displays the board in a user friendly way
        '''
        if show == True:
            for row in self.gameboard:
                print(row) #prints each row on a new line
            print("") #adds a new line for clarity
        pass

    def returnforinput(self,playersym,opponentsym):
        '''
        Returns the state of the gameboard for reading by a neural network
        '''
        inpt = []
        for y in range(0,6):
            for x in range(0,7):
                if self.gameboard[y][x] == "": #empty space is represented by a 1
                    inpt.append(1)
                elif self.gameboard[y][x] == playersym: #own piece is represented by the value 0.5
                    inpt.append(0.5)
                elif self.gameboard[y][x] == opponentsym: #opponents piece is represented by the value of -0.5
                    inpt.append(-0.5)
        return inpt #returns the board in NN format

    def checkwin(self):
        '''
        checks to see if the board has suffered a winning move, and returns the board with the winning connect four pieces highlighted
        '''
        #look for all poosible game pieces
        pieces = []
        for row in self.gameboard:
            for position in row:
                if position != "" and position not in pieces:
                    pieces.append(position) #adds one iteration of each piece found to the list pieces
        pieceswon = []
        checks = []
        if pieces != []: #only runs if there is a piece on the board
            #horizontal check
            rowno = 0
            for r in self.gameboard:
                for c in range(0,self.width):
                    try:
                        if row[c] != "":
                            connect = True #so far it is possible to be four in a row
                            for i in range(1,4):
                                if row[c] != row[c + i]:
                                    connect = False #if one of the next three tiles in the row is not the same piece or is empty,
                                                #it is not connect 4 and therefore correct is false
                        else:
                            connect = False
                    except IndexError:
                        connect = False #if there are not three more pieces available after this piece, it cannot be a
                                        #connect 4 and therefore must be false
                    if connect == True: #if four in a row is true:
                        checks.append(["horizontal",copy.copy(self.gameboard[rowno][c]),[copy.copy(rowno),copy.copy(c)]]) #appends the type of win, the piece that won, and coordinates to the list
                rowno += 1
                                           
            #vertical check - works same as above with different variables

            for column in range(0,self.width):
                for position in range(0,self.height):
                    try:
                        if self.gameboard[position][column] != "":
                            piece = self.gameboard[position][column]
                            connect = True
                            for i in range(1,4):
                                if self.gameboard[position][column] != self.gameboard[position + i][column]:
                                    connect = False
                        else:
                            connect = False
                    except IndexError:
                       connect = False
                    if connect == True:
                        checks.append(["vertical",copy.copy(piece),[copy.copy(position),copy.copy(column)]]) #appends the type of win, the piece that won, and coordinates to the list

		    #diagonal down

            for r in range(0,self.height):
                for c in range(0,self.width):
                    try:
                        if self.gameboard[r][c] != "":
                            connect = True
                            piece = self.gameboard[position][column]
                            for i in range(1,4):
                                if self.gameboard[r + i][c + i] != self.gameboard[r][c]:
                                    connect = False
                        else:
                            connect = False
                    except IndexError:
                        connect = False
                    if connect == True:
                        checks.append(["d-down",copy.copy(piece),[copy.copy(r),copy.copy(c)]]) #appends the type of win, the piece that won, and coordinates to the list

            #diagonal up

            for r in range(0,self.height):
                for c in range(0,self.width):
                    if self.gameboard[r][c] != "":
                        connect = True
                    else:
                        connect = False
                    try:
                        for i in range(1,4):
                            if self.gameboard[r + i][c - i] != self.gameboard[r][c]:
                                connect = False
                    except IndexError:
                        connect = False
                    if connect == True:
                        checks.append(["d-up",copy.copy(piece),[copy.copy(r),copy.copy(c)]]) #appends the type of win, the piece that won, and coordinates to the list

            if len(checks) > 0: #if the board has been won, capitalises the winning pieces
                for each in checks:
                    if each[0] == "horizontal":
                        for i in range(0,4):
                            self.gameboard[each[2][0]][each[2][1] + i] = self.gameboard[each[2][0]][each[2][1] + i].upper()
                    if each[0] == "vertical":
                        for i in range(0,4):
                            self.gameboard[each[2][0] + i][each[2][1]] = self.gameboard[each[2][0] + i][each[2][1]].upper()
                    if each[0] == "d-down":
                        for i in range(0,4):
                            self.gameboard[each[2][0] + i][each[2][1] + i] = self.gameboard[each[2][0] + i][each[2][1] + i].upper()
                    if each[0] == "d-up":
                        for i in range(0,4):
                            self.gameboard[each[2][0] + i][each[2][1] - i] = self.gameboard[each[2][0] + i][each[2][1] - i].upper()
                if rnd() > 0.99:
                    self.show()
                return True #and returns true to signalise that the game has been won
            else:
                return False #returns true to signalise that there are no winning combinations
        else:
            return False #returns false as there are no peices on the board, and therefore it cannot be won.

def intcheck(str,lb,ub):
    '''
    Takes a question start as str, an upper bound as ub and a lower bound as lb, then returns an integer inputted by the user between the ub and lb.
    Asks "{str} between {lb} and {ub}
    '''
    try:
        x = int(input("{0} between {1} and {2}: ".format(str,lb,ub))) #gets input
        if x >= lb and x <= ub: #if input is between the bounds, return the input
            return x
        else: #else, ask again
            print("Value entered outside the bounds")
            return intcheck(str,lb,ub)
    except ValueError: #if value entered is not an integer, tell the user and ask again
        print("Incorrect input type, please input an integer")
        return intcheck(str,lb,ub)
    pass


def setupplayers():
    '''
    allows the user to set up players, either a player versus computer game or 2 players vs each other, with input checking at each step.
    '''
    players = {}
    for i in range(0,intcheck("Enter a number of non-computer players",1,2)): #Sets up a specified number of players with unique names and symbols, either 1 player or 2
        run1 = True
        while run1 == True: #while name and symbol are not unique
            name = input("Please enter the name of non-computer player {0}: ".format(i + 1))
            if name not in players and name != "Computer": # checks to see if name is unique
                run2 = True
                while run2 == True:
                    psign = input("Enter this player's symbol: ").lower() #sets the player symbol
                    vs = []
                    for key,val in players.items(): #reads the already used symbols from the dictionary
                        vs.append(val)
                    if psign not in vs: #if the symbol is not already in use
                        print("{0}'s symbol accepted.".format(name))
                        players[name] = psign #adds both the name and the symbol to the dictionary
                        run1 = False
                        run2 = False #exits both while loops
                    else:
                        print("Non-unique symbol entered, try something else.") #returns to the symbol entrance

            else:
                print("Name already taken.") #returns to the name entrance

    if len(players) == 1: #if there are not already two players, adds a computer player
        name = "Computer"
        run2 = True
        while run2 == True: #uses the same code as above to get a unique symbol
            psign = input("Enter a player symbol for {0}: ".format(name)).lower()
            vs = []
            for key,val in players.items():
                vs.append(val)
            if psign not in vs:
                print("{0}'s symbol accepted.".format(name))
                players[name] = psign
                run2 = False
                cvsp = True #computer vs player is true
            else:
                print("Non-unique symbol entered, try something else.")
    else:
        cvsp = False #computer vs player is false as there are two human players
    print("The players entered are:") #prints the entered players
    for key,val in players.items():
        print("Player '{0}' using the symbol '{1}'".format(key,val))
    good = ynquestion("Are these players acceptable?")
    if good == True: #if correct, returns the dictionary containing the players and whether the game is computer vs player or player vs player
        return players, cvsp
    else: #if incorrect, tries again
        print("Restarting player setup")
        return setupplayers()
    pass

def ynquestion(str):
    '''
    asks a question, and takes only y or n for an answer, otherwise asks again until answer is correct
    '''
    good = input("{0} (y/n): ".format(str)).lower() #get the user input
    if good == "y": #if the answer is a coorect input and the answer is yes, return the boolean True
        return True
    elif good == "n": #if the answer is a coorect input and the answer is no, return the boolean False
        return False
    else: #If the input is invalid, tell the user, and ask again
        print("Invalid input, please enter either y or n")
        return ynquestion(str)
    pass

def getmove(network,input):
    '''
    Gets the move from a neural network and returns the value of the column it plays in. Takes the network, and the board in NN form as the input
    '''
    values = network.retval(np.array(input)) #takes the list of values returned from the network
    column = 0
    ret = (0,0)
    for i in range(0,len(values[0])):
        column += 1
        if ret[1] < values[0][i]: #if the calculated value of this column from the network is higher than the previous value, sets that column as the new best move
            ret = (column,values[0][i])
    return ret[0] #returns the column that has been determined the best move

def runnetworkgame(player1,player2):
    '''
    runs a game between two networks for the training of the NNs, and returns the score for each network in the order they are entered in
    '''
    x = 7
    y = 6
    gb = Gameboard(x,y,False)
    gameover = False
    player1sym = "x"
    player2sym = "o" #sets up everything needed for the game
    while gameover != True: #while the game is not over
        for each in [player1,player2]: #alternates between players 1 and 2
            if gb.checkwin() == False and gameover != True: # checks that game is not over or won
                if each == player1: #if player 1s turn, gets the board from player 1s perspective
                    inpt = gb.returnforinput(player1sym,player2sym)
                else: #if player 2s turn, gets the board from player 2s perspective
                    inpt = gb.returnforinput(player2sym,player1sym)
                move = getmove(each,inpt) #uses the player's network and the board for NN generated above to find the move
                if each == player1: #if the network was player 1, plays the move with player 1s symbol
                    movement = gb.insertpiece(move,player1sym) 
                else: #if the network was player 2, plays the move with player 2s symbol
                    movement = gb.insertpiece(move,player2sym)
                if movement != True: #if the movement failed, then a false move has been made, or there are no more moves to be played, and so the game is over
                    gameover = True
                    loser = each #the player who just made the move is the loser
            elif gb.checkwin() == True: #will trigger if last move won the game
                loser = each #last move won, therefore the player playing this turn has lost
                gameover = True
    if gb.checkwin() == True: #assigns scores based on who won
        if loser == player1:
            player1score = network.scale(gb.NoOfMoves,(0,(x*y)),(-1,0))
            player2score = network.scale(1/(gb.NoOfMoves-6),(0,0.5),(0,10))
        else:
            player2score = network.scale(gb.NoOfMoves,(0,(x*y)),(-1,0))
            player1score = network.scale(1/(gb.NoOfMoves-6),(0,1),(0,10))
    else: #will trigger if game was lost due to false move, assigning scores appropriately
        if loser == player1:
            player1score = -10
            player2score = 0
        else:
            player2score = -10
            player1score = 0
    return player1score, player2score

def computervsplayer(playerdict,network):
    x = 7
    y = 6
    gb = Gameboard(x,y,True)
    players=[]
    for key,val in playerdict.items():
        players.append([key,val])
    gameover = False #game is now ready to play
    while gameover != True: #while the game is not over
        for each in players: #alternates between players 1 and 2
            if gb.checkwin() == False and gameover != True: # checks that game is not over or won
                print("{0}'s turn:".format(each[0]))
                if each[0] == "Computer": #if player is the computer, runs the computers turn
                    inpt = gb.returnforinput(players[1][1],players[0][1])
                    move = getmove(network,inpt) #uses the player's network and the board for NN generated above to find the move
                    movement = gb.insertpiece(move,players[1][1])
                    while movement != True:
                        movement = random.randint(1,7)
                else: #if non-computer player's turn, runs their turn
                    movement = None
                    while movement != True:
                        move = intcheck("Please enter the column you want to play in",1,7)
                        movement = gb.insertpiece(move,each[1])
            elif gb.checkwin() == True: #will trigger if last move won the game
                loser = copy.copy(each[0]) #last move won, therefore the player playing this turn has lost
                gameover = True
    if loser == "Computer":
        print("Congratulations to {0} for their win".format(players[0][0]))
        gb.show(True)
    else:
        print("The computer has beaten you, better luck next time!")
        gb.show(True)

def playervsplayer(playerdict):
    players=[]
    for key,val in playerdict.items():
        players.append([key,val])
    gb = Gameboard(intcheck("Please enter the number of columns",4,20),intcheck("Please enter the number of rows",4,20))
    firstplayer = ynquestion("Does {0} want to play first?".format(players[0][0]))
    if firstplayer == False:
        players.reverse()
    gameover = False
    while gameover != True: #while the game is not over
        for each in players: #alternates between players 1 and 2
            if gb.checkwin() == False and gameover != True: # checks that game is not over or won
                print("{0}'s turn:".format(each[0]))
                movement = None
                while movement != True:
                    move = intcheck("Please enter the column you want to play in",1,gb.width)
                    movement = gb.insertpiece(move,each[1])
            elif gb.checkwin() == True: #will trigger if last move won the game
                loser = copy.copy(each[0]) #last move won, therefore the player playing this turn has lost
                gameover = True
    for i in players:
        if i[0] != loser:
            print("Congratulations {0}, you have won!".format(i[0]))
            gb.show(True)

def trainingmode():
    '''
    runs the training mode for the networks.
    '''
    print("Please only use this if you know what you are doing")
    if ynquestion("Are there previous generations? ") == False:
        #Generated new networks
        networks = mnetworks.NetworkGeneration("r", [42,150,203,87,7], generation_size = intcheck("Please enter the generation size",10,250))
    else:
        #continues training of already existing networks
        gen = input("Please enter the most recent generation: ")
        networks = mnetworks.NetworkGeneration("f","generation{0}.txt".format(gen))
    gensize = networks.generation_size
    run = True
    maxscore = []
    plt.show()
    while run == True: #starts infinite training loop
        x = []
        for i in range(gensize):
            x.append("")
        fitness = []
        for i in range(gensize):
            fitness.append(copy.deepcopy(x)) #sets up a 2 dimensional array for all the scores of the training
        for i in range(0,gensize):
            for n in range(0,gensize):
                if i != n and (fitness[i][n] == "" and fitness[n][i] == ""): #if they arent the same network, and they havents already played each other
                    x = runnetworkgame(networks.network_list[i], networks.network_list[n]) #returns the tuple of the two networks score
                    fitness[i][n] = x[0]
                    fitness[n][i] = x[1]
        for i in range(0,len(fitness)): #sums each networks score for evolution
            count = 0
            for item in fitness[i]:
                if item != "":
                    count += item
            fitness[i] = copy.copy(count)
        print("The best score this generation was {0}".format(max(fitness)))
        maxscore.append(copy.copy(max(fitness)))
        fig, (ax1, ax2) = plt.subplots(1, 2)
        ax1.hist(fitness, 20)
        ax2.plot(range(len(maxscore)), maxscore)
        plt.show(block=False)
        networks.evolve(fitness)


#setting up the game
if ynquestion("Enter training mode? "):
    trainingmode()
else:
    players, cvsp = setupplayers() #sets up the players for the game
    if cvsp == True:
        print("please select a generation from the below options") #shows all the options for the NNs you can play against
        for each in network.findfiles(network.currentfiledir()+"\\neuralnetworkdata\\"):
            print(each)
        keeptrying = True
        while keeptrying == True: #tries to load the networks from the file, keeps running until successful
            try:
                networks = network.NetworkGeneration(0,0,0,0,"Generation{0}.csv".format(input("Enter the number of the generation chosen: ")))
                keeptrying = False
            except: #repeats instructions and repeats options
                print("Please choose a generation number from the list of files below")
                for each in network.findfiles(network.currentfiledir()+"\\neuralnetworkdata\\"):
                    print(each)
        NN = networks.network_list[0] #selects the best network in that generation's list
        computervsplayer(players,NN)
    else:
        playervsplayer(players)