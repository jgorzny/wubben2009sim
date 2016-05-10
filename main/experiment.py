'''
Created on Mar 15, 2016

@author: jgorzny
'''

import random
import os
import time
from __init__ import TfTvsEmoBayesActor
import sys
import numpy
import scipy.stats as stats

def runExperiment(eName, N, p, path, timeout, idIn): 
    
    #First, we choose N identities, and set them to be female with probability p

    
    idFile = "D:\\Libraries\\Python\\bayesact-emot-supplemental\\bactfiles\\fidentities.dat"
    
    ids = chooseIdentities(N, idFile)

    name = "Experiment " + eName + " " +time.strftime("%d-%m-%Y") + "-" + time.strftime("%H-%M")
    directory = path + "\\" + name
    if not os.path.exists(directory):
        os.makedirs(directory)
            
    logFileName = directory + "\\" + name + " log.txt"
    logFile = open(logFileName, 'w')
    
    pFileName = directory + "\\" + name + "-plot.txt"
    plotLogFile = directory + "\\" + name + "-plot-log.txt"
    
    individualLogs = []
    
    numMale = 0
    numFemale = 0
    
    numNoEmo = 0
    numAnger = 0
    numDisappointment = 0
    
    numFemaleAnger = 0
    numFemaleDisappointment = 0
    numFemaleNoEmo =0 

    #Then we run each against a TfT player    
    for i in range(0,N):

        
        rVal = random.random()
        
        if(rVal >= p):
            gender = "male"
            numMale = numMale + 1
        else:
            gender = "female"
            numFemale = numFemale + 1
        
        
        if(idIn=="NA"):
            bayesID=ids[i]
        else:
            bayesID=idIn
            
        emoGroup = random.choice(["none","anger","disappointment"])
        
        if(emoGroup == "anger"):
            numAnger= numAnger + 1
            if(gender == "female"):
                numFemaleAnger = numFemaleAnger + 1
        elif(emoGroup == "disappointment"):
            numDisappointment = numDisappointment + 1
            if(gender == "female"):
                numFemaleDisappointment = numFemaleDisappointment + 1
        else:
            numNoEmo = numNoEmo + 1
            if(gender == "female"):
                numFemaleNoEmo = numFemaleNoEmo + 1
            
        specificLogFile = directory + "\\" + name + "--"+str(i)+"-("+gender + "," + bayesID+","+emoGroup+")log.txt"
        individualLogs.append(specificLogFile)
        logFile.write("EmoBayesActor is a " + gender + " " + bayesID + " in group "+ emoGroup+" whose data is in " + specificLogFile + "\n")
        logFile.flush()
        
        #redirect this output to 'specificLogFile'
        sys.stdout = open(specificLogFile, 'w')
        TfTvsEmoBayesActor(emoGroup, gender, bayesID, timeout)
        
    logFile.write("Number of males: " + str(numMale) + "\n")
    logFile.write("Number of females: " + str(numFemale) + "\n")
    logFile.write("Number of Anger participants (female): " + str(numAnger) + " (" + str(numFemaleAnger) + ")" + "\n")
    logFile.write("Number of Disappointment participants (female): " + str(numDisappointment) + " (" + str(numFemaleDisappointment) + ")" + "\n")
    logFile.write("Number of No Emotion participants (female): " + str(numNoEmo) + " (" + str(numFemaleNoEmo) + ")" + "\n")
    logFile.write("Timeout:" +str(timeout) + "\n")
    logFile.write("Fixed ID:" + idIn + "\n")
    logFile.close()
    
    #generate a file with information necessary to make a plot
    sys.stdout = open(plotLogFile, 'w')
    makePlotFile(pFileName, individualLogs)
    
    computeTtests(directory+"\\"+eName+"-t-tests.txt", directory+"\\", eName, pFileName)
    
def chooseIdentities(N, idFile):
    with open(idFile) as f:
        content = f.readlines()
        
    result = []
    for i in range(0, N):
        newID = random.randint(0,len(content)-1)
        #print "id selected",content[newID].split(',', 1)[0]
        result.append(content[newID].split(',', 1)[0])
        
    return result
        
        
def makePlotFile(pFileName, logs):
    pFile = open(pFileName, 'w')
    
    numGiven =[ [[],[],[],[],[]],  [[],[],[],[],[]],  [[],[],[],[],[]] ]
    
    for i in range(0, len(logs)):
        lFile= open(logs[i])
        lines = lFile.readlines()
        
        if(logs[i].count("anger") > 0):
            c = 1
        elif(logs[i].count("disappointment") > 0):
            c = 2
        else:
            c = 0
        
        record = False
        blockCount = 0
        for j in range(0, len(lines)):
            if(record):
                print c,blockCount,j, len(lines)
                numGiven[c][blockCount].append(float(lines[j].strip()))
                record = False
            
            if(lines[j].startswith("----- End of turn")):
                record = True
                if(lines[j].count(" 1 ") > 0 or lines[j].count(" 4 ") > 0 or lines[j].count(" 7 ") > 0 or lines[j].count(" 10 ") > 0):
                    blockCount = blockCount + 1

    pFile.write("Emotion,block,mean,sd\n")
    for k in range(0,4):
        pFile.write("No emotion,"+ str(k+1) + ",")
        pFile.write(str(numpy.mean(numGiven[0][k])) + "," + str(numpy.std(numGiven[0][k])) + "\n")
        pFile.flush()
    
    for k in range(0,4):
        pFile.write("Anger,"+ str(k+1) + ",")
        pFile.write(str(numpy.mean(numGiven[1][k])) + "," + str(numpy.std(numGiven[1][k]))+ "\n")
        pFile.flush()
                
    for k in range(0,4):
        pFile.write("Disappointment," + str(k+1) + ",")
        pFile.write(str(numpy.mean(numGiven[2][k])) + "," + str(numpy.std(numGiven[2][k]))+ "\n")
        pFile.flush()
                    
    '''
    pFile.write("no emotion\n")
    for k in range(0,len(numGiven)):
        pFile.write(str(numpy.mean(numGiven[0][k])) + "," + str(numpy.std(numGiven[0][k])) + "\n")
        pFile.flush()
    pFile.write("anger\n")
    for k in range(0,len(numGiven)):
        pFile.write(str(numpy.mean(numGiven[1][k])) + "," + str(numpy.std(numGiven[1][k]))+ "\n")
        pFile.flush()
    pFile.write("disappointment\n")        
    for k in range(0,len(numGiven)):
        pFile.write(str(numpy.mean(numGiven[2][k])) + "," + str(numpy.std(numGiven[2][k]))+ "\n")
        pFile.flush()                
    ''' 
    pFile.close()
                
def computeTtests(outputFile, directory, expName,plotOutputFile):
    print "Computing t-tests..."      
    
    rFileName = directory + "make-plot.r"
    
    #outputFile = "D:\\Research Data\\CS886\\Wubben2009\\Experiment similar-long 04-04-2016-23-32\\similar-long-t-tests.txt"
    #outputFile = "D:\\Research Data\\CS886\\Wubben2009\\Experiment undergrad-long 05-04-2016-19-55\\undergrad-long-t-tests.txt"
    logs = [] 
    
    #allfiles = os.listdir("D:\\Research Data\\CS886\\Wubben2009\\Experiment similar-long 04-04-2016-23-32")
    #allfiles = os.listdir("D:\\Research Data\\CS886\\Wubben2009\\Experiment undergrad-long 05-04-2016-19-55")
    allfiles = os.listdir(directory)
    for i in range(0, len(allfiles)):
        print allfiles[i]
        if(allfiles[i].count("--") > 0):
            #logs.append("D:\\Research Data\\CS886\\Wubben2009\\Experiment similar-long 04-04-2016-23-32\\" + allfiles[i])
            logs.append(directory + allfiles[i])
            print "...appended"
    
    pFile = open(outputFile, 'w')
    
    numGiven =[ [[],[],[],[],[]],  [[],[],[],[],[]],  [[],[],[],[],[]] ]
    
    distros = [ [], [], [] ]
    
    for i in range(0, len(logs)):
        lFile= open(logs[i])
        lines = lFile.readlines()
        
        if(logs[i].count("anger") > 0):
            c = 1
        elif(logs[i].count("disappointment") > 0):
            c = 2
        else:
            c = 0
        
        record = False
        blockCount = 0
        for j in range(0, len(lines)):
            if(record):
                print c,blockCount,j, len(lines)
                numGiven[c][blockCount].append(float(lines[j].strip()))
                
                distros[c].append(float(lines[j].strip()))
                
                record = False
            
            if(lines[j].startswith("----- End of turn")):
                record = True
                if(lines[j].count(" 1 ") > 0 or lines[j].count(" 4 ") > 0 or lines[j].count(" 7 ") > 0 or lines[j].count(" 10 ") > 0):
                    blockCount = blockCount + 1

    pFile.write("Emotion,t,p\n")
    pFile.write("Anger,")
    t_stat, p_value = stats.ttest_ind(distros[1], distros[0], equal_var=False)
    #(distros[1], distros[2], axis, False, nan_policy)
    # (distros[1], distros[0], equal_var=False)
    pFile.write(str(t_stat) + "," + str(p_value) + "\n")
    pFile.flush()
    
    pFile.write("Disappointment,")
    t_stat, p_value = stats.ttest_ind(distros[2], distros[0], equal_var=False)
    #(distros[1], distros[2], axis, False, nan_policy)
    # (distros[1], distros[0], equal_var=False)
    pFile.write(str(t_stat) + "," + str(p_value) + "\n")
    pFile.flush()

    rFile = open(rFileName, 'w')
    makePlotScript(rFile, directory, expName,plotOutputFile)

def makePlotScript(pFile, directory, expName, fileName):
    pFile.write("setwd('" + directory.replace('\\',"\\\\") + "')\n")
    pFile.write("mydata <- read.table(\"" + fileName.replace('\\',"\\\\") +"\", header=TRUE, sep=\",\")\n")

    pFile.write("mydata\n")
    pFile.write("library(ggplot2)\n")


    pFile.write("pdf(\"" + expName +".pdf\", width=5, height=5)\n")

    pFile.write("plot <- ggplot(mydata, aes(x=block, y=mean, colour=Emotion)) + \n")
    pFile.write("    geom_errorbar(aes(ymin=mean-sd, ymax=mean+sd), width=.1) +\n")
    pFile.write("    geom_line() +\n")
    pFile.write("    geom_point(aes(shape=Emotion), size=5)\n")
    pFile.write("plot + theme_light()\n")

    pFile.write("plot + labs(x = \"Block\", y = \"Donated Coins\")\n")
    pFile.write("dev.off()\n")
    pFile.flush()
    pFile.close()

    
if __name__ == "__main__":
    oldstdout = sys.stdout

    
    sys.stdout = oldstdout
    ''' #Example:
    print "Starting similar"
    runExperiment("similar", 100, 0.78, "D:\Research Data\CS886\Wubben2009", 5.0, "NA")
    sys.stdout = oldstdout
    '''

    print "Starting test"
    runExperiment("test-no-cosine", 3, 0.5, "D:\Research Data\CS886\Wubben2009", 5.0, "NA")
    sys.stdout = oldstdout
    
    #computeTtests()
    
    sys.stdout = oldstdout
    print "Done running experiments."