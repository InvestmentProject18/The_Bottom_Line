import random
import numpy as np
target = [1, 3, 2, 1, 1, 4, 1, 1]  

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
        
def genetic_algorithm(genetic_problem, num_generations):
    pop_size = len(genetic_problem.population)
    rng = genetic_problem.rng
    
    best_member = None
    best_score = -float("inf")
    generation_found = None
    history_best = []
    history_avg = []
    
    for gen in range(int(num_generations)):
        scores = [genetic_problem.objective_function(m) for m in genetic_problem.population]
        
        gen_best_idx = int(np.argmax(scores))
        gen_best_score = scores[gen_best_idx]
        gen_best_member = genetic_problem.population[gen_best_idx]
        
        if gen_best_score > best_score:
            best_score = gen_best_score
            best_member = list(gen_best_member)
        
        history_best.append(best_score)
        history_avg.append(float(np.mean(scores)))
        
        if best_score >= genetic_problem.fitness_goal:
            generation_found = gen
            break
        
        p = genetic_problem.fitness()
        
        new_population = []
        for _ in range(pop_size):
            i1, i2 = rng.choice(pop_size, size=2, replace=True, p=p)
            parent1 = genetic_problem.population[int(i1)]
            parent2 = genetic_problem.population[int(i2)]
            
            child = genetic_problem.reproduce(parent1, parent2)
            child = genetic_problem.mutate(child)
            new_population.append(child)
        
        genetic_problem.population = new_population
    
    return {
        "best_member": best_member,
        "best_score": best_score,
        "generation_found": generation_found,
        "history_best": history_best,
        "history_avg": history_avg,
    }    



if __name__ == "__main__":
    seed = 42
    rng = np.random.default_rng(seed)

    population_size = 100
    dna_len = len(target)
    gene_min, gene_max = 1, 4

    initial_population = [
        [int(rng.integers(gene_min, gene_max + 1)) for _ in range(dna_len)]
        for _ in range(population_size)
    ]


    genetic_problem = problem(
        initial_population=initial_population,
        objective_function=recipe_success,
        mutation_probability=0.2,
        fitness_goal=0,                 
        gene_min=gene_min,
        gene_max=gene_max,
        rng=rng,
    )

    out = genetic_algorithm(genetic_problem, 200)

    out["best_member"] = [int(x) for x in out["best_member"]]
    out["best_score"] = int(out["best_score"])
    out["history_best"] = [int(x) for x in out["history_best"]]

    print(out)