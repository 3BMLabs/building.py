import sys
import time
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

from geometry.point import Point
from objects.objectcollection import *
from project.fileformat import *


def calculate_execution_time(func1, func2):
    start_time = time.perf_counter()
    func1()
    end_time = time.perf_counter()
    execution_time_func1 = (end_time - start_time) * 1  # Convert to seconds

    start_time = time.perf_counter()
    func2()
    end_time = time.perf_counter()
    execution_time_func2 = (end_time - start_time) * 1  # Convert to seconds

    print(f"Execution time for func1: {execution_time_func1} seconds")
    print(f"Execution time for func2: {execution_time_func2} seconds")

calculate_execution_time(WorkPlane().create(1000,2000),WorkPlane().create(1000,2000))
