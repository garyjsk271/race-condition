
from threading import *
import time

BUFFER_SIZE = 100
k1 = 10
k2 = 5

obj = Semaphore(1)
buffer = [0 for i in range(BUFFER_SIZE)]

def produce(next_in):
    obj.acquire()
    while True:
        for i in range(k1):
            buffer[(next_in + i) % BUFFER_SIZE] += 1
        next_in = (next_in + k1) % BUFFER_SIZE
        time.sleep(1)
        obj.release()

def consume(next_out):
    obj.acquire()
    while True:
        time.sleep(3)
        for i in range(k2):
            data = buffer[(next_out + i) % BUFFER_SIZE]
            if data > 1:
                print(f"race condition detected with k1={k1}, k2={k2}, t1={1}, t2={3}\n")
                print(buffer)
                return
        next_out = (next_out + k2) % BUFFER_SIZE
        obj.release()

next_in = 0
next_out = 0
t1 = Thread(target = produce, args=[next_in])
t2 = Thread(target = consume, args=[next_out])

t1.start()
t2.start()