
import random
import itertools
import numpy.random
import sys

# this list indicates persons 1 and 3 are friends, and 5,7,8 are all friends
friends = [[1, 3],
           [5, 7, 8]]

# this list indicates 1 and 3 are enemies, and 4 and 7 are enemies
enemies = [[1, 2],
           [4, 7]]

# TODO
def fitness(seating):
  cur_fitness = 100
  first = seating[0]
  for x in range(1, 50):
    second = seating[x]
    #print second
    for y in friends: 
      if first in y: 
 	if second in y:
	  cur_fitness += 1.0 
    for i in enemies:
      if first in i:
	if second in i:
          cur_fitness += -1.0
    first = second
  return cur_fitness

# TODO
def crossover(parent1, parent2):
  child = [] 
  child = parent1[:25] + parent2[25:]
  return child 

# TODO
def mutate(seating):
  i = random.randint(0, 50)
  mylist = []
  for x in range(i, i+3):
    mylist.append(x)
  random.shuffle(mylist)
  return mylist

MAX_GENERATIONS = 1000
MAX_POPULATION = 50
NUMGUESTS = 50

print "crossover,mutation,maxpop,gen,fit"
for CROSSOVER in ["mycrossover"]:
    for MUTATION in [True, False]:
        for MAX_POPULATION in [10, 30, 50, 70, 90]:

            population = []
            parent1 = list(range(1, NUMGUESTS+1))
            random.shuffle(parent1)
            parent2 = list(range(1, NUMGUESTS+1))
            random.shuffle(parent2)


	    perfect = list(range(1, NUMGUESTS+1))
	    perfect[0] = 1
	    perfect[1] = 3
	    perfect[2] = 4
	    perfect[3] = 5
	    perfect[4] = 7
	    perfect[5] = 8
	    perfect[6] = 2
	    perfect[7] = 6
	    
#	    print perfect 

#	    parent1 = perfect
#	    parent2 = perfect

            fit1 = fitness(parent1)
            fit2 = fitness(parent2)
            population.append((parent1, fit1))
            population.append((parent2, fit2))

            fitness_sum = fit1 + fit2

            for generation in range(MAX_GENERATIONS):
                # select two individuals to breed; individuals with higher
                # fitness values are more likely to be selected
                fitness_pcts = []
                for (_, f) in population:
                    fitness_pcts.append(float(f)/float(fitness_sum))
                #print "population", population
                #print "fitness_pcts", fitness_pcts
                (idx1, idx2) = numpy.random.choice(range(len(population)), 2, False, fitness_pcts)
                (parent1, fitness1) = population[idx1]
                (parent2, fitness2) = population[idx2]
                #print "parent1", (parent1, fitness1)
                #print "parent2", (parent2, fitness2)
                if CROSSOVER == "mycrossover":
                    child = crossover(parent1, parent2)
                #print "child", child
                if MUTATION:
                    mutate(child) # modifies in-place
                child_fitness = fitness(child)
                population.append((child, child_fitness))
                fitness_sum += child_fitness
                #print "child", (child, child_fitness)

                # maybe the parents die? this is just one of many parameters in a
                # GA algorithm
                #population.remove((parent1, fitness1))
                #population.remove((parent2, fitness2))
                #fitness_sum -= (fitness1 + fitness2)

                if len(population) > MAX_POPULATION:
                    # kill the worst individual
                    population_sorted = sorted(population, key=lambda (ind, fit): fit)
                    fitness_sum -= population_sorted[0][1]
                    population.remove(population_sorted[0])

                if generation % 50 == 0:
                    for (_, f) in population:
                        print "%s,%s,%d,%d,%f" % (CROSSOVER, MUTATION, MAX_POPULATION, generation, f)


# generations are completed; find maximum fitness individual
population_sorted = sorted(population, key=lambda (ind, fit): fit, reverse=True)
print "population_sorted", population_sorted
print "best individual", population_sorted[0]

