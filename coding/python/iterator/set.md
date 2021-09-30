# Python Set 

**介紹如何使用 Python 的集合（set）變數儲存不重複的元素，並進行各種操作。**

## 建立集合

若要直接建立一個集合，可用大括號將所有元素包起來：

```python
# 建立集合
fruits = {'apple', 'orange', 'banana', 'avocado'}
print(fruits)
{'avocado', 'banana', 'apple', 'orange'}
```

亦可使用列表（list）的資料以 `set` 函數來建立集合，建立集合時重複的元素會被自動刪除：

```python
# 列表
my_list = ['apple', 'orange', 'banana', 'apple', 'orange']

# 從列表建立集合（重複元素會自動刪除）
set(my_list)
{'banana', 'apple', 'orange'}
```

若傳入單一字串，`set` 會將每個字母拆開建立集合：

```python
# 建立字母集合
set('apple')
{'a', 'e', 'p', 'l'}
```

**集合之內的元素排列是隨機的，沒有順序性。**



## 增加、刪除元素

若要增加元素至集合中，可用 `add`：

```python
# 新增元素
fruits.add('lemon')
print(fruits)
{'banana', 'lemon', 'apple', 'avocado', 'orange'}
```

當使用 `add` 添加元素時，如果該元素本來就存在於集合中，就不會有任何效果。

若要刪除集合中指定的元素，則可用 `remove`：

```python
# 刪除元素
fruits.remove('lemon')
print(fruits)
{'banana', 'apple', 'avocado', 'orange'}
```

`remove` 如果遇到該元素本來就不存在時，就會出現錯誤，如果要避免因為元素不存在所產生的錯誤，可以改用 `discard`：

```python
# 刪除元素（元素不存在也不會出錯）
fruits.discard('lemon')
```



## 判斷元素是否存在

若要判斷元素是否存在於指定的集合中，可以使用 `in` 運算子：

```python
# 判斷元素是否存在
if 'apple' in fruits:
  print('apple 存在')
else:
  print('apple 不存在')
apple 存在
```



## 元素個數

入要取得集合內的元素個數，可以使用 `len` 函數來計算：

```python
# 元素個數
len(fruits)
4
```



## 判斷子集合、超集合

若要判斷一個小的集合是否為另外一個集合的子集合，可以使用 `issubset`：

```python
s1 = {"a", "b"}
s2 = {"d", "c", "b", "a"}

# 判斷 s1 是否為 s2 的子集合
s1.issubset(s2)
True
```

若要判斷超集合，則可使用 `issuperset`：

```python
# 判斷 s1 是否為 s2 的超集合
s2.issuperset(s1)
True
```



## 計算交集、聯集、差集

計算兩個集合的交集（同時存在於兩個集合中）可以使用 AND（`&`）運算子：

```python
s1 = {"a", "b", "c"}
s2 = {"e", "d", "c", "b"}

# 交集
s3 = s1 & s2
print(s3)
{'b', 'c'}
```

計算兩個集合的差集（存在第一個集合中，但不存在於第二個集合中）可以使用減法（`-`）運算子：

```python
# 差集
s4 = s2 - s1
print(s4)
{'e', 'd'}
```

計算兩個集合的聯集（存在於任一個集合中）可以使用 OR（`|`）運算子：

```python
# 聯集
s5 = s1 | s2
print(s5)
{'c', 'b', 'a', 'e', 'd'}
```

若要篩選出只存在於其中一個集合的元素，可以使用 `^` 運算子：

```python
# 只存在於其中一個集合
s6 = s1 ^ s2
print(s6)
{'a', 'e', 'd'}
```

## 清空集合

若要清空集合內所有元素，可以使用 `clear`：

```python
# 清空集合
fruits.clear()
```

## 刪除列表重複元素

集合最常用來去除列表中重複的元素，只要將原始的列表資料轉為集合，再轉回列表即可：

```python
# 原始列表資料
raw = ['A', 'B', 'A', 'C', 'D', 'B', 'C']

# 去除重複元素
data = list(set(raw))
print(data)
['A', 'D', 'B', 'C']
```