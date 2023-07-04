import time

def factorize(*numbers):
    result = []
    for number in numbers:
        divisors = []
        for i in range(1, number + 1):
            if number % i == 0:
                divisors.append(i)
        result.append(divisors)
    return result

# Приклад вхідних даних (перевірка)
a, b, c, d = 128, 255, 99999, 10651060
start_time = time.time()
result = factorize(a, b, c, d)
end_time = time.time()
print(result)



execution_time = end_time - start_time

print(f"Синхронна версія: {execution_time} сек")
