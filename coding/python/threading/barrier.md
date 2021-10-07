# Barrier

是一種像是柵欄的狀態，必須要等到所有的線程都到齊了，才會開放柵欄往下執行，是一種同步機制。應用在線程同步的場景中，必須要等待所有的工作線程都準備好後，才會往下執行。而它與信號量 (semaphore) 不同的是，信號量是限制同一個時間內可以執行的線程數量。

**構造方法：**

* threading.Barrier(parties, action=None, timeout=None)
  * parties : 通過柵欄所需的線程數

**方法 : **

* n_waiting : 當前在柵欄中等待的線程數

* broken  : 檢測柵欄是否處於打破的狀態，返回True或False

* abort()  : 將柵欄置於broken狀態，等待中的線程或者調用等待方法的線程都會拋出異常(BrokenBarrierError)，直到reset方法來恢復柵欄

* wait(timeout=None) 等待通過柵欄，返回0到線程數-1的整數(barrier_id)，每個線程返回不同。如果wait方法設置了超時，並超時發送，柵欄將處於broken狀態。

* reset()  : 恢復柵欄，重新開始攔截



範例 : 模擬 abort 狀態

以下程式的第3個線程會執行 barrier.abort()，所以3,4,5線都會拋出異常，直到第6個線程重新恢復柵欄狀態

~~~python
import threading
import logging

logging.basicConfig(level=logging.INFO, format="%(threadName)s %(message)s")

def work(barrier: threading.Barrier):
    logging.info("n_waiting = {}".format(barrier.n_waiting))
    try:
        bid = barrier.wait()
        logging.info("after barrier {}".format(bid))
    except threading.BrokenBarrierError:
        logging.info("Broken Barrier in {}".format(threading.current_thread()))


if __name__ == '__main__':    
    barrier = threading.Barrier(3)    
    for x in range(1, 12):
        if x == 3:
            barrier.abort()
        elif x == 6:
            barrier.reset() 
        threading.Event().wait(1)
        threading.Thread(target=work, args=(barrier,), name="Barrier-{}".format(x)).start()
~~~

執行結果 :

~~~python
Barrier-1 n_waiting = 0
Barrier-2 n_waiting = 1
Barrier-2 Broken Barrier in <Thread(Barrier-2, started 8904)>
Barrier-1 Broken Barrier in <Thread(Barrier-1, started 5848)>
Barrier-3 n_waiting = 0 # 第3個線程執行abort，正在等待的 Barrier-1, Barrier-2 都會直接拋出異常
Barrier-3 Broken Barrier in <Thread(Barrier-3, started 2108)> # Barrier-3 拋出異常 
Barrier-4 n_waiting = 0
Barrier-4 Broken Barrier in <Thread(Barrier-4, started 5952)> # Barrier-4 拋出異常
Barrier-5 n_waiting = 0
Barrier-5 Broken Barrier in <Thread(Barrier-5, started 7516)> # Barrier-5 拋出異常
Barrier-6 n_waiting = 0 # 第6個線程執行reset，後面的線程執行才會正常執行
Barrier-7 n_waiting = 1
Barrier-8 n_waiting = 2
Barrier-8 after barrier 2
Barrier-6 after barrier 0
Barrier-7 after barrier 1
Barrier-9 n_waiting = 0
Barrier-10 n_waiting = 1
Barrier-11 n_waiting = 2
Barrier-11 after barrier 2
Barrier-10 after barrier 1
Barrier-9 after barrier 0
~~~

範例 : 模擬超時等待 (wait) 

1. 設定超時1秒後，就會拋出異常並且柵欄置於broken狀態。
2. 拋出異常後，後面的執行的線程都會持續拋出異常，直到柵欄狀態被重置。

~~~python
import threading
import logging
import time

logging.basicConfig(level=logging.INFO,format="%(thread)d %(threadName)s %(message)s")

def work(barrier:threading.Barrier, i:int):
    logging.info(f'n_waiting = {barrier.n_waiting}')
    try:
        if i < 3:
            bid = barrier.wait(1) # 超時等待時間
        if i == 6:
            barrier.reset()
        bid = barrier.wait()
        logging.info("after barrier {}".format(bid))
    except threading.BrokenBarrierError:
        logging.info(f'Broken Barrier in {threading.current_thread()}')

if __name__ == '__main__':
    barrier = threading.Barrier(3)
    for i in range(1, 12):
        threading.Event().wait(2) #強制延遲2秒,讓出時間片
        threading.Thread(target=work, args=(barrier, i), name="Barrier-{}".format(i)).start()
~~~

執行結果 :

~~~python
6940 Barrier-1 n_waiting = 0
6940 Barrier-1 Broken Barrier in <Thread(Barrier-1, started 6940)>
1552 Barrier-2 n_waiting = 0
1552 Barrier-2 Broken Barrier in <Thread(Barrier-2, started 1552)>
9448 Barrier-3 n_waiting = 0
9448 Barrier-3 Broken Barrier in <Thread(Barrier-3, started 9448)>
4292 Barrier-4 n_waiting = 0
4292 Barrier-4 Broken Barrier in <Thread(Barrier-4, started 4292)>
7872 Barrier-5 n_waiting = 0
7872 Barrier-5 Broken Barrier in <Thread(Barrier-5, started 7872)>
4192 Barrier-6 n_waiting = 0
1532 Barrier-7 n_waiting = 1
4392 Barrier-8 n_waiting = 2
4392 Barrier-8 after barrier 2
4192 Barrier-6 after barrier 0
1532 Barrier-7 after barrier 1
10112 Barrier-9 n_waiting = 0
4028 Barrier-10 n_waiting = 1
1216 Barrier-11 n_waiting = 2
1216 Barrier-11 after barrier 2
4028 Barrier-10 after barrier 1
10112 Barrier-9 after barrier 0
~~~

