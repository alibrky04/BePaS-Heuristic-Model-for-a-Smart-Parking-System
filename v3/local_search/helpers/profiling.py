import time
import psutil
import os


def profile_function(func, *args, **kwargs):
    process = psutil.Process(os.getpid())
    mem_before = process.memory_info().rss
    start_time = time.time()
    start_cpu_time = time.process_time()
    result = func(*args, **kwargs)
    end_time = time.time()
    end_cpu_time = time.process_time()
    execution_time = end_time - start_time
    cpu_time = end_cpu_time - start_cpu_time
    memory_usage = process.memory_info().rss - mem_before
    return result, execution_time, cpu_time, memory_usage
