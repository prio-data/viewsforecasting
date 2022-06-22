import random
import bisect
import numpy as np
from functools import partial
import pandas as pd
from sklearn.metrics import mean_squared_error
import pickle
import os
import sys
import uuid


class memoize:

    def __init__(self, file=None, refresh=False, save_every_n=1, directory='memos'):
        
        if directory and file:
            os.makedirs(directory, exist_ok=True)
            file = f"./{directory.strip('/')}/{file}"


        self.file = file
        #print(self.file)
        self.save_every_n = save_every_n
        if file:
            try:
                with open(file, 'rb') as f:
                    saved = pickle.load(f)
                    self.memo = saved[0]
                    self.fitness = saved[1]
            except:
                file = None
                pass

        if refresh or not file:
            print("Refreshing")
            self.memo = []
            self.fitness = []

    def lookup(self, dic):
        if dic in self.memo:
            lookup_index = self.memo.index(dic)
            organism = self.memo[lookup_index]
            fitness = self.fitness[lookup_index]
            return organism, fitness
        else:
            return None, None

    def save_organism(self, organism, fitness):
        self.memo.append(organism)
        self.fitness.append(fitness)
        if len(self.memo) % self.save_every_n == 0 and self.file:
            # print('WRITING')
            with open(self.file, 'wb') as f:
                pickle.dump((self.memo, self.fitness), f)


temp_file_name = uuid.uuid4().hex
memo = memoize(file=f'memo_{temp_file_name}.pickle', refresh=True)


def genetic_algorithm(population, fitness_fn, gene_pool, f_thres=None, ngen=1000, pmut=0.1, debug_store=True):
    fitness_list = []
    pop_len = len(population)
    for i in range(ngen):
        print(f"GEN {i} :", end='')

        # Keep clones of the best 10% for the next generation.
        keepers = population[0:int(len(population) * 0.1)]

        # Create a new generation with everyone in the pool.
        random.shuffle(population)
        population = [mutate(recombine(*select(2, population, fitness_fn)), gene_pool, pmut)
                      for i in range(len(population))]

        fittest_individual = fitness_threshold(fitness_fn, f_thres, population)
        if fittest_individual:
            print("FI")
            return fittest_individual

        # compute the fitness function
        # Add the keeper clones to the new population:
        population += keepers
        # Compute the fitness:
        fitness = [fitness_fn(i) for i in population]
        # sort by fitness:
        fitness_list = [(i, j) for j, i in sorted(zip(fitness, population), reverse=True)]
        # cull the least efficient to keep the population numbers constant:
        fitness_list = fitness_list[0:pop_len]
        # make new population sorted:
        population = [i for i, j in fitness_list]

        if debug_store:
            os.makedirs('exploration_pickle', exist_ok=True)
            with open(f'exploration_pickle/gen_{i}_{temp_file_name}.p', 'wb') as pickle_file:
                pickle.dump(fitness_list, pickle_file)

        best_ten = fitness_list[0:10]

        total_fit = sum([j for i, j in best_ten]) / len(best_ten)
        max_fit = fitness_fn(best_ten[0][0])
        print(f'AVG FITNESS BEST 10: {total_fit}, BEST FIT : {max_fit}')

    print("Optimized")

    return fitness_list


def fitness_threshold(fitness_fn, f_thres, population):
    if not f_thres:
        return None

    fittest_individual = max(population, key=fitness_fn)
    if fitness_fn(fittest_individual) >= f_thres:
        return fittest_individual

    return None


def weighted_sampler(seq, weights):
    """Return a random-sample function that picks from seq weighted by weights."""
    totals = []
    for w in weights:
        totals.append(w + totals[-1] if totals else w)
    return lambda: seq[bisect.bisect(totals, random.uniform(0, totals[-1]))]


def select(r, population, fitness_fn):
    fitnesses = map(fitness_fn, population)
    sampler = weighted_sampler(population, fitnesses)
    return [sampler() for i in range(r)]


def recombine(x, y):
    n = len(x)
    c = random.randrange(0, n)
    return x[:c] + y[c:]


def recombine_uniform(x, y):
    n = len(x)
    result = [0] * n
    indexes = random.sample(range(n), n)
    for i in range(n):
        ix = indexes[i]
        result[ix] = x[ix] if i < n / 2 else y[ix]

    return ''.join(str(r) for r in result)


def mutate(x, gene_pool, pmut):
    if random.uniform(0, 1) >= pmut:
        return x

    n = len(x)
    g = len(gene_pool)
    c = random.randrange(0, n)
    r = random.randrange(0, g)

    new_gene = gene_pool[r]
    return x[:c] + [new_gene] + x[c + 1:]


def linear_genes(search_start=0, search_stop=1, search_step=0.02):
    """
    Make discrete genes from a continuous distribution, discretizing by step
    :param search_start: lowest value of the search range
    :param search_stop: highest value of the search range
    :param search_step: The discretization step.
    :return: A discrete gene pool
    """
    return np.linspace(search_start, search_stop, int((search_stop - search_start) / search_step) + 1)


def init_population_sum(pop_number, gene_pool, number_of_models, min_range, max_range):
    """
    :param pop_number:
    :param gene_pool:
    :param number_of_models:
    :param min:
    :param max:
    :return:
    """
    g = len(gene_pool)
    population = []
    i = 0
    j = 0
    while (i < pop_number):
        j+=1
#        if j > 1000*pop_number:
#            raise ValueError("The gene pool you selected is really bad for this task! ")
        new_individual = [gene_pool[random.randrange(0, g)] for j in range(number_of_models)]
        if min_range < sum(new_individual) < max_range:
            population.append(new_individual)
            i += 1
    return population




def init_population(pop_number, gene_pool, number_of_models):
    """Initializes population for genetic algorithm
    pop_number  :  Number of individuals in population
    gene_pool   :  List of possible values for individuals
    state_length:  The length of each individual"""

    g = len(gene_pool)
    population = []
    for i in range(pop_number):
        new_individual = [gene_pool[random.randrange(0, g)] for j in range(number_of_models)]
        population.append(new_individual)
    return population


def fetch_data():
    df = pd.read_csv('data_sim/simulated.csv')
    df = df[df.month_id == 3]
    df = df[['a', 'b', 'c', 'resp']]
    Y = df['resp']
    X = df.copy()
    del X['resp']
    return Y, X


def weighted_mse_score(Y_true, X, eval_func, genes):
    """
    :param Y_true:
    :param X:
    :param eval_func:
    :param genes:
    :return:
    """

    organism, fitness = memo.lookup(genes)
    if fitness:
        # print("FOUND")
        return fitness

    Y_pred = (X * genes).sum(axis=1)
    fitness = 2.71 ** (1 / (eval_func(Y_true, Y_pred) + 10e-16))

    memo.save_organism(genes, fitness)
    # print(genes, fitness)

    return fitness


def test_run():
    population = init_population(100, linear_genes(), 3)
    Y, X = fetch_data()

    inst_mse = partial(weighted_mse_score, Y, X, mean_squared_error)
    x = genetic_algorithm(population, inst_mse, linear_genes(), f_thres=None, ngen=250, pmut=0.25)
    for i in x:
        print(f'Genes/weights: {i}, MSE: {1 / inst_mse(i)}')


if __name__ == '__main__':
    test_run()
