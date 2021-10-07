# 如何取得程序的 PID

需要導入 os 模組

~~~python
import multiprocessing
import os

def say_hello_to(name):
   	# 取得子程序的 PPID 是否由主程序所創造的
    print(f'Child PPID: {os.getppid()}')
    # 取得目前在這個函數運行的主程序 PID
    print(f'Child PID: {os.getpid()}')
    print(name)

if __name__ == '__main__':
    print(f'Main PID: {os.getpid()}')
    mp = multiprocessing.Process(target=say_hello_to, args=('edwin', ), daemon=True)
    mp.start()
    mp.join()
~~~

執行結果：

~~~python
Main PID: 4832
Child PPID: 4832
Child PID: 8156
edwin
~~~





