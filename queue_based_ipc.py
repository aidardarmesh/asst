from multiprocessing import Process, Queue

def producer(q):
    q.put("Hello from producer")
    q.put("Another message")
    q.put("STOP")  # Signal for consumer to stop

def consumer(q):
    while True:
        msg = q.get()
        if msg == "STOP":
            break
        print(f"Consumer received: {msg}")

if __name__ == '__main__':
    queue = Queue()

    p1 = Process(target=producer, args=(queue,))
    p2 = Process(target=consumer, args=(queue,))

    p1.start()
    p2.start()

    p1.join()
    p2.join()
