# thread local

多線程的全域變數是共用的資源，若是每個線程對該變數同一時間修改會造成數值不正確。thread.local 可以對每個線程儲存一份成為自己的全域變數，修改全域變數就不會互相影響了。

~~~python
import threading
import time

local = threading.local()

def worker():
     local.x = 0
     for i in range(100):
         time.sleep(0.0001)
         local.x += i
     print(threading.current_thread(), local.x)

if __name__ == '__main__':
    for _ in range(10):
        threading.Thread(target=worker).start()
~~~

執行結果

~~~python
<Thread(Thread-3, started 4568)>  4950
<Thread(Thread-9, started 2848)>  4950
<Thread(Thread-1, started 7324)>  4950
<Thread(Thread-4, started 11904)> 4950
<Thread(Thread-10, started 9276)> 4950
<Thread(Thread-5, started 11588)> 4950
<Thread(Thread-7, started 10996)> 4950
<Thread(Thread-6, started 11980)> 4950
<Thread(Thread-2, started 5504)>  4950
<Thread(Thread-8, started 11876)> 4950
~~~



