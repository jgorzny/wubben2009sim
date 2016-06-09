def main():
    
    #generate large function for reward
    for i in range(1,12):
        for j in range(1,12):
            print "elif sample.x[1] ==",i,"and sample.x[2] ==",j,":"
            keptVal = (0.5 * (10.0 - (10.0 - (i-1.0))))
            receivedVal = (10.0 - (j - 1.0))
            total = keptVal + receivedVal   
            print "    xreward =", total

if __name__ == "__main__":
    main()

