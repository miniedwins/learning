# 排序 (bisect)



## 基本介紹

這個模組維護一個已經排序過的 list ，當我們每次做完插入後**不需要再次排序整個 list** 。一個很長的 list 的比較操作很花費時間，為了改進這點，這個模組是其中一個常用的方法。這個模組被命名為來自他使用一個基礎的 bisection 演算法實作。



## 函數使用方法

這個模組要先確保資料是已經被排序過的。

~~~python
data = [5, 12, 6, 25]
data.sort() # [5, 6, 12, 25]
~~~

### bisect

它的目的是找出該數值會插入到哪個位置中，並且返回該位置，但是不會真正的將數值插入，這點必須要注意。

~~~python
position = bisect.bisect(data, 20)
print(position) # 3
~~~

`bisect_left` 和 `bisect_right` 函數，若是遇到相同的數值，找到第一個相同的數值，然後以下動作 :

* bisect_left : 返回原先數值的前面
* bisect_right :  返回原先數值的後面

~~~python
# 返回從左邊開始計算插入的位置
bisect.bisect_left(data, 12) # 2

# 返回從右邊開始計算插入的位置
bisect.bisect_right(data, 12) # 3
~~~

### insort

然後透過 `insort` 函數插入任一個數字，插入的結果不會影響原先的排序內容。

~~~python
bisect.insort(data, 9)
print(data) # [5, 6, 9, 12, 25]
~~~

`insort_left` 和 `insort_right` 函數，若是遇到相同的數值，找到第一個相同的數值，然後以下動作 :

* insort_left : 插入在原先數值的前面
* insort_right :  插入在原先數值的後面

~~~python
# 12[new] 12[old]
bisect.insort_left(data, 12) # [5, 6, 12, 12, 25]

# 12[old] 12[old] 12[new]
bisect.insort_right(data, 12) # [5, 6, 12, 12, 12, 25]
~~~



## 範例說明

### 查詢最後一次出現的數值

~~~python
from bisect import bisect_right

def binary_search(data, value):
    position = bisect_right(data, value)
    if data[position - 1] == value:
        return (position - 1)
    else:
        return False

if __name__ == '__main__':
    data_list = [1, 2, 3, 3, 4, 5]
    value = 3

    if position := binary_search(data_list, value):
        print(f"Number is present at {position}")
    else:
        print("Number Not Found")
~~~

