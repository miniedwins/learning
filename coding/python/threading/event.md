# Event

 多個線程等待某個事件的發生，在事件發生後，所有的線程都會被啟動，是一個線程同步處理的方式。

**方法：**

* set() : 發送信號 ( flag : True)，讓目前所有的運行 "event.wait" 的線程繼續執行

* clear() : 重置event ( flag : False)，使得所有該event事件都處於待命狀態

* wait(timeout=None) : 
  * 阻塞當前的線程，等待接收 "event.set" 信號
  
  * 設置等待時間
  
    * None : 無限等待，直到事件通知為止。
    * 等到事件通知了返回 True，未等到超時了就返回 False
  
    

範例 : 建立五個線程，運作到 event.wait() 都會阻塞並不會往下執行，必須等待主線程執行event.set()，所有的線程才會開始運作。

~~~python
import time
import threading

class MyThread(threading.Thread):
    def __init__(self, name, event):
        super().__init__()
        self.name = name
        self.event = event

    def run(self):
        print('Thread: {} start at {}'.format(self.name, time.ctime(time.time())))
        # 等待event.set()後，才能往下執行
        self.event.wait()
        print('Thread: {} finish at {}'.format(self.name, time.ctime(time.time())))
        
threads = []
event = threading.Event()

# 定義五個線程
[threads.append(MyThread(str(i), event)) for i in range(1,5)]

# 重置event，使得event.wait()起到阻塞作用
event.clear()

# 啟動所有線程
[t.start() for t in threads]

print('等待5s...')
time.sleep(5)

print('喚醒所有線程...')
event.set()
~~~

執行結果 : 

~~~python
Thread: 1 start at Tue Apr  6 16:09:43 2021
Thread: 2 start at Tue Apr  6 16:09:43 2021
Thread: 3 start at Tue Apr  6 16:09:43 2021
Thread: 4 start at Tue Apr  6 16:09:43 2021
Wait for 5s...
Wake up all threads...
Thread: 1 finish at Tue Apr  6 16:09:48 2021
Thread: 3 finish at Tue Apr  6 16:09:48 2021
Thread: 2 finish at Tue Apr  6 16:09:48 2021
Thread: 4 finish at Tue Apr  6 16:09:48 2021
~~~



範例 : 

work thread : 工人產生杯子，等到產生完畢後設定 event.set()

boss thread : 等待工人產生完畢，如果超過等待時間會顯示 "Bad Job"

~~~python
import threading
import logging
import time
logging.basicConfig(level=logging.INFO)

def boss(e:threading.Event):
    if e.wait(5): # 等待事件通知，若是沒有超過等待時間則會返回 "True"
        logging.info("Good Job")
    else:
        logging.info("Bad Job")
        
def worker(max_num, e:threading.Event):
    while True:
        time.sleep(0.5)
        cups.append(1)
        logging.info('make 1')
        if len(cups) > max_num:
            logging.info(f'Finished my job')            
	        e.set() # 產生完畢後發出事件通知
            break

if __name__ == '__main__':
    cups = []
    event = threading.Event()
    b = threading.Thread(target=boss, name='boss', args=(event, ))
    w = threading.Thread(target=worker, name='worker', args=(10, event, ))
    w.start()
    b.start()
~~~

執行結果 : 

~~~python
INFO:root:make 1
INFO:root:make 1
INFO:root:make 1
INFO:root:make 1
INFO:root:make 1
INFO:root:make 1
INFO:root:Finished my job
INFO:root:Good Job
~~~

