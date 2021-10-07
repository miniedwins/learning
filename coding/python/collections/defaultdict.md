## defaultdict

通常在我們取用調用某個dict的key值的時候，都必須事先檢查這個key值是否存在，否則如果直接調用不存在的key值，會直接拋出一個Key Error，比如說：

#### (1) 統計一個list裡每個元素出現的個數：

```python
a_list = ['a','b','x','a','a','b','z']
counter_dict = {}
for element in a_list:
    if element not in counter_dict:
        counter_dict[element] = 1
    else:
        counter_dict[element] += 1
```

#### (2) 建立一個一對多的 multidict:

```python
key_values = [('even',2),('odd',1),('even',8),('odd',3),('float',2.4),('odd',7)]

multi_dict = {}
for key,value in key_values:
    if key not in multi_dict:
        multi_dict[key] = [value]
    else:
        multi_dict[key].append(value)
```

collections提供的defaultdict給我們一個很好的解決方案，顧名思義，defaultdict對於我們調用一個不存在的key值，他會先建立一個default值給我們，而這個default值必須由一個可呼叫的函數產生，在我們初始化一個defaultdict時，必須先指定一個產生default值的函數：

```python
from collections import defaultdict

better_dict = defaultdict(list) # default值以一個list()方法產生
check_default = better_dict['a']
print(check_default) # 會輸出list()方法產生的空串列[]

better_dict['b'].append(1) # [1] 
better_dict['b'].append(2) # [1,2] 
better_dict['b'].append(3) # [1,2,3] 
print(better_dict['b'])
```

因此若想要建立一個multidict，只要用defaultdict(list)就可以很輕鬆的達成，不需要事先檢查key值存不存在，進而提高程式的可讀性:

```python
from collections import defaultdict

multi_dict = defaultdict(list) 
key_values = [('even',2),('odd',1),('even',8),('odd',3),('float',2.4),('odd',7)]

for key,value in key_values:
    multi_dict[key].append(value)

print(multi_dict) 
# 會輸出defaultdict(<class 'list'>, {'float': [2.4], 'even': [2, 8], 'odd': [1, 3, 7]})
```

但若我們想要直接給予一個固定的值給defaultdict是不行的，會產生TypeError的例外，比如說是在統計元素個數的狀況下，我想要讓default值為0，那有一個方法就是建構一個生成0的函數：

```python
from collections import defaultdict

def zero():
    return 0

counter_dict = defaultdict(zero) # default值以一個zero()方法產生
a_list = ['a','b','x','a','a','b','z']

for element in a_list:
        counter_dict[element] += 1

print(counter_dict) 
# 會輸出defaultdict(<function zero at 0x7fe488cb7bf8>, {'x': 1, 'z': 1, 'a': 3, 'b': 2})
```

然後因為這個defaultdict是dict的一個子類別，也就是說他繼承了dict的所有方法，或是現在這個defaultdict是dict的擴充，一般用在dict的使用方法在defaultdict也可以使用。
