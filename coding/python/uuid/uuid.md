# Python 產生 UUID 通用唯一辨識碼

介紹如何在 Python 中產生 UUID，當成具有唯一性質的識別代碼。


通用唯一辨識碼（Universally Unique Identifier，縮寫為 UUID）是一種 128 位元的識別碼，由於它幾乎不可能重複，所以在各種應用中常被拿來做為唯一性的識別代碼。



## uuid 模組

Python 的 `uuid` 模組可以用自動產生 UUID，首先引入 `uuid` 模組：

```python
# 引入 uuid 模組
import uuid
```

產生 UUID 的方法有好多種版本，第一版的 UUID 是根據日期、時間與網路卡的 MAC 位址所產生的：

```python
# 產生第一版 UUID（根據日期、時間與 MAC 位址）
uuid.uuid1()
UUID('c1f0ebf0-0088-11ea-a213-04d3b0813557')
```

第三版的 UUID 是根據根據命名空間與指定的名稱，以 MD5 雜湊演算法所產生的，所以同樣的參數設定就會產生相同的 UUID：

```python
# 產生第三版 UUID（根據命名空間與名稱，MD5）
uuid.uuid3(uuid.NAMESPACE_DNS, 'officeguide.cc')
UUID('f14cb77b-bce8-3847-ba73-da0f6b436093')
```

第四版的 UUID 是以隨機亂數的方式產生的：

```python
# 產生第四版 UUID（隨機）
uuid.uuid4()
UUID('ff18da9a-9152-4466-a2b6-b7e010bcdaff')
```

第五版的 UUID 跟第三版類似，只不過改用 SHA1 雜湊演算法：

```python
# 產生第五版 UUID（根據命名空間與名稱，SHA1）
uuid.uuid5(uuid.NAMESPACE_DNS, 'officeguide.cc')
UUID('ddff9a00-5d04-59cf-bca3-3c260c328420')
```



## uuid 與字串

若要將產生的 UUID 物件轉為普通字串，可以使用 `str` 函數：

```python
# UUID 轉為字串
my_uuid = uuid.uuid4()
str(my_uuid)
'bc5f89c0-63d8-4aeb-bfde-108f2fff2a8a'
```

若是想要轉成 Bytes 型態，可以使用 bytes

~~~python
my_uuid.bytes
~~~

反之若想要將普通字串轉為 UUID 物件，則可用 `uuid.UUID` 函數：

```python
# 字串轉為 UUID
uuid.UUID('bc5f89c0-63d8-4aeb-bfde-108f2fff2a8a')
UUID('bc5f89c0-63d8-4aeb-bfde-108f2fff2a8a')
```

若要以純 16 進位表示 UUID，可以取用 `hex` 屬性：

```python
# 以純 16 進位表示
my_uuid = uuid.UUID('bc5f89c0-63d8-4aeb-bfde-108f2fff2a8a')
my_uuid.hex
'bc5f89c063d84aebbfde108f2fff2a8a'
```

