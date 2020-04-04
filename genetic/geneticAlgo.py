'''
CP465 Project - Supervised Genetic Learning Algorithm
'''

import random
import csv

# Number of elements in each generation 
POPULATION_SIZE = 50

# Valid genes 
GENDER = ['female', 'male']
GROUP = ['group A','group B','group C','group D','group E']
LUNCH = ['standard', 'free/reduced']
COURSE = ['none', 'completed']
MATH = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
READING = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
WRITING = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

# Target data to be generated 
TARGET = ['female','group C','free/reduced','none', '8', '5', '7']

# Create the list of dataset from the given csv file
with open('StudentsPerformanceBinned.csv', newline='') as f:
    reader = csv.reader(f)
    result = list(reader)
DATA = result[1:]

''' 
Class representing element in population 
'''
class Element(object): 
    def __init__(self, chromosome): 
        self.chromosome = chromosome  
        self.fitness = self.calulate_fitness() 

    ''' 
    Create random genes for mutation
    '''
    @classmethod
    def mutate_genes(self, index): 
        global GENDER, GROUP, LUNCH, COURSE, MATH, READING, WRITING
        gene = ''

        if index == 0:
            mutated_gender = random.choice(GENDER)
            gene = mutated_gender
        elif index == 1:
            mutated_group = random.choice(GROUP)
            gene = mutated_group
        elif index == 2:
            mutated_lunch = random.choice(LUNCH)
            gene = mutated_lunch
        elif index == 3:
            mutated_course = random.choice(COURSE)
            gene = mutated_course
        elif index == 4:
            mutated_math = random.choice(MATH)
            gene = mutated_math
        elif index == 5:
            mutated_reading = random.choice(READING)
            gene = mutated_reading
        else:
            mutated_writing = random.choice(WRITING)
            gene = mutated_writing

        return gene

    ''' 
    Create chromosome from the given dataset
    '''
    @classmethod
    def create_chromosome(self, listOfData):
        data = random.choice(listOfData)
        chromosome = [data[0], data[1], data[3], data[4], data[5], data[6], data[7]]

        return chromosome

    ''' 
    Perform mating and produce new offspring
    '''
    def mate(self, parent2):
        # Chromosome for offspring
        child_chromosome = []

        for i in range(7):
            # Random probability
            prob = random.random()

            # If probability is less than 0.45, insert gene from parent 1 (gene1)
            if prob < 0.45:
                child_chromosome.append(self.chromosome[i])

            # If probability is between 0.45 and 0.90, insert gene from parent 2 (gene2)
            elif prob < 0.90:
                child_chromosome.append(parent2.chromosome[i])

            # Otherwise insert mutated gene for maintaining diversity
            else:
                child_chromosome.append(self.mutate_genes(i))

        # Create new Element(offspring) using generated chromosome for offspring 
        return Element(child_chromosome)

    ''' 
    Calculate fittness score
    '''
    def calulate_fitness(self):
        global TARGET
        fitness = 0

        for gs, gt in zip(self.chromosome, TARGET):
            if gs != gt:
                fitness += 1
        
        return fitness

'''
Main code
'''
def main(): 
    global POPULATION_SIZE
    global DATA

    # Current generation 
    generation = 1

    found = False
    population = []

    # Create initial population from the given dataset
    for _ in range(POPULATION_SIZE):
        initial_chrom = Element.create_chromosome(DATA)
        population.append(Element(initial_chrom))

    # Print targeted data
    print("-------------------------------------------------------------------------------------------------")
    print("Targeted: {0}".format(" ".join(TARGET)))
    print("-------------------------------------------------------------------------------------------------")
    
    while not found:
        # Sort the population in ascending order of fitness score
        population = sorted(population, key = lambda x:x.fitness)

        # If the element having lowest fitness score, then we know that we have reached to the target
        # Therefore, break the loop
        if population[0].fitness <= 0: 
            found = True
            break

        # Otherwise generate new offsprings for new generation
        new_generation = []

        # 10% of fittest population goes to the next generation
        s = int((10*POPULATION_SIZE)/100)
        new_generation.extend(population[:s])

        # From 50% of fittest population, Elements will mate to produce offspring
        s = int((90*POPULATION_SIZE)/100)
        for _ in range(s):
            parent1 = random.choice(population[:50])
            parent2 = random.choice(population[:50])
            child = parent1.mate(parent2)
            new_generation.append(child)

        population = new_generation

        # Sort the population in ascending order of fitness score
        population = sorted(population, key = lambda x:x.fitness)

        print("Generation: {0}".format(generation))
        for i in range(5):
            print("Chromosome: {0} (Fitness: {1})".format(" ".join(population[i].chromosome), population[i].fitness))
        print("...")
        for i in range(-6, -1):
            print("Chromosome: {0} (Fitness: {1})".format(" ".join(population[i].chromosome), population[i].fitness))
        print("")

        generation += 1

if __name__ == '__main__':
    main()