# 如何使用進程池

進程池內部維護一個進程序列，當使用時，則去進程池中獲取一個進程，如果進程池序列中沒有可供使用的進程，那麼程序就會等待，直到進程池中有可用進程為止。進程池設置最好等於CPU核心數量

## 建立一個簡單的進程池

使用 multiprocessing 模組建立一個進程池，並限定一次處理程序的數量，平行的去處理任務。

~~~python
from multiprocessing import Process, Pool
import os, time

def main_map(i):    
    print(f'Start Process Id: {os.getpid()}')
	
    # 模擬程序處理時間
    time.sleep(1)
    result = i * i
    
    print(f'End Process Id: {os.getpid()}')
    return result

if __name__ == ‘__main__':
    inputs = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    # 設定處理程序數量 (當前機器的 CPU 核心數量)　
    pool = Pool(4)   

    # 運行多處理程序
    pool_outputs = pool.map(main_map, inputs)

    # 輸出執行結果
    print(pool_outputs)
~~~

也可以使用 with 的方法

~~~python
with pool(4) :
    # code
    pool.close()
    pool.join()
~~~

運行結果 : 一次產生4個執行程序並且同時處理任務

~~~python
Start Process Id: 768
Start Process Id: 11168
Start Process Id: 1792
Start Process Id: 13780
End Process Id: 768
End Process Id: 11168
End Process Id: 1792
Start Process Id: 11168
Start Process Id: 768
Start Process Id: 1792
End Process Id: 13780
Start Process Id: 13780
End Process Id: 1792
End Process Id: 11168
End Process Id: 768
Start Process Id: 11168
Start Process Id: 1792
End Process Id: 13780
End Process Id: 1792
End Process Id: 11168
[0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
~~~



##  pool 同步與非同步調用

###  pool.map (同步)

調用 pool.map 會將主程序阻塞直到所有子程序結束後，才會繼續運行主程序

~~~python
from multiprocessing import Process, Pool

def main_map(num):
    result = num * num
    print(result)
    return result

if __name__ == '__main__':

    inputs = [0, 1, 2, 3]
    pool = Pool(4)

    pool_outputs = pool.map(main_map, inputs)
    print(‘將會阻塞並於 pool.map 子程序結束後觸發')
~~~

輸出結果 :

~~~python
0
1
4
9
將會阻塞並於 pool.map 子程序結束後觸發
~~~



### pool.map_async (非同步)

~~~python
from multiprocessing import Process, Pool

def main_async(num):
    result = num * num
    print(result)
    return result

if __name__ == ‘__main__’:

    inputs = [0, 1, 2, 3]
    pool = Pool(4)

    pool_outputs = pool.map_async(main_async, inputs)
    print('將不會阻塞並和 pool.map_async 並行觸發')

    pool.close() 	# 關閉進程池，避免還有多個執行任務提交到進程池
    pool.join()		# 等待子程序執行完畢，才會繼續運行主程序
~~~

輸出結果 :

~~~python
將不會阻塞並和 pool.map_async 並行觸發
0
1
4
9
~~~



### pool.map_async 和 pool.map 的差異

主處理程序是否同步並行，而 pool.map 會阻塞主程序，待所有子程序結束後，才會繼續運行主程序。 pool.map_async 反之，所以最後要寫 close 和 join 來避免主程序結束後，子程序被迫關閉。



### pool.apply_async  (非同步)

對於apply_async(func,args)，func為要執行任務的函數名，args為一個列表或元組這樣的可迭代對象，裡面包含的是要傳遞給func的參數，對於多個子任務，要分別多次調用apply_async()一一添加，不過這可以通過列表解析實現，以讓多個進程的結果返回保存在一個列表中。

~~~python
import multiprocessing

def say_hello_to(name):
    return name

names = ['John', 'Ben', 'Bill', 'Alex', 'Jenny']

if __name__ == '__main__':
    pool = multiprocessing.Pool(4)    
    tasks = []
    for name in names:        
        # 不阻塞主程序，並且回傳 ApplyResult object
        task = pool.apply_async(say_hello_to, (name,))		
        # 將每個任務放到清單上，等待任務執行完畢後，取出結果
        tasks.append(task)         
    pool.close()
    pool.join()

    for result in tasks:
        # 透過 get() 方法將每個執行完成的任務的結果取出來
        print(result.get()) 
~~~

建立多子程序任務也可以使用下列方法建立 : 

~~~python
tasks = [pool.apply_async(say_hello_to, (name,)) for name in names]
~~~

輸出結果 :

~~~python
John
Ben
Bill
Alex
Jenny
~~~



### pool.apply_async  (異常處理)

由於是手動指定進程並添加任務，這樣每個進程的執行結果之間是獨立的，會分別保存，這樣的好處在於，盡管可能其中某幾個進程出現了錯誤，拋出異常，但是並不會導致其他的進程也失敗，其他的進程並不會受影響，而且當獲取這個拋出異常的進程的結果時，還會返回異常信息。

~~~python
def say_hello_to(name):
    if name == 'Bill':
		raise ValueError(f'Name Error : {name}') # 模擬拋出異常訊息
    print(name)
    return name

names = ['John', 'Ben', 'Bill', 'Alex', 'Jenny']

if __name__ == '__main__':
    pool = multiprocessing.Pool(4)
    tasks = []
    for name in names:
        task = pool.apply_async(say_hello_to, (name,))
        tasks.append(task)
    pool.close()
    pool.join()
~~~

若是沒有去調用 get() 方法取得任務結果，執行完成後也不會拋出異常錯誤

~~~python
John
Ben
Alex
Jenny
~~~

若是要取得拋出異常錯誤的訊息，需要取得每個執行任務的結果，程式修改如下 :

~~~python
for result in tasks:
    try:
        print(result.get())
    except Exception as err:
        print(err)
~~~

輸出結果 :

~~~python
John
Ben
Name Error : Bill
Alex
Jenny
~~~



### pool.apply_async  (回調函數)

回調函數最終還是由主程序去執行，執行的結果可以看到 main pid & callback pid 都是相同的

~~~python
from multiprocessing import Pool
import os

def func(num):
    print('func pid', os.getpid())
    return num * num

def mycallback(arg):
    print('callback pid', os.getpid())
    print(arg)

if __name__ == "__main__":
    print('main pid：', os.getpid())
    pool = Pool(4)
    pool.apply_async(func, args=(10,), callback=mycallback)
    pool.close()
    pool.join()
~~~

執行結果 : 

~~~python
main pid： 5328
func pid 11128
callback pid 5328
100
~~~





