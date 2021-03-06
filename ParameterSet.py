import numpy as np
import math

class ParameterSet:
    def __init__(self, id, gen, weights):
        self.weights = weights
        self.gen = gen
        self.id = id
        self.fitness = (-1)

    def getWeight(self, index):
        return self.weights[index]

    def getWeights(self):
        return self.weights
    
    def setWeights(self, weights):
        self.weights = weights

    def getGen(self):
        return self.gen
    
    def getID(self):
        return self.id

    def __str__(self):
        return  "ID: " + str(self.id) + " Gen: " + str(self.gen) + " mit Gewichten: " + str(self.weights) + " Fitness: " + str(self.fitness)

    def sumOfWeights(self):
        return np.sum(self.weights)

    def normalize(self):
        newWeights = self.weights * (100/np.sum(self.weights))
        self.weights = newWeights

    def setFitness(self, fitness):
        self.fitness = fitness

    def getFitness(self):
        return self.fitness

    def __lt__(self, other):
        return self.fitness < other.fitness 

    #THE FITNESS FUNCTION
    #calculates the fitness for a single Parameterset
    def calcParameterFitness(self):
        weights = self.getWeights()
        #fitness = math.sqrt( weights[0]**2 + weights[1]**2 + weights[2]**2 + weights[3]**2 + weights[4]**2 ) - 44.721359549995796
        #fitness = math.sqrt( weights[0]**2 + weights[1]**2 + weights[2]**2 + weights[3]**2 + weights[4]**2 )
        fitness = (weights[0]*2 - weights[1] + weights[2])**2
        self.fitness = fitness
