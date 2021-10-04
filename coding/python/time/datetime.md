# datetime



## 取得當前時間

~~~python
from datetime import datetime

today = datetime.today() # 取得今天的日期
# 2021-08-13 15:50:23.473673

now = datetime.now() # 取得現在時間
# 2021-08-13 15:51:25.979489
~~~



## 自訂義日期格式化

~~~python
import datetime

 # 日期格式化
datetime_dt = datetime.datetime.today()
datetime_str = datetime_dt.strftime("%Y/%m/%d %H:%M:%S")
# '2021/08/10 11:54:02'

# 日期格式化
datetime_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
datetime_str = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S") 
datetime_str = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
# '2021-08-13 08:14:45'
~~~



## 時間的相加減 (時間差)

使用 `datetime.timedelta` 產生一個自訂義的時間差，可以透過這個方式作為計時器，以下是該類別 __new__ 方法的宣告 : 

~~~python
def __new__(cls, days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0):
~~~

範例 :  

~~~python
import datetime

datetime_dt = datetime.datetime.today() 
# 2021-08-10 14:52:06.149313

datetime_delta = datetime.timedelta(minutes=10) # 也可以包括天數相加減  
# 0:10:00

datetime_new_time = datetime_dt + datetime_delta # 時間相加
# 2021-08-10 15:02:06.149313

datetime_new_time = datetime_dt - datetime_delta # 時間相減
# 2021-08-10 15:42:06.149313

print(datetime.now() + timedelta(days=1,minutes=5)) # 目前的時間再加上預期加入的時間
~~~



## 計算程式運行時間

~~~python
import datetime

start_time = datetime.datetime.now() 
end_time = datetime.datetime.now()

elapsed_time = end_time - start_time # 相減後取得執行時間
# datetime.timedelta(seconds=10, microseconds=259387)

elapsed.total_seconds() # 轉換成總共時間
# 10.259387

elapsed.seconds # 取得整數時間
# 10
~~~

# datetime.date



## 修改日期

~~~python
from datetime import date
d = date(2002, 12, 31)
d.replace(day=26)

# datetime.date(2002, 12, 26)
~~~



## 計算剩餘天數

~~~python
import time
from datetime import date

today = date.today()
my_birthday = date(today.year, 12, 25)
days = (my_birthday - today).days # 轉換成天數 (type: int)
print(days) # 134
~~~



# 範例說明



## 建立簡單的計時器 (裝飾器)

~~~python
def timer(func):
    def wrapped(*args, **kwargs):        
        print(f'Start time: {start_time}')
        start_time = datetime.datetime.now()
        func(*args, **kwargs)        
        print(f'End time: {end_time}')
        end_time = datetime.datetime.now()
        print(f'elapsed time : {elapsed}')
        elapsed = (end_time - start_time).total_seconds() # 返回時間間隔包含了多少秒        
    return wrapped

@timer
def test_time():
    print('sleep 5 seconds')
    time.sleep(5)
~~~

輸出結果 : 

~~~shell
Start time: 2021-08-10 15:09:46.454650
sleep 5 seconds
End time: 2021-08-10 15:09:51.455164
elapsed time : 5.000514
~~~

# 注意事項

### timestamp 

Python 雖然有為 datetime 模組提供方便的 timestamp 方法，但仍有需要注意的地方，否則將會導致我們拿到錯誤的時間戳(timestamp)，衍伸出不必要的麻煩。

首先， Python 在文件中提到：

> Naive datetime instances are assumed to represent local time …

當我們使用 datetime 時， datetime 預設會使用當地時間(也就是伺服器的時間及時區)。

以 UTC+8 的台灣為例，當我們試圖取得 2019 年 1 月 1 號的 timestamp 時，其數值為 `1546272000.0` ：

```
>>> from datetime import datetime
>>> datetime(2019, 1, 1).timestamp()
1546272000.0
```

但是如果我們真正想取得的是 UTC+0 2019 年 1 月 1 號的 timestamp 時，這麼做就會是錯的，必須明確指定時區才行：

```
>>> from datetime import datetime, timezone
>>> datetime(2019, 1, 1, tzinfo=timezone.utc).timestamp()
1546300800.0
```

從結果可以發現我們如果不指定時區(timezone)的話， 2 種 timestamp 呼叫所得到的數值差了 `-28800` 秒(1546272000 - 1546300800 剛好 8 小時)，原因在於在不指定時區的情況下， Python 會先將當地時間先轉回 UTC+0 的時間再取得 timestamp ，因此 2019 年 1 月 1 號的台灣時間剛好對應到 UTC+0 的 2018 年 12 月 31 號 16:00 ：

```
>>> from datetime import datetime, timezone
>>> datetime(2018, 12, 31, 16, 0, tzinfo=timezone.utc).timestamp()
1546272000.0
```

因此當我們試圖呼叫 timestamp() 請額外注意時區產生的問題，千萬別以為 `datetime(2019, 1, 1).timestamp()` 就是取得 UTC+0 的 2019 年 1 月 1 號的 UNIX timestamp 喔！
