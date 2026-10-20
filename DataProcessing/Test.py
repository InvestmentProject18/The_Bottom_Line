import random
import numpy as np

target = [1, 3, 2, 1, 1, 4, 1, 1]   # global constant

def recipe_success(state):
    """
    Takes a state (list of 8 integers).
    Returns -total_distance, where total_distance is the sum of
    absolute differences between state and target.
    """
    
    total_distance = 0
    #Gene Loop
    for i in range(len(target)) :
        total_distance += abs(state[i]-target[i])
    return -total_distance

print(recipe_success([1, 3, 2, 1, 1, 4, 1, 1])) 
print(recipe_success([5, 5, 5, 5, 5, 5, 5, 5]))
print(recipe_success([2, 3, 2, 1, 1, 4, 1, 1]))