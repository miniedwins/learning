
# 字串操作

## find ( 尋找 )

* 若是找到字串返回一個 index 
* 沒有找到字串返回 -1 

~~~python
test_str = '01234567edwin'
index = test_str.find('edwin') # index=8
~~~



## isalpha ( 判斷字串為字元 )

若是字串有包含 "空白" 或是 "特殊字元" 也會返回 False

~~~python
test_str1 = 'Iamedwin'
test_str2 = 'I am edwin'
test_str3 = 'Iam18edwin'

test_str1.isalpha() # True
test_str2.isalpha() # False
test_str3.isalpha() # False
~~~



## ljust & rjust ( 填充字元 )

~~~python
# ljust
'abc'.ljust(5, '*')		# 'abc**'

# rjust
'abc'.rjust(5, '*')		# '**abc'
~~~



##  lower & upper ( 英文大小寫轉換 )

~~~python
'ABC'.lower()	# 'abc'
'abc'.upper()	# 'ABC'
~~~



## replace ( 置換 )

~~~python
# 返回一個 string type
'This is a test'.replace('is', 'eez') # 'Theez eez a test'
~~~



## strip ( 刪除字串 ) 

**語法 : str.replace(old, new[, max])**

old -- 將被替換的子字串。
new -- 新字串，用於替換old子字串。
max -- 可選字串, 替換不超過 max 次

~~~python
# 默認刪除空白字串（包括'\n', '\r', '\t', ' ')
test_string = '\n\r\tabc\r\n' # abc

# 删除字串開頭和結尾的空白（但不包括中間的空白）。
' internal whitespace is kept '.strip() # 'internal whitespace is kept'

# 指定刪除 (前後 "空白" "星號" "金探號")
'*** SPAM * for * everyone!!! ***'.strip(' *!') # 'SPAM * for * everyone'
~~~



## lstring ( 刪除開頭字串 )

~~~python
test_string = "   this is string example....wow!!!   ";
print(test_string.lstrip())		# this is string example....wow!!!

test_string = "88888888this is string example....wow!!!8888888";
print(test_string.lstrip('8'))	# this is string example....wow!!!8888888
~~~



## startswith ( 檢查字串開頭  )

**語法 : str.startswith(str, beg=0,end=len(string))**

str -- 這是要檢查的字符串。
beg -- 這是可選的參數設置匹配邊界的初始索引。
end -- 這是可選的參數設置匹配邊界的結束索引。

~~~python
str = "this is string example....wow!!!";
print str.startswith( 'this' )			# True
print str.startswith( 'is', 2, 4 )		# True
print str.startswith( 'this', 2, 4 )	# False
~~~



## endswith ( 檢查字串結尾  )

~~~python
text='welcome to qttc blog'
print text.endswith('g')        # True
print text.endswith('go')       # False
print text.endswith('og')       # True
print text.endswith('')         # True
print text.endswith('g ')       # False

# Example
fileName = 'text.exe'
if f.endswith('.exe'):
    print("YES")
else:
    print("NO")
~~~

# 字串連接

## join ( 列表轉字串 )

~~~python
a = ['1','2','3','4','5']
'x'.join(a) # '1x2x3x4x5'
'.'.join(a) # '1.2.3.4.5'
'-'.join(a) #　'1-2-3-4-5'
'/'.join(a) # '1/2/3/4/5'
'~'.join(a) # '1~2~3~4~5'
~~~



## join ( 字典轉字串 )

注意：會取得字典的 Key  

~~~python
a = {'a':1,'b':2,'c':3}
'$'.join(a) # 'a$b$c' 
~~~

# 字串分割

## split ( 分割 ) 

~~~python
# 返回一個 list type

'1+2+3+4+5'.split('+') # ['1', '2', '3', '4', '5']
'/usr/bin/env'.split('/') # ['', 'usr', 'bin', 'env']
'Using the default'.split() # ['Using', 'the', 'default']
~~~



## splitlines ( 跳行分割 )

語法 : str.splitlines([keepends])

按照行('\r', '\r\n', \n')分隔，返回一個 list type。

~~~python
str1 = 'ab c\n\nde fg\rkl\r\n'
str1.splitlines() # ['ab c', '', 'de fg', 'kl']

for s in str.splitlines():
	print(s)  #  一行一行列出結果
~~~

如果參數 keepends 為 False，不包含換行。
如果為 True，則保留換行。

~~~python
str2 = 'ab c\n\nde fg\rkl\r\n'
str2.splitlines(True) # ['ab c\n', '\n', 'de fg\r', 'kl\r\n']
~~~
