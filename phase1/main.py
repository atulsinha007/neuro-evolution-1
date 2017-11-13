
import array
import random
import json

import numpy
from math import sqrt

from deap import algorithms
from deap import base
from deap import benchmarks
from deap.benchmarks.tools import diversity, convergence
from deap import creator
from deap import tools

from Population import *
from network import Neterr
from chromosome import Chromosome

n_hidden = 10
indim = 8
outdim = 1
creator.create("FitnessMin", base.Fitness, weights=(-1.0, -1.0, -1.0, -1.0))
creator.create("Individual", Chromosome, fitness=creator.FitnessMin)

toolbox = base.Toolbox()

def minimize(individual):
	network_obj = Neterr(indim, outdim, n_hidden, np.random)

	outputarr = network_obj.feedforward_ne(individual)

	neg_log_likelihood_val = give_neg_log_likelihood(outputarr, network_obj.resty)
	mean_square_error_val = give_mse(outputarr, network_obj.resty)
	false_positve_rat = give_false_positive_ratio(outputarr, network_obj.resty)

	false_negative_rat = give_false_negative_ratio(outputarr, network_obj.resty)

	return neg_log_likelihood_val, mean_square_error_val, false_positve_rat, false_negative_rat

def mycross(ind1, ind2):
	return ind1, ind2

def mymutate(ind1):
	return ind1

def initIndividual(ind_class, inputdim, outputdim):
	ind = ind_class(inputdim, outputdim)
	return ind

toolbox.register("individual", initIndividual, creator.Individual, indim, outdim)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("evaluate", minimize)
toolbox.register("mate", mycross)
toolbox.register("mutate", mymutate)
toolbox.register("select", tools.selNSGA2)

def main(seed=None):
	random.seed(seed)

	NGEN = 250
	MU = 100
	CXPB = 0.9

	stats = tools.Statistics(lambda ind: ind.fitness.values)
	#stats.register("avg", numpy.mean, axis=0)
	#stats.register("std", numpy.std, axis=0)
	stats.register("min", numpy.min, axis=0)
	stats.register("max", numpy.max, axis=0)
	
	logbook = tools.Logbook()
	logbook.header = "gen", "evals", "std", "min", "avg", "max"
	pop = toolbox.population(n=MU)

	# Evaluate the individuals with an invalid fitness
	invalid_ind = [ind for ind in pop if not ind.fitness.valid]
	fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
	for ind, fit in zip(invalid_ind, fitnesses):
		ind.fitness.values = fit

	# This is just to assign the crowding distance to the individuals
	# no actual selection is done
	pop = toolbox.select(pop, len(pop))
	
	record = stats.compile(pop)
	logbook.record(gen=0, evals=len(invalid_ind), **record)
	print(logbook.stream)

	# Begin the generational process
	for gen in range(1, NGEN):
		# Vary the population
		offspring = tools.selTournamentDCD(pop, len(pop))
		offspring = [toolbox.clone(ind) for ind in offspring]
		
		for ind1, ind2 in zip(offspring[::2], offspring[1::2]):
			if random.random() <= CXPB:
				toolbox.mate(ind1, ind2)
			
			toolbox.mutate(ind1)
			toolbox.mutate(ind2)
			del ind1.fitness.values, ind2.fitness.values
		
		# Evaluate the individuals with an invalid fitness
		invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
		fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
		for ind, fit in zip(invalid_ind, fitnesses):
			ind.fitness.values = fit

		# Select the next generation population
		pop = toolbox.select(pop + offspring, MU)
		record = stats.compile(pop)
		logbook.record(gen=gen, evals=len(invalid_ind), **record)
		print(logbook.stream)

	#print("Final population hypervolume is %f" % HyperVolume(pop, [11.0, 11.0]))

	return pop, logbook
		
if __name__ == "__main__":
	pop, stats = main()
	pop.sort(key=lambda x: x.fitness.values)
	
	'''print(stats)
	print("Convergence: ", convergence(pop, optimal_front))
	print("Diversity: ", diversity(pop, optimal_front[0], optimal_front[-1]))'''
	
	import matplotlib.pyplot as plt
	import numpy
	
	front = numpy.array([ind.fitness.values for ind in pop])
	plt.scatter(front[:,0], front[:,1], c="b")
	plt.axis("tight")
	plt.show()

if __name__ == "__main__":
	main()