



# import module

* module (頂級階層資料夾)

  * package_a
    * 可以到導入同一階層內所有套件 (package_b1, package_b2)
    * 可以導入頂級階層內所有套件 (module_a, module_b)
    * 不能再往上導入比頂級階層更高的套件
  * package_b
    * 可以到導入同一階層內所有套件 (package_a1, package_a2)
    * 可以導入頂級階層內所有套件 (module_a, module_b)
    * 不能再往上導入比頂級階層更高的套件


## FileTree

~~~shell
├── demo
│   ├── module
│   │   ├── package_a
│   │   │   ├── __init__.py
│   │   │   ├── package_a1.py
│   │   │   └── package_a2.py
│   │   └── package_b
│   │       ├── __init__.py
│   │       ├── package_b1.py
│   │       └── package_b2.py
│   ├── module_a.py
│   └── module_b.py
└── main.py		
~~~

## main.py

~~~python
import module

from module.package_a.package_a1 import PA1
a = PA1()

from module.package_b.package_b1 import PB1
b = PB1()
~~~

## module

### module_a.py

~~~python
class A1:
    def __init__(self):
        pass

class A2:
    def __init__(self):
        pass

# 導入相同階層(檔案)內的套件
from .module_b import B1
b1 = B1()

# 導入相同階層(資料夾)內的檔案套件
from .package_a import package_a1
package_a1.show_package_a1()
~~~

### module_b.py

~~~python
class B1:
    def __init__(self):
        pass

class B2:
    def __init__(self):
        pass
~~~

## package_a

### package_a1.py

~~~python
class PA1:
    def __init__(self):
        pass

def show_package_a1():
    print("show_package_a1")
  
# 導入相同階層(檔案)內的套件 
from .package_a2 import PA2
a2 = PA2()

# 導入上一個階層的(資料夾)內的套件
from ..package_b import package_b1
package_b1.show_package_b1()

# 導入上一個階層的(檔案)套件
from ..module_a import A1
a = A1()
~~~

### package_a2.py

~~~python
class PA2:
    def __init__(self):
        pass

def show_package_a2():
    print("show_package_a2")
~~~

## package_b

### package_b1.py

~~~python
class PB1:
    def __init__(self):
        pass

def show_package_b1():
    print("show_package_b1")

from ..package_a import package_a1
package_a1.show_package_a1()
~~~
