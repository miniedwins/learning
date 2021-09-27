import time
from contextlib import contextmanager

@contextmanager
def time_this(label):
    start = time.time()
    try:
        yield
    finally:
        end = time.time()
        print('{}: {}'.format(label, end - start))

if __name__ == '__main__':
    with time_this('counting'):
        n = 10000000
        while n > 0:
            n -= 1