# list comprehension

## List (列表)


```python
[i + 1 for i in range(5)] 
# [1, 2, 3, 4, 5]

[x for x in range(10) if x%2 == 0] 
# [0, 2, 4, 6, 8]

original_prices = [1.25, -9.45, 10.22, 3.78, -5.92, 1.16]
[i if i > 0 else 0 for i in original_prices] 
# [1.25, 0, 10.22, 3.78, 0, 1.16]

[x.lower() for x in ["A","B","C"]] 
# ['a', 'b', 'c']
```


```python
list_1 = [1,2,3]
list_2 = [4,5,6]
[(x, y) for x, y in zip(list_1, list_2)] 
# [(1, 4), (2, 5), (3, 6)]

d = {1: 'A', 2: 'B', 3: 'C'}
d = [str(k) + '=' + v for k, v in d.items()]
# ['1=A', '2=B', '3=C']
```



## List (列表  two or more level)


```python
[x+y for x in [1,2,3] for y in [4,5,6]]　
# [5, 6, 7, 6, 7, 8, 7, 8, 9]

[i for i in range(4) for j in range(3)] 
# [0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3]

[[i for i in range(4)] for j in range(3)] 
# [[0, 1, 2, 3], [0, 1, 2, 3], [0, 1, 2, 3]]

[ [ 1 if item_idx == row_idx else 0 for item_idx in range(0, 3) ] for row_idx in range(0, 3) ] 
# [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
```


```python
txns = [1.09, 23.56, 57.84, 4.56, 6.78]
TAX_RATE = .08

def get_price_with_tax(txn):
    return txn * (1 + TAX_RATE)

final_prices = [get_price_with_tax(i) for i in txns]
# [1.1772000000000002, 25.4448, 62.467200000000005, 4.9248, 7.322400000000001]
```



## Dictionary (字典)


```python
d = {x: x*x for x in range(5)} 
# {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}
```




```python
values = [1,2,3,4,5]
names = ["num1", "num2", "num3", "num4", "num5"]

d = {k:v for k, v in zip(names, values)} 
# {'num1': 1, 'num2': 2, 'num3': 3, 'num4': 4, 'num5': 5}
```




```python
values = [1,2,3,4,5]
names = ["num1", "num2", "num3", "num4", "num5"]

d = dict(zip(names, values))
# {'num1': 1, 'num2': 2, 'num3': 3, 'num4': 4, 'num5': 5}
```




```python
mcase = {'a':10, 'b': 34, 'A': 7, 'Z':3}

mcase_frequency = { k.lower() : mcase.get(k.lower(), 0) + mcase.get(k.upper(), 0) for k in mcase.keys()}
# {'a': 17, 'b': 34, 'z': 3}
```



## Set (集合)


```python
L = [1,2,3,4,5,5,4,3,2,1]

s = {x for x in L} 
# {1, 2, 3, 4, 5}
```

