import time
import typing
from multiprocessing import Process, Manager
from easy_console_table import TwoEntryTable


def execute_function(func: typing.Callable):
    start_time = time.perf_counter()
    func()
    return time.perf_counter() - start_time


def run_test(return_values: dict, func: typing.Callable, iterations: int = 1):
    total_times = []
    for _ in range(iterations):
        result = execute_function(func)
        total_times.append(result)

    # data analysis
    total_time = sum(total_times)
    average_time = sum(total_times) / iterations
    function_name = func.__name__
    max_time = max(total_times)
    min_time = min(total_times)

    return_values[function_name] = [total_time, average_time, max_time, min_time, max_time-min_time]


class ExecutionComparator:
    def __init__(self):
        self.table = TwoEntryTable()
        self.table.add_column_names("Total\nExecution\nTime", "Average\nTime", "Max\nTime\nExecution",
                                    "Min\nTime\nExecution", "Difference", "Iterations")
        self.table.title = "Time\nCalculator"
        manager = Manager()
        self.return_values = manager.dict()

    def compare_execution(self, *args: typing.Callable, iterations: int = 1):
        processes = []
        for func in args:
            process = Process(target=run_test, args=[self.return_values, func, iterations])
            processes.append(process)
            process.start()

        for process in processes:
            process.join()

        for k, v in self.return_values.items():
            self.table.add_line_names(k)
            v = [f"{val: .4E}" if isinstance(val, float) else val for val in v]
            self.table.add_values(k, v + [iterations])

        return str(self.table)
