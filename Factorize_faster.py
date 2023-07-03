import multiprocessing
import time

def factorize(numbers):
    num_cores = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(processes=num_cores)
    result = pool.map(find_divisors, numbers)
    pool.close()
    pool.join()
    return result

def find_divisors(number):
    divisors = []
    for i in range(1, number + 1):
        if number % i == 0:
            divisors.append(i)
    return divisors



# Приклад вхідних даних
numbers = [15, 20, 25, 30, 35, 40, 45, 50]

# Виміряємо час виконання
start_time = time.time()
result = factorize(numbers)
end_time = time.time()

execution_time = end_time - start_time

print(f"Оновлена версія: {execution_time} сек")
