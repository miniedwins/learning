# map 使用方法


```python
"""
格式 ：map(function, iterable, ...)
說明 : iterable 中的每一個元素
"""
```



## 單一個list

透過map我們就能夠對list每一個元素做 '乘2'


```python
def multiple(x):
    return x * 2

my_list = [1, 2, 3, 4, 5]
result = list(map(multiple, my_list))
# [2, 4, 6, 8, 10]
```

 map 函式的功能也能夠用list comprehensive 來達成

```python
result = [multiple(x) for x in my_list]
# [2, 4, 6, 8, 10] 
```



## 同時接受多個 list

 map也可以同時接收多個list做處裡


```python
def add_fun(x, y, z):
    return x + y + z

list1 = [1,3,5,7,9]
list2 = [2,4,6,8,10]
list3 = [100,100,100,100,100] 
result = list(map(add_fun, list1, list2, list3))
# [103, 107, 111, 115, 119]
```

map 函式的功能也能夠用list comprehensive 來達成

```python
result = [add_fun(x,y,z) for x,y,z in zip(list1,list2,list3)]
# [103, 107, 111, 115, 119]
```



## 使用 lambda 表示

透過 lambda 來實現


```python
list(map(lambda x: x % 2, range(5)))
# [0, 1, 0, 1, 0]
```

lambda 多個參數組合


```python
list(map(lambda x,y : (x**y, x+y), [1,2,3], [1,2,3] ))
# [(1, 2), (4, 4), (27, 6)]
```

map 函式的功能也能夠用list comprehensive 來達成


```python
[x % 2 for x in range(5)]
# [0, 1, 0, 1, 0] 
```



## 取得字典的key


```python
list(map(int, {1:2,2:3,3:4}))
# [1, 2, 3]
```



## list 字串轉成 int


```python
result = map(int, ["1", "2", "3"])
for x in result:
    print(type(x))
    print(x)
 
# Output 
'''
<class 'int'>
1
<class 'int'>
2
<class 'int'>
3
'''
```



## list 字串轉成 tuple


```python
list(map(tuple, ["a", "b", "c"]))
# [('a',), ('b',), ('c',)] 
```

