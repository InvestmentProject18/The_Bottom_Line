import random
import numpy as np
target = [1, 3, 2, 1, 1, 4, 1, 1]   # global constant

def recipe_success(state):
    total_distance = 0
    #Gene Loop
    for i in range(len(target)) :
        total_distance += abs(state[i]-target[i])
    return -total_distance


class problem() :
    def __init__(self, initial_population, objective_function, mutation_probability, fitness_goal, gene_min=1, gene_max=4, rng=None) :
       self.initial_population = initial_population
        