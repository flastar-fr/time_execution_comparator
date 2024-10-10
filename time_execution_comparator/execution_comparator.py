import time
import typing

from inspect import signature

from easy_console_table import TwoEntryTable
from tqdm import tqdm


def execute_function(func: typing.Callable, args=None):
    if args is None:
        args = []
    start_time = time.perf_counter()
    func(*args)
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

    def execute_iterations(self, func: typing.Callable, iterations: int, func_args: list):
        progress_bar = tqdm(total=iterations, desc=f"Overall Progress for {func.__name__}")
        function_values = []
        for i in range(iterations):
            if i < len(func_args):
                function_values.append(execute_function(func, func_args[i]))
            else:
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

    def compare_execution(self, *args: typing.Callable, iterations: int = 1, args_generator: typing.Callable = None):
        func_args = self.generate_funcs_args(args_generator, iterations, *args)

        for func in args:
            self.execute_iterations(func, iterations, func_args)

        for k, v in self.returned_value.items():
            self.table.add_line_names(k)
            v = [f"{val: .4E}" if isinstance(val, float) and 0.1 < float(val) < 10 else val for val in v]
            self.table.add_values(k, v + [f"{iterations: _}"])

        return str(self.table)

    @staticmethod
    def generate_funcs_args(args_generator, iterations, *args) -> list[typing.Any]:
        args_amount = min([ExecutionComparator.get_params_function(func) for func in args])
        func_args = []
        if args_generator is not None and args_amount > 0:
            for _ in range(iterations):
                func_args.append([args_generator() for _ in range(args_amount)])

        return func_args

    @classmethod
    def get_params_function(cls, func: typing.Callable) -> int:
        return len(signature(func).parameters)
