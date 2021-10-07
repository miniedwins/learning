# Constant

python語言本身沒有提供 Constant，但實際上可能會遇到需要使用 Constant 的情形這一功能。

一旦參被數設定的時，會自動執行 `__setattr__` 魔法方法，可以透過 `hasattr`函式判斷該值是否重新被賦值。若是該參數重複被賦值則可以拋出自定義的例外。

~~~python
class Const:
    def __setattr__(self, key, value):
        if hasattr(self, key):
            raise ConstError("ConstError")
        self.__dict__[key] = value
~~~

這裡可以特別定義 `Constant Exception`

~~~python
class ConstError(TypeError):
    def __init__(self, *args, **kwargs):
        pass
~~~

主程式 :

~~~python
class Foo(Const):
    pass

f = Foo()
f.a = 100
f.a = 200
~~~

執行結果 :

~~~python
Traceback (most recent call last):
  File "C:\Users\copol\PycharmProjects\StudyPython\singleton.py", line 17, in <module>
    f.a = 200
  File "C:\Users\copol\PycharmProjects\StudyPython\singleton.py", line 4, in __setattr__
    raise ConstError("ConstError")
__main__.ConstError: ConstError
~~~



