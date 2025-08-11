import threading
import queue
import time

def worker(q, thread_id):
    while True:
        try:
            # Get a task from the queue, timeout after 3 seconds if no task
            task = q.get(timeout=3)
        except queue.Empty:
            print(f"Thread-{thread_id}: No more tasks, exiting")
            break
        print(f"Thread-{thread_id} processing task: {task}")
        time.sleep(0.5)  # Simulate work by sleeping
        q.task_done()  # Indicate the task is done

def main():
    q = queue.Queue()

    num_worker_threads = 3

    # Start worker threads
    threads = []
    for i in range(num_worker_threads):
        t = threading.Thread(target=worker, args=(q, i+1))
        t.start()
        threads.append(t)

    # Put tasks into the queue
    for task_num in range(10):
        q.put(f"Task-{task_num+1}")

    # Wait until all tasks have been processed
    q.join()

    # Wait for all threads to exit after finishing all tasks
    for t in threads:
        t.join()

    print("All tasks processed and all threads exited.")

if __name__ == "__main__":
    main()
