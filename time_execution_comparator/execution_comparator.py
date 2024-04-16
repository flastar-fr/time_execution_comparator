import time
import typing
from multiprocessing import Process, Manager
from easy_console_table import TwoEntryTable
from tqdm import tqdm


def execute_function(func: typing.Callable):
    start_time = time.perf_counter()
    func()
    return time.perf_counter() - start_time


class ExecutionComparator:
    def __init__(self):
        self.table = TwoEntryTable()
        self.table.add_column_names("Total\nExecution\nTime", "Average\nTime", "Max\nTime\nExecution",
                                    "Min\nTime\nExecution", "Difference", "Iterations")
        self.table.title = "Time\nCalculator"
        manager_returned_values = Manager()
        self.return_values = manager_returned_values.dict()
        manager_advancements = Manager()
        self.advancements = manager_advancements.dict()

    def run_test(self, return_values: dict, func: typing.Callable, iterations: int = 1):
        total_times = []
        function_name = func.__name__
        for i in range(iterations):
            self.advancements[function_name] = i
            result = execute_function(func)
            total_times.append(result)

        # data analysis
        total_time = sum(total_times)
        average_time = sum(total_times) / iterations
        max_time = max(total_times)
        min_time = min(total_times)

        return_values[function_name] = [total_time, average_time, max_time, min_time, max_time - min_time]

    def reset(self):
        self.table = TwoEntryTable()
        self.table.add_column_names("Total\nExecution\nTime", "Average\nTime", "Max\nTime\nExecution",
                                    "Min\nTime\nExecution", "Difference", "Iterations")
        self.table.title = "Time\nCalculator"
        manager_returned_values = Manager()
        self.return_values = manager_returned_values.dict()
        manager_advancements = Manager()
        self.advancements = manager_advancements.dict()

    def compare_execution(self, *args: typing.Callable, iterations: int = 1):
        processes = []
        for func in args:
            process = Process(target=self.run_test, args=[self.return_values, func, iterations])
            processes.append(process)
            process.start()

        progress_bar = tqdm(total=iterations, desc="Overall Progress")

        while True:
            all_finished = all(not process.is_alive() for process in processes)

            if all_finished:
                break

            min_advancement = 0
            if len(self.advancements.values()) > 0:
                min_advancement = min(self.advancements.values())

            progress_bar.update(min_advancement - progress_bar.n)

            time.sleep(0.1)

        progress_bar.update(iterations)
        progress_bar.close()

        # prevent bugs
        for process in processes:
            process.join()

        for k, v in self.return_values.items():
            self.table.add_line_names(k)
            v = [f"{val: .4E}" if isinstance(val, float) else val for val in v]
            self.table.add_values(k, v + [iterations])

        return str(self.table)
