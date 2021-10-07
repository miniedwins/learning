## 如何加入回呼函式 (Callback)

**說明 :** 

透過多執行緒執行每一個 `URL`下載，然後等待執行結果完畢後，呼叫`Callback Function` 處理後續需要的動作。

~~~python
import requests
from concurrent import futures
from concurrent.futures import as_completed

# callback func 負責顯示下載輸出結果
def Callback_func(future):
    response = future.result(timeout=1)
    print(f'url: {response.url}, code : {response.status_code}')

# 主要負責下載網頁資料
def download_url_data(url):    
    request = requests.get(url)
    return request

def thread_executor(url_list):
    with futures.ThreadPoolExecutor(max_workers=4) as pool:
        tasks = [pool.submit(download_url_data, url) for url in url_list]
        # 只要任一執行緒結束後，立刻返回future
        for future in as_completed(tasks):
            # 將返回的結果 request class，傳遞到 callback_func
            future.add_done_callback(Callback_func)
~~~

主程式碼

~~~python
if __name__ == '__main__':
    url_list = ['https://www.google.com.tw/',
                'https://www.yahoo.com.tw/']
    thread_executor(url_list)
~~~

