# time 時間模組

## 名詞介紹

### 時間元組

struct_time : 這是一個由九個數值組裝起來的時間類型。如下表所示 :

| 位置 |   參數   |    意義    |   範圍    |
| :--: | :------: | :--------: | :-------: |
|  0   | tm_year  |   西元年   |  四位數   |
|  1   |  tm_mon  |    月份    |   1~12    |
|  2   |  tm_day  |    日期    |   1~31    |
|  3   | tm_hour  |    小時    |   0~23    |
|  4   |  tm_min  |    分鐘    |   0~59    |
|  5   |  tm_sec  |    秒數    |   0~59    |
|  6   | tm_wday  |    星期    |    0~6    |
|  7   | tm_yday  | 今年第幾天 |   1~366   |
|  8   | tm_isdst |  夏令時間  | 0 or 1 or |

### 時間戳

時間戳(timestamp) : 以秒為單位的一個時間類型，起始時間為1970年1月1日0點0分0秒，因此假如現在是1970年1月1日12點0分0秒，所對應到的時間戳會為43200($12\times60\times60$)，通常時間戳最常被拿來用作時間的分析，因為它的形式最為簡單，沒有什麼格式需要考量，它的缺點就是有範圍的限制，**因為起始值是1970年**，那麼1970年前就沒有時間戳了，而且它也有限制最大的年份大約在2262年。

~~~python
# 輸出時間元組
time.localtime(0)
time.struct_time(tm_year=1970, tm_mon=1, tm_mday=1, tm_hour=8, tm_min=0, tm_sec=0, tm_wday=3, tm_yday=1, tm_isdst=0)
~~~

### 時間格式

時間格式全部都是使用一個%，加上一個字母來代表，其中大小寫會有不同的意義，這裡舉一寫比較常使用到的引述作為舉例。

| 引述 |      代表      |  例子   |
| :--: | :------------: | :-----: |
|  %a  |    星期簡寫    |   Mon   |
|  %A  |      星期      | Monday  |
|  %b  |    月份簡寫    |   Jan   |
|  %B  |      月份      | January |
|  %d  |      日期      |   31    |
|  %H  | 小時(24小時制) |   23    |
|  %I  | 小時(12小時制) |   12    |
|  %p  |    AM 或 PM    |   AM    |
|  %P  |    am 或 pm    |   am    |
|  %m  |  月份(十進制)  |   01    |
|  %M  |      分鐘      |   59    |
|  %S  |      秒數      |   59    |
|  %y  | 年份(沒有世紀) |   99    |
|  %Y  |  年份(有世紀)  |  1999   |



## time.time

### 取得當前時間的時間戳

`time.time` 可以傳回從 1970/1/1 00:00:00 算起至今的秒數，通常是用來作為時間戳記，例如 : 測量程式執行時間。

```python
# 從 1970/1/1 00:00:00 至今的秒數
seconds = time.time()

# 輸出結果
print(seconds)
1569376996.8464663
```

### 取得現在時間

~~~python
# 取得現在時間
nowTime = int(time.time())

# 轉換成時間元組
struct_time = time.localtime(nowTime) 

# 將時間元組轉換成想要的字串
timeString = time.strftime("%Y %m %d %I:%M:%S %P", struct_time) 

# 輸出結果
print(timeString)
2020 12 15 13:15:24 pm
~~~



## time.ctime

`time.ctime` 函數可以將 `time.time` 所產生的秒數，轉換為本地時間：

```python
# 從 1970/1/1 00:00:00 至今的秒數
seconds = time.time()

# 將秒數轉為本地時間
local_time = time.ctime(seconds)

# 輸出結果
print("本地時間：", local_time)
本地時間： Wed Sep 25 10:17:09 2019
```

如果不加任何參數，`time.ctime` 會直接採用目前的時間：

```python
# 現在時間
now = time.ctime()

# 輸出結果
print("現在時間：", now)
現在時間： Wed Sep 25 10:21:35 2019
```



## time.sleep

說明 : 通常程式有時候必需要等待一段時間後才繼續往下執行，所以可以使用 `time.sleep` 做短時間的暫停。

```python
# do something ...
time.sleep(5.0) # 暫停 5.0 秒
```



## time.localtime

* 根據當地時間，或是伺服器放置的時區，將時間戳轉換成時間元組 `struct_time`
* 沒有放時間戳的話，預設取得當下時間的 `struct_time` 。

```python
# 沒有放時間戳
struct_time = time.localtime()

# 輸出結果
print(struct_time)
time.struct_time(tm_year=2021, tm_mon=9, tm_mday=10, tm_hour=15, tm_min=1, tm_sec=41, tm_wday=4, tm_yday=253, tm_isdst=0)
```

可以將 `time.time` 所產生的秒數，轉換為時間元組 `struct_time` 格式的本地時間。

~~~python
# 取得時間戳
time_stamp = time.time() # 1631257609.296616

# 轉換為 struct_time 格式的本地時間
time.localtime(time_stamp)

# 輸出結果
print(result)
time.struct_time(tm_year=2021, tm_mon=9, tm_mday=10, tm_hour=15, tm_min=6, tm_sec=49, tm_wday=4, tm_yday=253, tm_isdst=0)
~~~

`struct_time` 格式的好處就是可以直接取出日期或時間裡面的任意數值：

```python
# 輸出日期與時間
print("年：", result.tm_year)
print("月：", result.tm_mon)
print("日：", result.tm_mday)
print("時：", result.tm_hour)
print("分：", result.tm_min)
print("秒：", result.tm_sec)
print("星期幾：", result.tm_wday) # 0 代表星期一
年： 2019
月： 9
日： 25
時： 10
分： 3
秒： 16
星期幾： 2
```



## time.gmtime

`time.gmtime` 函數的用途跟 `time.localtime` 函數類似，只不過它傳回的時間是世界協調時間（UTC + 0）

```python
# 轉換為 struct_time 格式的本地時間
result = time.gmtime(1569376996)

# 輸出結果
print(result)
time.struct_time(tm_year=2019, tm_mon=9, tm_mday=25, tm_hour=2, tm_min=3, tm_sec=16, tm_wday=2, tm_yday=268, tm_isdst=0)
```



## time.mktime 

`time.mktime` 函數跟 `time.localtime` 互為反函數，可將 `struct_time` 格式的時間轉為秒數：

```python
# Example1
gm_time = time.gmtime()  # 取得時間元組
mk_time = time.mktime(gm_time) # 將時間員組轉成時間戳
print(mk_time) # 輸出結果: 1599656030.0

# Example2
struct_time = time.localtime(1569376996) # 將秒數轉換為 struct_time 格式
s = time.mktime(struct_time) # 將 struct_time 格式轉換為秒數
print(s) # 輸出結果: 1569376996.0
```

### 時間格式改成時間戳

說明 : 當資料為字串的時候，無法使用字串來做運算或比較，所以直接轉成時間戳，讓參數都變成一個數值，然後再作分析。

~~~python
# 時間格式為字串
timeString = "2020-09-09 19:00:00" 

# 轉成時間元組
struct_time = time.strptime(timeString, "%Y-%m-%d %H:%M:%S") 

# 轉成時間戳
time_stamp = int(time.mktime(struct_time)) 

# 輸出結果 
print(time_stamp)
1599678000
~~~

### 時間戳改成時間格式

說明 : 當所有數據處理完，因為通常是用時間戳作分析，我們不能一眼馬上判斷是何時，所以需要轉化成想要或者規定的字串形式。

~~~python
# 設定timeStamp
time_stamp = 1599678000 

# 轉成時間元組
struct_time = time.localtime(time_stamp) 

# 設定日期格式轉成字串
timeString = time.strftime("%Y-%m-%d %H:%M:%S", struct_time) 

# 輸出結果
print(timeString)
'2020-09-09 19:00:00'
~~~



## time.asctime

`time.asctime()` 函數可將 `struct_time` 格式的時間轉為文字：

```python
# 將秒數轉換為 struct_time 格式
t = time.localtime(1569376996)

# 將 struct_time 格式轉換為文字
result = time.asctime(t)

# 輸出結果
print(result)
Wed Sep 25 10:03:16 2019
```



## time.strftime

依照指定的格式將時間元組 `struct_time` 時間資料轉換為文字輸出：

```python
import time

# 取得 struct_time 格式的時間
t = time.localtime()

# 依指定格式輸出
result = time.strftime("%m/%d/%Y, %H:%M:%S", t)
print(result)
09/25/2019, 14:57:52
```



## time.strptime

`time.strptime` 函數則是跟 `time.strftime` 函數相反，它是依據指定的格式，解析文字資料中的時間，輸出 `struct_time` 格式

```python
import time

# 文字資料
time_string = "09/25/2019, 14:57:52"

# 依指定格式解析文字資料中的時間，輸出 struct_time 格式的時間
result = time.strptime(time_string, "%m/%d/%Y, %H:%M:%S")

# 輸出結果
print(result)
time.struct_time(tm_year=2019, tm_mon=9, tm_mday=25, tm_hour=14, tm_min=57, tm_sec=52, tm_wday=2, tm_yday=268, tm_isdst=-1)
```

