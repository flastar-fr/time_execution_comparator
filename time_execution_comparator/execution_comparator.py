import itertools
import time
import typing
from multiprocessing import Pool
from easy_console_table import TwoEntryTable


def execute_function(func: typing.Callable):
    start_time = time.perf_counter()
    func()
    return time.perf_counter() - start_time


def run_test(func: typing.Callable, iterations: int = 1):
    total_times = []
    for _ in range(iterations):
        result = execute_function(func)
        total_times.append(result)

    # data analysis
    total_time = sum(total_times)
    average_time = sum(total_times) / iterations
    function_name = func.__name__

    return function_name, total_time, average_time, iterations


class ExecutionComparator:
    def __init__(self):
        self.table = TwoEntryTable()
        self.table.add_column_names("Total\nExecution\nTime", "Average\nTime", "Iterations")
        self.table.title = "Time\nCalculator"

    def compare_execution(self, *args: typing.Callable, iterations: int = 1):
        with Pool() as pool:
            results = pool.starmap(run_test, zip(args, itertools.repeat(iterations)))

        for line in results:
            self.table.add_line_names(line[0])
            self.table.add_values(line[0], line[1:])

        return str(self.table)
