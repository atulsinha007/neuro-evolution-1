import random

class GeneticAlgorithm(object):
	def __init__(self, genetics):
		self.genetics = genetics

	def run(self):
		population = self.genetics.initial()
		while True:
			fits_pops = [(self.genetics.fitness(ch),  ch) for ch in population]
			if self.genetics.check_stop(fits_pops): break
			population = self.next(fits_pops)
		return population

	def next(self, fits):
		parents_generator = self.genetics.parents(fits)
		size = len(fits)
		nexts = []
		while len(nexts) < size:
			parents = next(parents_generator)
			cross = random.random() < self.genetics.probability_crossover()
			children = self.genetics.crossover(parents) if cross else parents
			for ch in children:
				mutate = random.random() < self.genetics.probability_mutation()
				nexts.append(self.genetics.mutation(ch) if mutate else ch)
		return nexts[0:size]
	

"""
example: Mapped guess prepared Text
"""
class OptimizeFunction():
	def __init__(self, D, limit=200, size=100, prob_crossover=0.9, prob_mutation=0.2):
		self.counter = 0
		self.limit = limit
		self.size = size
		self.prob_crossover = prob_crossover
		self.prob_mutation = prob_mutation
		

	# GeneticFunctions interface impls
	def probability_crossover(self):
		return self.prob_crossover

	def probability_mutation(self):
		return self.prob_mutation

	def initial(self):
		return [self.random_chromo() for j in range(self.size)]

	def fitness(self, chromo):
		# larger is better, matched == 0
		return sum(i*i for i in chromo)

	def check_stop(self, fits_populations):
		self.counter += 1
		best_match = list(sorted(fits_populations))[-1][1]

		if self.chromo2text(best_match) == self.chromo2text(self.target):
			print("==>[G %3d] Reached: %r" % (self.counter, self.chromo2text(best_match)))
            
			print("(" + str(self.size) + "," + str(self.counter) + ")")
			return True

		if self.counter % 10 == 0:	
			fits = [f for f, ch in fits_populations]
			best = max(fits)
			worst = min(fits)
			ave = sum(fits) / len(fits)
			print(
				"[G %3d] score=(%4d, %4d, %4d): %r" %
				(self.counter, best, ave, worst, self.chromo2text(best_match)))
			

		return self.counter >= self.limit

	def parents(self, fits_populations):
		while True:
			father = self.tournament(fits_populations)
			mother = self.tournament(fits_populations)
			yield (father, mother)
			
	def crossover(self, parents):
		father, mother = parents
		index1 = random.randint(1, len(self.target) - 2)
		index2 = random.randint(1, len(self.target) - 2)
		if index1 > index2: index1, index2 = index2, index1
		child1 = father[:index1] + mother[index1:index2] + father[index2:]
		child2 = mother[:index1] + father[index1:index2] + mother[index2:]
		return (child1, child2)

	def mutation(self, chromosome):
		index = random.randint(0, len(self.target) - 1)
		vary = random.randint(-5, 5)
		mutated = list(chromosome)
		mutated[index] += vary
		return mutated

	# internals
	def tournament(self, fits_populations):
		alicef, alice = self.select_random(fits_populations)
		bobf, bob = self.select_random(fits_populations)
		return alice if alicef > bobf else bob

	def select_random(self, fits_populations):
		return fits_populations[random.randint(0, len(fits_populations)-1)]

	def random_chromo(self):
		return [random.uniform(-100,100) for i in range(D)]
	
GeneticAlgorithm(GuessText("Hello World!", 200, 400, 0.9, 0.2)).run()