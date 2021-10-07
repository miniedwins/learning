# Python configparser



**INI 檔案（副檔名為 `.ini`）**是一種格式簡單、應用廣泛的文字設定檔格式，普遍被應用於 Windows 系統以及其他的應用程式中，而在 Python 中若要讀取或寫入 INI 檔案，可以使用 `ConfigParser` 這個設定檔解析模組，以下是該模組的使用教學。



## INI 檔案格式簡介

INI 檔案格式非常簡單且直覺，每一條設定都是以 `名稱=值` 的方式來定義，並以區段（section）的方式將不同類別的設定區分開來，區段名稱是以中括號包來表示，而所有以分號（`;`）或井字號（`#`）開頭的行都會被視為註解。

以下是一個基本的 INI 設定檔範例：

```python
; 這是 owner 區段
[owner]
name = John Doe
organization = Acme Widgets Inc.

[database]
# 這些是資料庫相關的設定
server = 192.168.2.62
port = 143
file = C:\payroll.dat
```

在這個例子中正個設定檔總共有 `[owner]` 與 `[database]` 兩個區段，各自記錄了不同的設定。



## 讀取 INI 檔案

若要使用 `ConfigParser` 這個模組讀取 INI 設定檔的內容，首先引入模組，然後建立一個 `ConfigParser` 物件：

注意 : 若是 INI 檔案的 Section 不存在，會拋出例外 `configparser.NoOptionError`

```python
# 引入 configparser 模組
import configparser

# 建立 ConfigParser
config = configparser.ConfigParser()
```

接著以 `read` 方法函數讀取 INI 設定檔：

```python
# 讀取 INI 設定檔
config.read('example.ini')
```

只要知道區段與設定值的名稱，就可以直接取得對應的設定值：

```python
# 取得設定值
print(config['owner']['name'])
John Doe

# 使用 "get" 方法取得設定值
print(config.get('owner', 'name'))
John Doe
```

若要列出所有區段的名稱，可以使用 `sections` 方法函數：

```python
# 列出所有區段
print(config.sections())
['owner', 'database']
```

若要列出指定區段下的所有設定名稱與值，可以使用：

```python
# 列出 database 區段下所有設定
for key in config['database']:
  print("{}: {}".format(key, config['database'][key]))

server: 192.168.2.62
port: 143
file: C:\payroll.dat
```

或者使用 `config.items (section)` 讀取指定區段內所有的設定名稱與值

~~~python
# 列出 database 區段下所有設定
for key, value in config.items('database'):
    print("{}: {}".format(key, value)

server: 192.168.2.62
port: 143
file: C:\payroll.dat          
~~~

所有以 `ConfigParser` 從 INI 檔案中讀取出來的資料都是文字型態，數值或布林值的資料在使用前要先轉換，或是改用 `getint`、`getfloat`、`getboolean` 等方式。

```python
# 轉換為整數
port = int(config['database']['port'])

# 讀取並轉換為整數
port = config['database'].getint('port')
```



## 建立 INI 檔案

若要將設定寫入 INI 檔案中，只要將各區段與對應的設定都整理好在一個 `ConfigParser` 之中，再一次寫入 INI 檔案中即可：

```python
import configparser
config = configparser.ConfigParser()

# 建立設定區段
config['owner'] = {'name': 'John Doe',
                   'organization': 'Acme Widgets Inc.'}

# 不同的建立設定區段方式
config['database'] = {}
config['database']['server'] = '192.168.2.62'

# 寫入 INI 檔案
with open('example.ini', 'w') as configfile:
  config.write(configfile)
```

這樣就可以產生一個 `example.ini` 設定檔了。

`ConfigParser` 的所有設定值都是文字，所以如果有數值或其他型態的資料，都必須先轉換為文字之後才能存入其中。



## 修改 INI 檔案

若要更改 INI 檔案內設定值，只要將設定讀取出來並修改之後，再寫回去即可：

注意 : 若是 INI 檔案的 Section 不存在，會拋出例外 `configparser.NoOptionError`

```python
import configparser
config = configparser.ConfigParser()

# 讀取 INI 設定檔
config.read('example.ini')

# 更改設定方法 1
config['database']['server'] = '192.168.35.87'

# 更改設定方法 2
config.set('database', 'server', '192.168.35.87')

# 寫入 INI 檔案
with open('example.ini', 'w') as configfile:
  config.write(configfile)
```