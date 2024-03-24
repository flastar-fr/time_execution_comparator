Import ExecutionComparator class and use compare_execution that takes functions as arguments and iterations.
You need to install the easy-console-libary

Example :
```py
import random

from time_execution_comparator.execution_comparator import ExecutionComparator


def test():
    _ = [i for i in range(random.randint(0, 10_000))]


def test2():
    liste = []
    for i in range(random.randint(0, 10_000)):
        liste.append(i)


if __name__ == "__main__":
    c = ExecutionComparator()
    print(c.compare_execution(test, test2, iterations=10_000))
```