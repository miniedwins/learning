

# namedtuple

## 介紹

tuple 是一種 iterable，它是透過 index 方式取值，若是結構較小的內容，相當容易存取寫入，並不會造成維護上的困擾。但是一旦資料結構變成較為大的時候，通常可讀性與維護性上就會衍生出麻煩。

如果要訪問 tuple 裡的第100個參數的一個值，雖然使用 index 取值非常簡單，但維護該 tuple 結構卻不直觀，因為不清楚該 index 代表什麼意義，我們只是指定一個 index 數字來讀取或是寫入 tuple 內的第幾個位置，久而久之這個數字就會變成所謂的**魔幻數字**。

## 使用方法

宣告 namedtuple 需要給定兩個參數，第一個是名稱(type_name)，再來是欄位名稱(field_names)。namedtuple 建立完成後，就可以使用欄位名稱 (filed_names) 來讀取數值 (類似使用類別的方式)。

~~~python
from collections import namedtuple

# type_name : User
# filed_name : ['name', 'age', 'birthday']

User = namedtuple("User", ['name', 'age', 'birthday'])
user = User('edwin', 18, '9/11')
print(f"User: user.name}, Age:{user.age}, Birthday: {user.birthday}")

# 輸出結果
User:edwin, Age:18, Birthday: 9/11
~~~

獲取某個欄位值

~~~python
print(getattr(user, 'name')) # edwin
print(user.name) # edwin
~~~

列出所有的欄位的名稱

~~~python
print(user._fields)

# 輸出結果
('name', 'age', 'birthday')
~~~

### unpack

說明 : 可以使用同樣的 tuple 功能解包

~~~python
name, age, birthday = user
print(f"{name}, {age}, {birthday})

# 輸出結果
edwin, 18, 9/11
~~~

### dict to namedtuple

轉換一個字典到 namedtuple，使用 ** 兩星操作符，拆解引數列表（Unpacking Argument Lists）

~~~python
User = namedtuple("User", ['name', 'age', 'birthday'])
d = {'name': 'edwin', 'age': 18, 'birthday': '9/11'}
user = User(**d)
print(f"User:{user.name}, Age:{user.age}, Birthday: {user.birthday}")

# 輸出結果
User:edwin, Age:18, Birthday: 9/11
~~~

### add namedtuple

說明 : 使用現存的namedtuple來新增一個新的namedtuple

~~~python
User = namedtuple("User", ['name', 'age', 'birthday'])
Address = namedtuple("Address", 'city, home, code')
Person = namedtuple("Person", User._fields + Address._fields)
person = Person('edwin', '18', '9/11', 'Taipei', 'Yonghe', '234')
print(person)

# 輸出結果
Person(name='edwin', age='18', birthday='9/11', city='Taipei', home='Yonghe', code='234')
~~~

### _asdict

~~~python
user_dict = user._asdict()
print(user_dict)

# 輸出結果
{'name': 'edwin', 'age': '18', 'birthday': '9/11'}
~~~

### _replace

返回一個新的命名元組實例，並將指定域替換為新的值

~~~python
user._replace(name='edward')
print(user)

# 輸出結果
User(name='edwin', age='18', birthday='9/11')
~~~
