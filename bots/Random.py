'''
Created on Mar 2, 2016

@author: jgorzny
'''
import random

class RandomBot(object):
    '''
    classdocs
    '''
    

    def __init__(self, params):
        '''
        Constructor
        '''
        print("New TitForTat player created for a new game.")
        self.name = params[0]
        print("Player " + self.name + " initially has 0 score.")
        
        #value of coins
        self.score = 0.0
        
        #lastAction will be an integer saying how many coins the opponent gave
        #on the last round
        self.lastAction = -1
        
        self.turnNumber = 0
        
        
    def takeTurn(self, turnNumber):
        print(self.name + " is taking turn " + str(self.turnNumber))
        toGive = random.randint(0,10)
        print(self.name + " is giving " + str(toGive) + " coins. (Keeping " + str((10-toGive)) + " coins.)")
        return toGive
        
    def updateScore(self, numReceived, numKept):
        self.score = self.score + numReceived + (0.5 * numKept)
        
    def updateLastAction(self, numReceived):
        self.lastAction = numReceived
        
    def increaseTurnNum(self):
        self.turnNumber = self.turnNumber + 1
        
    def reportScore(self):
        print(self.name + " has " + str(self.score) + " coins.")