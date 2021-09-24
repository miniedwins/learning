#　Singleton



## inhibit class

* 透過繼承 Singleton 類別，確認該物件是否已經被建立 ? 
* 若是該物件沒有存在則建立新的物件，否則回傳先前已建立好的物件

[class_singleton.py](https://github.com/miniedwins/learning/blob/main/coding/python/example/class_singleton.py)

~~~python
class Singleton:
    __instance = None
    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls) # 透過 __new__ 產生新的物件
            return cls.__instance # 執行後，會呼叫 Foo().__init__ 初始化物件內容
        else:
            return cls.__instance

class Foo(Singleton):
    def __init__(self, name): 
        self.name = name

if __name__ == '__main__':
    foo1 = Foo('foo')
    foo2 = Foo('foo')
    print(id(foo1))
    print(id(foo2))
~~~



## metaclass

* 透過自訂義 metaclass 可以實現建立 instance 方法

[metaclass_singleton.py](https://github.com/miniedwins/learning/blob/main/coding/python/example/metaclass_singleton.py)
~~~python
class Singleton(type):
    def __init__(self, *args, **kwargs):
        self.__instance = None
        super().__init__(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        if self.__instance is None:
            # 執行後 super().__call__ 會呼叫 Foo.__init__()
            # 初始化後會返回一個已經創建好的 instance
            self.__instance = super().__call__(*args, **kwargs)
            return self.__instance
        else:
            return self.__instance
~~~

另外一種創建方式

~~~python
    def __call__(self, *args, **kwargs):
        if self.__instance is None:
			obj = object.__new__(self) # object.__new__ 方法會建立 Foo instance
            obj.__init__(*args, **kwargs) # 得到建立的 instance，然後再進行物件初始化
            self.__instance = obj # 在物件傳遞給內部屬性 self.__instance
            return self.__instance
        else:
            return self.__instance
~~~

只要創建 instance，就會呼叫元類別的 `__call__` 方法

~~~python
class Foo(metaclass=Singleton):
    def __init__(self, name):
        self.name = name
        print('Create foo')

if __name__ == '__main__':
    foo1 = Foo('foo')
    foo2 = Foo('foo')
    print(id(foo1))
    print(id(foo2))
    print(foo1.__dict__)
~~~







