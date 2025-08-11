import threading
import time

class ThreadSafeCounter:
    def __init__(self):
        self.value = 0
        self.lock = threading.Lock()

    def increment(self):
        with self.lock:
            self.value += 1

def worker(counter, increments, thread_id):
    print(f"Thread-{thread_id} started")
    start = time.perf_counter()
    
    for _ in range(increments):
        counter.increment()
    
    end = time.perf_counter()
    print(f"Thread-{thread_id} finished, duration: {end - start:.4f} seconds")

def main():
    num_threads = 10
    increments_per_thread = 100_000
    counter = ThreadSafeCounter()

    threads = []
    overall_start = time.perf_counter()

    for i in range(num_threads):
        thread = threading.Thread(target=worker, args=(counter, increments_per_thread, i+1))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    overall_end = time.perf_counter()

    print(f"Final counter value: {counter.value}")
    print(f"Total execution time: {overall_end - overall_start:.4f} seconds")

if __name__ == "__main__":
    main()
