# 讀寫 JSON 資料



## 編碼與解碼簡單範例

### 編碼

#### 轉換成 JSON 編碼格式

~~~python
data = {'name': 'edwin', 'age' : 18}
json_obj = json.dumps(data)
~~~

#### 轉換成 JSON 編碼並且寫入到檔案文件

~~~python
data = {'name': 'edwin', 'age' : 18}
file = open('json_obj.json', 'w')
json.dump(data, file)
~~~

#### 轉換成排序後的 JSON 編碼

~~~python
data = {'5': '123', 'a': '56', '1': 'cd', '0': '12'}
json.dumps(data, sort_keys=True)

# Output : '{"0": "12", "1": "cd", "5": "123", "a": "56"}'
~~~

#### 略過無法處理的 key

~~~python
data = {'name': 'edwin', 'age': 18, ( 10 , 20 ): 88 }
json.dumps(data, skipkeys=True)

# Output : '{"name": "edwin", "age": 18}'
~~~

#### 美觀的方式寫入檔案內容

若是需要一種更加美觀的方式寫入檔案內容，需加入參數 `indent`，修改如下 : 

~~~python
json.dump(data, file, indent=4)
~~~



### 解碼

#### 讀取 JSON 檔案格式並且轉換成 dict

~~~python
file = open('json_obj.json', 'r')
json.loads(file)
~~~



#### 美觀顯示輸出結果

讀取的 JSON 格式編碼有大量的嵌套結構，容易造成的閱讀不美觀，可以考慮使用 `pprint` 套件

~~~json
{
  "array": [
    1,
    2,
    3
  ],
  "boolean": true,
  "color": "gold",
  "null": null,
  "number": 123,
  "object": {
    "a": "b",
    "c": "d"
  },
  "string": "Hello World"
}
~~~

主程式 : 

~~~python
from pprint import pprint

file = open('sample.json', 'r')
data = json.load(file)
~~~

使用 print 輸出結果 : 

~~~python
{'array': [1, 2, 3], 'boolean': True, 'color': 'gold', 'null': None, 'number': 123, 'object': {'a': 'b', 'c': 'd'}, 'string': 'Hello World'}
~~~

使用 pprint 輸出結果 : 

~~~python
{
  "array": [
    1,
    2,
    3
  ],
  "boolean": true,
  "color": "gold",
  "null": null,
  "number": 123,
  "object": {
    "a": "b",
    "c": "d"
  },
  "string": "Hello World"
}
~~~



## 範例說明

### JSON 轉換為一個自訂義 Python 物件

`json.loads` 本該返回的是 dict 物件，但是我們可以透過 `object_hook` 將該返回值傳遞給指定的類別或函式，來實現自定義解碼器。

~~~python
class JSONObject:
    def __init__(self, d):
        self.__dict__ = d

data = json.loads(json_obj, object_hook=JSONObject)
print(type(data)) # <class '__main__.JSONObject'>
~~~

### 如何將一個類別物件序列化

類別物件是無法直接轉換成 JSON 格式，所以必須要提供一個序列化函式來處理。

`json.dumps` 直接對類別物件處理的話，執行後會報錯誤訊息，因為無法支持自動轉化。

~~~python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

p = Point(2, 3)
json.dumps(p) # 執行後會報錯誤訊息
~~~

若是想要序列化，可以使用簡單的方式執行，下列這個方式直接透過該物件所建立的 `__dict__` 轉換

~~~python
def serialize_instance(obj):
    return obj.__dict__

p = Point(2, 3)
json.dumps(serialize_instance(p))
~~~



### 自訂義轉換 JSON 編解碼格式

JSON 模組無法處理類別物件，所以需要使用自訂義的編碼方式，針對不同的型態可以做不同的字串處理。

`JSONEncoder and JSONDecoder` 可以透過 `default` 函式進行編解碼轉換，所以我們可以覆寫該函式方法。

#### JSONEncoder

* 首先繼承 `JSONEncoder` 並且覆寫 `default` 方法
* 每個 key's item 會被迭代執行 `default` 函式
* 然後使用 `isinstance` 判別不同型態，並且對 key's item 轉型成字串型別

~~~python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return {'x':self.x, 'y':self.y}
    
class JsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, complex):
            return [obj.real, obj.imag]

        if isinstance(obj, Point):
            return obj.__str__()

        if isinstance(obj, datetime):
            return obj.__str__()

        return json.JSONEncoder.default(self, obj)
~~~

主程式 : 

~~~python
p = Point(1,2)
json_data = {"Point": p, "number": 100, "time" : datetime.now(), "num": 2 + 1j}
data = JsonEncoder(indent=4).encode(json_data)
print(data)
~~~

輸出結果 : 

~~~python
{
    "Point": {
        "x": 1,
        "y": 2
    },
    "number": 100,
    "time": "2021-08-03 10:45:15.791055",
    "num": [
        2.0,
        1.0
    ]
}
~~~



#### JSONDecoder

**Example File : JSONDecoder_to_object.py**

* 首先繼承 `JSONDecoder` 並且指定 `object_hook` 函式
* 每個 key's item 會被迭代執行指定函式
* 使用 `isinstance` 判別不同型態，並且對 key's item 做自訂義字串處理

~~~python
class JSONDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, obj):
        if isinstance(obj, dict):
            for key in list(obj):
                obj[key] = self.object_hook(obj[key]) # 遞歸執行處理每個 Key Value
            return obj

        if isinstance(obj, list):
            for i in range(0, len(obj)):
                obj[i] = self.object_hook(obj[i]) # 遞歸執行處理每個 list item
            return obj

        if isinstance(obj, float):
            return f"{obj:.2f}"	# 遇到浮點值則取兩位數

        return obj
~~~

主程式 :

~~~python
json_data = '{"name": "Edwin", "birthdate": "2020-02-22","high": 169, ' \
            '"weight": 62.12345, "address": ["taiwan", "taipei"]}'
data = JSONDecoder().decode(json_data)
print(data)
~~~

輸出結果 : 

~~~python
{'name': 'Edwin', 'birthdate': '2020-02-22', 'high': 169, 'weight': '62.12', 'address': ['taiwan', 'taipei']}
~~~

