import pandas as pd
import datetime
import optimizer

SEARCH_CONFIG = {
    'cores':1,
    'times':1,
    'optimizer_config':{
                            'pop_size':40,
                            'generations':5,
                            'mutation_rate':0.05,
                            'if_print':True,
                            'search_threshold':0.3,
                            },
    }


params_scope = [
    ('param1', 'category', ['c1', 'c2', 'c3']),
    ('param2', 'int', [1, 100]),
    ('param3', 'float', [0.0, 1.0]),
]

def signal_func():
    return

def backtest(signal):
    return 

def evaluate_fitness(params):
    signal = signal_func(**params)
    fitness = backtest(signal)
    return fitness

class MultiCoreSearch(optimizer.MultiCoreSearch):

    def __init__(self, cores, times):
        super().__init__(cores, times)

    def search(self, index, result_queue):
        config = SEARCH_CONFIG['optimizer_config']
        optimizer = optimizer.GeneticAlgorithmOptimizer(evaluate_fitness, params_scope)
        optimizer.pop_size = config['pop_size']
        optimizer.generations = config['generations']
        optimizer.mutation_rate = config['mutation_rate']
        optimizer.if_print = config['if_print']
        optimizer.print_title = f'Search Index {index}:'
        result = optimizer.search(threshold=config['search_threshold'])
        return result


if __name__ == '__main__':

    cores = SEARCH_CONFIG['cores']
    times = SEARCH_CONFIG['times']
    multiCoreSearch = MultiCoreSearch(cores, times)
    results = multiCoreSearch.run()

    best_ind_list = []
    best_fitness_list = []
    for best_ind, best_fitness in results:
        print('-'*40)
        print(best_ind)
        print(best_fitness)

        if best_ind:
            best_ind_list.append(best_ind)
            best_fitness_list.append(best_fitness)

    now = datetime.datetime.now().strftime('(%Y-%m-%d %H%M%S)')
    pd.DataFrame(best_ind_list).to_csv(f'{now}ind.csv', index=False)
    pd.DataFrame(best_fitness_list).to_csv(f'{now}fitness.csv', index=False)


