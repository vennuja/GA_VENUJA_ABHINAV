# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 2022

@author: tdrumond & agademer

Template file for your Exercise 3 submission 
(generic genetic algorithm module)
"""
import random

class Individual:
    """Represents an Individual for a genetic algorithm"""

    def __init__(self, chromosome: list, fitness: float):
        """Initializes an Individual for a genetic algorithm

        Args:
            chromosome (list[]): a list representing the individual's
            chromosome
            fitness (float): the individual's fitness (the higher the value,
            the better the fitness)
        """
        self.chromosome = chromosome
        self.fitness = fitness

    def __lt__(self, other):
        """Implementation of the less_than comparator operator"""
        return self.fitness < other.fitness

    def __repr__(self):
        """Representation of the object for print calls"""
        return f'Indiv({self.fitness:.1f},{self.chromosome})'


class GAProblem:
    """Defines a Genetic algorithm problem to be solved by ga_solver"""

    def generate_chromosome(self):
        """Generate a valid chromosome"""
        pass

    def compute_fitness(self, chromosome):
        """Calculate fitness score"""
        pass

    def crossover(self, parent1, parent2):
        """Combine two parents to produce offspring"""
        pass

    def mutate(self, chromosome):
        """Mutate a chromosome"""
        pass


class GASolver:
    def __init__(self, problem: GAProblem, selection_rate=0.5, mutation_rate=0.1):
        """Initializes an instance of a ga_solver for a given GAProblem

        Args:
            problem (GAProblem): GAProblem to be solved by this ga_solver
            selection_rate (float, optional): Selection rate between 0 and 1.0. Defaults to 0.5.
            mutation_rate (float, optional): mutation_rate between 0 and 1.0. Defaults to 0.1.
        """
        self._problem = problem
        self._selection_rate = selection_rate
        self._mutation_rate = mutation_rate
        self._population = []

    def reset_population(self, pop_size=50):
        """ Initialize the population with pop_size random Individuals """
        self._population = []
        for _ in range(pop_size):
            chrom = self._problem.generate_chromosome()
            fitness = self._problem.compute_fitness(chrom)
            self._population.append(Individual(chrom, fitness))

    def evolve_for_one_generation(self):
        """ Apply the process for one generation : 
            -	Sort the population (Descending order)
            -	Selection: Remove x% of population (less adapted)
            -   Reproduction: Recreate the same quantity by crossing the 
                surviving ones 
            -	Mutation: For each new Individual, mutate with probability 
                mutation_rate i.e., mutate it if a random value is below   
                mutation_rate
        """

        # Selection
        self._population.sort(reverse=True)
        cutoff = int(len(self._population) * self._selection_rate)
        survivors = self._population[:cutoff]

        # Reproduction with crossover
        new_population = []
        while len(new_population) < (len(self._population) - len(survivors)):
            parent1, parent2 = random.sample(survivors, 2)
            child_chrom = self._problem.crossover(parent1.chromosome, parent2.chromosome)
            child_fitness = self._problem.compute_fitness(child_chrom)
            new_population.append(Individual(child_chrom, child_fitness))
        
         # Mutation
        for individual in new_population:
            if random.random() < self._mutation_rate:
                mutated = self._problem.mutate(individual.chromosome)
                individual.chromosome = mutated
                individual.fitness = self._problem.compute_fitness(mutated)

        self._population = survivors + new_population

    def show_generation_summary(self):
        """ Print some debug information on the current state of the population """
        best = self.get_best_individual()
        avg_fitness = sum(ind.fitness for ind in self._population) / len(self._population)
        print(f"Generation Summary: Best Fitness = {best.fitness}, Avg Fitness = {avg_fitness}")

    def get_best_individual(self):
        """ Return the best Individual of the population """
        return max(self._population, key=lambda ind: ind.fitness)

    def evolve_until(self, max_nb_of_generations=500, threshold_fitness=None):
        """ Launch the evolve_for_one_generation function until one of the two condition is achieved : 
            - Max nb of generation is achieved
            - The fitness of the best Individual is greater than or equal to
              threshold_fitness
        """
        for _ in range(max_nb_of_generations):
            self.evolve_for_one_generation()
            self.show_generation_summary()
            best = self.get_best_individual()
            if threshold_fitness and best.fitness >= threshold_fitness:
                break
