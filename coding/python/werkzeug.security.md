# werkzeug.security

## 應用說明 

這種加密方式的原理：加密時混入一段“隨機”字符串（salt）再進行哈希加密。即使
密碼相同，如果 Salt 不同，那麼哈希值也是不一樣的。



## 函數功能 

- **密碼生成函數：generate_password_hash**

  **函數定義 :**

  ~~~python
  werkzeug.security.generate_password_hash(password, method='pbkdf2:sha1', salt_length=8)
  ~~~

  **參數說明：**

  - password: 明文密碼；
  - method：哈希加密的方法（需要 hashlib 庫支持的），格式為pdpdf2:[:iterations]
    method：哈希的方式，一般為SHA1
    iterations：（可選參數）迭代次數，默認為1000

  

- **密碼驗證函數：check_password_hash**

  **函數定義 :**

  ~~~python
  werkzeug.security.check_password_hash(pwhash, password)
  ~~~

  **參數說明：**

  - **pwhash：** generate_password_hash 生成的哈希字符串（即加密後的密碼）
  - **password：**需要驗證的明文密碼



## 基本應用

### 如何進行加密

~~~python
from werkzeug.security import  generate_password_hash,check_password_hash
print (generate_password_hash('123456'))
print (generate_password_hash('123456'))
~~~

**輸出結果**

因為 Salt 值是隨機的，所以就算是相同的密碼，生成的哈希值也不會是一樣的。

~~~python
pbkdf2:sha1:1000$0yy56h3w$ae1030bd575e95a1b7066120d6b2381ae01f678d
pbkdf2:sha1:1000$Roji1qH7$c6867df485c8c9ff094025e1bf779cbf570dcbf1
~~~

### 驗證加密內容

~~~python
from werkzeug.security import  generate_password_hash,check_password_hash

pwhash = "pbkdf2:sha1:1000$Roji1qH7$c6867df485c8c9ff094025e1bf779cbf570dcbf1"
print(check_password_hash(pwhash,'123456'))
~~~

**輸出結果**

~~~python
輸出：True
~~~



## 程式碼範例

1. 使用者設定密碼，然後加密內容。
2. 透過 verify_password 函數，確認密碼是否正確。

~~~python
from werkzeug.security import generate_password_hash, check_password_hash

class User:
    def __init__(self):
        self._password_hash = None

    # 這邊會回傳已經被加密過後的密碼 (SHA1)
    @property
    def password(self):
        if self._password_hash is None:
            raise AttributeError('Password is None')
        return self._password_hash

    # 設定使用者密碼
    @password.setter
    def password(self, password):
        if password:
            self._password_hash = generate_password_hash(password)
        else:
            raise AttributeError('Password is None')
	
    # 驗證密碼，若是正確回傳 'True' 否則回傳 'False'
    def verify_password(self, password):
        return check_password_hash(self._password_hash, password)


user = User()
user.password = '123'
print(user.password)
print(user.verify_password('123')) # True
print(user.verify_password('456')) # False
~~~

