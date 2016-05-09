from bots.TitForTat import TitForTat
from bots.Random import RandomBot
from bots.BayesActor import PDAgentB
from bots.BayesActor import BayesActor
from bots.EmoBayesActor import EmoBayesActor



from bayesact import *

#def main(argv):
def main():
    argv = []
    #testingTfT()
    #testingTfTRandom()
    if(len(argv) > 1):
        tftEmotion = argv[0]
        bayesGender = argv[1]
        bayesID = argv[2]
    else:
        bayesGender = "male"
        bayesID = "friend"
        tftEmotion = "anger"
    
    TfTvsEmoBayesActor(tftEmotion, bayesGender, bayesID)
    
def TfTvsEmoBayesActor(tftEmotion, bayesGender, bayesID, timeout):
    print("Starting a game.")
    tftPlayer = TitForTat(["Alice", tftEmotion])
    bayesPlayer = EmoBayesActor(["Bob", bayesGender, bayesID, "Alice", timeout])
    
    for i in range(0,14):
        print("---------- Turn " + str(i) + " ------------------------")
        tftGives = tftPlayer.takeTurn(i)
        bayesGives = bayesPlayer.takeTurn(i)
        
        tftPlayer.updateScore(bayesGives, 10-tftGives)
        bayesPlayer.updateScore(tftGives, 10-bayesGives)
        
        tftPlayer.updateLastAction(bayesGives)
        
        if(i%3 == 1 and i < 13):
            ei1 = round(tftPlayer.reportEmotionIntensity()*10)

            print(tftPlayer.name + " is feeling " + tftPlayer.emotion + " with intensity " + str(ei1) )
            
            bayesPlayer.updateLastActionWithEmotion(tftGives, ei1, tftPlayer.emotion)
            
            tftPlayer.resetShortVals()
        else:
            bayesPlayer.updateLastAction(tftGives)
        
        
        print 5*"-","End of turn",i,"results",5*"-"
        print bayesGives
        tftPlayer.reportScore()
        bayesPlayer.reportScore()
        print 30*""
        
        tftPlayer.increaseShortVals(bayesGives, 10)        
        
            
        
        tftPlayer.increaseTurnNum()
        bayesPlayer.increaseTurnNum()
        print("-------------------------------------------")
        
    print "Done!"
        
def TfTvsBayesActor(tftEmotion, bayesGender, bayesID):
    print("Starting a game.")
    tftPlayer = TitForTat(["Alice", tftEmotion])
    bayesPlayer = BayesActor(["Bob", bayesGender, bayesID])
    
    for i in range(0,14):
        print("---------- Turn " + str(i) + " ------------------------")
        tftGives = tftPlayer.takeTurn(i)
        bayesGives = bayesPlayer.takeTurn(i)
        
        tftPlayer.updateScore(bayesGives, 10-tftGives)
        bayesPlayer.updateScore(tftGives, 10-bayesGives)
        
        tftPlayer.updateLastAction(bayesGives)
        bayesPlayer.updateLastAction(tftGives)
        
        tftPlayer.reportScore()
        bayesPlayer.reportScore()
        
        tftPlayer.increaseShortVals(bayesGives, 10)        
        
        if(i%3 == 1 and i < 13):
            ei1 = round(tftPlayer.reportEmotionIntensity()*10)

            print(tftPlayer.name + " is feeling " + tftPlayer.emotion + " with intensity " + str(ei1) )
            
            #bayesPlayer.receiveMessage(ei1, tftEmotion)
            
            tftPlayer.resetShortVals()
        
        tftPlayer.increaseTurnNum()
        bayesPlayer.increaseTurnNum()
        print("-------------------------------------------")
        
    print "Done!"

def testingTfT():
    print("Starting a game.")
    player1 = TitForTat(["Alice", "none"])
    player2 = TitForTat(["Bob", "none"])
    
    for i in range(0,14):
        print("---------- Turn " + str(i) + " ------------------------")
        player1Gives = player1.takeTurn(i)
        player2Gives = player2.takeTurn(i)
        
        player1.updateScore(player2Gives, 10-player1Gives)
        player2.updateScore(player1Gives, 10-player2Gives)
        
        player1.updateLastAction(player2Gives)
        player2.updateLastAction(player1Gives)
        
        player1.reportScore()
        player2.reportScore()
        
        player1.increaseShortVals(player2Gives, 10)
        player2.increaseShortVals(player1Gives, 10)
        
        
        if(i%3 == 1 and i < 13):
            ei1 = round(player1.reportEmotionIntensity()*10)
            ei2 = round(player1.reportEmotionIntensity()*10)

            print(player1.name + " is feeling " + player1.emotion + " with intensity " + str(ei1) )
            print(player2.name + " is feeling " + player2.emotion + " with intensity " + str(ei2) )
            player1.resetShortVals()
            player2.resetShortVals()
        
        player1.increaseTurnNum()
        player2.increaseTurnNum()
        print("-------------------------------------------")
        
def testingTfTRandom():
    print("Starting a game.")
    player1 = TitForTat(["Alice", "none"])
    player2 = RandomBot(["Bob"])
    
    for i in range(0,14):
        print("---------- Turn " + str(i) + " ------------------------")
        player1Gives = player1.takeTurn(i)
        player2Gives = player2.takeTurn(i)
        
        player1.updateScore(player2Gives, 10-player1Gives)
        player2.updateScore(player1Gives, 10-player2Gives)
        
        player1.updateLastAction(player2Gives)
        player2.updateLastAction(player1Gives)
        
        player1.reportScore()
        player2.reportScore()

        player1.increaseShortVals(player2Gives, 10)
                
        if(i%3 == 1 and i < 13):
            ei = round(player1.reportEmotionIntensity()*10)
            print(player1.name + " is feeling " + player1.emotion + " with intensity " + str(ei) )
            player1.resetShortVals()
        
        player1.increaseTurnNum()
        player2.increaseTurnNum()        
 
#makes this the main method
if __name__ == "__main__":
    main()