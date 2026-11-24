import numpy as np
import pandas as pd


df1 = pd.read_csv('Data/Historical Income Tax Rates and Brackets, 1862-2025.csv',
                  na_values="NaN", nrows=7)

RATE_COL = "Married Filing Jointly (Rates/Brackets)"
THRESH_COL = "Unnamed: 2" 


def parse_rate(s):
    return float(str(s).strip().rstrip("%"))


def parse_money(s):
    s = str(s).strip()
    if s in ("", "nan", "NaN"):
        return None
    return int(s.replace("$", "").replace(",", ""))


baseline_rates = [parse_rate(v) for v in df1[RATE_COL].tolist()]
lowers = [parse_money(v) for v in df1[THRESH_COL].tolist()]
lowers = [0 if x is None else x for x in lowers]

uppers = []
for i in range(len(lowers)):
    if i + 1 < len(lowers):
        uppers.append(lowers[i + 1])
    else:
        uppers.append(np.inf)

rng_data = np.random.default_rng(seed=42)
N_HOUSEHOLDS = 5000
incomes = rng_data.lognormal(mean=10.8, sigma=0.9, size=N_HOUSEHOLDS).astype(float)


def tax_due(income, rates, lowers, uppers):
    """Progressive tax: sum of (rate * income_in_bracket) across all brackets."""
    total = 0.0
    for rate, lo, hi in zip(rates, lowers, uppers):
        if income <= lo:
            break
        total += (rate / 100.0) * (min(income, hi) - lo)
    return total


baseline_revenue = sum(tax_due(inc, baseline_rates, lowers, uppers) for inc in incomes)

def revenue_objective(state):
    new_rev = sum(tax_due(inc, state, lowers, uppers) for inc in incomes)
    revenue_dev = abs(new_rev - baseline_revenue) / baseline_revenue
    rate_spread = max(state) - min(state)
    return -(rate_spread + 100.0 * revenue_dev)


class problem:

    def __init__(self, initial_population, objective_function, mutation_probability,
                 fitness_goal, gene_min=0.0, gene_max=50.0, rng=None):
        self.population = initial_population
        self.objective_function = objective_function
        self.mutation_probability = mutation_probability
        self.fitness_goal = fitness_goal
        self.gene_min = gene_min
        self.gene_max = gene_max
        self.rng = rng if rng is not None else np.random.default_rng()

    def fitness(self):
        scores = [self.objective_function(m) for m in self.population]
        min_scores = min(scores)
        max_scores = max(scores)
        if max_scores != min_scores:
            buffer = (max_scores - min_scores) * 0.05
        else:
            buffer = 1e-6
        adjusted = [(s - min_scores) + buffer for s in scores]
        total = sum(adjusted)
        p_reproduce = [a / total for a in adjusted]
        return p_reproduce

    def reproduce(self, parent1, parent2):
        k = self.rng.integers(1, len(parent1))
        child = list(parent1[:k]) + list(parent2[k:])
        return child

    def mutate(self, child):
        if self.rng.uniform(0, 1) < self.mutation_probability:
            index = self.rng.integers(0, len(child))
            new_value = self.rng.uniform(self.gene_min, self.gene_max)
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


#Initial Populatio
if __name__ == "__main__":
    POP_SIZE = 50
    N_GENERATIONS = 80
    MUTATION_PROB = 0.15
    FITNESS_GOAL = -1.0

    rng = np.random.default_rng(seed=123)

    initial_population = []
    for _ in range(POP_SIZE):
        candidate = [max(0.0, r + rng.normal(0, 5.0)) for r in baseline_rates]
        initial_population.append(candidate)

    tax_problem = problem(
        initial_population=initial_population,
        objective_function=revenue_objective,
        mutation_probability=MUTATION_PROB,
        fitness_goal=FITNESS_GOAL,
        gene_min=0.0,
        gene_max=60.0,
        rng=rng,
    )
    result = genetic_algorithm(tax_problem, N_GENERATIONS)

    baseline_str = ", ".join(["{}%".format(round(r, 1)) for r in baseline_rates])
    best_str = ", ".join(["{}%".format(round(r, 1)) for r in result["best_member"]])
    print("Baseline rates:        " + baseline_str)
    print("Best candidate rates:  " + best_str)

    base_spread = max(baseline_rates) - min(baseline_rates)
    best_spread = max(result["best_member"]) - min(result["best_member"])
    print("Spread: {} -> {} pp".format(round(base_spread, 2), round(best_spread, 2)))

    best_rev = sum(tax_due(inc, result["best_member"], lowers, uppers) for inc in incomes)
    rev_pct = (best_rev - baseline_revenue) / baseline_revenue * 100
    print("Revenue change: {:+.2f}%".format(rev_pct))