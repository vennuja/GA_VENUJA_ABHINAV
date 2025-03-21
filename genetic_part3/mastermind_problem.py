# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 2022

@author: tdrumond & agademer

Template file for your Exercise 3 submission 
(GA solving Mastermind example)
"""
from ga_solver import GAProblem
import mastermind as mm
import random 

class MastermindProblem(GAProblem):
    """Implementation of GAProblem for the mastermind problem"""
    
    def __init__(self, match):
        self._match = match

    def generate_chromosome(self):
        """Generate a random guess"""
        return self._match.generate_random_guess()

    def compute_fitness(self, chrom):
        """Fitness = match's rating"""
        return self._match.rate_guess(chrom)

    def crossover(self, parent1, parent2):
        """Single-point crossover"""
        x_point = random.randint(0, len(parent1)-1)
        return parent1[:x_point] + parent2[x_point:]

    def mutate(self, chrom):
        """Replace a random color"""
        mutated = list(chrom)
        pos = random.randint(0, len(chrom)-1)
        mutated[pos] = random.choice(mm.get_possible_colors())
        return mutated


if __name__ == '__main__':

    from ga_solver import GASolver

    match = mm.MastermindMatch(secret_size=4)
    problem = MastermindProblem(match)
    solver = GASolver(problem)

    solver.reset_population()
    solver.evolve_until()

    best = solver.get_best_individual()
    print(f"Best guess: {best.chromosome}")
    print(f"Problem solved? {match.is_correct(best.chromosome)}")

    
