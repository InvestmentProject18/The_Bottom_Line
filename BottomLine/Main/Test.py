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

    def __init__(self, initial_population, objective_function, mutation_probability, fitness_goal, gene_min=1, gene_max=4,) :
        self.population = initial_population
        self.objective_function = recipe_success
        self.mutation_probability = mutation_probability
        self.fitness_goal = fitness_goal
        self.gene_min,gene_max = gene_min,gene_max

    def fitness(self) :
        scores = [self.objective_function(m) for m in self.population]
        min_scores = min(scores)
        max_scores = max(scores)
        if max_score != min_score :
            buffer = (max_score - min_score) * 0.05
        else :
            buffer = 1e-6
        adjusted = [(score-min_score) + buffer for s in scores)]
        total = sum(adjusted)
        p_reproduce = [a / total for a in adjusted]
        return p_reproduce
        
        
