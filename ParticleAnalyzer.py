## Running this program as a whole allows the user to generate PDF's for multiple inputs
## as well as execute other particle analyzation actions
class ParticleAnalyzer:

    ## Initializes a FindPDF object
    def __init__(self):
        self.finalDic = {}
        pass
    
    ## Private helper method of findPDF
    def __returnFinalDic(self, n):
        self.__makeString(n, '', 0)
        returnedDic = {}
        for key in self.finalDic.keys():
            returnedDic[key] = self.finalDic[key]
        self.finalDic = {}
        return returnedDic 
    
    
    
    ## Private helper method of findPDF
    def __makeString(self, n, str, i):

        if i == n: 
            finalSeqList = self.findFinalTree(0, self.symbolToSequence(str))
            finalParticleNum = len(finalSeqList)

            if finalParticleNum in self.finalDic.keys():
                self.finalDic[finalParticleNum] = self.finalDic[finalParticleNum] + 1
            else:
                self.finalDic[finalParticleNum] = 1
            return
      
     
        newstr = str + '+'
        self.__makeString(n, newstr, i + 1)  
  
        newstr = str + '-'
        self.__makeString(n, newstr, i + 1)
        

    ## Turns a sequence of symbols into a list of particles.
    ## Input example '+-0'
    ## Output example [[0.0, 1.0, 1.0], [1.0, 1.0, -1.0], [2.0, 1.0, 0.0]]
    ## Note the particle lists have the form [position, mass, velocity] in doubles
    ## Returns a list of particles representing the sequence in [] form
    def symbolToSequence(self,symbols):

        position = 0.0
        sequence = []

        for symbol in symbols:

            if symbol == '+':
                sequence.append([position, 1.0, 1.0])
            elif symbol == '-':
                sequence.append([position, 1.0, -1.0])
            elif symbol == '0':
                sequence.append([position, 1.0, 0.0])

            position = position + 1.0
        
        return sequence ## Returns one list

   
    ## Takes in an initial time and a list of triples representing particles at said time
    ## Triples have format [position, mass, velocity]
    ## Returns the time of the first collision(s) and the list of updated particles post-collision
    ## Puts 'no' as the list if the particles don't collide
    ## Precondition is that the input list has at least one triple, or else there is an error
    def findTime(self,initialTime, list):

        iTime = initialTime

        ## Pulls information from first triple in the list
        ## Creates output list 
        finalListOrg = [] ## template for final particle list since original is destroyed
        for item in list:
            finalListOrg.append(item)
        firstTriple = list.pop(0)
        pos1 = firstTriple[0]
        velocity1 = firstTriple[2]
        times = []
        
        ## Compares adjacent particles in the list
        for secondTriple in list:
            pos2 = secondTriple[0]
            velocity2 = secondTriple[2]

            if (velocity1 - velocity2) == 0.0: ## particles have same slope
                times.append(0)
            else: 
                currTime = (pos2 - pos1) / (velocity1 - velocity2)
                if currTime < 0: 
                    times.append(0)
                else:
                    times.append(currTime) ## This is possible so add to list
                    
            ## Updates current particle to previous particle
            pos1 = pos2
            velocity1 = velocity2

        ## Point of this section is to find minimum time and note indices when collision
        ## occurs at this time
        newTimes = times
        min = float('inf') 
        minIndex = []
        currIndex = 0

        for time in newTimes:
            if time <= min and time > 0:
                if time == min:
                    minIndex.append(currIndex)
                else :
                    minIndex = []
                    minIndex.append(currIndex)
                    min = time
            currIndex = currIndex + 1


        currIndex = 0
        finalList = [] 
        finalLen = len(finalListOrg)

        finalCol = False

        ## if no collisions then no final list is created
        if min == float('inf'):
            return [initialTime, 'no']
        else:
            
            while currIndex < finalLen:
                if currIndex not in minIndex:
                    newParticleP = finalListOrg[currIndex][0] + (finalListOrg[currIndex][2] * min) ## Updates position by advancing by min time
                    finalList.append([newParticleP,finalListOrg[currIndex][1],finalListOrg[currIndex][2]])
                    currIndex = currIndex + 1
                else:
                    ## Adds a collision particle and skips forward to next non-collision particle
                    newParticleP = finalListOrg[currIndex][0] + (finalListOrg[currIndex][2] * min)
                    newParticleM = finalListOrg[currIndex][1] + finalListOrg[currIndex + 1][1]
                    newParticleV = (finalListOrg[currIndex][1]*finalListOrg[currIndex][2] + finalListOrg[currIndex + 1][1]*finalListOrg[currIndex + 1][2])/newParticleM

                    ## This loop accounts for collisions of more than one particle
                    while (currIndex + 1) < finalLen - 1  and (currIndex + 1) in minIndex:
                        currIndex = currIndex + 1
                        newParticleM = newParticleM + finalListOrg[currIndex + 1][1]
                        newParticleV = ((newParticleM - finalListOrg[currIndex + 1][1])*newParticleV + finalListOrg[currIndex + 1][1]*finalListOrg[currIndex + 1][2])/newParticleM

                    newParticle = [newParticleP, newParticleM, newParticleV]
                    finalList.append(newParticle)
                    currIndex = currIndex + 2
                    

            finalTime = iTime + min

            return [finalTime, finalList] ## Returns final time and list
     
    ## Takes a start time and current list of particles as an input
    ## Returns the final particle configuration as a list
    ## Again precondition is just a valid list, inital time should be set to the time of
    ## the original state of the particles (this will usually be 0.0).
    def findFinalTree(self,initialTime, list):

        iTime = initialTime
        currList = list
        currListCopy = []
        noCollisions = False

        while not noCollisions:

            for thing in currList:
                currListCopy.append(thing)

            newList = self.findTime(iTime, currList)

            newITime = newList[0]
            newCurrList = newList[1]

            if newCurrList == 'no':
                noCollisions = True
            else:
                iTime = newITime
                currList = newCurrList
                currListCopy = []
        return currListCopy ## Returns final list after all posibble collisions as time goes to infinity


    ## Given an input length >= 1, generates the Probability Density Function (PDF) for that length
    ## Prints PDF to terminal
    ## Returns dictionary with final number of particles as keys, and probability as values
    ## Basically returns the PDF in dictionary form
    def findPDF(self, n):

        self.finalDic = {}

        finalFinalDic = self.__returnFinalDic(n)

        totalSeqs = 2**n
               
        print ' '
        print "Final PDF for " + str(n) + " particles:"
        print ''
        print "Number of Final Particles          Probability"

        for key in finalFinalDic.keys():
            print str(key) + "                                  " + str(finalFinalDic[key]) + " / " + str(totalSeqs)
        
        rDic = {}

        for key in finalFinalDic.keys():
            rDic[key] = finalFinalDic[key] / float(2**n)
        
        return rDic 
