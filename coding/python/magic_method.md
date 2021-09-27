# magic method

## all

說明 : 可用於限制模組導入時的套件，例如：from module import *

### 範例 : 限制可導入類別 (單一檔案)

#### 主程式 (main.py)

~~~python
from module import *
a1 = A1()

# 沒有設定可以導入'A2'類別，因此會拋出異常
# NameError: name 'A2' is not defined
a2 = A2()

# 若是直接指定導入'A2'，IDE會提示沒有 'A2 is not declared in __all__'
from module import A2
~~~

#### 模組檔案內容 (module.py)

~~~python
# 指定只能導入'A1'類別
__all__ = ['A1']

class A1:
    def __init__(self):
        pass

class A2:
    def __init__(self):
        pass
~~~



### 範例 : 限制可導入套件

#### 設定 (init)

~~~python
module
	|--> __init__.py
    |--> module_a.py
    |--> module_b.py

# 需要先導入要指定的套件
from .module_a import A1, A2
from .module_b import B1

# 指定導入套件的類別或函數
__all__ = ('A1', 'A2', 'B1')
~~~

#### 主程式 (main.py)

~~~python
from module import *
a1 = A1()
a2 = A2()
b1 = B1()

# __init__ 沒有指定導入該類別，因此會拋出錯誤訊息
b2 = B2()
~~~

#### 模組檔案內容

~~~python
# module_a.py
class A1:
    def __init__(self):
        pass

class A2:
    def __init__(self):
        pass
    
# module_b.py
class B1:
    def __init__(self):
        pass

class B2:
    def __init__(self):
        pass
~~~

## with 

說明 : 實現一個新的上下文管理器，以便使用with語句 。

### 範例 : 代碼塊計時功能

[Example : with_example_timethis.py](https://github.com/miniedwins/learning/blob/main/coding/python/example/contextlib/with_example_timethis.py)

在函數 `time_this()` 中，`yield` 之前的代碼會在上下文管理器中作為 `__enter__()` 方法執行， 所有在 `yield` 之後的代碼會作為 `__exit__()` 方法執行。 如果出現了異常，異常會在yield語句那裡拋出。

~~~python
import time
from contextlib import contextmanager

@contextmanager
def time_this(label):
    start = time.time()
    try:
        yield
    finally:
        end = time.time()
        print('{}: {}'.format(label, end - start))

if __name__ == '__main__':    
    with time_this('counting'):
        n = 10000000
        while n > 0:
            n -= 1
~~~

若是執行時發生錯誤，如何解決 ?

我們假設在 `contextmanager` 語句拋出一個例外 `RuntimeError` Execption

~~~python
@contextmanager
def time_this(label):
try:
	yield
	raise RuntimeError('RuntimeError Exception') # 假設一個例外拋出
finally:
		....
~~~

呼叫端需要使用 try except 語句去捕捉例外訊息

~~~python
try:
    with time_this('counting'):
        n = 10000000
        while n > 0:
            n -= 1
except Exception as err: # 這裡捕捉 "contextmanager" 拋出的例外訊息
    print(err)
~~~

### 範例 : 魔法方法實現

[Example : with_magic_method.py](https://github.com/miniedwins/learning/blob/main/coding/python/example/with_magic_method.py)

1. 執行 with 語句並將參數帶入給 `__init__`
2. `__enter__` 方法返回的值是 `self.fd`，賦值給呼叫方的變數 `fd`
3. 完成 with 代碼塊結束後，最後 `__exit__` 方法會被調用
4. `__exit__`方法返回的是 `None` (如果沒有 `return` 語句那麼方法會返回`None`)

~~~python
class OpenFile:
    def __init__(self, filename, mode='r'):
        self.fd = open(filename, mode)

    def __enter__(self):
        return self.fd

    def __exit__(self, type, value, trace):
        try:
            if type is None: # 若是沒有發生異常，則為 None 型態
                return
            else:
                self.handle_error(type, value, trace)
        finally:
            self.close_fd()
            return True

    def handle_error(self, type, value, trace):
        print('type:', type)
        print('value:', value)
        print('trace:', trace)

    def close_fd(self):
        self.fd.close()

if __name__ == '__main__':
    with OpenFile('demo.txt') as fd:
        fd.write('Hello World!')
~~~

如果發生異常，Python會將異常的`type`,`value`和`traceback`傳遞給`__exit__`方法。 它讓`__exit__`方法來決定如何關閉文件以及是否需要其他步驟。

**當異常發生時，`with`語句會採取哪些步驟。** 

* 它把異常的`type`,`value`和`traceback`傳遞給`__exit__`方法 
* 它讓`__exit__`方法來處理異常 :
  * 返回值是 `True`，那麼這個異常就被優雅地處理了。 
  * 返回值是 `True` 以外的任何東西，那麼這個異常將被`with`語句拋出。

**以下是發生異常後的狀態**

~~~python
type: <class 'io.UnsupportedOperation'>
value: not writable
trace: <traceback object at 0x0000022154692A80>
~~~

若是想要由呼叫端處理異常，則是用 try except 語句捕捉異常，`__exit__` 只要 `return` 返回值 `Fasle`

~~~python
if __name__ == '__main__':
    try:
    	with OpenFile('demo.txt') as fd:
        	fd.write('Hello World!')
    except Exception as err:
        print(err)
~~~



