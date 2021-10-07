# semaphore

信號量，信號量對象內部維護一個倒計數器，每一次acquire都會減1，當acquire方法發現計數為0就阻塞請求的線程，直到其它線程對信號量release後，計數大於0，恢復阻塞的線程。 

**構造方法 :** 

* Semaphore(value=1) : 
  * value < 0，raise ValueError
  * default=1

**方法：**

* acquire(blocking=True,timeout=None) : 獲取信號量，計數器減1，獲取成功返回True
* release() : 釋放信號量，計數器加1



範例 : 開啟十個線程，但是同一個時間只能有兩個線程可以運行。

~~~python
import time
import threading

def work(s: threading.Semaphore):
   s.acquire()
   print(f'Thread {threading.current_thread().ident} acquire')
   time.sleep(1)
   s.release()
   print(f'Thread {threading.current_thread().ident} release')

if __name__ == '__main__':
    semaphore = threading.Semaphore(2)
    for _ in range(10):
        threading.Thread(target=work, args=(semaphore, )).start()
~~~

執行結果 : 

~~~python
Thread 7000 acquire
Thread 2704 acquire
Thread 2704 release
Thread 11592 acquire
Thread 7000 release
Thread 11480 acquire
Thread 11592 release
Thread 10340 acquire
Thread 11480 release
Thread 11968 acquire
Thread 11968 release
Thread 3204 acquire
Thread 10340 release
Thread 11128 acquire
Thread 3204 release
Thread 2440 acquire
Thread 11128 release
Thread 3200 acquire
Thread 2440 release
Thread 3200 release
~~~

計數器永遠不會低於0，因為acquire的時候，發現是0，都會被阻塞。
