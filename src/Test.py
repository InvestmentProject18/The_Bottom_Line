import numpy as np
from GeneticAlgorithm import problem, recipe_success, target, genetic_algorithm

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