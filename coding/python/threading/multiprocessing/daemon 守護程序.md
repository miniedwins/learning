# daemon 守護程序

假設 Python 主程式執行時，如果有子程序正在背景執行而且尚未結束，此時如果將 Python 主程式結束執行，這時候背景子程序仍會繼續執行，導致主程式看起來無法結束執行（但其實是因為此時子程序仍然在執行之中）。但我們希望主程序結束後子程序也要一併結束，所以就必須在創建子程序時，設定 daemon=True。

範例 : 模擬子程序執行一個無窮迴圈的函數

設定 daemon=True，主程序會等待3秒後結束，主程序退出，子程序也會立刻退出。

~~~python
def say_hello_to(name):
    while True:
        time.sleep(1)
        print(name)

if __name__ == '__main__':
    mp = multiprocessing.Process(target=say_hello_to, args=('edwin', ), daemon=True)
    mp.start()
    print('Main ...')
    time.sleep(3)
    print('End ...')
~~~

執行結果 

~~~python
Start Main Process
edwin
edwin
End Main Process
~~~

若是設定 daemon=False，主程序會等待子程序執行完畢，所以子程序會一直循環運行輸出  "edwin"。

~~~python
Start Main Process
edwin
edwin
End Main Process
edwin
edwin
edwin
.....
edwin
~~~





