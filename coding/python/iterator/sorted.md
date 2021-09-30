# Python sort 與 sorted 排序法

介紹在 Python 中如何排序數值、文字，以及反向排序、自訂排序鍵值函數。

## 基本排序

在 Python 中若要對 list 中的元素進行排序，有兩種方式，一種是使用 `sorted`，他會對元素排序之後，傳回一個排序好的新 list，而原本的 list 則不受影響：

```python
x = [4, 2, 5, 3, 1]

# 排序並建立新的 List
y = sorted(x)
print(y)
[1, 2, 3, 4, 5]
```

另外一種方式是直接呼叫 list 本身的 `sort` 函數進行排序，這種方式會直接改變原本的 list 內容：

```python
x = [4, 2, 5, 3, 1]

# 對原本的 List 排序
x.sort()
print(x)
[1, 2, 3, 4, 5]
```

`sorted` 與 `sort` 也可以處理文字的排序，預設會依照英文字母的順序排列：

```python
# 文字排序
com = ['Microsoft', 'Google', 'Amazon', 'Facebook', 'Apple']
print(sorted(com))
['Amazon', 'Apple', 'Facebook', 'Google', 'Microsoft']
```

## 反向排序

如果要進行反向排序（數字由大到小），可以加上 `reverse = True` 參數：

```python
x = [4, 2, 5, 3, 1]

# 反向排序
y = sorted(x, reverse=True)
print(y)
[5, 4, 3, 2, 1]
```

`sort` 與 `sorted` 兩個函數的參數用法都一樣：

```python
x = [4, 2, 5, 3, 1]

# 反向排序
x.sort(reverse = True)
print(x)
```

文字亦可進行反向排序：

```python
# 反向排序
com = ['Microsoft', 'Google', 'Amazon', 'Facebook', 'Apple']
print(sorted(com, reverse=True))
['Microsoft', 'Google', 'Facebook', 'Apple', 'Amazon']
```

## 自訂排序鍵值函數

對於比較複雜的資料，我們也可以自己定義排序鍵值函數（就是指定要根據哪一個值來排序）。以下是一個範例，根據每個項目中的第三個數字元素進行排序：

```python
scores = [
    ('Jane', 'B', 12),
    ('John', 'A', 15),
    ('Dave', 'B', 11)]

# 依照第三個數字元素排序
print(sorted(scores, key=lambda s: s[2]))
[('Dave', 'B', 11), ('Jane', 'B', 12), ('John', 'A', 15)]
```

`sort` 的自訂排序鍵值函數的用法也相同：

```python
scores = [
    ('Jane', 'B', 12),
    ('John', 'A', 15),
    ('Dave', 'B', 11)]

# 依照第三個數字元素排序
scores.sort(key = lambda s: s[2])
print(scores)
[('Dave', 'B', 11), ('Jane', 'B', 12), ('John', 'A', 15)]
```

對具名屬性的物件，也可以自訂排序鍵值：

```python
class Score:
    def __init__(self, name, grade, age):
        self.name = name
        self.grade = grade
        self.age = age
    def __repr__(self):
        return repr((self.name, self.grade, self.age))

scores_obj = [
    Score('Jane', 'B', 12),
    Score('John', 'A', 15),
    Score('Dave', 'B', 11)]

# 依照 age 排序
print(sorted(scores_obj, key=lambda s: s.age))
[('Dave', 'B', 11), ('Jane', 'B', 12), ('John', 'A', 15)]
```

## Operator 模組函數

由於類似上面這種自訂排序鍵值的方式很常見，所以 Python 的 operator 模組另外提供一種更簡潔、更有效率的 `itemgetter` 與 `attrgetter` 函數，專門用來處理這樣的情況。

對於普通的 tuple，可使用 `itemgetter` 以索引指定鍵值：

```python
from operator import itemgetter, attrgetter

scores = [
    ('Jane', 'B', 12),
    ('John', 'A', 15),
    ('Dave', 'B', 11)]

# 依照第三個數字元素排序
print(sorted(scores, key = itemgetter(2)))
[('Dave', 'B', 11), ('Jane', 'B', 12), ('John', 'A', 15)]
```

對具名屬性的物件，則使用 `attrgetter` 函數以名稱指定鍵值：

```python
from operator import itemgetter, attrgetter

class Score:
    def __init__(self, name, grade, age):
        self.name = name
        self.grade = grade
        self.age = age
    def __repr__(self):
        return repr((self.name, self.grade, self.age))

scores_obj = [
    Score('Jane', 'B', 12),
    Score('John', 'A', 15),
    Score('Dave', 'B', 11)]

# 依照 age 排序
print(sorted(scores_obj, key=attrgetter('age')))
[('Dave', 'B', 11), ('Jane', 'B', 12), ('John', 'A', 15)]
```

## 多鍵值排序

有時候主要的鍵值會有相同的狀況，這時候可能就會需要採用第二個或更多的鍵值來排序，`itemgetter` 可以接受多個鍵值，以下是簡單的範例：

```python
# 以第二個元素排序，若相同則以第三個元素排序
print(sorted(scores, key=itemgetter(1, 2)))
[('John', 'A', 15), ('Dave', 'B', 11), ('Jane', 'B', 12)]
```

這是 `attrgetter` 函數的範例：

```python
# 以 grade 排序，若相同則以 age 排序
print(sorted(scores_obj, key=attrgetter('grade', 'age')))
[('John', 'A', 15), ('Dave', 'B', 11), ('Jane', 'B', 12)]
```

