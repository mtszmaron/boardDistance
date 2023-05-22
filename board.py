import math
import random
import time
import matplotlib.pyplot as plt

POPULATION_SIZE = 100
COUNTER_SIZE = 100
BOARD_WIDTH = 15
BOARD_HEIGHT = 15


def createGenes(x,y):
    genes = []
    for i in range(x):
        for ii in range(y):
            if not(i == 0 and ii == 0):
                genes.append([i,ii])
    return genes

class Individual(object):
    def __init__(self, chromosome):
        self.chromosome = chromosome
        self.distance = self.cal_distance()
    
    @classmethod
    def mutated_genes(self, genes):
        gene = random.choice(genes)
        genes.remove(gene) 
        return gene
    
    @classmethod
    def create_gnome(self, genes):
        gnome = []
        gnome.append([0,0])
        gnome_len = len(genes)
        for _ in range(gnome_len):
            gnome.append(self.mutated_genes(genes))
        gnome.append([0,0])
        return gnome
    
    def cal_distance(self):
        distance = 0
        for i in range (len(self.chromosome) - 1):
            distance += math.dist(self.chromosome[i], self.chromosome[i+1])
        return distance
    
    def mate(self, secondParent):
        child = []
        child.append([0,0])
        s1 = self.chromosome.copy()
        s2 = secondParent.chromosome.copy()
        s1 = s1[slice(1, len(s1) - 1)]
        s2 = s2[slice(1,len(s2) - 1)]
        rand = random.randint(0, len(s1) - 1)
        rand2 = random.randint(1, len(s1) - rand)
        sliced = s1[slice(rand, rand + rand2)]
        for number in sliced:
            s2.remove(number)
        middle = len(sliced)//2
        firstHalf = sliced[:middle]
        secondHalf = sliced[middle:]
        child += firstHalf
        child += s2
        child += secondHalf
        child.append([0,0])        
        return Individual(child)
        
    def mutate(self):
        mutated = self.chromosome.copy()
        rand = random.randint(1, len(mutated) - 2)
        while True:
            rand2 = random.randint(1, len(mutated) - 2)
            if rand2 != rand:
                break
        mutated[rand], mutated[rand2] = mutated[rand2], mutated[rand]
        return Individual(mutated)
        
def main():
    t0 = time.time()
    generation = 1
    found = False
    population = []
    distance = -1
    
    for _ in range(POPULATION_SIZE):
        genes = board.copy()
        gnome = Individual.create_gnome(genes)
        population.append(Individual(gnome))
        
    while not found:
        population = sorted(population, key = lambda x:x.distance)
        
        if distance != population[0]:
            distance = population[0]
            counter = 0
        else:
            counter +=1
        
        if counter == COUNTER_SIZE:
            break
        
        new_generation = []        
        s = int((10*POPULATION_SIZE)/100)
        new_generation.extend(population[:s])
 
        s = int((90*POPULATION_SIZE)/100)
        for _ in range(s):
            parent1 = random.choice(population[:50])
            parent2 = random.choice(population[:50])
            child = parent1.mate(parent2)
            new_generation.append(child)       
        
        population = new_generation        
        population = sorted(population, key = lambda x:x.distance)
        
        for i in range(POPULATION_SIZE//2):
            population[POPULATION_SIZE//2 + i] = population[i].mutate()
 
        generation += 1
        print("Generation: " + str(generation) + "  Counter: " + str(counter) + "  Distance: " + str(distance.distance))
        
    t1 = time.time()
    totalTime = t1-t0
    
    print("Generation: {} \nPath: {} \nDistance: {} \nTime: {}".\
          format(generation-counter,population[0].chromosome, population[0].distance, totalTime))
        
    plt.rcParams["figure.figsize"] = [7.50, 7.50]
    plt.rcParams["figure.autolayout"] = True
    x_values = []
    y_values = []
    index = 0
    for point in population[0].chromosome:
        x_values.append(point[0])
        y_values.append(point[1])
        if index != len(population[0].chromosome)-1:
         plt.text(point[0]+0.03, point[1]+0.15, index)
         index += 1
    plt.plot(x_values, y_values, 'bo', linestyle="--")
    plt.show()
    
if __name__ == '__main__':
    board = createGenes(BOARD_WIDTH,BOARD_HEIGHT)
    main()