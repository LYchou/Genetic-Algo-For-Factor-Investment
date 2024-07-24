# 多核心基因演算法優化器

此專案實作了一個多核心基因演算法優化器，用於搜索交易訊號的最佳參數。該優化器設計為使用多個CPU核心並行運行，以加快搜索過程。

## 目錄

- [配置](#配置)
- [使用方法](#使用方法)
- [參數範圍](#參數範圍)

## 配置

搜索配置在 `SEARCH_CONFIG` 字典中定義：

```python
SEARCH_CONFIG = {
    'cores': 1,  # 使用的CPU核心數
    'times': 1,  # 搜索運行的次數
    'optimizer_config': {
        'pop_size': 40,  # 基因演算法的種群大小
        'generations': 5,  # 演化的世代數
        'mutation_rate': 0.05,  # 基因演算法的突變率
        'if_print': True,  # 是否打印進度
    },
}
```

根據需求調整這些參數。

## 使用方法

1. **定義參數空間：**

    ```python
    params_scope = [
        ('param1', 'category', ['c1', 'c2', 'c3']),
        ('param2', 'int', [1, 100]),
        ('param3', 'float', [0.0, 1.0]),
    ]
    ```

2. **實作 `signal_func` 和 `backtest` 函數：**

    ```python
    def signal_func(**params):
        # 根據給定的參數生成交易訊號
        return

    def backtest(signal):
        # 對給定的交易訊號進行回測
        return
    ```

3. **實作 `evaluate_fitness` 函數：**

    ```python
    def evaluate_fitness(params):
        signal = signal_func(**params)
        fitness = backtest(signal)
        return fitness
    ```

4. **運行優化器：**

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

這將執行搜索過程，打印最佳找到的參數及其適應度分數，並將其保存到CSV文件中。

## 參數範圍

`params_scope` 是基因演算法優化器的關鍵組成部分，定義了要優化的參數。每個參數在一個元組中描述，由參數名稱、搜索空間類型和搜索參數組成。這使優化器能夠理解如何在優化過程中生成和突變個體。

### 定義 `params_scope`

`params_scope` 是一個元組列表，其中每個元組定義了一個要優化的參數。每個元組具有以下結構：

```python
(param_name, search_type, search_arg)
```

- `param_name`：參數名稱。
- `search_type`：搜索空間的類型，可以是 `'int'`、`'float'` 或 `'category'`。
- `search_arg`：定義搜索空間的參數，取決於 `search_type` 而異。

### 示例

這是一個 `params_scope` 示例：

```python
params_scope = [
    ('param1', 'category', ['c1', 'c2', 'c3']),  # 類別參數
    ('param2', 'int', [1, 100]),  # 整數參數，範圍為 [1, 100]
    ('param3', 'float', [0.0, 1.0]),  # 浮點數參數，範圍為 [0.0, 1.0]
]
```

### 詳細描述

1. **類別參數**：
    - 定義為：`('param1', 'category', ['c1', 'c2', 'c3'])`
    - 參數 `param1` 可以取列表 `['c1', 'c2', 'c3']` 中的一個值。
    - 在突變期間，如果突變條件滿足（隨機數 < `mutation_rate`），`param1` 將被重新分配一個從 `['c1', 'c2', 'c3']` 中隨機選擇的新值。

2. **整數參數**：
    - 定義為：`('param2', 'int', [1, 100])`
    - 參數 `param2` 是範圍在 `[1, 100]` 內的整數。
    - 在突變期間，如果突變條件滿足，`param2` 將被重新分配一個在1到100（包括1和100）之間隨機選擇的新整數值。

3. **浮點數參數**：
    - 定義為：`('param3', 'float', [0.0, 1.0])`
    - 參數 `param3` 是範圍在 `[0.0, 1.0]` 內的浮點數。
    - 在突變期間，如果突變條件滿足，`param3` 將被重新分配一個在0.0到1.0之間隨機選擇的新浮點值。

### 自定義 `params_scope`

你可以根據具體要優化的參數來自定義 `params_scope`。確保每個參數適當地定義了名稱、類型及相應的搜索空間參數。這樣可以讓優化器有效地探索參數空間，並找到最佳表現的參數，用於你的交易策略或其他優化任務。

通過理解並正確定義 `params_scope`，你可以充分利用基因演算法優化器的潛力來增強你的交易策略或任何其他參數優化問題。