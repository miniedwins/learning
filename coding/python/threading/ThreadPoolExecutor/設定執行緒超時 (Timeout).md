## 設定執行緒超時 (Timeout)

**問題 :**  

如何設定超過限定時間的執行緒停止，並且取得當前停止後運算的資料結果

**解決方法 :** 

將要執行的行為以一個物件的方式封裝，並且設定中斷旗標。如此一來只要拋出 Timeout 異常，捕捉中斷後可以透過旗標方式，將超時的執行緒停止，並取得當前停止後運算的資料結果。

~~~python
import concurrent.futures
import datetime

max_numbers = [10000000, 20000000, 30000000, 40000000, 50000000]

class Task:
    def __init__(self, max_number):
        self.max_number = max_number        
        self.interrupt_requested = False	# 設定中斷旗標

    def __call__(self, *args, **kwargs):
        print("Started:", datetime.datetime.now(), self.max_number)
        last_number = 0
        for i in range(1, self.max_number):
            if self.interrupt_requested:	# 一旦觸發中斷旗標，就停止目前超時的執行緒
                print("Interrupted at", i)
                break
            last_number = i * i
        print("Reached the end")
        return last_number # 停止超時的執行緒後，回傳目前所計算的數值

    def interrupt(self):
        self.interrupt_requested = True
~~~

`future.result`  阻塞當前的程序，並等待運結果完畢。這邊設定 `Timeout=1` ，如果執行緒超過時間內還未運行完畢 ，就會拋出一個`TimeoutError`的異常，只要程式捕捉到異常，就會發送中斷，並將超時的執行緒停止。

~~~python
def main():
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        # 將需要執行的工作集中在一個列表中
        tasks = [Task(num) for num in max_numbers]
        # 執行所有的 tasks，並建立一個tuple，有利於追蹤執行的狀態
        for task, future in [(i, executor.submit(i)) for i in tasks]:
            try:
                print(future.result(timeout=1))
            # 當發生異常後，發送一個中斷請求
            except concurrent.futures.TimeoutError:
                print('this took too long time ...')              
                task.interrupt()
                
if __name__ == '__main__':
    def main()
~~~

