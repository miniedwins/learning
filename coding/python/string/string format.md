# Python 字串格式化

介紹 Python 的字串格式化方法，調整文字與數值的輸出格式，並提供實用的範例程式碼。


在 Python 中若要以特定的格式來輸出文字或數值，可以使用透過各種字串的格式化方法來處理，而 Python 字串格式化的方法有兩種，一種是類似 C 語言 `printf` 的語法，另外一種是後來發展的 `format` 語法，兩種都可以使用，以下是各種格式化的使用方式。



## 基本字串格式化

基本的字串格式化方法是使用 `%` 運算子，前面放置輸出的文字樣板，後面放置要安插的資料：

```python
# 字串格式化
msg = 'Hello, %s!' % 'World'
print(msg) # Hello, World!
```

文字樣板的語法就跟 C 語言的 `printf` 樣板類似，以下是常見的幾種格式：

| 語法       | 說明                         |
| :--------- | :--------------------------- |
| `%s`       | 以 `str()` 函數輸出文字。    |
| `%f`       | 以浮點數方式輸出數值。       |
| `%d`       | 以十進位整數方式輸出數值。   |
| `%e`、`%E` | 以科學記號輸出數值。         |
| `%o`       | 以八進位整數方式輸出數值。   |
| `%x`、`%X` | 以十六進位整數方式輸出數值。 |
| `%c`       | 以字元方式輸出。             |
| `%r`       | 以 `repr()` 函數輸出文字。   |
| `%%`       | 輸出 `%` 百分比符號。        |

若有多組文字需要放進樣板中，則可用小括號包起來的 tuple：

```python
# 多組文字
msg = '%s, %s!' % ('Hello', 'World')
print(msg) # Hello, World!
```

這是輸出整數的例子：

```python
# 整數
msg = 'I am %d years old.' % 5
print(msg) # I am 5 years old.
```

文字與整數混用：

```python
# 文字與整數
msg = '%s is %d years old.' % ("James", 5)
print(msg) # James is 5 years old.
```

除了類似 C 語言 `printf` 的用法之外，亦可使用新的 `format` 語法：

```python
# 字串格式化
msg = '{}, {}!'.format('Hello', 'World')
print(msg) # Hello, World!
```

新的 `format` 語法可以在大括號中指定安插的參數，例如：

```python
# 改變參數順序
msg = '{1}, {0}!'.format('Hello', 'World')
print(msg) # Hello, World!
```

在一般的狀況下，`format` 會自動處理各種類型的資料，不用像 C 語言的 `printf` 一樣個別指定樣板，統一使用 `{}` 即可：

```python
# 文字與整數
msg = '{} is {} years old.'.format("James", 5)
print(msg) # James is 5 years old.
```

我們也可以明確指定每一項的資料類型：

```python
# 明確指定資料類型
msg = '{:s} is {:d} years old.'.format("James", 5)
print(msg) # James is 5 years old.
```

## 空間與對齊

有時候在輸出資料時，為了要讓文字排版整齊，會固定資料輸出的寬度。只要在樣板上加上數字，即可指定輸出的寬度：

```python
# 指定寬度
msg = '(%10s)' % 'Hello'
print(msg)　# (     Hello)
```

若要靠左對齊，可以加上負號：

```python
# 靠左對齊
msg = '(%-10s)' % 'Hello'
print(msg) # (Hello     )
```

若是浮點數，可以使用 `總寬度.小數位數` 的方式來指定：

```python
# 指定浮點數位數
msg = '(%8.3f)' % 12.3456
print(msg) #　(  12.346)
```

若要限制輸出字串的長度上限，可以在數字前方加上一個點：

```python
# 文字長度上限
msg = '(%.3s)' % 'Hello'
print(msg)　# (Hel)
```

以下是用新的 `format` 語法改寫的結果：

```python
# 指定寬度
msg = '({:10})'.format('Hello')
print(msg)
(Hello     )
# 靠右對齊
msg = '({:>10})'.format('Hello')
print(msg)
(     Hello)
# 靠左對齊
msg = '({:<10})'.format('Hello')
print(msg)
(Hello     )
# 置中對齊
msg = '({:^10})'.format('Hello')
print(msg)
(  Hello   )
# 指定浮點數位數
msg = '({:8.3f})'.format(12.3456)
print(msg)
(  12.346)
# 文字長度上限
msg = '({:.3})'.format('Hello')
print(msg) # (Hel)
```

## 數值格式

若要讓數值前方的空白以 `0` 填補，可以在指定寬度時加上一個 `0`：

```python
# 空白補 0
msg = '%06.2f' % 3.14159
print(msg) #　003.14
```

若要強迫數值加上正負號，可以加上一個加號：

```python
# 加上正負號
msg = '%+4.2f, %+4.2f' % (3.14, -3.14)
print(msg) # +3.14, -3.14
```

負數加負號，正數留空白：

```python
# 負數加負號，正數留空白
msg = '(% d), (% d)' % (3, -3)
print(msg) # ( 3), (-3)
```

以下是 `format` 的寫法：

```python
# 空白補 0
msg = '{:06.2f}'.format(3.14159)
print(msg) # 003.14

# 加上正負號
msg = '{:+4.2f}, {:+4.2f}'.format(3.14, -3.14)
print(msg) # +3.14, -3.14

# 負數加負號，正數留空白
msg = '({: d}), ({: d})'.format(3, -3)
print(msg) # ( 3), (-3)
```

## 字典與具名參數

格式或文字時，也可以直接使用字典（dictionary）變數：

```python
# 使用字典
data = {'first': 'Hello', 'last': 'World'}
msg = '%(first)s, %(last)s!' % data
print(msg) #　Hello, World!
```

以下是 `format` 的寫法：

```python
# 使用字典
data = {'first': 'Hello', 'last': 'World'}
msg = '{first}, {last}!'.format(**data)
print(msg) # Hello, World!
```

`format` 亦可使用具名參數的方式指定：

```python
# 使用具名參數
msg = '{first}, {last}!'.format(first = 'Hello', last = 'World')
print(msg) # Hello, World!
```

## 日期與時間

`format` 亦可接受 `datetime` 物件，依照指定的樣板輸出日期與時間：

```python
# 輸出日期與時間
from datetime import datetime
msg = '{:%Y-%m-%d %H:%M}'.format(datetime.today())
print(msg) # 2018-09-27 14:41
```

## 動態格式

樣板中的格式也可以透過參數動態來指定：

```python
# 動態格式
msg = '%.*s = %.*f' % (3, 'Gibberish', 3, 2.7182)
print(msg) #　Gib = 2.718
```

以下是 `format` 的寫法：

```python
# 動態格式
msg = '{:.{prec}} = {:.{prec}f}'.format('Gibberish', 2.7182, prec=3)
print(msg)　#　Gib = 2.718
```

