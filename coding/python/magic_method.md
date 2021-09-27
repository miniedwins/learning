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

[with_example_timethis.py]: https://github.com/miniedwins/learning/blob/main/coding/python/example/contextlib/with_example_timethis.py

在函數 `timethis()` 中，`yield` 之前的代碼會在上下文管理器中作為 `__enter__()` 方法執行， 所有在 `yield` 之後的代碼會作為 `__exit__()` 方法執行。 如果出現了異常，異常會在yield語句那裡拋出。

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

呼叫端需要使用 try catch 語句去捕捉例外訊息

~~~python
try:
    with time_this('counting'):
        n = 10000000
        while n > 0:
            n -= 1
except Exception as err: # 這裡捕捉 "contextmanager" 拋出的例外訊息
    print(err)
~~~

### 範例 : 使用魔法方法 (enter and exit)

~~~python
class Demo:
    def __enter__(self):
        return self

    def __exit__(self, type, value, trace):
        print('type:', type)
        print('value:', value)
        print('trave:', trace)

    def do_something(slef):
        bar = 1 / 0
        return bar + 10

with Demo() as demo:
    demo.do_something()
~~~

