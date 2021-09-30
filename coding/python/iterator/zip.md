# zip


```python
"""
語法 : 
zip(iterable, ...)

說明 : 
用於將可迭代的對象作為參數，將對象中對應的元素打包成一個個元組，然後返回由這些元組組成的對象，這樣做的好處是節約了不少的內存。
我們可以使用 list() 轉換來輸出列表。如果各個迭代器的元素個數不一致，則返回列表長度與最短的對象相同，利用 * 號操作符，可以將元組解壓為列表。
"""
```



##  打包為tuple的列表


```python
numbers = [1, 2, 3]
letters = ['a', 'b', 'c']

# 返回一個 zip object
zipped = zip(numbers, letters)

# <class 'zip'>
type(zipped) 

# list() 轉換為列表
list(zipped) # [(1, 'a'), (2, 'b'), (3, 'c')]
```



## 元素個數與最短的列表一致


``` python
numbers1 = [1, 2, 3]
numbers2 = [4, 5, 6, 7, 8]

list(zip(numbers1, numbers2)) # [(1, 4), (2, 5), (3, 6)]
```



##  使用iterools將不一致列表填滿


```python
from itertools import zip_longest
numbers = [1, 2, 3]
letters = ['a', 'b', 'c']
longest = range(5)
zipped = zip_longest(numbers, letters, longest, fillvalue='?')
list(zipped) # [(1, 'a', 0), (2, 'b', 1), (3, 'c', 2), ('?', '?', 3), ('?', '?', 4)]
```



## 僅有一個參數


```python
a = [1, 2, 3]

# 返回一個 zip object
zipped = zip(a)

list(zipped) # [(1,), (2,), (3,)]
```



## 多個參數


```python
integers = [1, 2, 3]
letters = ['a', 'b', 'c']
floats = [4.0, 5.0, 6.0]

# Three input iterables
zipped = zip(integers, letters, floats)  

list(zipped) # [(1, 'a', 4.0), (2, 'b', 5.0), (3, 'c', 6.0)]
list(zip(range(5), range(100))) # [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4)]
```



##  使用 Set 作為參數給 zip


```python
s1 = {2, 3, 1}
s2 = {'b', 'a', 'c'}
list(zip(s1, s2)) # [(1, 'b'), (2, 'c'), (3, 'a')]
```



## 轉換成字典

~~~python
dict(zip(['one', 'two', 'three'], [1, 2, 3])) # {'one': 1, 'two': 2, 'three': 3}

DIAL_COD = [(86, 'China'), (99, 'Taiwan')]
d = {country: code for code ,country in DIAL_COD}
print(d)	# {'China': 86, 'Taiwan': 99}
~~~



## 解包回先前的資料的狀態


```python
a = [1,2,3]
b = ["a", "b", "c"]
zipped = zip(a,b) # [(1, 'a'), (2, 'b'), (3, 'c')]

# 與 zip 相反，可理解為解壓
# 會返回 tuple 型態
numbers, letters = zip(*zipped)

print(numbers) # (1, 2, 3)
print(letters) # ('a', 'b', 'c')
```

```python
pairs = [(1, 'a'), (2, 'b'), (3, 'c'), (4, 'd')]
numbers, letters = zip(*pairs)

print(numbers) # (1, 2, 3, 4)
print(letters) # ('a', 'b', 'c', 'd')
```

```python
x = [1, 2, 3]
y = [4, 5, 6]
zipped = zip(x, y)

#[(1, 4), (2, 5), (3, 6)]
list(zipped)

# ((1, 2, 3), (4, 5, 6))
x2, y2 = zip(*zip(x, y))

# True
x == list(x2) and y == list(y2)
```

## 關於用’*‘解包

```python
# 帶*號的表達式獲取序列前面部分
*a,b,c = 1,2,3,4,5 # a = [1, 2, 3], b = 4, c=5

# 帶*號的表達式獲取序列中間部分
a,*b,c = 1,2,3,4,5 # a=1, b=[2, 3, 4], c=5

# 帶*號的表達式獲取序列剩餘部分
a, b, *c = 1,2,3,4,5 # a=1, b=2, c=[3, 4, 5]

l1 = [1, 2, 3]
l2 = 'XYZ'
l = [*l1, *l2] 	# [1, 2, 3, 'x', 'y', 'z']

d1 = {'a': 1, 'b': 2}
d2 = {'c': 3}
d = {**d1, **d2, **d3} 	# {'a': 1, 'b': 2, 'c':3}
```

### 巢狀的unpacking

~~~python
# a=1, b=2, c=3, d=4
a, b, (c, d) = [1, 2, [3, 4]] 

# a=1, b=[2, 3], c='x', d='y', e='z'
a, *b, (c, d, e) = [1, 2, 3, 'xyz'] 

# a=1, b=[2, 3], c='p', d=['y', 't', 'h', 'o', 'n']
a, *b, (c, *d) = [1, 2, 3, 'python']  

# a=1, b=2, c=3, d=4
(a,b),(c,d) = (1,2),(3,4) 
~~~

### 使用unpacking來處理parameters

規則：

- 關鍵字參數(keyword argument)後方不能再接位置參數(positional arguments)
- 你不能在`*args`的後方再使用位置參數
- 你不能在`**kwargs`的後方再傳入任何參數

```python
def func(a, b, *args, d):
    print('a : ', a)
    print('b : ', b)
    print('args : ', args)
    print('d : ', d)

# 這樣是不行的，沒有指名keyword arguments
func(1, 2, 'x', 'y', d)   

# 這樣是可以的 (a=1, b=2, args=('x', 'y'), d=3)
func(1, 2, 'x', 'y', d=3)
```

### 用tuple**收集**所有或剩下的

~~~python
def my_func(a, b, *args):
    # your code here
    
l = [1, 2, 3, 4]
my_func(*l)  # a=1, b=2, args=[3, 4]
~~~

### 強制不要傳入位置參數

~~~python
 # 強制不要傳入位置參數，指定 d 傳入
def func(*, d):
    # code here
    
# 最多只能傳a，b這2個位置參數，另外強制傳入關鍵字參數d
def func(a, b=1, *, d, e=True):
    # code here

# 最少要傳a這個位置參數，另外強制傳入關鍵字參數d, f
def func(a, b=1, *args, d, e=True, f): 
    # code here
~~~
