# pytest-mock

mock的技術，就是在測試時，不修改源碼的前提下，替換某些物件內容或是回傳值，模擬測試環境。

## mocker.patch

* 對一個物件使用後會成為一個 **MagicMock**，然後使用 mock 提供的函數或是屬性執行功能
* 被包裝成 **MagicMock**，並不會真正執行函數的本身的功能 **(重要)**

### patch

說明 :  模擬當執行 filename 為真的狀態，並且確認該函數是否有被呼叫

~~~python
def exists(filename):
    if not os.path.exists(filename): # 會假定判斷這個 filename 都為真的狀態
        raise

def test_exists(mocker):
    filename = 'test.file'
    mocker.patch('os.path.exists')
    exists(filename) # 執行後並不會拋出異常
    os.path.exists.assert_called_once_with(filename) # 查看是否被呼叫一次
~~~

### dict

說明 : 用於在一定范圍內設置字典中的值，並在測試結束時將字典恢復為其原始狀態

~~~python
foo = {'key': 'value'}

def test_dict_method(mocker):
    original = foo.copy()
    mocker.patch.dict(foo, {'new_key': 'new_value'}, clear=True)
    assert foo == {'new_key': 'new_value'}
    mocker.stopall()
    assert foo == original
~~~



### side_effect

說明 : 模擬拋出例外訊息，一旦執行後就會直接拋出錯誤訊息

~~~python
def echo_filename(filename):
    if not os.path.isfile(filename):
        raise ValueError(f'{filename} is not file.')
    return filename

def test_echo_filename(mocker):
    mocker.patch('os.path.isfile', side_effect=TypeError)
    with pytest.raises(TypeError):
        echo_filename('test')
~~~

### wraps

說明 : 可以既把某些函數包裝成 **MagicMock** 又不改變它的執行效果，也完全可以替換成另一個函數。

~~~python
def echo_name(filename):
    if not os.path.isfile(filename):
        raise ValueError(f'{filename} is not file.')
    print(f'filename: ', filename)
    print(f'length: ', len(filename))
    return filename

def test_echo_filename(mocker):
    mocker.patch('os.path.isfile', return_value=True)
    mock_print = mocker.patch('builtins.print', wraps=print)
    mock_len = mocker.patch(__name__ + '.len', wraps=len)
    assert 'test' == echo_name('test')
    assert mock_print.called
    assert mock_len.called
~~~



## mocker.patch.object

* 使用在某個類別中的函數或是其它模組上的函數

~~~python
class Foo:
    field = "foo"

    def func1(self):   
        return "external value"

    def func2(self, value):
        return self.func1() * value
    
    def func3(self, vale):
        return value * 2
~~~

### object

對類別中某一個函數成為一個 Mock，並且確認該函數是否有被呼叫

~~~python
def test_foo_func1(mocker):
    foo = Foo()
    mock_func1 = mocker.patch.object(foo, 'func1')
    foo.func1()
    assert mock_func1.called # 確認該函示是否被呼叫
~~~

模擬給予當前類別假定的屬性值，最後並確認是否為該值

~~~python
def test_foo_filed(mocker):
    foo = Foo()
    mocker.patch.object(foo, 'field', 'mock')
    # do something ...
    assert 'mock' == foo.field
~~~

### return_value

對類別中某一個函數成為一個 Mock，並且模擬一個假的回傳值

說明 : 測試的對象是 func2，它會呼叫 func1，主要為了避免 func1 可能需要真正的外部數值，所以模擬假的回傳值

~~~python
def test_fool_func2(mocker):
    foo = Foo()
	mocker.patch.object(foo, 'func1', return_value=10) # 模擬這個物件傳回值是10
    assert foo.func2(10) == 100 # 呼叫func2，得到的會是數值100
~~~

### side_efffect

模擬執行函數後拋出例外訊息

注意 : 一旦執行該函數就會直接拋出錯誤訊息

~~~python
def test_func3(mocker):
    foo = Foo()
    mocker_func3 = mocker.patch.object(foo, 'func3', side_effect=TypeError)
    with pytest.raises(TypeError):
        assert foo.func3(2) == 4
    assert mocker_func3.called
~~~



## mocker.spy

如果只是想用 **MagicMock** 包裝一個東西，而又不想改變其功能，就可以使用 spy。

注意 : 變成 spy 會真正執行該函數功能

~~~python
# module.py
def foo(value):
    return value * 2

# test_utils.py
def test_spy_listdir(mocker):
    mock_listdir = mocker.spy(os, 'listdir')
    print(os.listdir())
    assert mock_listdir.called
    
def test_spy_function(mocker):
    spy = mocker.spy(drive, 'foo')
    assert module.foo(5) == 10
    assert spy.call_count == 1
    assert spy.spy_return == 10

def test_spy_method(mocker):
    class Foo(object):
        def bar(self, v):
            return v * 2

    foo = Foo()
    spy = mocker.spy(foo, 'bar')
    assert foo.bar(21) == 42

    spy.assert_called_once_with(21)
    assert spy.spy_return == 42
~~~

