from ParameterSet import ParameterSet
from Plots import plotIndividumOverview
import numpy as np
import random
##MATPLOTLIB
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap


#initialization
def init(n, numberOfGenes):
    genOne = []
    idCounter = 1
    for i in range(n):
        newWeights = 100 * np.random.random_sample((numberOfGenes,))
        newIndividum = ParameterSet(idCounter, 0 , newWeights) 
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
        randomSet.calcParameterFitness() #MAYBE THIS CAN BE REMOVED because of redundancy


def main():
    #parameter
    n = 1000 #number of Individums
    numberOfGenes = 5
    numberOfGenerations = 20
    mutationRate = 0.5 #proportion of the population that will have one gene changed
    mutationChanging = 0.2 #the mutations changes a gene by how much
    searchForHighValues = True #should tge fitness be maximized oder minimized
    
    #Output
    showConsoleOutput = False 
    showIndividumOverviewPlot = True

    # "global" varibles
    idCounter = n + 1 #the first IDs are created in the init function
    genCounter = 2 #the first gen is created in the init function
    numberOfGenerations = numberOfGenerations - 1 #because numbering the generations shall be beginn with zero
    individumOverview = np.zeros([n, numberOfGenerations]) #array that stores the fitness of every Individum

    #initialization
    currentGen = init(n,numberOfGenes)
    for i in range(numberOfGenerations):
        print(" Current Generation: " + str(i))
        
        #-----BEGINN: filter old GEN---------------
        calcFitness(currentGen)
        currentGen.sort()
        #-----END: filter old GEN---------------

        #-----BEGIN: GENERATE OUTPUT---------------
        #Add current gen to overview for later plots
        if(showIndividumOverviewPlot):
            for c in range(len(currentGen)):
                individumOverview[c,i] = currentGen[c].getFitness()
        #print best 5
        if(showConsoleOutput):
            if (searchForHighValues): #searching for high Values
                for y in  range(5):
                    print("H Platz: " + str(y) + " --> " + str(currentGen[n-y-1]))
            else:                     #searching for low Values
                for y in  range(5):
                    print("L Platz: " + str(y) + " --> " + str(currentGen[y]))
        #-----END: GENERATE OUTPUT---------------
        
        
        #-----BEGINN: create new GEN---------------
        """
        IMPORTANT 
        [X:] --> SEARCH HIGH AND KILL ALL LOW (WARNING OVERFLOW)
        [:X] --> SEARCH LOW AND KILL ALL HIGH
        """
        individumOverviewcurrentGen = []
        if (searchForHighValues): #searching for high Values
            individumOverviewcurrentGen = currentGen[int(n/2):] #the Best (1/2)*N of the last generation
        else:                     #searching for low Values
            individumOverviewcurrentGen = currentGen[:int(n/2)] #the Best (1/2)*N of the last generation    
        
        newIndividums = recombination(individumOverviewcurrentGen, numberOfGenes, idCounter, genCounter) # the best (1/2)*N of last gen produces new (1/2)*N Sets
        nextGen = np.append(individumOverviewcurrentGen, newIndividums)
        mutation(nextGen,numberOfGenes, mutationRate, mutationChanging)
        idCounter = idCounter + int(n/2) #half of the gen more because recombination adds (1/2)*N 
        currentGen = nextGen
        #-----End: create new GEN---------------
        genCounter = genCounter + 1

    print("Finished")
    #plot results
    if(showIndividumOverviewPlot):
        calcFitness(currentGen)
        currentGen.sort()
        print("Bestes Element")
        if(searchForHighValues):
            print(currentGen[len(currentGen)-1])
        else:
            print(currentGen[0])
        plotIndividumOverview(individumOverview,n,numberOfGenerations)
    

if __name__ == '__main__':
    main()


