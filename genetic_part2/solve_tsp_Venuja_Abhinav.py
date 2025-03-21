# -*- coding: utf-8 -*-
"""
Created on Mon Feb 21 11:24:15 2022

@author: agademer & tdrumond

Template for exercise 1
(genetic algorithm module specification)
"""

import cities
import random

# Loading city data 
city_dict = cities.load_cities("cities.txt")

class Individual:
    # Represents the TSP solution (road) with fitness value
    def __init__(self, chromosome, fitness):
        self.chromosome = chromosome  
        self.fitness = fitness        

    def __lt__(self, other):
        """Enable sorting by fitness"""
        return self.fitness < other.fitness

    def __repr__(self):
        return f'Road Length: {-self.fitness:.1f}'

class GASolver:
    # Genetic Algorithm implementation for TSP
    def __init__(self, selection_rate=0.5, mutation_rate=0.1):
        self._selection_rate = selection_rate
        self._mutation_rate = mutation_rate
        self._population = []

    # Initializing the population
    def reset_population(self, pop_size=50):
        """Create initial population of random valid roads"""
        self._population = []
        for _ in range(pop_size):
            # Generate valid chromosome (all cities, no duplicates)
            chromosome = cities.default_road(city_dict)
            random.shuffle(chromosome)
            # Calculate fitness as negative road length
            fitness = -cities.road_length(city_dict, chromosome)
            self._population.append(Individual(chromosome, fitness))

    # Evolution
    def evolve_for_one_generation(self):
        """Execute one full evolution cycle"""
        # Selection, Keep top individuals
        self._population.sort(reverse=True)
        cutoff = int(len(self._population) * self._selection_rate)
        survivors = self._population[:cutoff]

        # Reproduction, Ordered crossover
        new_offspring = []
        while len(new_offspring) < (len(self._population) - len(survivors)):
            parent1, parent2 = random.sample(survivors, 2)
            child = self._crossover(parent1.chromosome, parent2.chromosome)
            fitness = -cities.road_length(city_dict, child)
            new_offspring.append(Individual(child, fitness))

        # Mutation, Swap two cities
        for ind in new_offspring:
            if random.random() < self._mutation_rate:
                idx1, idx2 = random.sample(range(len(ind.chromosome)), 2)
                ind.chromosome[idx1], ind.chromosome[idx2] = ind.chromosome[idx2], ind.chromosome[idx1]
                ind.fitness = -cities.road_length(city_dict, ind.chromosome)

        self._population = survivors + new_offspring

    def _crossover(self, parent1, parent2):
        #Ordered crossover to create valid child chromosome
        size = len(parent1)
        start, end = sorted(random.sample(range(size), 2))
        
        # Initialing child with parent1's segment
        child = [None] * size
        child[start:end+1] = parent1[start:end+1]
        
        # Fill from parent2 while skipping duplicates
        ptr = 0
        for i in range(size):
            if child[i] is None:
                while parent2[ptr] in child:
                    ptr += 1
                child[i] = parent2[ptr]
                ptr += 1
        return child

    # Getting the solution
    def get_best_individual(self):
        """Return best solution found"""
        return max(self._population, key=lambda x: x.fitness)

    def evolve_until(self, max_nb_of_generations=500, threshold_fitness=None):
        """Run evolution until stopping condition"""
        for _ in range(max_nb_of_generations):
            self.evolve_for_one_generation()
            best = self.get_best_individual()
            if threshold_fitness and best.fitness >= threshold_fitness:
                break

# Testing
if __name__ == "__main__":
    solver = GASolver()
    solver.reset_population() # Initialize population
    solver.evolve_until()  # Run evolution

    best = solver.get_best_individual()
    print(f"Best solution found: {best}")
    cities.draw_cities(city_dict, best.chromosome)  