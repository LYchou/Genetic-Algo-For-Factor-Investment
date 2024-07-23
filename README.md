# Multi-Core Genetic Algorithm Optimizer

This project implements a multi-core genetic algorithm optimizer for searching the best parameters for trading signals. The optimizer is designed to run in parallel using multiple CPU cores to speed up the search process.

## Table of Contents

- [Configuration](#configuration)
- [Usage](#usage)
- [Parameter Scope](#parameter-scope)

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
    },
}
```

Adjust these parameters according to your requirements.

## Usage

1. **Define Your Parameter Space:**

    ```python
    params_scope = [
        ('param1', 'category', ['c1', 'c2', 'c3']),
        ('param2', 'int', [1, 100]),
        ('param3', 'float', [0.0, 1.0]),
    ]
    ```

2. **Implement the `signal_func` and `backtest` Functions:**

    ```python
    def signal_func(**params):
        # Generate a trading signal based on the given parameters
        return

    def backtest(signal):
        # Perform a backtest on the given trading signal
        return
    ```

3. **Implement the `evaluate_fitness` Function:**

    ```python
    def evaluate_fitness(params):
        signal = signal_func(**params)
        fitness = backtest(signal)
        return fitness
    ```

4. **Run the Optimizer:**

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

This will execute the search process, print the best-found parameters and their fitness scores, and save them to CSV files.

## Parameter Scope

The `params_scope` is a crucial component of the genetic algorithm optimizer, defining the parameters to be optimized. Each parameter is described in a tuple consisting of the parameter name, the type of search space, and the search arguments. This allows the optimizer to understand how to generate and mutate individuals during the optimization process.

### Defining the `params_scope`

The `params_scope` is a list of tuples, where each tuple defines a parameter to be optimized. Each tuple has the following structure:

```python
(param_name, search_type, search_arg)
```

- `param_name`: The name of the parameter.
- `search_type`: The type of the search space, which can be `'int'`, `'float'`, or `'category'`.
- `search_arg`: The arguments defining the search space, which vary depending on the `search_type`.

### Example

Here is an example `params_scope`:

```python
params_scope = [
    ('param1', 'category', ['c1', 'c2', 'c3']),  # Categorical parameter
    ('param2', 'int', [1, 100]),  # Integer parameter with bounds [1, 100]
    ('param3', 'float', [0.0, 1.0]),  # Float parameter with bounds [0.0, 1.0]
]
```

### Detailed Description

1. **Categorical Parameter**:
    - Defined as: `('param1', 'category', ['c1', 'c2', 'c3'])`
    - The parameter `param1` can take on one of the values in the list `['c1', 'c2', 'c3']`.
    - During mutation, if the mutation condition is met (random number < `mutation_rate`), `param1` will be assigned a new value randomly chosen from `['c1', 'c2', 'c3']`.

2. **Integer Parameter**:
    - Defined as: `('param2', 'int', [1, 100])`
    - The parameter `param2` is an integer within the bounds `[1, 100]`.
    - During mutation, if the mutation condition is met, `param2` will be assigned a new integer value randomly chosen between 1 and 100 (inclusive).

3. **Float Parameter**:
    - Defined as: `('param3', 'float', [0.0, 1.0])`
    - The parameter `param3` is a float within the bounds `[0.0, 1.0]`.
    - During mutation, if the mutation condition is met, `param3` will be assigned a new float value randomly chosen between 0.0 and 1.0.

### Customizing `params_scope`

You can customize the `params_scope` according to the specific parameters you want to optimize. Ensure each parameter is appropriately defined with its name, type, and the corresponding search space arguments. This allows the optimizer to effectively explore the parameter space and find the best-performing parameters for your trading signals or other optimization tasks.

By understanding and correctly defining the `params_scope`, you can leverage the full potential of the genetic algorithm optimizer to enhance your trading strategies or any other parameter optimization problems.