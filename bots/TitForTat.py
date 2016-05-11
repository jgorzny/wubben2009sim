'''
Created on Mar 2, 2016

@author: jgorzny
'''

class TitForTat(object):
    '''
    classdocs
    '''
    

    def __init__(self, params):
        '''
        Constructor
        '''
        print("New TitForTat player created for a new game.")
        self.name = params[0]
        self.emotion = params[1]
        print("Player " + self.name + " initially has 0 score, and feels " + self.emotion)
        
        #value of coins
        self.score = 0.0
        
        #lastAction will be an integer saying how many coins the opponent gave
        #on the last round
        self.lastAction = -1
        
        self.turnNumber = 0
        
        #will be used to calculate emotion intensity
        self.shortScore = 0
        self.shortMax = 0
        
        
    def takeTurn(self, turnNumber):
        print(self.name + " is taking turn " + str(self.turnNumber))
        toGive = 0
        if(self.turnNumber == 0):
            toGive = 10
        else: 
            toGive = self.lastAction
        print(self.name + " is giving " + str(toGive) + " coins. (Keeping " + str((10-toGive)) + " coins.)")
        return toGive
        
    def updateScore(self, numReceived, numKept):
        self.score = self.score + numReceived + (0.5 * numKept)
        
    def updateLastAction(self, numReceived):
        self.lastAction = numReceived
        
    def increaseTurnNum(self):
        self.turnNumber = self.turnNumber + 1
        
    def increaseShortVals(self, numReceived, potential):
        self.shortScore = self.shortScore + numReceived
        self.shortMax = self.shortMax + potential
        
    def resetShortVals(self):
        self.shortScore = 0
        self.shortMax = 0
                
    def reportEmotionIntensity(self):
        if(self.shortMax == 0):
            return float(0)
        else:
            print("Computing intensity:",self.shortScore,self.shortMax)
            return float(1)-float(float(self.shortScore)/float(self.shortMax))
        
    def reportScore(self):
        print(self.name + " has " + str(self.score) + " coins.")