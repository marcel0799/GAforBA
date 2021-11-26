from ParameterSet import ParameterSet
import numpy as np
import random

#initialization
def init(n, numberOfGenes):
    genOne = []
    idCounter = 1
    for i in range(n):
        newWeights = 100 * np.random.random_sample((numberOfGenes,))
        newIndividum = ParameterSet(idCounter, 1 , newWeights) 
        newIndividum.normalize()
        genOne.append(newIndividum)
        idCounter = idCounter + 1
    return genOne

#calculate the fitness for an generation
def calcFitness(gen):
    for x in gen:
        x.calcParameterFitness()

#The current Generation gets sorted by theire Parameterset Fitness
def sortFunction(currentParameterSet):
    return currentParameterSet.fitness

def recombinatingTwoSets(a : ParameterSet, b: ParameterSet, numberOfGenes, idCounter, genCounter):
    newIndividums = []
    weightsFromA = a.getWeights()
    weightsFromB = b.getWeights()
    #creating child 1 --> C
    weightsC = weightsFromA[ : (int(numberOfGenes/2))]
    weightsC = np.append(weightsC, weightsFromB[(int(numberOfGenes/2)) : ] )
    c = ParameterSet(idCounter, genCounter, weightsC)
    c.normalize()
    idCounter = idCounter + 1
    #creating child 2 --> D
    weightsD = weightsFromA[(int(numberOfGenes/2)) : ]
    weightsD = np.append(weightsFromB[ : (int(numberOfGenes/2))] , weightsD)
    d = ParameterSet(idCounter, genCounter, weightsD)
    d.normalize()
    newIndividums.append(c)
    newIndividums.append(d)
    return newIndividums

def recombination(currentGen, numberOfGenes, idCounter, genCounter):
    #the index shall only look at every second object
    newIndividums = []
    for i in range(int(len(currentGen)/2)):
        index = i*2
        parentOne = currentGen[index]
        parentTwo = currentGen[index+1]
        newChildren = recombinatingTwoSets(parentOne,parentTwo,numberOfGenes, idCounter, genCounter)
        newIndividums = np.append(newIndividums,newChildren)
        idCounter = idCounter + 2
    return newIndividums

def mutation(currentGen, numberOfGenes, mutationRate, mutationChanging):
    for i in range( int( len(currentGen)*mutationRate ) ): 
        randomIndex = random.randint(0, (len(currentGen)-1) )
        randomSet = currentGen[randomIndex]
        randomGene = random.randint(0, (numberOfGenes-1) )
        weights = randomSet.getWeights()
        oldWeight = weights[randomGene]
        newWeight = oldWeight * random.uniform(1-mutationChanging,1+mutationChanging)
        weights[randomGene] = newWeight
        randomSet.setWeights(weights)
        randomSet.normalize()
        randomSet.calcParameterFitness()

def main():
    #parameter
    n = 1000 #number of Individums
    numberOfGenes = 3
    numberOfGenerations = 1000
    mutationRate = 0.5 #proportion of the population that will have one gene changed
    mutationChanging = 0.2 #the mutations changes a gene by how much
    searchForHighValues = False

    # "global" varibles
    idCounter = n + 1 #the first IDs are created in the init function
    genCounter = 2 #the first gen is created in the init function

    #initialization
    currentGen = init(n,numberOfGenes)
    for i in range(1, (numberOfGenerations+1)):
        #-----BEGINN: filter old GEN---------------
        print("_______new Gen: " + str(i))
        calcFitness(currentGen)
        currentGen.sort()
        #print best 5
        if (searchForHighValues): #searching for high Values
            for y in  range(5):
                print("H Platz: " + str(y) + " --> " + str(currentGen[n-y-1]))
        else:                     #searching for low Values
            for y in  range(5):
                print("L Platz: " + str(y) + " --> " + str(currentGen[y]))
        #-----END: filter old GEN---------------
        #-----BEGINN: create new GEN---------------
        """
        IMPORTANT 
        [X:] --> SEARCH HIGH AND KILL ALL LOW (WARNING OVERFLOW)
        [:X] --> SEARCH LOW AND KILL ALL HIGH
        """
        bestOfcurrentGen = []
        if (searchForHighValues): #searching for high Values
            bestOfcurrentGen = currentGen[int(n/2):] #the Best (1/2)*N of the last generation
        else:                     #searching for low Values
            bestOfcurrentGen = currentGen[:int(n/2)] #the Best (1/2)*N of the last generation    
        
        newIndividums = recombination(bestOfcurrentGen, numberOfGenes, idCounter, genCounter) # the best (1/2)*N of last gen produces new (1/2)*N Sets
        nextGen = np.append(bestOfcurrentGen, newIndividums)
        mutation(nextGen,numberOfGenes, mutationRate, mutationChanging)
        idCounter = idCounter + int(n/2) #half of the gen more because recombination adds (1/2)*N 
        currentGen = nextGen
        #-----End: create new GEN---------------
        genCounter = genCounter + 1
    print("Finished")
    

if __name__ == '__main__':
    main()



