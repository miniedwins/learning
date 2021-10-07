# Condition

Condition常用於生產者、消費者模型，為瞭解決生產者消費者速度匹配問題。

構造方法Condition(lock=None)，可以傳入一個Lock或RLock對象，默認RLock。

**方法：**

* acquire(*args) 獲取鎖

* release()   釋放鎖

* wait(timeout=None) 等待通知或直到發生超時

* notify(n=1) 喚醒至多指定個數的等待的線程，沒有等待的線程就沒有任何操作

* notify_all() 喚醒所有等待的線程。



範例 : 生產者每秒鐘生成一條數據，消費者每0.5秒就來取一次數據。

~~~python
import threading, random, logging

logging.basicConfig(level=logging.INFO)


class Dispatcher:
    def __init__(self):
        self.data = 0
        self.event = threading.Event()
        self.cond = threading.Condition()

    def produce(self):
        for i in range(10):
            data = random.randint(1, 10)
            with self.cond:
                self.data = data
                self.cond.notify_all()  # 通知所有等待的線程
            self.event.wait(1)  # 每秒生產一次數據

    def custom(self):
        while True:
            with self.cond:
                self.cond.wait() # 無限等待
                logging.info(self.data)
            self.event.wait(0.5)  # 0.5 秒消費一次數據

if __name__ == '__main__':
    d = Dispatcher()
    p = threading.Thread(target=d.produce)
    c = threading.Thread(target=d.custom)

    c.start()
    p.start()
~~~

執行結果 : 

~~~python
INFO:root:8
INFO:root:9
INFO:root:6
INFO:root:10
INFO:root:10
INFO:root:2
INFO:root:4
INFO:root:6
INFO:root:4
INFO:root:4
~~~

範例 : 生產者先生產數據，2個消費者一個一個來消費數據。

~~~python
import threading, random, logging

logging.basicConfig(level=logging.INFO, format="%(thread)d %(threadName)s %(message)s")


class Dispatcher:
    def __init__(self):
        self.data = 0
        self.event = threading.Event()
        self.cond = threading.Condition()

    def produce(self):
        for i in range(100):
            data = random.randint(1, 100)
            logging.info(self.data)
            with self.cond:
                self.data = data
                self.cond.notify(2) # 發生通知，一次只能讓兩個線程運行
            self.event.wait(1)

    def custom(self):
        while True:
            with self.cond:
                self.cond.wait() # 一旦產生者發出通知，兩個線程同時執行
                logging.info(self.data) 

if __name__ == '__main__':
    d = Dispatcher()
    p = threading.Thread(target=d.produce, name='produce')

    for i in range(5):
        threading.Thread(target=d.custom, name='c-{}'.format(i)).start()

    p.start()
~~~

執行結果 : 

~~~python
3196 produce 0
7088 c-0 55
8624 c-1 55
3196 produce 55
3332 c-2 46
6520 c-3 46
3196 produce 46
5036 c-4 90
7088 c-0 90
3196 produce 90
8624 c-1 2
3332 c-2 2
3196 produce 2
6520 c-3 5
5036 c-4 5
3196 produce 5
7088 c-0 30
8624 c-1 30
3196 produce 30
3332 c-2 55
6520 c-3 55
3196 produce 55
5036 c-4 88
7088 c-0 88
3196 produce 88
8624 c-1 67
3332 c-2 67
3196 produce 67
~~~





