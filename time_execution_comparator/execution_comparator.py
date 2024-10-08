import time
import typing
from collections.abc import Callable

from easy_console_table import TwoEntryTable
from tqdm import tqdm


def execute_function(func: typing.Callable):
    start_time = time.perf_counter()
    func()
    return time.perf_counter() - start_time


class ExecutionComparator:
    def __init__(self):
        self.table: TwoEntryTable = TwoEntryTable()
        self.table.add_column_names("Total\nExecution\nTime", "Average\nTime", "Max\nTime\nExecution",
                                    "Min\nTime\nExecution", "Difference", "Iterations")
        self.table.title = "Time\nCalculator"
        self.returned_value: dict[str: list[float]] = {}

    def reset(self):
        self.table: TwoEntryTable = TwoEntryTable()
        self.table.add_column_names("Total\nExecution\nTime", "Average\nTime", "Max\nTime\nExecution",
                                    "Min\nTime\nExecution", "Difference", "Iterations")
        self.table.title = "Time\nCalculator"
        self.returned_value: dict[str: list[float]] = {}

    def execute_iterations(self, func: Callable, iterations: int):
        progress_bar = tqdm(total=iterations, desc=f"Overall Progress for {func.__name__}")
        function_values = []
        for _ in range(iterations):
            function_values.append(execute_function(func))
            progress_bar.update(1)
        max_value = max(function_values)
        min_value = min(function_values)
        self.returned_value[func.__name__] = [
            sum(function_values),  # total time
            sum(function_values) / iterations,  # average time
            max_value,  # max time
            min_value,  # min time
            max_value - min_value  # difference
        ]
        progress_bar.close()

    def compare_execution(self, *args: typing.Callable, iterations: int = 1):
        for func in args:
            self.execute_iterations(func, iterations)

        for k, v in self.returned_value.items():
            self.table.add_line_names(k)
            v = [f"{val: .4E}" if isinstance(val, float) else val for val in v]
            self.table.add_values(k, v + [f"{iterations: _}"])

        return str(self.table)
