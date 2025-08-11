import time

counter = 0
iterations = 100_000

start_time = time.perf_counter()

for _ in range(10):
    for _ in range(iterations):
        counter += 1

end_time = time.perf_counter()

print(f"Final counter value: {counter}")
print(f"Execution time: {end_time - start_time:.6f} seconds")