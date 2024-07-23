import numpy as np
import multiprocessing

EPSILON = 1e-15


class MultiCoreSearch:

    def __init__(self, cores: int, times: int):
        self.cores = cores
        self.times = times

    def search(self, index, result_queue):
        # override
        pass
    
    def _search_wrapper(self, index, result_queue):

        print(f'Search Index {index} Start')
        result = self.search(index, result_queue)
        print(f'Search Index {index} End')
        result_queue.put(result)
        # try:
        #     print(f'Search Index {index} Start')
        #     result = self.search(index, result_queue)
        #     print(f'Search Index {index} End')
        #     result_queue.put(result)
        # except Exception as e:
        #     print(f'Error in Search Index {index}: {e}')
        #     result_queue.put(None)

    def run(self) -> list:
        result_queue = multiprocessing.Queue()
        processes = []

        for i in range(self.times):
            p = multiprocessing.Process(
                target=self._search_wrapper,
                args=(i+1, result_queue)
            )
            processes.append(p)
            p.start()

            if len(processes) >= self.cores:
                for p in processes:
                    p.join()
                processes = []

        for p in processes:
            p.join()

        results = [result_queue.get() for _ in range(self.times)]

        return results

class GeneticAlgorithmOptimizer:
    """
    A Genetic Algorithm optimizer for searching multiple local optima.

    Attributes:
        evaluate_fitness (callable): The fitness evaluation function.
        params_scope (list of tuples): Parameters to be optimized, each defined as a tuple 
                                 (param_name, search_type, search_arg).
        pop_size (int): The population size.
        generations (int): The number of generations to evolve.
        mutation_rate (float): The probability of mutation for each parameter in an individual.
    """

    def __init__(self, evaluate_fitness, params_scope, pop_size=50, generations=100, mutation_rate=0.01, if_print=True, print_title='') -> None:
        """
        Initializes the GeneticAlgorithmOptimizer with given parameters.

        Args:
            evaluate_fitness (callable): The fitness evaluation function.
            params_scope (list of tuples): Parameters to be optimized, each defined as a tuple 
                                     (param_name, search_type, search_arg).
            pop_size (int, optional): The population size. Default is 50.
            generations (int, optional): The number of generations to evolve. Default is 100.
            mutation_rate (float, optional): The probability of mutation for each parameter in an individual. Default is 0.01.
        """
        self.evaluate_fitness = evaluate_fitness
        self.params_scope = params_scope
        self.pop_size = pop_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        
        self.if_print = if_print
        self.print_title = print_title

        self.best_ind = None
        self.best_fitness = None
        self.generations_best = []

    def search(self):
        """
        The core genetic algorithm implementation.

        Returns:
            tuple: The best individual and its fitness score.
        """
        population = self.initialize_population(self.pop_size, self.params_scope)
        best_fitness = -np.inf
        best_ind = {}
        for generation in range(self.generations):
            probs = []
            for ind in population:
                fitness = self.evaluate_fitness(ind)
                probs.append(fitness + EPSILON)
                if fitness>best_fitness:
                    best_fitness = fitness
                    best_ind = ind
            self.generations_best.append((best_fitness, best_ind))
            probs /= sum(probs)
            parents = self.select_parents(population, probs)
            new_population = []
            for i in range(0, self.pop_size, 2):
                if (i+1)==self.pop_size:
                    continue
                parent1, parent2 = parents[i], parents[i+1]
                child1, child2 = self.crossover(parent1, parent2), self.crossover(parent1, parent2)
                new_population.extend([self.mutate(child1, self.params_scope, self.mutation_rate), self.mutate(child2, self.params_scope, self.mutation_rate)])
            
            population = new_population
            print(f'Generation {generation+1}, Best Fitness: {best_fitness}')

        self.best_ind = best_ind
        self.best_fitness = best_fitness

        return best_ind, best_fitness

    
    @staticmethod
    def initialize_population(pop_size, params_scope):
        """
        Initializes the population.

        Args:
            pop_size (int): The population size.
            params_scope (list of tuples): Parameters to be optimized, each defined as a tuple 
                                     (param_name, search_type, search_arg).

        Returns:
            list: A list of individuals, where each individual is a dictionary of parameter values.
        """
        population = []
        for _ in range(pop_size):
            individual = {}
            for param_name, search_type, search_arg in params_scope:
                if search_type == 'int':
                    lb, ub = search_arg
                    individual[param_name] = np.random.randint(lb, ub+1)
                elif search_type == 'float':
                    lb, ub = search_arg
                    individual[param_name] = np.random.uniform(lb, ub)
                elif search_type == 'category':
                    individual[param_name] = np.random.choice(search_arg)
            population.append(individual)
        return population

    @staticmethod
    def select_parents(population, probs):
        """
        Selects parents based on their fitness.

        Args:
            population (list): The current population.
            probs (list): The probs scores of the population.

        Returns:
            list: A list of selected parents.
        """
        probs_sum = sum(probs)
        probs = [prob / probs_sum for prob in probs]
        parents_indices = np.random.choice(len(population), size=len(population), p=probs)
        parents = [population[i] for i in parents_indices]
        return parents

    @staticmethod
    def crossover(parent1, parent2):
        """
        Performs crossover between two parents to produce a child.

        Args:
            parent1 (dict): The first parent.
            parent2 (dict): The second parent.

        Returns:
            dict: The child produced from the crossover.
        """
        child = {}
        for param in parent1:
            if np.random.rand() > 0.5:
                child[param] = parent1[param]
            else:
                child[param] = parent2[param]
        return child

    @staticmethod
    def mutate(individual, params_scope, mutation_rate=0.01):
        """
        Performs mutation on an individual.

        Args:
            individual (dict): The individual to mutate.
            params_scope (list of tuples): Parameters to be optimized, each defined as a tuple 
                                     (param_name, search_type, search_arg).
            mutation_rate (float): The probability of mutation for each parameter in an individual.

        Returns:
            dict: The mutated individual.
        """
        for param_name, search_type, search_arg in params_scope:
            if np.random.rand() < mutation_rate:
                if search_type == 'int':
                    lb, ub = search_arg
                    individual[param_name] = np.random.randint(lb, ub+1)
                elif search_type == 'float':
                    lb, ub = search_arg
                    individual[param_name] = np.random.uniform(lb, ub)
                elif search_type == 'category':
                    individual[param_name] = np.random.choice(search_arg)
        return individual
