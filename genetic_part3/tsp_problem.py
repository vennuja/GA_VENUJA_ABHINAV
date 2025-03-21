# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 2022

@author: tdrumond & agademer

Template file for your Exercise 3 submission 
(GA solving TSP example)
"""
from ga_solver import GAProblem
import cities
import random

class TSProblem(GAProblem):
    """Implementation of GAProblem for the traveling salesperson problem"""
    def __init__(self, city_dict):
        self.city_dict = city_dict
        self.possible_cities = cities.default_road(city_dict)

    def generate_chromosome(self):
        """From solve_tsp_Venuja_Abhinav.py: Generate a shuffled road"""
        chrom = self.possible_cities.copy()
        random.shuffle(chrom)
        return chrom
    
    def compute_fitness(self, chrom):
        """From solve_tsp_Venuja_Abhinav.py: Fitness = -road_length"""
        return -cities.road_length(self.city_dict, chrom)
    
    def crossover(self, parent1, parent2):
        """From solve_tsp_Venuja_Abhinav.py: Ordered crossover"""
        start, end = sorted(random.sample(range(len(parent1)), 2))
        child = [None] * len(parent1)
        child[start:end+1] = parent1[start:end+1]
        ptr = 0
        for i in range(len(parent1)):
            if child[i] is None:
                while parent2[ptr] in child:
                    ptr += 1
                child[i] = parent2[ptr]
                ptr += 1
        return child
    
    def mutate(self, chrom):
        """From solve_tsp_Venuja_Abhinav.py: Swap two cities"""
        mutated = chrom.copy()
        pos1, pos2 = random.sample(range(len(chrom)), 2)
        mutated[pos1], mutated[pos2] = mutated[pos2], mutated[pos1]
        return mutated
                                   
                                
if __name__ == '__main__':

    from ga_solver import GASolver

    city_dict = cities.load_cities("cities.txt")
    problem = TSProblem(city_dict)
    solver = GASolver(problem)
    solver.reset_population()
    solver.evolve_until()
    best = solver.get_best_individual()
    cities.draw_cities(city_dict, solver.get_best_individual().chromosome)
