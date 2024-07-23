# Multi-Core Genetic Algorithm Optimizer

This project implements a multi-core genetic algorithm optimizer for searching the best parameters for trading signals. The optimizer is designed to run in parallel using multiple CPU cores to speed up the search process.

## Table of Contents

- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Files](#files)
- [License](#license)

## Installation

To install the necessary dependencies, run:

```bash
pip install pandas
```

Ensure you have the `optimizer` module available in your Python environment. If it is a custom module, make sure it is in the Python path.

## Configuration

The search configuration is defined in the `SEARCH_CONFIG` dictionary:

```python
SEARCH_CONFIG = {
    'cores': 1,  # Number of CPU cores to use
    'times': 1,  # Number of times to run the search
    'optimizer_config': {
        'pop_size': 40,  # Population size for the genetic algorithm
        'generations': 5,  # Number of generations to evolve
        'mutation_rate': 0.05,  # Mutation rate for the genetic algorithm
        'if_print': True,  # Whether to print progress
        'search_threshold': 0.3,  # Fitness threshold to stop the search
    },
}
```

You can adjust these parameters according to your requirements.

## Usage

1. Define your parameter space in the `params_scope` list:

    ```python
    params_scope = [
        ('param1', 'category', ['c1', 'c2', 'c3']),
        ('param2', 'int', [1, 100]),
        ('param3', 'float', [0.0, 1.0]),
    ]
    ```

2. Implement the `signal_func` and `backtest` functions:

    ```python
    def signal_func(**params):
        # Generate a trading signal based on the given parameters
        return

    def backtest(signal):
        # Perform a backtest on the given trading signal
        return
    ```

3. Implement the `evaluate_fitness` function:

    ```python
    def evaluate_fitness(params):
        signal = signal_func(**params)
        fitness = backtest(signal)
        return fitness
    ```

4. Run the optimizer:

    ```python
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
    ```

This will execute the search process, print the best found parameters and their fitness scores, and save them to CSV files.

## Files

- `optimizer.py`: Contains the implementation of the genetic algorithm optimizer.
- `main.py`: The main script to run the multi-core search.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
```

Feel free to adjust the content as needed to better fit your project specifics.