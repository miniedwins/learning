# 正規化表達式



## 匹配規則



### 常見匹配規則

* 一般常見的 [...] 匹配規則 : 匹配方格裡任意字元，**裡面沒有特殊符號表示法**
  * [aeiou] 
  * [a-z]
  * [A-Z]
  * [0-9]
  * [^aeiou]
  * [^0-9]
  * [^a-z]
  * [^A-Z]



#### 範例 : [aeiou]

~~~python
# 匹配 xy or xz，相當於或運算
re.findall('x[yz]', 'xyuuuxz') # ['xy', 'xy']

# 匹配方格裡面個別的字元
re.findall('[.*+]', 'a.cd+') # ['.', '+']
~~~

#### 範例 : [a-z]

~~~python
# 匹配的是 qa, qb, ...qz
re.findall('q[a-z]', 'qabcdqz') # ['qa', 'qz']

# 星號前面表示要匹配[a-z]，所以所有的字串都顯示出來
re.findall('q[a-z]*', 'qabcdqz') # ['qabcdqz']

# 星號前面表示要匹配[a-z]而非數字，所以不會包含數字
re.findall('q[a-z]*', 'qabcdqz0') # ['qabcdqz']

# 方格沒有特殊符號表示，所以(星號)也代表是一個字元符號
re.findall('q[a*z]', 'qabcdq*z') # ['qa', 'q*']

# 除了[a-z]以外的字串，其他字串都匹配出來
re.findall('q[^a-z]', 'qAbcdqZq0') # ['qA', 'qZ', 'q0']
~~~

#### 範例 : [0-9]

~~~python
# 星號前面表示要匹配[0-9]數字
re.findall('q[0-9]*', 'qabcdqz0') # ['q']
~~~



### 特殊符號匹配

* 一些特殊符號代表的匹配功能
  * **\d** : 匹配任何數字，相當於 (0-9)
  * **\D** : 匹配任何非數字，包含特殊符號 (!@#$%%^&*(){}|等)
  * **\w** : 匹配字母 (a-z) 以及數字 (0-9) 下滑線 (_)
  * **\W** : 匹配非字母 (a-z) 數字 (0-9) 下滑線 (_)
  * **\s** : 匹配空白字母，相當於(\t\n\r\f)
  * **\S** : 匹配非空白字母
  * **'^'** : 匹配字串起始位置
  * **'$'** : 匹配字串結束位置
  * **'\\'** : 跳脫字元
  * **"\|"** : 分割符號
  * **"[]"** : 可以單獨列出，比如 `[amk]` 匹配 `'a'`， `'m'`， 或者 `'k'`
  * **.(dot)** : 符合單一字元 (符號, 數字, 空格)

#### 範例 : 特殊符號

~~~python
re.findall('\d', 'abc123') # ['1', '2', '3']
re.findall('\D', 'a!@#$%[{') # ['a', '!', '@', '#', '$', '%', '[', '{']
re.findall('\s', 'hello world') # [' ']
re.findall('\w', 'hello_') # ['h', 'e', 'l', 'l', '_']

# 開頭
re.findall('^abc', 'abcd') # ['abc']
re.findall('^abc', 'defgabc') # []

# 結尾
re.findall(r'abcdef$', 'abcdef') # ['abcdef'] 
re.findall(r'abcdef$', 'abcdabc') # []

# 分割
re.findall('ab|cd', 'ab123cd456') # ['ab', 'cd']
~~~

#### 範例 1 : 特殊符號轉譯

說明 : **特殊符號 (*.?+)** 都代表有不同的功能，**如果要找特殊字元時，可以使用跳脫字元的方式來搜索**，必須前面要加一個斜槓符號

~~~python
# 遇到了 "\n" 就無法匹配成功
re.findall('www.', 'www\nyahoo.com') # []

# 符號 (\b) 對直譯器而言是有意義的，所以輸出會被轉譯，所以需要使用跳脫字元
re.findall('I\b', 'I am Hero') # []

# python -> 傳遞 "\b"  (沒有跳脫字元) -> re.findall('收到轉譯字元')
# python -> 傳遞 "\\b" (加上跳脫字元) -> re.findall('收到真正的\b字元')
re.findall('I\\b', 'I am Hero') # ['I']

# 前面加上 'r' 直譯器就不會對任何字元作轉譯，也就是原生字元輸出
# re module 就可以收到真正要接收的字元
re.findall(r'I\b', 'I am Hero') # ['I']
~~~

#### 範例 2 : 特殊符號轉譯

目標是要匹配 **"\l"** 字串，但是為什麼要加上兩個 **"\\\\"** ? 

*  re 模組中也有特殊字元的表示方法，若是需要匹配單純的特殊字元，因此要需要加上跳脫字元
* 而直譯器中也需要將要傳遞這些單純的特殊字元給 re 模組 ，所以也需要加上跳脫字元

~~~python
# *** re 角度來看這件事情 ***
# 匹配單純的特殊字元，所以要加上跳脫字元
re.findall("c\\l", "abc\l") # !!! 錯誤的輸出結果 !!!

# *** Python 角度來看這件事情 ***
# Python要傳遞該字串 "c\\l" 給 re module
# 所以需要對特殊字元再加上跳脫字元，這樣才不會發生錯誤
re.findall("c\\\\l", "abc\l") # ['c\\l']

# 加上 'r'，直譯器就不會對任何字元作轉譯，直接傳遞原生字串
re.findall(r"c\\l", "abc\l") # ['c\\l']
~~~



### 貪婪與非貪婪模式

匹配過程中匹配的數量，會有下列兩種模式：

- **貪婪**：可能嘗試匹配更多的字元或是字串
- **非貪婪**：可能的減少匹配字元或是字串，並且減少重複的匹配

#### 語法說明

* **貪婪模式** 
  * **'*'** : 匹配 ***0 ~ N 次***
  * **'+'** : 匹配 ***1 ~ N 次***
* **非貪婪模式**
  * **'?'** : 匹配 ***0 ~ 1次***
  * **'{ }'** : 匹配 ***0 ~ N次***
  * **'{n, m}?'** : 匹配 **n ~ m 次**
  * **'{n, }?'** : 匹配 **n or n 次以上**
  * **'??'** : 
* 惰性匹配
  * **'*?'** : 最小只要 **0次** 匹配 (因為 **[ * ]** 在前面)
  * **'+?'** : 最小只要 **1次** 匹配  (因為 **[ + ]** 在前面)  



#### 範例 : 貪婪模式 

說明 :  **'*'** 代表最多可以匹配 ***0 ~ N 次***

~~~python
# 因最少匹配可以(0)次，因此字元(n)可以不用匹配成功
re.findall('edwin*', 'edwi') # ['edwi']

# 可以匹配無限次
re.findall('edwin*', 'edwinnnnnn') # ['edwinnnnnn']
~~~

說明 :  **'+'** 代表最多可以匹配 ***1 ~ N 次***

~~~python
# 最少要匹配一次，但是沒有匹配到
re.findall('edwin+', 'edwi') # []

# 符合最少要匹配一次
re.findall('edwin+', 'edwin') # [edwin]

# 可以匹配無限次
re.findall('edwin+', 'edwinnnnnn') # ['edwinnnnnn']
~~~



#### 範例 : 非貪婪模式 

說明 :  **'?'** 代表最多可以匹配 ***0 ~ 1次***

~~~python
# 最少匹配可以(0)次，因此字元(n)可以不用匹配成功
re.findall('edwin*?', 'edwinnnnnn') # ['edwi']
~~~

說明 :  **'{ }'** 代表作多可以匹配多少個字元

~~~python
re.findall('abc{0}', 'abc') # ['ab']
re.findall('abc{1}', 'abc') # ['abc']
re.findall('abc{1}', 'abccc') # ['abc']
re.findall('abc{2}', 'abccc') # ['abcc']

# 沒有符合最低字元次數，匹配不成功
re.findall('abc{4}', 'abccc') # []
~~~

說明 :  **'{n,m}'** 限制匹配 **n ~ m 次數**

~~~python
# 限制匹配次數，至少要有(1)次，最多(2)次
re.findall('edwin{1,2}', 'edwinnnnnn') # ['edwinn']
~~~

說明 :  **'{n, }'** 限制匹配 **n ~ 無限次數**

~~~python
# 至少匹配要有(1)次，但並未成功匹配
re.findall('edwin{1,}', 'edwi') # []

# 至少匹配要有(1)次，最多無限次
re.findall('edwin{1,}', 'edwinnnnnn') # ['edwinnnnnn']

# 最多只匹配一次
re.findall('abc{1,}?', 'abccccc') # ['abc']
~~~



#### 範例 : 惰性匹配

說明 : **'*?'** : 最小匹配只要 **0次**

~~~python
re.findall('abc*?', 'abccccc') # [ab]
~~~

說明 : **'+?'** : 最小匹配只要 **1次**

~~~python
re.findall('abc*?', 'abccccc') # [abc]
~~~



### 特殊使用方法

#### (?P=name)

說明 : （命名組合）類似正則組合，但是匹配到的子串組在外部是通過定義的 *name* 來獲取的

~~~python
# 匹配成功後會將年齡給顯示出來，但是我們只想要取姓名，就需要分組匹配
re.search("(?P<name>[a-z]+)\d+", "edwin18edward20") # edwin18

# 透過括號分組匹配，在該符號內 "<>" 設定為 "name"，只要匹配成功後就可以透過定義的 "name" 獲取
re.search("(?P<name>[a-z]+)\d+", "edwin18edward20").group('name') # 'edwin'

# 分成兩組的方式 ?P<name> and ?P<age>
re.search("(?P<name>[a-z]+)(?P<age>\d+)", "edwin18edward20").group('name') # 'edwin'
re.search("(?P<name>[a-z]+)(?P<age>\d+)", "edwin18edward20").group('age') # '18'
~~~

#### (?=...)

說明 : 匹配 `…` 的內容，但是並不消費樣式的內容。這個叫做 *lookahead assertion*。比如， `Isaac (?=Asimov)` 匹配 `'Isaac '` 只有在後面是 `'Asimov'` 的時候。

~~~python
s = "IsaacAsimov"
re.search("\w+(?=Asimov)", s)
<re.Match object; span=(0, 5), match='Isaac'>
~~~

#### (?<=...)

說明 : 匹配字符串的當前位置，它的前面匹配 `...` 的內容到當前位置。這叫 *positive lookbehind assertion* （正向後視斷定）

注意 :  positive lookbehind assertions 開始的樣式，如 `(?<=abc)def` ，並不是從 a 開始搜索，而是從 d 往回看的。

~~~python
re.search('(?<=abc)\w+', 'abcdef')
<re.Match object; span=(3, 6), match='def'>
~~~



### 標誌符號 (FLAGS)



## 函數操作方法

### match

說明 : 從字串的**起始位置**開始進行匹配，只要匹配成功的話，就會直接返回**位置資訊**，若是不符合直接回傳 None

語法 : match(pattern, string, flags=0)

備註 : 只會匹配成功一次，並不會重複匹配

#### 範例 : 基本使用方法

~~~python
# 字串起始位置有匹配到結果
text = "https://www.google.com"
re.match('https', text) # <re.Match object; span=(0, 5), match='https'>

# 直接取得匹配結果的位置
re.match('https', text).span() # (0,5)

# 字串起始位置沒有匹配成功，所以返回 None
re.match('google', text) # None
~~~

#### 範例 : GROUP 用法

~~~python
# 匹配成功後，透過 group 取得結果
re.match("\d+", "18edwin32edward").group() # '18'

# 注意: 如果沒有匹配成功，然後使用group取值會拋出異常(AttributeError)
re.match("\d+", "edwin32edward").group()
~~~

#### 範例 : FLAGS 用法

~~~python
# 添加 re.I 忽略大小寫
re.match('HTTPS', text, flags=re.I) # <re.Match object; span=(0, 5), match='https'>
~~~

#### 範例 : GROUPS 用法

下面被括號的地方，我們就可以透過 groups 分組的方式取得匹配結果

~~~python
text = 'Edwin lives in Taipei and he is 18 years old'
r = re.match(r'(.*) lives in ([a-z]*) and he is (\d+).*', text, re.I)
# <re.Match object; span=(0, 44), match='Edwin lives in Taipei and he is 18 years old'>

# groups 取得所有匹配結果
print(r.groups()) # ('Edwin', 'Taipei', '18')

r.group(0) # 'Edwin lives in Taipei and he is 18 years old.'
r.group(1) # 'Edwin'
r.group(2) # 'Taipei'
r.group(3) # '18'
~~~

### search

說明 : 搜尋整個字串，找到匹配成功後傳回，如果失敗傳回 None

語法 : search(pattern, string, flags=0)

備註 : 只會匹配成功一次，並不會重複匹配

#### 範例 : 基本使用方法

~~~python
text = 'https://www.google.com'
re.search("google", text) # <re.Match object; span=(12, 18), match='google'>
re.search("google", text).span() # (12, 18)
~~~

#### 範例 : GROUP 用法

~~~python
# 匹配成功後，透過 group 取得結果
re.search("[a-z]+\d+", "edwin18edward20").group() # 'edwin18'

# 注意: 如果沒有匹配成功，然後使用group取值會拋出異常(AttributeError)
re.search("\d+", "edwinedward").group()
~~~

#### 範例 : FLAGS 用法

~~~python
# 添加 re.I 忽略大小寫
re.search("GOOGLE", text, re.I) # <re.Match object; span=(12, 18), match='google'>
~~~

#### 範例 : GROUPS 用法

~~~python
re.search("([a-z]+)\d+", "edwin18edward20").groups() # ('edwin',)
re.search("([a-z]+)\d+", "edwin18edward20").group(0) # 'edwin18'
re.search("([a-z]+)\d+", "edwin18edward20").group(1) # 'edwin'
~~~

#### 備註 : match & search 

* search 會搜尋整個字串，來決定有沒有匹配成功
* match 開始的起始位置就一定要匹配成功



### findall

說明 : 找尋字串中**所有符合匹配的結果**，並且返回一個 **list**，如果沒有找到匹配的字符，就會回傳一個空的 **list**

語法 : findall(pattern, string, flags=0)

#### 範例 : 基本使用方法

~~~python
# 只要字串中有符合，返回所有結果在一個 list
re.findall("www\.yahoo|google\.com", "www.yahoo.com,123,www.google.com") # ['yahoo', 'google']
re.findall('T..pei', 'I live in Taipei and he is not lives in Taipei') # [Taipei, Taipei]

# 沒有符合匹配的字串，返回一個空的 list
re.findall('Taiwan', 'I am living in Taipei') # []
~~~

#### 範例 : 分組使用方法

~~~python
# 分組前
re.findall("[a-z]+\d+", "edwin18edward20")  # ['edwin18', 'edward20']

# 分組後 (匹配成功後，會優先取分組所關注的內容，然後將資料顯示出來)
re.findall("([a-z]+)\d+", "edwin18edward20") # ['edwin', 'edward']
re.findall("[a-z]+(\d+)", "edwin18edward20") # ['18', '20']
re.findall("([a-z]+)(\d+)", "edwin18edward20") # [('edwin', '18'), ('edward', '20')]
~~~



### finditer 

說明 : 所有符合匹配成功後，返回一個迭代器當作回傳值

語法 : finditer(pattern, string, flags)

#### 範例 : 基本使用方法

~~~python
# 找出年紀前的姓名
result = re.finditer('[a-z]+', 'Edwin18Ada13Edwrad40', re.I)

# <callable_iterator object at 0x000001B8E78CAD30>
print(type(result))

# 列印出符合的結果
for ret in result: 
    print(ret.group()) 

# Edwin
# Ada
# Edwrad
~~~



### sub

說明 : 匹配成功後的字串，替換成我們想要的字元或是字串

語法 : sub(pattern, repl, string, count=0, flags=0)

* repl : 欲要替換的字串，可以用函數的形式傳入

* count : 代表要替換字串的次數，預設全部替換

#### 範例 : 基本使用方法

~~~python
# 預設全部替換
text = "yahoo and google and amazon"
re.sub('\sand\s', ' & ', text) # 'yahoo & google & amazon'

# 設定只替換一次
re.sub('\sand\s', ' & ', text, count=1)
'yahoo & google and amazon'

# 多重替換
text = "a,bc.d"
re.sub("[.,]", "", text) # 'abcd'
~~~

#### 範例 : 使用函數方法替換

若是替換的字串需要複雜的處理方式，可以透過呼叫函數去執行

~~~python
import re
text = 'Jack66Jen58Ken28,Cathy38'

# 將匹配好的數字做平方計算
def square(match_result):
  num = int(match_result.group('number')) 
  return str(num**2)

# 給定我們匹配值一個名稱，用?P<name>
re.sub('(?P<number>\d+)', square, text)
~~~



### split

說明 : 匹配成功的字串進行分割，並且回傳一組串列

語法 : split(pattern, string, maxsplit, flags)

* maxsplit : 設定分割次數，default=0 (不限分割次數)

#### 範例 : 基本使用方法

~~~python
# 使用數字做分割
text = 'Edwin18Ada13Edward'
re.split('\d+', text) # ['Edwin', 'Ada', 'Edward']

# 匹配剛好在前後的位置，就會傳回空值
text = 'Edwin18Ada13'
re.split('\d+', text) # ['Edwin', 'Ada', '']

# 將數字也傳進陣列
re.split('(\d+)', text) # ['Edwin', '18', 'Ada', '13', 'Edward']

# 如果找不到匹配會回傳全部字串
re.split('\s', text) # ['Edwin18Ada13']

# 多重分割方法

# 方格裡面都只有字串沒有特殊符號，裡面的運最相當於邏輯運算(OR)
re.split('[.,]', 'a,bc.d') # ['a', 'bc', 'd']

# (a) 分割 : 分割若是左邊沒有內容就是空字串 
# (b) 分割 : 因為剛剛(a)分割後已經是空字串，分出來也是空字串
# (ab)分割 : 前面兩個都是空，就只剩下 "c"
re.split('[ab]', 'abc') # ['', '', 'c']
re.split('[ab]', 'asdabcd') # ['', 'sd', '', 'cd']
~~~

設定只做一次分割

~~~python
re.split('\d+', text, maxsplit=1) # ['Edwin', 'Ada13']
~~~

先定義匹配規則，再將該參數傳遞到 split

~~~python
pattern = re.compile('\d+')
re.split(pattern, text) # ['Edwin', 'Ada', 'Edward']
~~~



### compile

說明 : 定義正則表達式的匹配規則，回傳一個 pattern 類別。然後 match、search、findall 函數都可以透過這個規則使用。

語法 : compile(pattern, flags)

#### 範例 : 基本使用方法

~~~python
# 定義匹配規則
pattern = re.compile('www\.[a-z]*\.com', re.I)

# match
pattern.match('www.google.com') # <re.Match object; span=(0, 14), match='www.google.com'>
pattern.match('https://www.google.com') # None

# search
pattern.search('https://www.google.com, www.yahoo.com') 
# <re.Match object; span=(8, 22), match='www.google.com'>

# findall
pattern.findall('www.yahoo.com, www.***.com, www.google.com') # ['www.yahoo.com', 'www.google.com']
~~~
