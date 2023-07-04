import multiprocessing
import time

def factorize(*numbers):
    num_cores = multiprocessing.cpu_count()
    print(num_cores)
    pool = multiprocessing.Pool(processes=num_cores)
    result = pool.map(find_divisors, numbers)
    pool.close()
    pool.join()
    return result

def find_divisors(number):
    return [i for i in range(1, number + 1) if number % i == 0]

if __name__ == '__main__':
    # Приклад вхідних даних (перевірка)
    a, b, c, d = 128, 255, 99999, 10651060
    start_time = time.time()
    result = factorize(a, b, c, d)
    end_time = time.time()
    print(result)



    execution_time = end_time - start_time

    print(f"Оновлена версія: {execution_time} сек")
