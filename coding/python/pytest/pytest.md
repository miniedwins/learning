# pytest

## pytest.fixture

### 語法說明

~~~python
fixture(callable_or_scope=None, *args, scope="function", params=None, autouse=False, ids=None, name=None)
~~~

### 基本使用方法 ( 不帶參數)

~~~python
import pytest

@pytest.fixture()
def fixture_demo():
    return 'This is fixture demo'

# 取得裝飾函式的返回值
def test_demo(fixture_demo):
    print(f'\n{fixture_demo}')
~~~

**運行結果**

~~~python
============================= test session starts =============================
test_pytest2.py::test_demo PASSED                                        [100%]
This is fixture demo
============================== 1 passed in 0.01s ==============================
~~~

### 參數使用方法 ( params )

~~~python
import pytest

@pytest.fixture(params=['test_data1', 'test_data2', 'test_data3'])
def fixture_demo(request): # 需要透過 request 取得資料
    return request.param

def test_demo(fixture_demo): # 呼叫函示 fixture_demo 取得資料內容
    print(f'\n{fixture_demo}')
~~~

**運行結果**

~~~python
============================= test session starts =============================
test_pytest2.py::test_demo[test_data1] PASSED                            [ 33%]
test_data1

test_pytest2.py::test_demo[test_data2] PASSED                            [ 66%]
test_data2

test_pytest2.py::test_demo[test_data3] PASSED                            [100%]
test_data3
============================== 3 passed in 0.02s ==============================
~~~

### 參數使用進階 ( params )

~~~python
@pytest.fixture(params=[
    ('redis', '6379'),
    ('elasticsearch', '9200')
])
def param(request):
    return request.param

@pytest.fixture(autouse=True)
def db(param):
    print('\nSucceed to connect %s:%s' % param)

    yield

    print('\nSucceed to close %s:%s' % param)

def test_api():
    assert 1 == 1
~~~

**運行結果**

~~~python
============================= test session starts =============================
test_pytest2.py::test_api[param0] 
Succeed to connect redis:6379
PASSED                                 [ 50%]
Succeed to close redis:6379

test_pytest2.py::test_api[param1] 
Succeed to connect elasticsearch:9200
PASSED                                 [100%]
Succeed to close elasticsearch:9200
============================== 2 passed in 0.02s ==============================
~~~

### 裝飾函數 ( List )

~~~python
data = [1,2,3,4,5] # 定義資料
@pytest.fixture(params=data) # params 可以接受 list,tuple,dictionary
def login_data(request): # 需要透過 request 取得資料
    return request.param

def test_case(login_data): # 呼叫函示 login_data   
    expect = [1,2,3,4,5]
    assert login_data in expect
~~~

**運行結果**

~~~python
============================= test session starts =============================
test_pytest2.py::test_case[1] PASSED                                     [ 20%]
test_pytest2.py::test_case[2] PASSED                                     [ 40%]
test_pytest2.py::test_case[3] PASSED                                     [ 60%]
test_pytest2.py::test_case[4] PASSED                                     [ 80%]
test_pytest2.py::test_case[5] PASSED                                     [100%]
============================== 5 passed in 0.02s ==============================
~~~

### 裝飾函數 ( 進階 )

~~~python
import pytest

# 測試目的 : 找出弱密碼

# 可以使用讀取外部檔案取得測試資料
# users = json.loads(open('./users.test.json', 'r').read())

# tom, mike 這兩條測試資料將會測試失敗
users = [
  {"name":"jack","password":"Iloverose"},
  {"name":"rose","password":"Ilovejack"},
  {"name":"tom","password":"password123"},  
  {"name":"mike","password":"password"},
  {"name":"james","password":"AGoodPasswordWordShouldBeLongEnough"}
]

class TestUserPasswordWithParam(object):
    @pytest.fixture(params=users) # 需要透過 request 取得測試資料 
    def user(self, request):	  
        return request.param 

    def test_user_password(self, user):
        passwd = user['password']
        assert len(passwd) >= 6
        msg = "user %s has a weak password" %(user['name'])
        assert passwd != 'password', msg
        assert passwd != 'password123', msg
~~~

**運行結果**

~~~python
============================= test session starts =============================
platform win32 -- Python 3.8.5, pytest-6.1.0, py-1.9.0, pluggy-0.13.1 -- C:\Users\PC\.virtualenvs\pythonProject-t6Q-1LJA\Scripts\python.exe
cachedir: .pytest_cache
metadata: {'Python': '3.8.5', 'Platform': 'Windows-10-10.0.18362-SP0', 'Packages': {'pytest': '6.1.0', 'py': '1.9.0', 'pluggy': '0.13.1'}, 'Plugins': {'html': '2.1.1', 'metadata': '1.10.0'}}
rootdir: C:\Users\PC\PycharmProjects\pythonProject, configfile: pytest.ini
plugins: html-2.1.1, metadata-1.10.0
collecting ... collected 5 items

test_pytest2.py::TestUserPasswordWithParam::test_user_password[user0] 
test_pytest2.py::TestUserPasswordWithParam::test_user_password[user1] 
test_pytest2.py::TestUserPasswordWithParam::test_user_password[user2] PASSED [ 20%]PASSED [ 40%]FAILED [ 60%]
test_pytest2.py:17 (TestUserPasswordWithParam.test_user_password[user2])
self = <test_pytest2.TestUserPasswordWithParam object at 0x0000026A955B1C70>
user = {'name': 'tom', 'password': 'password123'}

    def test_user_password(self, user):
        passwd = user['password']
        assert len(passwd) >= 6
        msg = "user %s has a weak password" %(user['name'])
        assert passwd != 'password', msg
>       assert passwd != 'password123', msg
E       AssertionError: user tom has a weak password
E       assert 'password123' != 'password123'

test_pytest2.py:23: AssertionError
FAILED [ 80%]
test_pytest2.py:17 (TestUserPasswordWithParam.test_user_password[user3])
self = <test_pytest2.TestUserPasswordWithParam object at 0x0000026A955AB3A0>
user = {'name': 'mike', 'password': 'password'}

    def test_user_password(self, user):
        passwd = user['password']
        assert len(passwd) >= 6
        msg = "user %s has a weak password" %(user['name'])
>       assert passwd != 'password', msg
E       AssertionError: user mike has a weak password
E       assert 'password' != 'password'

test_pytest2.py:22: AssertionError
PASSED [100%]
Assertion failed

Assertion failed

Assertion failed

Assertion failed

test_pytest2.py::TestUserPasswordWithParam::test_user_password[user3] 
test_pytest2.py::TestUserPasswordWithParam::test_user_password[user4] 

================================== FAILURES ===================================
_____________ TestUserPasswordWithParam.test_user_password[user2] _____________

self = <test_pytest2.TestUserPasswordWithParam object at 0x0000026A955B1C70>
user = {'name': 'tom', 'password': 'password123'}

    def test_user_password(self, user):
        passwd = user['password']
        assert len(passwd) >= 6
        msg = "user %s has a weak password" %(user['name'])
        assert passwd != 'password', msg
>       assert passwd != 'password123', msg
E       AssertionError: user tom has a weak password
E       assert 'password123' != 'password123'

test_pytest2.py:23: AssertionError
_____________ TestUserPasswordWithParam.test_user_password[user3] _____________

self = <test_pytest2.TestUserPasswordWithParam object at 0x0000026A955AB3A0>
user = {'name': 'mike', 'password': 'password'}

    def test_user_password(self, user):
        passwd = user['password']
        assert len(passwd) >= 6
        msg = "user %s has a weak password" %(user['name'])
>       assert passwd != 'password', msg
E       AssertionError: user mike has a weak password
E       assert 'password' != 'password'

test_pytest2.py:22: AssertionError
=========================== short test summary info ===========================
FAILED test_pytest2.py::TestUserPasswordWithParam::test_user_password[user2]
FAILED test_pytest2.py::TestUserPasswordWithParam::test_user_password[user3]
========================= 2 failed, 3 passed in 0.10s =========================
~~~

### 多個參數裝飾

~~~python
import pytest

@pytest.fixture(params=["unittest", "pytest"])
def fix1(request):
    yield request.param

@pytest.fixture(params=["python", "java"])
def fix2(request):
    yield request.param

def test_main(fix1, fix2):
    print("\n{} - {}".format(fix1, fix2))
~~~

**運行結果**

~~~python
============================= test session starts =============================
test_pytest2.py::test_main[unittest-python] PASSED                       [ 25%]
unittest - python

test_pytest2.py::test_main[unittest-java] PASSED                         [ 50%]
unittest - java

test_pytest2.py::test_main[pytest-python] PASSED                         [ 75%]
pytest - python

test_pytest2.py::test_main[pytest-java] PASSED                           [100%]
pytest - java
============================== 4 passed in 0.02s ==============================
~~~

### 多個 fixture 引用

~~~python
import pytest

@pytest.fixture
def fix1():
    print("call fix1")

@pytest.fixture
def fix2(fix1):
    print("call fix2")

def test_main(fix2):
    pass
~~~

**運行結果**

~~~python
============================= test session starts =============================
test_pytest2.py::test_main 
call fix1

call fix2
PASSED                                        [100%]
============================== 1 passed in 0.01s ==============================
~~~

### 共享函式 (conftest)

**conftest**

在測試過程中，多個測試檔案可能都要呼叫 fixture 函式，可以將其移動到 conftest.py 檔案中。conftest.py 檔案中的 fixture 函式不需要在測試函式中匯入，可以被 pytest 自動識別，查詢順序從測試類開始，然後是測試模組，然後是 conftest.py 檔案，最後是內建外掛和第三方外掛。

**知識點：**

一個工程下可以有多個conftest.py的檔案，在工程根目錄下設定的conftest檔案起到全域性作用。在不同子目錄下也可以放conftest.py的檔案，作用範圍只能在改層級以及以下目錄生效，另conftest是不能跨模組呼叫的。

**Python File : conftest.py**

~~~python
import pytest

@pytest.fixture()
def user():
    return "user"
~~~

**Python File : test_demo.py**

~~~python
import pytest

def test_user(user):
    assert user == "user"
~~~

**運行結果**

~~~python
============================= test session starts =============================
platform win32 -- Python 3.8.5, pytest-6.0.2, py-1.9.0, pluggy-0.13.1 -- C:\Users\copol\AppData\Local\Programs\Python\Python38\python.exe
cachedir: .pytest_cache
metadata: {'Python': '3.8.5', 'Platform': 'Windows-10-10.0.19041-SP0', 'Packages': {'pytest': '6.0.2', 'py': '1.9.0', 'pluggy': '0.13.1'}, 'Plugins': {'assume': '2.4.2', 'forked': '1.3.0', 'html': '3.1.1', 'metadata': '1.11.0', 'ordering': '0.6', 'repeat': '0.9.1', 'rerunfailures': '9.1.1', 'xdist': '2.2.1'}}
rootdir: c:\Users\copol\OneDrive\桌面\python, configfile: test_script\pytest.ini
plugins: assume-2.4.2, forked-1.3.0, html-3.1.1, metadata-1.11.0, ordering-0.6, repeat-0.9.1, rerunfailures-9.1.1, xdist-2.2.1
collecting ... collected 1 item

test_script/test_demo.py::test_user PASSED

- generated xml file: C:\Users\copol\AppData\Local\Temp\tmp-11236U8jtB5SEoP08.xml -
============================== 1 passed in 0.02s ==============================
~~~



### 自動裝飾 ( autouse )

#### scope = function

當測試用例很多的時候，每次都傳這個參數，會很麻煩。fixture裡面有個參數autouse，默認是False沒開啟的，可以設置為True。

這樣用例就不用每次都去傳參數了，就會自動調用fixture功能。

~~~python
import pytest

# default : scope=function (作用域可以依測試方法彈性修改)
@pytest.fixture(autouse=True) 
def test1():
    print('\n開始執行function')
 
def test_a():
    print('---用例a執行---')
  
class TestCase:
    def test_b(self):
        print('---用例b執行---')
~~~

**運行結果**

~~~python
============================= test session starts =============================
test_pytest2.py::test_a 
開始執行function
PASSED                                 [ 50%]
---用例a執行---

test_pytest2.py::TestCase::test_b 
開始執行function
PASSED                                 [100%]
---用例b執行---
============================== 2 passed in 0.02s ==============================
~~~

#### scope = class

~~~python
import pytest

@pytest.fixture(scope='class', autouse=True)
def test1():
    print('\n開始執行function')
   
# 注意 : 雖然 scope='class'，但是單一個函式依然會執行
def test_a():
    print('\n---用例a執行---')

class TestCase1:
    def test_b(self):
        print('\n---用例b執行---')

class TestCase2:
    def test_c(self):
        print('\n---用例c執行---')
~~~

**運行結果**

~~~python
============================= test session starts =============================
test_pytest2.py::test_a 
開始執行function
PASSED                                [ 33%]
---用例a執行---

test_pytest2.py::TestCase1::test_b 
開始執行function
PASSED                                [ 66%]
---用例b執行---

test_pytest2.py::TestCase2::test_c 
開始執行function
PASSED                                [100%]
---用例c執行---
============================== 3 passed in 0.02s ==============================
~~~

#### 實際用法 (進階)

~~~python
import pytest
import time

DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

@pytest.fixture(scope='session', autouse=True)
def timer_session_scope():
    start = time.time()
    print('\nstart: {}'.format(time.strftime(DATE_FORMAT, time.localtime(start))))

    yield

    finished = time.time()
    print('finished: {}'.format(time.strftime(DATE_FORMAT, time.localtime(finished))))
    print('Total time cost: {:.3f}s'.format(finished - start))

@pytest.fixture(autouse=True)
def timer_function_scope():
    start = time.time()
    yield
    print('\nTime cost: {:.3f}s'.format(time.time() - start))
~~~

**運行結果**

~~~python
============================= test session starts =============================
test_pytest2.py::test_1 
start: 2020-10-06 16:55:46
PASSED                                           						 [50%]
Time cost: 1.004s

test_pytest2.py::test_2 PASSED                                           [100%]
Time cost: 2.005s
finished: 2020-10-06 16:55:49
Total time cost: 3.012s
============================== 2 passed in 3.03s ==============================
~~~

### 作用域 ( scope )

#### 函示 ( Function )

fixture裡面有個`scope`參數可以控制fixture的作用範圍，scope參數可以是session， module，class，function， 默認為function。

- session 會話級別：是多個文件調用一次，可以跨.py文件調用，每個.py文件就是module。
- module 模塊級別：模塊裡所有的用例執行前執行一次module級別的fixture。
- class 類級別 ：每個類執行前都會執行一次class級別的fixture。
- function  函數級別：每個測試用例執行前都會執行一次function級別的fixture。

~~~python
import pytest

# 預設 scope=function 
# 檔案內每一個 test case 只要有呼叫 "test_fixture" 都會 "完整的執行函示一次"

@pytest.fixture()
def test_fixture(): 
    a = "hello"
    print("每個測試用例之前運行一次")
    yield a

def test_01(test_fixture):
    print("這是test_01")

def test_02(test_fixture):
    print("這是test_02")
~~~

**運行結果**

~~~python
============================= test session starts =============================
test_pytest2.py::test_01 每個測試用例之前運行一次
PASSED                                          [ 50%]
test_01

test_pytest2.py::test_02 每個測試用例之前運行一次
PASSED                                          [100%]
test_02
============================== 2 passed in 0.02s ==============================
~~~

#### 類別 ( Class  )

~~~python
import pytest

# scope='class'
# (1) 若測試檔案內有多個 class，都會先執行一次 "test_fixture" 得到回傳的 DB obj
# (2) 每一個 class 裡的函示，只要呼叫 "test_fixture" 都會使用相同的 DB obj
# (3) 每一個 class 裡的函示運行的結果都會得到相同的 id value

class DB(object):
    def __init__(self):
        pass

@pytest.fixture(scope='class')
def test_fixture():
    return DB()

class TestDemo: 
    def test_demo01(self, test_fixture):
        print(f'\n {id(test_fixture)}') # 2083795359392

    def test_demo02(self, test_fixture):
        print(f'\n {id(test_fixture)}') # 2083795359392

class TestDemo2: 
    def test_demo03(self, test_fixture): # 2083795375584
        print(f'\n {id(test_fixture)}')

    def test_demo04(self, test_fixture):
        print(f'\n {id(test_fixture)}') # 2083795375584
~~~

**運行結果**

~~~python
============================= test session starts =============================
test_pytest2.py::TestDemo::test_demo01 PASSED                            [ 25%]
 2083795359392

test_pytest2.py::TestDemo::test_demo02 PASSED                            [ 50%]
 2083795359392

test_pytest2.py::TestDemo2::test_demo03 PASSED                           [ 75%]
 2083795375584

test_pytest2.py::TestDemo2::test_demo04 PASSED                           [100%]
 2083795375584
============================== 4 passed in 0.02s ==============================
~~~

#### 模組 ( Module )

(1) 當前.py腳本裡面所有用例開始前只執行一次。

(2) 每一個測試函示運行的結果都會得到相同的 id value

**Python File : conftest.py**

~~~python
# conftest.py

class DB(object):
    def __init__(self):
        pass

@pytest.fixture(scope='module')
def test_fixture():
    return DB()
~~~

**Python File : test_pytest2.py**


~~~python
# test_pytest2.py

import pytest

class TestDemo:
    def test_demo01(self, test_fixture):
        print(f'\n {id(test_fixture)}')	# 2874389465504

    def test_demo02(self, test_fixture):
        print(f'\n {id(test_fixture)}') # 2874389465504

class TestDemo2:
    def test_demo03(self, test_fixture):
        print(f'\n {id(test_fixture)}') # 2874389465504

    def test_demo04(self, test_fixture):
        print(f'\n {id(test_fixture)}') # 2874389465504
~~~

**Python File : test_pytest3.py**

~~~python
# test_pytest3.py

import pytest

class TestDemo3:
    def test_demo05(self, test_fixture):
        print(f'\n {id(test_fixture)}')	# 2874389464400

    def test_demo06(self, test_fixture):
        print(f'\n {id(test_fixture)}') # 2874389464400

class TestDemo4:
    def test_demo07(self, test_fixture):
        print(f'\n {id(test_fixture)}') # 2874389464400

    def test_demo08(self, test_fixture):
        print(f'\n {id(test_fixture)}') # 2874389464400
~~~

**運行結果**

~~~python
============================= test session starts =============================                           
test_pytest2.py::TestDemo::test_demo01
 2874389465504
PASSED
test_pytest2.py::TestDemo::test_demo02
 2874389465504
PASSED
test_pytest2.py::TestDemo2::test_demo03
 2874389465504
PASSED
test_pytest2.py::TestDemo2::test_demo04
 2874389465504
PASSED
test_pytest3.py::TestDemo3::test_demo05
 2874389464400
PASSED
test_pytest3.py::TestDemo3::test_demo06
 2874389464400
PASSED
test_pytest3.py::TestDemo4::test_demo07
 2874389464400
PASSED
test_pytest3.py::TestDemo4::test_demo08
 2874389464400
PASSED
============================== 8 passed in 0.16s ==============================
~~~

#### 會議 ( Session )

session 級別是可以跨模塊調用的，多個模塊下的用例只需調用一次fixture，可以設置為scope="session"，並且寫到conftest.py文件裡。

**conftest.py作用域：放到項目的根目錄下就可以全局調用了，如果放到某個package下，那就在改package內有效。**

**Python File : conftest.py**

~~~python
import pytest

@pytest.fixture(scope='session')
def commonData():
    str = ' 通過conftest.py 共享fixture'
    print('獲取到%s' % str)
    return str

~~~

**Python File : test_scope_1.py**

~~~python
import pytest

def testScope1(commonData):
    print(commonData)
    assert commonData == ' 通過conftest.py 共享fixture'

~~~

**Python File : test_scope_2.py**

~~~python
import pytest

def testScope2(commonData):
    print(commonData)
    assert commonData == ' 通過conftest.py 共享fixture'
~~~

**運行結果**

~~~python
======================================================= test session starts =======================================================
platform win32 -- Python 3.8.5, pytest-6.0.2, py-1.9.0, pluggy-0.13.1 -- c:\users\copol\appdata\local\programs\python\python38\python.exe
cachedir: .pytest_cache
metadata: {'Python': '3.8.5', 'Platform': 'Windows-10-10.0.19041-SP0', 'Packages': {'pytest': '6.0.2', 'py': '1.9.0', 'pluggy': '0.13.1'}, 'Plugins': {'assume': '2.4.2', 'forked': '1.3.0', 'html': '3.1.1', 'metadata': '1.11.0', 'ordering': '0.6', 'repeat': '0.9.1', 'rerunfailures': '9.1.1', 'xdist': '2.2.1'}}
rootdir: C:\Users\copol\OneDrive\桌面\python\test_script, configfile: pytest.ini
plugins: assume-2.4.2, forked-1.3.0, html-3.1.1, metadata-1.11.0, ordering-0.6, repeat-0.9.1, rerunfailures-9.1.1, xdist-2.2.1      
collected 2 items                                                                                                                   

test_scope1.py::testScope1 獲取到 通過conftest.py 共享fixture
 通過conftest.py 共享fixture
PASSED
test_scope2.py::testScope2  通過conftest.py 共享fixture
PASSED

======================================================== 2 passed in 0.04s ========================================================
~~~



### 異常處理

####  yiled

- 如果yield前面的程式碼，即setup部分已經丟擲異常了，則不會執行yield後面的teardown內容
- 如果測試用例丟擲異常，yield後面的teardown內容還是會正常執行

~~~python
import pytest

@pytest.fixture(scope='module')
def open():
    print("開啟瀏覽器！！！")
    yield
    print('關閉瀏覽器！！！')

def test01():
    print("\n我是第一個用例")
    # 如果第一個用例異常了，不影響其他的用例執行
    raise Exception #此處異常

def test02(open):
    print("\n我是第二個用例")

if __name__ == '__main__':
    pytest.main(["-q", "test_fixtrueYield.py"])
~~~

運行結果

~~~python
============================= test session starts =============================
platform win32 -- Python 3.8.5, pytest-6.0.2, py-1.9.0, pluggy-0.13.1 -- C:\Users\copol\AppData\Local\Programs\Python\Python38\python.exe
cachedir: .pytest_cache
metadata: {'Python': '3.8.5', 'Platform': 'Windows-10-10.0.19041-SP0', 'Packages': {'pytest': '6.0.2', 'py': '1.9.0', 'pluggy': '0.13.1'}, 'Plugins': {'assume': '2.4.2', 'forked': '1.3.0', 'html': '3.1.1', 'metadata': '1.11.0', 'ordering': '0.6', 'repeat': '0.9.1', 'rerunfailures': '9.1.1', 'xdist': '2.2.1'}}
rootdir: c:\Users\copol\OneDrive\桌面\python, configfile: test_script\pytest.ini
plugins: assume-2.4.2, forked-1.3.0, html-3.1.1, metadata-1.11.0, ordering-0.6, repeat-0.9.1, rerunfailures-9.1.1, xdist-2.2.1
collecting ... collected 2 items

test_script/test_demo.py::test01 
我是第一個用例
FAILED
test_script/test_demo.py::test02 開啟瀏覽器！！！

我是第二個用例
PASSED關閉瀏覽器！！！


================================== FAILURES ===================================
___________________________________ test01 ____________________________________

    def test01():
        print("\n我是第一個用例")
        # 如果第一個用例異常了，不影響其他的用例執行
>       raise Exception  # 此處異常
E       Exception

test_script\test_demo.py:14: Exception
- generated xml file: C:\Users\copol\AppData\Local\Temp\tmp-11236kldFOw0owA48.xml -
=========================== short test summary info ===========================
FAILED test_script/test_demo.py::test01 - Exception
========================= 1 failed, 1 passed in 0.12s =========================
~~~



## pytest.mark.parametrize

### 語法說明

~~~python
parametrize(argnames, argvalues, indirect=False, ids=None, scope=None)
~~~

### 基本使用方法

**pytest.mark.parametrize : 裝飾器可以讓我們每次參數化fixture的時候傳入多個項目**

**test_imput : 測試資料**

**expected : 驗證結果**

~~~python
import pytest

@pytest.mark.parametrize("test_input,expected", [
    ("3+5", 8),
    ("2+4", 6),
    ("6*9", 42),
])
def test_eval(test_input, expected):
    assert eval(test_input) == expected
~~~

**運行結果**

~~~python
============================= test session starts =============================


test_pytest2.py::test_eval[3+5-8] 
test_pytest2.py::test_eval[2+4-6] 
test_pytest2.py::test_eval[6*9-42] PASSED                                 [ 33%]PASSED                                 [ 66%]FAILED                                [100%]
test_pytest2.py:2 (test_eval[6*9-42])
54 != 42

Expected :42
Actual   :54
<Click to see difference>

test_input = '6*9', expected = 42

    @pytest.mark.parametrize("test_input,expected", [
        ("3+5", 8),
        ("2+4", 6),
        ("6*9", 42),
    ])
    def test_eval(test_input, expected):
>       assert eval(test_input) == expected
E       assert 54 == 42

test_pytest2.py:9: AssertionError

Assertion failed

Assertion failed


================================== FAILURES ===================================
______________________________ test_eval[6*9-42] ______________________________

test_input = '6*9', expected = 42

    @pytest.mark.parametrize("test_input,expected", [
        ("3+5", 8),
        ("2+4", 6),
        ("6*9", 42),
    ])
    def test_eval(test_input, expected):
>       assert eval(test_input) == expected
E       assert 54 == 42

test_pytest2.py:9: AssertionError
=========================== short test summary info ===========================
FAILED test_pytest2.py::test_eval[6*9-42] - assert 54 == 42
========================= 1 failed, 2 passed in 0.09s =========================
~~~

### 裝飾函數 ( List )

~~~python
import pytest

data = ["edward", "edwin"]

# 個別將資料 edward, edwin 傳送測試
@pytest.mark.parametrize("name",data)
def test_demo(name):
    print("測試數據為{}".format(name))
~~~

**運行結果**

~~~python
============================= test session starts =============================
test_pytest2.py::test_demo[edward] PASSED                                [ 50%]測試數據為edward
test_pytest2.py::test_demo[edwin] PASSED                                 [100%]測試數據為edwin
============================== 2 passed in 0.02s ==============================
~~~

### 裝飾函數 ( Dictionary )

~~~python
import pytest

account = [
    {"username": "admin1", "password": "123456"},
    {"username": "admin2", "password": "12345678"},
]
@pytest.mark.parametrize("data", account)
def test_login(data):
    print("Account:{}, Password:{}".format(data["username"],data["password"]))
~~~

**運行結果**

~~~python
============================= test session starts =============================
test_pytest2.py::test_login[data0] PASSED                                [ 50%]
Account:admin1, Password:123456

test_pytest2.py::test_login[data1] PASSED                                [100%]
Account:admin2, Password:12345678
============================== 2 passed in 0.01s ==============================
~~~

### 裝飾函數 ( Tuple )

~~~python
import pytest

data = [ ("admin1", "123456"), ("admin2", "12345678") ]
@pytest.mark.parametrize("username,password", data)
def test_login(username,password):
    print("賬號:{},密碼:{}".format(username, password))
~~~

 **運行結果**

~~~python
============================= test session starts =============================
test_pytest2.py::test_login[admin1-123456] PASSED                        [ 50%]Account:admin1,Password:123456

test_pytest2.py::test_login[admin2-12345678] PASSED                      [100%]Account:admin2,Password:12345678
============================== 2 passed in 0.01s ==============================
~~~

### 裝飾類別 ( Class )

~~~python
import pytest

@pytest.mark.parametrize("username,password",[("admin01","123456"),("admin02","12345678")])
class TestDemo:
    def test_demo1(self,username,password):
        print("\nAccount:{},Password:{}".format(username,password))

    def test_demo2(self,username,password):
        print("\nAccount:{},Password:{}".format(username,password))        
~~~

**運行結果**

~~~python
============================= test session starts =============================
test_pytest2.py::TestDemo::test_demo1[admin01-123456] PASSED             [ 25%]
Account:admin01,Password:123456

test_pytest2.py::TestDemo::test_demo1[admin02-12345678] PASSED           [ 50%]
Account:admin02,Password:12345678

test_pytest2.py::TestDemo::test_demo2[admin01-123456] PASSED             [ 75%]
Account:admin01,Password:123456

test_pytest2.py::TestDemo::test_demo2[admin02-12345678] PASSED           [100%]
Account:admin02,Password:12345678
============================== 4 passed in 0.02s ==============================
~~~

***注意：裝飾測試類別時，類別內所有的方法必須接收測試資料，否則會報錯；***

***裝飾測試函數時比較靈活，如果函數不使用數據就可以不裝飾。***

```python
import pytest

@pytest.mark.parametrize("username,password",[("admin01","123456"),("admin02","12345678")], scope='class')
class TestDemo:
    def test_demo1(self,username,password):
        print("\nAccount:{},Password:{}".format(username,password))

    def test_demo2(self,username,password):
        print("\nAccount:{},Password:{}".format(username,password))

	# 這邊沒有加入測試資料, 所以會報錯誤訊息。
    def test_demo3(self):  
        pass
```
**運行錯誤結果**

~~~python
=================================== ERRORS ====================================
______________________ ERROR collecting test_pytest2.py _______________________
In test_demo3: function uses no argument 'username'
=========================== short test summary info ===========================
ERROR test_pytest2.py::TestDemo
!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
============================== 1 error in 0.13s ===============================
~~~

### 多個參數裝飾 (一)

~~~python
import pytest

username = ["admin1", "admin2", "admin3"]
password = ["123456", "1234567", "12345678"]
@pytest.mark.parametrize("uname",username)
@pytest.mark.parametrize("pwd",password)
def test_demo(uname,pwd):
    print("\nAccount:{},Password:{}".format(uname, pwd))
~~~

**運行結果**

~~~python
============================= test session starts =============================
test_pytest2.py::test_demo[123456-admin1] PASSED                         [ 11%]
Account:admin1,Password:123456

test_pytest2.py::test_demo[123456-admin2] PASSED                         [ 22%]
Account:admin2,Password:123456

test_pytest2.py::test_demo[123456-admin3] PASSED                         [ 33%]
Account:admin3,Password:123456

test_pytest2.py::test_demo[1234567-admin1] PASSED                        [ 44%]
Account:admin1,Password:1234567

test_pytest2.py::test_demo[1234567-admin2] PASSED                        [ 55%]
Account:admin2,Password:1234567

test_pytest2.py::test_demo[1234567-admin3] PASSED                        [ 66%]
Account:admin3,Password:1234567

test_pytest2.py::test_demo[12345678-admin1] PASSED                       [ 77%]
Account:admin1,Password:12345678

test_pytest2.py::test_demo[12345678-admin2] PASSED                       [ 88%]
Account:admin2,Password:12345678

test_pytest2.py::test_demo[12345678-admin3] PASSED                       [100%]
Account:admin3,Password:12345678
============================== 9 passed in 0.04s ==============================
~~~

### 多個參數裝飾 (二)

~~~python
import pytest

@pytest.fixture(params=[1, 2, 3])
def fixture_param(request):
    print("\n\033[31;1m我是fixture_param，這是第%s次打印\033[0m" % request.param)
    return request.param

# indirect=True (fixture_param 當函數來使用)
# indirect=False (fixture_param 當傳遞變數來使用)
@pytest.mark.parametrize("fixture_param", ["a", "b", 'c'], indirect=True)
@pytest.mark.parametrize("a,b", [(1, 6), (2, 3)])
def test_fixture_param_and_parametrize(a, b, fixture_param):
    print("\n我是測試函數test_fixture_param_and_parametrize，參數a是%s，b是%s"%(a,b))
~~~

**運行結果**

~~~python
============================= test session starts =============================
test_pytest2.py::test_fixture_param_and_parametrize[1-6-a] 
我是fixture_param，這是第a次打印
PASSED        [ 16%]
我是測試函數test_fixture_param_and_parametrize，參數a是1，b是6

test_pytest2.py::test_fixture_param_and_parametrize[1-6-b] 
我是fixture_param，這是第b次打印
PASSED        [ 33%]
我是測試函數test_fixture_param_and_parametrize，參數a是1，b是6

test_pytest2.py::test_fixture_param_and_parametrize[1-6-c] 
我是fixture_param，這是第c次打印
PASSED        [ 50%]
我是測試函數test_fixture_param_and_parametrize，參數a是1，b是6

test_pytest2.py::test_fixture_param_and_parametrize[2-3-a] 
我是fixture_param，這是第a次打印
PASSED        [ 66%]
我是測試函數test_fixture_param_and_parametrize，參數a是2，b是3

test_pytest2.py::test_fixture_param_and_parametrize[2-3-b] 
我是fixture_param，這是第b次打印
PASSED        [ 83%]
我是測試函數test_fixture_param_and_parametrize，參數a是2，b是3

test_pytest2.py::test_fixture_param_and_parametrize[2-3-c] 
我是fixture_param，這是第c次打印
PASSED        [100%]
我是測試函數test_fixture_param_and_parametrize，參數a是2，b是3
============================== 6 passed in 0.04s ==============================
~~~

### 參數做為執行函數 ( indirect )

~~~python
import pytest

class MyTester:
    def __init__(self, x):
        self.x = x	# ---> (3)

    def dothis(self):
        assert self.x # # ---> (5)      

@pytest.fixture
def tester(request): # 這邊會接受來自 True, False 的參數
    """Create tester object"""
    return MyTester(request.param) # 透過 request 取得參數 ---> (2)

class TestIt: 
    # 個別將 True, False 傳遞到 tester  ---> (1)
    # indirect=True，參數為函數名稱，執行的時候會當做函數來執行
    @pytest.mark.parametrize('tester', [True, False], indirect=True) 
    def test_tc1(self, tester):
       tester.dothis() # ---> (4)      
~~~

**運行結果**

~~~python
============================= test session starts =============================
test_pytest2.py::TestIt::test_tc1[True] 
test_pytest2.py::TestIt::test_tc1[False] True
PASSED                           [ 50%]  False
FAILED                           [100%]
test_pytest2.py:17 (TestIt.test_tc1[False])
self = <test_pytest2.TestIt object at 0x000001B949B4D160>
tester = <test_pytest2.MyTester object at 0x000001B949B4D940>

    @pytest.mark.parametrize('tester', [True, False], indirect=True)
    def test_tc1(self, tester):
>      tester.dothis()

test_pytest2.py:20: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

self = <test_pytest2.MyTester object at 0x000001B949B4D940>

    def dothis(self):
>       assert self.x
E       assert False
E        +  where False = <test_pytest2.MyTester object at 0x000001B949B4D940>.x

test_pytest2.py:8: AssertionError

Assertion failed

Assertion failed

Assertion failed

Assertion failed


================================== FAILURES ===================================
___________________________ TestIt.test_tc1[False] ____________________________

self = <test_pytest2.TestIt object at 0x000001B949B4D160>
tester = <test_pytest2.MyTester object at 0x000001B949B4D940>

    @pytest.mark.parametrize('tester', [True, False], indirect=True)
    def test_tc1(self, tester):
>      tester.dothis()

test_pytest2.py:20: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

self = <test_pytest2.MyTester object at 0x000001B949B4D940>

    def dothis(self):
>       assert self.x
E       assert False
E        +  where False = <test_pytest2.MyTester object at 0x000001B949B4D940>.x

test_pytest2.py:8: AssertionError
---------------------------- Captured stdout setup ----------------------------
False
=========================== short test summary info ===========================
FAILED test_pytest2.py::TestIt::test_tc1[False] - assert False
========================= 1 failed, 1 passed in 0.09s =========================
~~~

### 增加可讀性 ( ids )

~~~python
import pytest

data = [ (1, 2, 3), (4, 5, 9) ]

# ids 標示格式
ids = ["a:{} + b:{} = expect:{}".format(a, b, expect) for a, b, expect in data]

def add(a, b):
    return a + b

@pytest.mark.parametrize('a, b, expect', data, ids=ids)
def test_parametrize_1(a, b, expect):
    print('\n測試資料\n{}-{}'.format(a, b))
    assert add(a, b) == expect
~~~

**運行結果**

~~~python
============================= test session starts =============================
test_pytest2.py::test_parametrize_1[a:1 + b:2 = expect:3] PASSED         [ 50%]
測試資料
1-2

test_pytest2.py::test_parametrize_1[a:4 + b:5 = expect:9] PASSED         [100%]
測試資料
4-5
============================== 2 passed in 0.02s ==============================
~~~

### 參數搭配  ( pytest.param )

~~~python
import pytest

@pytest.mark.parametrize(
    'test_input, expected',
    [('3+5', 8),
     ('1+2', 3),
     pytest.param('6*9', 42, marks=pytest.mark.xfail, id='XFAIL')])
def test_data2(test_input, expected):
    assert eval(test_input) == expected
~~~

**運行結果**

~~~python
============================= test session starts =============================
test_pytest2.py::test_data2[3+5-8] 
test_pytest2.py::test_data2[1+2-3] 
test_pytest2.py::test_data2[XFAIL] 
======================== 2 passed, 1 xfailed in 0.10s =========================
~~~

## pytest.mark.usefixtures

語法 : `pytest.mark.usefixtures(names)`

1. 既可以裝飾測試類，也可以裝飾測試方法；
2. 參數為 fixture 的名字，必須是 str 類型；

**usefixtures & fixture 區別**

* fixture() 可以有返回值
* usefixture() 就無法獲取到返回值

~~~python
import pytest

@pytest.fixture()
def test1():
    print('\n開始執行function')

# 裝飾在 function，直接呼叫 "test1"
@pytest.mark.usefixtures('test1')
def test_a():
    print('\n---用例a執行---')

    # 這邊無法取得返回值
    print('取返回值 : ', test1) 

# 裝飾在 class，直接呼叫 "test1"
@pytest.mark.usefixtures('test1')
class TestCase:

    def test_b(self):
        print('\n---用例b執行---')

    def test_c(self):
        print('\n---用例c執行---')
~~~

**運行結果**

~~~python
============================= test session starts =============================
test_pytest2.py::test_a 
開始執行function
PASSED                                 [ 33%]
---用例a執行---
取返回值 :  <function test1 at 0x000001DC015DB280>

test_pytest2.py::TestCase::test_b 
開始執行function
PASSED                                 [ 66%]
---用例b執行---

test_pytest2.py::TestCase::test_c 
開始執行function
PASSED                                 [100%]
---用例c執行---
============================== 3 passed in 0.02s ==============================
~~~

---

## pytest.mark

**使用標籤：webtest和hello，使用mark標記功能對於以後分類測試非常有用處**

~~~python
import pytest

@pytest.mark.webtest
def test_send_http():
    print("\nmark web test")

def test_something_quick():
    pass

def test_another():
    pass

@pytest.mark.hello
class TestCase:
    def test_01(self):
        print("\n---執行test_01---")

    def test_02(self):
        print("\n---執行test_02---")
~~~

**為了方便後續執行指令的時候能準確使用mark的標籤，可以寫入到pytest.ini文件**

標記好之後，可以使用 pytest --markers 查看到

~~~python
[pytest]

markers =
  webtest:  Run the webtest case
  hello:    Run the hello case
~~~

**運行結果**

~~~python
# 指定執行 pytest.mark.hello 
$ pytest -v test_pytest2.py -m hello 
============================= test session starts =============================
test_pytest2.py::TestClass::test_01 PASSED                     [ 50%]                                     test_pytest2.py::TestClass::test_02 PASSED                     [100%]                                   
======================= 2 passed, 3 deselected in 0.07s =======================                        

# hello 以外的測試案例都會被測試
$ pytest -v test_pytest2.py -m "not hello"
============================= test session starts =============================
test_pytest2.py::test_send_http PASSED                         [33%]                                     test_pytest2.py::test_something_quick PASSED                   [66%]                                     test_pytest2.py::test_another PASSED                           [100%]
======================= 3 passed, 2 deselected in 0.07s =======================                        
~~~

---

## pytest.mark.skip

語法：`@pytest.mark.skip(reason=None)`

說明：跳過執行測試用例，可選參數reason，跳過的原因，會在執行結果中打印。

用法：在類、方法或函數上添加`@pytest.mark.skip`。

~~~python
import pytest

@pytest.mark.skip(reason="功能未實現,暫不執行")
class TestDemo(object):

    def test_demo01(self):
        print("\n這是test_demo01")

    def test_demo02(self):
        print("\n這是test_demo02")
~~~

**運行結果**

~~~python
============================= test session starts =============================
test_pytest2.py::TestDemo::test_demo01 SKIPPED                           [ 50%]
Skipped: 功能未實現,暫不執行

test_pytest2.py::TestDemo::test_demo02 SKIPPED                           [100%]
Skipped: 功能未實現,暫不執行
============================= 2 skipped in 0.01s ==============================
~~~

**補充：除了通過使用標籤的方式，還可以在測試用例中調用`pytest.skip()`方法來實現跳過，傳入msg參數來說明跳過原因**

~~~python
import pytest

def test_demo01():
    n = 1
    while True:
        print("\n當前的的值為{}".format(n))
        n += 1
        if n == 4:
            pytest.skip("跳過的值為{}".format(n))
~~~

**運行結果**

~~~python
============================= test session starts =============================
test_pytest2.py::test_demo01 SKIPPED                                     [100%]
當前的的值為1
當前的的值為2
當前的的值為3
Skipped: 跳過的值為4
============================= 1 skipped in 0.01s ==============================
~~~

## pytest.mark.skipif

語法：`@pytest.mark.skipif(self,condition, reason=None)`。

說明：跳過執行測試用例，condition參數為條件，可選參數reason，跳過的原因，會在執行結果中打印

~~~python
import pytest
import sys

def test_demo01():
    print("\n這是test_demo01")

# 當前的 python 版本為 3.8.5，要求版本必須大於3.9，否則跳過測試。
@pytest.mark.skipif(sys.version < '3.9', reason="python版本必須大於3.7")
def test_demo02():
    print("\n這是test_demo02")
~~~

**運行結果**

~~~python
============================= test session starts =============================
test_pytest2.py::test_demo01 PASSED                                      [ 50%]
這是test_demo01

test_pytest2.py::test_demo02 SKIPPED                                     [100%]
Skipped: python版本必須大於3.7
======================== 1 passed, 1 skipped in 0.02s =========================
~~~

## pytest.mark.xfail

應用場景：用例功能不完善或者用例執行失敗，可以標記為xfail。

語法：`@pytest.mark.xfail(self,condition=None, reason=None, raises=None, run=True, strict=False)`。

說明：期望測試用例是失敗的，但是不會影響測試用例的的執行。如果測試用例執行失敗的則結果是xfail（不會額外顯示出錯誤信息）；如果測試用例執行成功的則結果是xpass。

~~~python
import pytest

def test_demo01():
    print("\n這是test_demo01")

# pytest 使用 x 表示預見的失敗（XFAIL）
# 預期的測試結果會是失敗的    
@pytest.mark.xfail()
def test_demo02():
    print("\n這是test_demo02")
    assert 1 == 2
~~~

**運行結果**

~~~python
============================= test session starts =============================
test_pytest2.py::test_demo01 PASSED                                      [ 50%]
這是test_demo01

test_pytest2.py::test_demo02 XFAIL                                       [100%]
這是test_demo02

@pytest.mark.xfail()
    def test_demo02():
        print("\n這是test_demo02")
>       assert 1 == 2
E       assert 1 == 2

test_pytest2.py:10: AssertionError
======================== 1 passed, 1 xfailed in 0.09s =========================
~~~

接下將用例斷言成功，標記為xfail。

~~~python
import pytest

def test_demo01():
    print("\n這是test_demo01")

# 如果預見的是失敗，但實際運行測試卻成功通過，pytest 使用 X 進行標記（XPASS）。
# 注意 : 這樣代表測試此案例有問題
@pytest.mark.xfail()
def test_demo02():
    print("\n這是test_demo02")
    assert 1 == 1
~~~

**運行結果**

~~~python
============================= test session starts =============================
test_pytest2.py::test_demo01 PASSED                                      [ 50%]
這是test_demo01

test_pytest2.py::test_demo02 XPASS                                       [100%]
這是test_demo02
======================== 1 passed, 1 xpassed in 0.01s =========================
~~~

## pytest stop at first failure

**一旦發生錯誤就停止測試 (-x) **

執行命令 : pytest -vx test_pytest2.py 

**或是設定最大容錯才停止 --maxfail=num (最大容錯數目)**

執行命令 : `pytest -v -x --maxfail=2 test_pytest2.py  `

~~~python
import pytest

def test_demo01():
    print("\n這是test_demo01")

def test_demo02():
    assert 0

def test_demo03():
    print("\n這是test_demo03")

def test_demo04():
    assert 0

def test_demo05():
    print("\n這是test_demo05")

~~~

**運行結果**

~~~python
=======================  test session starts =======================
platform win32 -- Python 3.8.5, pytest-6.0.2, py-1.9.0, pluggy-0.13.1 -- c:\users\copol\appdata\local\programs\python\python38\python.exe
cachedir: .pytest_cache
metadata: {'Python': '3.8.5', 'Platform': 'Windows-10-10.0.19041-SP0', 'Packages': {'pytest': '6.0.2', 'py': '1.9.0', 'pluggy': '0.13.1'}, 'Plugins': {'assume': '2.4.2', 'forked': '1.3.0', 'html': '3.1.1', 'metadata': '1.11.0', 'ordering': '0.6', 'repeat': '0.9.1', 'rerunfailures': '9.1.1', 'xdist': '2.2.1'}}
rootdir: C:\Users\copol\OneDrive\桌面\python\test_script, configfile: pytest.ini
plugins: assume-2.4.2, forked-1.3.0, html-3.1.1, metadata-1.11.0, ordering-0.6, repeat-0.9.1, rerunfailures-9.1.1, xdist-2.2.1      
collected 5 items                                                                                                                   

test_demo.py::test_demo01 
這是test_demo01
PASSED
test_demo.py::test_demo02 FAILED
test_demo.py::test_demo03
這是test_demo03
PASSED
test_demo.py::test_demo04 FAILED

=======================   FAILURES =======================  
_______________________   test_demo02  ___________________   

    def test_demo02():
>       assert 0
E       assert 0

test_demo.py:9: AssertionError
_______________________   test_demo04  ___________________   

    def test_demo04():
>       assert 0
E       assert 0

test_demo.py:17: AssertionError
=======================   short test summary info =======================
FAILED test_demo.py::test_demo02 - assert 0
FAILED test_demo.py::test_demo04 - assert 0
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! stopping after 2 failures !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! 
=======================   2 failed, 2 passed in 0.23s  =======================
PS C:\Users\copol\OneDrive\桌面\python\test_script> 
~~~

## pytest.raises

**預期異常的斷言** 

使用 **pytest.raises()** 對於測試自己的代碼故意引發的異常的情況

~~~python
import pytest

def func_excetion(name):
    if name != "Yana":
        raise Exception("Invalid User")
    else:
        return "Username is properly set"

def test_username_exception():
    """test that exception is raised for invalid username"""

    with pytest.raises(Exception):
        assert func_excetion("Ana")
~~~

如果您需要訪問實際的異常信息，可以使用如下：

* excinfo 是一個 ExceptionInfo 實例，它是引發的實際異常的包裝
* 主要成員特徵是 type, value , traceback

~~~python
def test_zero_division():
    with pytest.raises(ZeroDivisionError) as exceptionInfo:
        100 / 0
        
    assert exceptionInfo.type == ZeroDivisionError 			# 斷言異常型別
    assert "division by zero" in str(exceptionInfo.value) 	# 斷言異常的值
~~~

**match 使用**

~~~python
def test_zero_division_match():
    with pytest.raises(ZeroDivisionError, match=".*zero.*") as exceptionInfo:
        100 / 0
    
    # 也可以這樣
    with pytest.raises(ZeroDivisionError, match="zero") as exceptionInfo:
        100 / 0
~~~

**@pytest.mark.xfail** 使用check函數可能更適合記錄未修復的錯誤（測試描述了“應該”發生的情況）或依賴項中的錯誤。

~~~python
@pytest.mark.xfail(raises=IndexError)
def test_f():
    f()
~~~

# pytest package

## pytest - repeat

**設定重複次數 (--count)**

執行命令 :  pytest --count=3 test_file.py

應用 : 也可以配合只要遇到測試錯誤立刻停止的參數 (-x)，重複測試單一案例，只要發生問題就可以立刻停止

以下測試會依序針對每個函式重複驗證三次

~~~python
import pytest
from src import calculator

def test_add():
    except_result = 3
    real_result = calculator.add(1, 2)
    assert real_result == except_result

def test_sub():
    except_result = -1
    real_result = calculator.sub(1, 2)
    assert real_result == except_result
~~~

運行結果

~~~python
=======================  test session starts =======================
platform win32 -- Python 3.8.5, pytest-6.0.2, py-1.9.0, pluggy-0.13.1 -- c:\users\copol\appdata\local\programs\python\python38\python.exe
cachedir: .pytest_cache
metadata: {'Python': '3.8.5', 'Platform': 'Windows-10-10.0.19041-SP0', 'Packages': {'pytest': '6.0.2', 'py': '1.9.0', 'pluggy': '0.13.1'}, 'Plugins': {'assume': '2.4.2', 'forked': '1.3.0', 'html': '3.1.1', 'metadata': '1.11.0', 'ordering': '0.6', 'repeat': '0.9.1', 'rerunfailures': '9.1.1', 'xdist': '2.2.1'}}
rootdir: C:\Users\copol\OneDrive\桌面\python\test_script
plugins: assume-2.4.2, forked-1.3.0, html-3.1.1, metadata-1.11.0, ordering-0.6, repeat-0.9.1, rerunfailures-9.1.1, xdist-2.2.1      
collected 6 items

test_calculator.py::test_add[1-3] PASSED
test_calculator.py::test_add[2-3] PASSED
test_calculator.py::test_add[3-3] PASSED
test_calculator.py::test_sub[1-3] PASSED
test_calculator.py::test_sub[2-3] PASSED
test_calculator.py::test_sub[3-3] PASSED

=======================  6 passed in 0.04s =======================
PS C:\Users\copol\OneDrive\桌面\python\test_script> 
~~~

下面會是針對範圍重複驗證  (這樣就可以針對這個範圍區塊驗證三次)

**設定範圍驗證 (--repeat-scope= function, class, module)**

執行命令 : pytest -s -v --count=3 --repeat-scope=class test_demo.py

使用裝飾器 (mark.repeat) : 

* @pytest.mark.repeat(x)  (x=重複次數)
* 執行命令可以不用加上 --count (pytest -s -v --repeat-scope=class test_demo.py)

~~~python
import pytest

@pytest.fixture(scope="class")
def prefill():
    pass

@pytest.fixture(scope="class")
def verify():
    pass

# @pytest.mark.repeat(3)
class TestCase():
    def test_prefill(self, prefill):
        pass

    def test_verify_disk_before(self, verify):
        pass

    def test_download_microcode(self):
        pass

    def test_verify_disk_after(self, verify):
        pass
~~~

**運行結果**

~~~python
======================================================= test session starts =======================================================
platform win32 -- Python 3.8.5, pytest-6.0.2, py-1.9.0, pluggy-0.13.1 -- c:\users\copol\appdata\local\programs\python\python38\python.exe
cachedir: .pytest_cache
metadata: {'Python': '3.8.5', 'Platform': 'Windows-10-10.0.19041-SP0', 'Packages': {'pytest': '6.0.2', 'py': '1.9.0', 'pluggy': '0.13.1'}, 'Plugins': {'assume': '2.4.2', 'forked': '1.3.0', 'html': '3.1.1', 'metadata': '1.11.0', 'ordering': '0.6', 'repeat': '0.9.1', 'rerunfailures': '9.1.1', 'xdist': '2.2.1'}}
rootdir: C:\Users\copol\OneDrive\桌面\python\test_script, configfile: pytest.ini
plugins: assume-2.4.2, forked-1.3.0, html-3.1.1, metadata-1.11.0, ordering-0.6, repeat-0.9.1, rerunfailures-9.1.1, xdist-2.2.1      
collected 12 items

test_demo.py::TestCase::test_prefill[1-3] PASSED
test_demo.py::TestCase::test_verify_disk_before[1-3] PASSED
test_demo.py::TestCase::test_download_microcode[1-3] PASSED
test_demo.py::TestCase::test_verify_disk_after[1-3] PASSED
test_demo.py::TestCase::test_prefill[2-3] PASSED
test_demo.py::TestCase::test_verify_disk_before[2-3] PASSED
test_demo.py::TestCase::test_download_microcode[2-3] PASSED
test_demo.py::TestCase::test_verify_disk_after[2-3] PASSED
test_demo.py::TestCase::test_prefill[3-3] PASSED
test_demo.py::TestCase::test_verify_disk_before[3-3] PASSED
test_demo.py::TestCase::test_download_microcode[3-3] PASSED
test_demo.py::TestCase::test_verify_disk_after[3-3] PASSED

======================================================= 12 passed in 0.06s ======================================================== 
~~~



## pytest - rerunfailures

**設定重跑次數 (--rerun)**

執行命令 :  pytest --rerun 3 test_file.py

**設定間隔多少秒後再運行 (--rerun-delay)**

執行命令 :  pytest --reruns 5 --reruns-delay 3  test_file.py

**備註 : 重跑後，若是成功通過測試則會停止重跑**

~~~python
import pytest
import random

def test_case():
    res = random.randint(1, 4)
    expected = 3
    assert res == expected
~~~

**運行結果**

~~~python
=======================  test session starts =======================    
platform win32 -- Python 3.8.5, pytest-6.0.2, py-1.9.0, pluggy-0.13.1 -- c:\users\copol\appdata\local\programs\python\python38\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\copol\OneDrive\桌面\python\test_script
plugins: ordering-0.6, rerunfailures-9.1.1
collected 1 item                                                                                                                    

test_fixture.py::test_case RERUN
test_fixture.py::test_case RERUN
test_fixture.py::test_case PASSED

=======================  1 passed, 2 rerun in 2.14s =======================
PS C:\Users\copol\OneDrive\桌面\python\test_script> 
~~~



## pytest - assume

主要用來當斷言發生錯誤後 (正常會是立刻停止)，也會繼續往下執行後續的程式

~~~python
import pytest
import random

@pytest.mark.parametrize(('x', 'y'), [(1, 1), (1, 0), (0, 1)])
def test_assume(x, y):
    assert x == y
    assert 1 == 1
    assert 2 > 3

~~~

**運行結果**

~~~python
============================= test session starts =============================
platform win32 -- Python 3.8.5, pytest-6.0.2, py-1.9.0, pluggy-0.13.1 -- C:\Users\copol\AppData\Local\Programs\Python\Python38\python.exe
cachedir: .pytest_cache
rootdir: c:\Users\copol\OneDrive\桌面\python
plugins: assume-2.4.2, ordering-0.6, rerunfailures-9.1.1
collecting ... collected 3 items

test_script/test_fixture.py::test_assume[1-1] FAILED
test_script/test_fixture.py::test_assume[1-0] FAILED
test_script/test_fixture.py::test_assume[0-1] FAILED

================================== FAILURES ===================================
______________________________ test_assume[1-1] _______________________________

x = 1, y = 1

    @pytest.mark.parametrize(('x', 'y'), [(1, 1), (1, 0), (0, 1)])
    def test_assume(x, y):
        assert x == y
        assert 1 == 1
>       assert 2 > 3
E       assert 2 > 3

test_script\test_fixture.py:9: AssertionError
______________________________ test_assume[1-0] _______________________________

x = 1, y = 0

    @pytest.mark.parametrize(('x', 'y'), [(1, 1), (1, 0), (0, 1)])
    def test_assume(x, y):
>       assert x == y
E       assert 1 == 0
E         +1
E         -0

test_script\test_fixture.py:7: AssertionError
______________________________ test_assume[0-1] _______________________________

x = 0, y = 1

    @pytest.mark.parametrize(('x', 'y'), [(1, 1), (1, 0), (0, 1)])
    def test_assume(x, y):
>       assert x == y
E       assert 0 == 1
E         +0
E         -1

test_script\test_fixture.py:7: AssertionError
- generated xml file: C:\Users\copol\AppData\Local\Temp\tmp-10084a7hoBUOp3mYS.xml -
=========================== short test summary info ===========================
FAILED test_script/test_fixture.py::test_assume[1-1] - assert 2 > 3
FAILED test_script/test_fixture.py::test_assume[1-0] - assert 1 == 0
FAILED test_script/test_fixture.py::test_assume[0-1] - assert 0 == 1
============================== 3 failed in 0.13s ==============================
~~~



## pytest - xdist

使用平行執行測試的方式運行

執行命令 : pytest -n xxx

執行參數 : 

*  -n 代表 number processes 指定執行處理器的 Thread 數量
* -n auto 的話代表自動偵測 CPU 數量。

~~~python
import pytest
import time

@pytest.mark.parametrize('x', list(range(10)))
def test_process(x):
    time.sleep(1)
    print(x)
~~~

**運行結果**

~~~python
============================= test session starts =============================
platform win32 -- Python 3.8.5, pytest-6.0.2, py-1.9.0, pluggy-0.13.1 -- c:\users\copol\appdata\local\programs\python\python38\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\copol\OneDrive\桌面\python\test_script
plugins: assume-2.4.2, forked-1.3.0, ordering-0.6, rerunfailures-9.1.1, xdist-2.2.1
[gw0] win32 Python 3.8.5 cwd: C:\Users\copol\OneDrive\桌面\python\test_script
[gw1] win32 Python 3.8.5 cwd: C:\Users\copol\OneDrive\桌面\python\test_script
[gw2] win32 Python 3.8.5 cwd: C:\Users\copol\OneDrive\桌面\python\test_script
[gw3] win32 Python 3.8.5 cwd: C:\Users\copol\OneDrive\桌面\python\test_script
[gw0] Python 3.8.5 (tags/v3.8.5:580fbb0, Jul 20 2020, 15:57:54) [MSC v.1924 64 bit (AMD64)]
[gw1] Python 3.8.5 (tags/v3.8.5:580fbb0, Jul 20 2020, 15:57:54) [MSC v.1924 64 bit (AMD64)]
[gw2] Python 3.8.5 (tags/v3.8.5:580fbb0, Jul 20 2020, 15:57:54) [MSC v.1924 64 bit (AMD64)]
[gw3] Python 3.8.5 (tags/v3.8.5:580fbb0, Jul 20 2020, 15:57:54) [MSC v.1924 64 bit (AMD64)]
gw0 [10] / gw1 [10] / gw2 [10] / gw3 [10]
scheduling tests via LoadScheduling

test_fixture.py::test_process[0]
test_fixture.py::test_process[1]
test_fixture.py::test_process[3]
test_fixture.py::test_process[2]
[gw0] PASSED test_fixture.py::test_process[0] 
[gw3] PASSED test_fixture.py::test_process[3]
test_fixture.py::test_process[7]
test_fixture.py::test_process[4]
[gw2] PASSED test_fixture.py::test_process[2]
[gw1] PASSED test_fixture.py::test_process[1]
test_fixture.py::test_process[6]
test_fixture.py::test_process[5]
[gw3] PASSED test_fixture.py::test_process[7] 
[gw0] PASSED test_fixture.py::test_process[4]
test_fixture.py::test_process[9]
test_fixture.py::test_process[8]
[gw1] PASSED test_fixture.py::test_process[5]
[gw2] PASSED test_fixture.py::test_process[6]
[gw0] PASSED test_fixture.py::test_process[9] 
[gw3] PASSED test_fixture.py::test_process[8]

============================= 10 passed in 4.36s ============================= 
~~~

# pytest ini

## mark

**作用：**測試用例中添加了 @pytest.mark.webtest 裝飾器，如果不添加marks選項的話，就會報warnings

**格式：**list列表類型

~~~python
[pytest]

markers =
  webtest:  Run the webtest case
  hello: Run the hello case
~~~

指定標示的 mark 測試

~~~python
import pytest

@pytest.mark.webtest
def test_send_http():
    print("mark web test")

def test_something_quick():
    pass

def test_another():
    pass

@pytest.mark.hello
class TestClass:
    def test_01(self):
        print("hello :")

    def test_02(self):
        print("hello world!")

if __name__ == "__main__":
    pytest.main(["-v", "test_mark.py", "-m=hello"])
~~~



## addopts

**作用：**addopts參數可以更改默認命令行選項，這個當我們在cmd輸入一堆指令去執行用例的時候，就可以用該參數代替了，省去重復性的敲命令工作

**比如：**想測試完生成報告，失敗重跑兩次，一共運行兩次，通過分佈式去測試，如果在cmd中寫的話，命令會很長

~~~python
[pytest]
addopts = -v --reruns 1 --capture=sys --html=report.html --self-contained-html
~~~



## xfail_strict

**作用：**設置xfail_strict = True可以讓那些標記為@pytest.mark.xfail但實際通過顯示XPASS的測試用例被報告為失敗

**格式：**True 、False（默認），1、0

~~~python
[pytest]
xfail_strict = true
~~~

test_case2 會從原先的 **xpass** 變成顯示 **failed**，這樣比較不會判斷錯誤

~~~python
import pytest

def test_hello():
    print("hello world!")
    assert 1

@pytest.mark.xfail()
def test_case1():
    a = "hello"
    b = "hello world"
    assert a == b

@pytest.mark.xfail()
def test_case2():
    a = "hello"
    b = "hello world"
    assert a != b
~~~

**運行結果**

~~~python
============================= test session starts =============================
platform win32 -- Python 3.8.5, pytest-6.0.2, py-1.9.0, pluggy-0.13.1 -- C:\Users\copol\AppData\Local\Programs\Python\Python38\python.exe
cachedir: .pytest_cache
metadata: {'Python': '3.8.5', 'Platform': 'Windows-10-10.0.19041-SP0', 'Packages': {'pytest': '6.0.2', 'py': '1.9.0', 'pluggy': '0.13.1'}, 'Plugins': {'allure-pytest': '2.8.40', 'assume': '2.4.2', 'forked': '1.3.0', 'html': '3.1.1', 'metadata': '1.11.0', 'ordering': '0.6', 'repeat': '0.9.1', 'rerunfailures': '9.1.1', 'xdist': '2.2.1'}}
rootdir: c:\Users\copol\OneDrive\桌面\python, configfile: test_script\pytest.ini
plugins: allure-pytest-2.8.40, assume-2.4.2, forked-1.3.0, html-3.1.1, metadata-1.11.0, ordering-0.6, repeat-0.9.1, rerunfailures-9.1.1, xdist-2.2.1
collecting ... collected 3 items

test_script/test_demo.py::test_hello hello world!
PASSED
test_script/test_demo.py::test_case1 XFAIL
test_script/test_demo.py::test_case2 FAILED

================================== FAILURES ===================================
_________________________________ test_case2 __________________________________
[XPASS(strict)] 
- generated xml file: C:\Users\copol\AppData\Local\Temp\tmp-10732Okm76HKWi60X.xml -
-- generated html file: file://c:\Users\copol\OneDrive\桌面\python\report.html --
=========================== short test summary info ===========================
FAILED test_script/test_demo.py::test_case2
=================== 1 failed, 1 passed, 1 xfailed in 0.14s ====================
~~~



## log-cli (日誌)

**作用：**控制台實時輸出日誌

**格式：**log_cli=True 或False（默認），或者log_cli=1 或 0

~~~python
[pytest]

log_cli = 1
log_cli_level = INFO
log_cli_format = %(asctime)s [%(levelname)s] %(message)s (%(filename)s:%(lineno)s)
log_cli_date_format=%Y-%m-%d %H:%M:%S
~~~



## testpaths

**作用：**指定測試路徑

~~~python
[pytest]

testpaths = test_scripts
~~~

