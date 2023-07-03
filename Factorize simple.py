import time

def factorize(numbers):
    result = []
    for number in numbers:
        divisors = []
        for i in range(1, number + 1):
            if number % i == 0:
                divisors.append(i)
        result.append(divisors)
    return result

# Приклад вхідних даних
numbers = [15, 20, 25, 30, 35, 40, 45, 50]

# Виміряємо час виконання
start_time = time.time()
result = factorize(numbers)
end_time = time.time()

execution_time = end_time - start_time

print(f"Синхронна версія: {execution_time} сек")

