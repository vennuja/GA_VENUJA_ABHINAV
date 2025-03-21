# -*- coding: utf-8 -*-
"""
Created on Mon Feb 21 11:24:15 2022

@author: agademer & tdrumond

Template for exercise 1
(genetic algorithm module specification)
"""

import mastermind as mm
import random


MATCH = mm.MastermindMatch(secret_size=4)

class Individual:
    """Represents an Individual for a genetic algorithm"""

    def __init__(self, chromosome: list, fitness: float):
        """Initializes an Individual for a genetic algorithm 

        Args:
            chromosome (list[]): a list representing the individual's chromosome
            fitness (float): the individual's fitness (the higher, the better the fitness)
        """
        self.chromosome = chromosome
        self.fitness = fitness

    def __lt__(self, other):
        """Implementation of the less_than comparator operator"""
        return self.fitness < other.fitness

    def __repr__(self):
        """Representation of the object for print calls"""
        return f'Indiv({self.fitness:.1f},{self.chromosome})'


class GASolver:
    def __init__(self, selection_rate=0.5, mutation_rate=0.1):
        """Initializes an instance of a ga_solver for a given GAProblem

        Args:
            selection_rate (float, optional): Selection rate between 0 and 1.0. Defaults to 0.5.
            mutation_rate (float, optional): mutation_rate between 0 and 1.0. Defaults to 0.1.
        """
        self._selection_rate = selection_rate
        self._mutation_rate = mutation_rate
        self._population = []

    def reset_population(self, pop_size=50):
        """ Initialize the population with pop_size random Individuals """

        self._population = []
        for _ in range(pop_size):
            chromosome = MATCH.generate_random_guess() # Create a random chromosome
            fitness = MATCH.rate_guess(chromosome) # Evaluate the fitness
            new_individual = Individual(chromosome, fitness) # Create a new individual
            self._population.append(new_individual)  # Add to the population

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

        # Sorting individuals by fitness in descending order
        self._population.sort(reverse=True)

        # selecting only the top individuals
        cutoff = int(len(self._population) * self._selection_rate)
        self._population = self._population[:cutoff]

        # Reproduction: Generating new individuals
        # 'a' is parent1 and 'b' is parent2
        new_population = []
        while len(new_population) < len(self._population):
            a, b = random.sample(self._population, 2)
            x_point = random.randrange(0, len(a.chromosome))
            new_chrom = a.chromosome[0:x_point] + b.chromosome[x_point:]
            new_individual = Individual(new_chrom, MATCH.rate_guess(new_chrom))
            new_population.append(new_individual)

        # Mutation: Introducing variability
        for individual in new_population:
            if random.random() < self._mutation_rate:
                pos = random.randrange(len(individual.chromosome))
                valid_colors = mm.get_possible_colors()
                new_gene = random.choice(valid_colors)
                new_chrom = individual.chromosome[0:pos] + [new_gene] + individual.chromosome[pos+1:]
                individual.fitness = MATCH.rate_guess(new_chrom)
                individual.chromosome = new_chrom
                new_individual = Individual(new_chrom, MATCH.rate_guess(new_chrom)) 
        self._population.extend(new_population)    
    
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


if __name__ == "__main__":
    """Main script execution: Initialize game, run GA solver, and display results"""
    solver = GASolver()
    solver.reset_population()
    solver.evolve_until(threshold_fitness=MATCH.max_score())

    best = solver.get_best_individual()
    print(f"Best guess: {best.chromosome}")
    print(f"Problem solved? {MATCH.is_correct(best.chromosome)}")