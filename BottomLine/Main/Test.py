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

    def __init__(self, initial_population, objective_function, mutation_probability, fitness_goal, gene_min=1, gene_max=4, rng = None) :
        self.population = initial_population
        self.objective_function = objective_function
        self.mutation_probability = mutation_probability
        self.fitness_goal = fitness_goal
        self.gene_min, self.gene_max = gene_min, gene_max
        self.rng = rng if rng is not None else np.random.default_rng()

    def fitness(self) :
        scores = [self.objective_function(m) for m in self.population]
        min_scores = min(scores)
        max_scores = max(scores)
        if max_scores != min_scores :
            buffer = (max_scores - min_scores) * 0.05
        else :
            buffer = 1e-6
        adjusted = [(s-min_scores) + buffer for s in scores]
        total = sum(adjusted)
        p_reproduce = [a / total for a in adjusted]
        return p_reproduce
        
    def reproduce(self,parent1,parent2) :
        k = self.rng.integers(1, len(parent1))
        child = parent1[:k] + parent2[k:]
        return(child)
        
    def mutate(self,child) :
       if self.rng.uniform(0, 1) < self.mutation_probability:
           index = self.rng.integers(0, len(child))
           new_value = self.rng.integers(self.gene_min, self.gene_max + 1)
           child[index] = new_value
       return child
    
