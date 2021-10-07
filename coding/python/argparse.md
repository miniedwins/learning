# Python Argparse 教學

## 概念

藉由命令 **ls** 的使用開始這些功能的介紹：

```bash
$ ls
cpython  devguide  prog.py  pypy  rm-unused-function.patch
$ ls pypy
ctypes_configure  demo  dotviewer  include  lib_pypy  lib-python ...
$ ls -l
total 20
drwxr-xr-x 19 wena wena 4096 Feb 18 18:51 cpython
drwxr-xr-x  4 wena wena 4096 Feb  8 12:04 devguide
-rwxr-xr-x  1 wena wena  535 Feb 19 00:05 prog.py
drwxr-xr-x 14 wena wena 4096 Feb  7 00:59 pypy
-rw-r--r--  1 wena wena  741 Feb 18 01:01 rm-unused-function.patch
$ ls --help
Usage: ls [OPTION]... [FILE]...
List information about the FILEs (the current directory by default).
Sort entries alphabetically if none of -cftuvSUX nor --sort is specified.
...
```

我們可以從四個命令中可以學到的幾個概念：

- 命令 **ls** 在執行時不用其他參數就可以顯示出當前目錄底下的內容。
- 根據這樣的概念延伸後來舉個例子，如果我們想秀出一個不在目錄的資料夾 `pypy` 的內容。我們可以在命令後加上一個位置參數。會用位置參數這樣的名稱是因為程式會知道輸入的參數該做的事情。這樣的概念很像另一個命令 **cp**，基本的使用方式是 `cp SRC DEST`。第一個位置參數代表的是*想要複製的目標*，第二個位置的參數代表的則是*想要複製到的地方*。
- 現在我們想再增加一些，要顯示除了檔名之外更多的資訊。在這裡就可以選擇加上 `-l` 這個參數。
- 這是 help 文件的片段。對於以前從未使用過的程序來說非常有用，可以透過這些 help 文件來瞭解這些該怎麼使用。

## 基本用法

我們以一個很簡單的例子開始下面的介紹：

```python
import argparse
parser = argparse.ArgumentParser()
parser.parse_args()
```

下面是運行這些代碼的結果：

```python
$ python3 prog.py
$ python3 prog.py --help
usage: prog.py [-h]

optional arguments:
  -h, --help  show this help message and exit
$ python3 prog.py --verbose
usage: prog.py [-h]
prog.py: error: unrecognized arguments: --verbose
$ python3 prog.py foo
usage: prog.py [-h]
prog.py: error: unrecognized arguments: foo
```

接者是發生的情況：

- 運行這個腳本而沒有給與任何參數時就不會顯示任何東西至標準輸出畫面上。這裡並不是這麼的有用。
- 第二個我們呈現出了 [`argparse`](https://docs.python.org/zh-tw/3/library/argparse.html#module-argparse) 模組的用處。我們幾乎沒有做什麼事情，但已經得到一個很好的幫助信息。
- 這個 `--help` 選項可以簡短的表示成 `-h` , 這是唯一一個選項我們不用去指明的（意即，沒有必要在這個參數後加上任何數值）。如果指定其他參數給他會造成錯誤。也因為這樣，我們得到了一個免費的信息。

## 介紹位置參數

例子：

```python
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("echo")
args = parser.parse_args()
print(args.echo)
```

運行這段代碼：

```python
$ python3 prog.py
usage: prog.py [-h] echo
prog.py: error: the following arguments are required: echo
$ python3 prog.py --help
usage: prog.py [-h] echo

positional arguments:
  echo

optional arguments:
  -h, --help  show this help message and exit
$ python3 prog.py foo
foo
```

接者是發生的情況：

- 我們增加了 `add_argument()` ，利用這個方法可以指名讓我們的程式接受哪些命令列參數。
- 現在呼叫我們的程序時需要指定一個參數選項。
- 在這個例子中， `parse_args()` 這個方法確實根據了 `echo` 這個選項回傳了資料。
- 這一變量是 [`argparse`](https://docs.python.org/zh-tw/3/library/argparse.html#module-argparse) 免費施放的某種 “魔法”（即是說，不需要指定哪個變量是存儲哪個值的）。你也可以注意到，這一名稱與傳遞給方法的字符串參數一致，都是 `echo`。

注意, 雖然 help 秀出了看起來不錯的信息, 但現在並沒有給予到實質幫助。像剛剛增加的 `echo` 這個位置參數，除了猜測和讀原始碼之外，我們根本不曉得該怎麼使用他。因此我們來做一點事讓他變得更有用：

```python
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("echo", help="echo the string you use here")
args = parser.parse_args()
print(args.echo)
```

然後我們得到：

```python
$ python3 prog.py -h
usage: prog.py [-h] echo

positional arguments:
  echo        echo the string you use here

optional arguments:
  -h, --help  show this help message and exit
```

現在來做一些更有用處的事情：

```python
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("square", help="display a square of a given number")
args = parser.parse_args()
print(args.square**2)
```

下面是運行這些代碼的結果：

```python
$ python3 prog.py 4
Traceback (most recent call last):
  File "prog.py", line 5, in <module>
    print(args.square**2)
TypeError: unsupported operand type(s) for ** or pow(): 'str' and 'int'
```

那並沒有如預期這樣。這是因為 [`argparse`](https://docs.python.org/zh-tw/3/library/argparse.html#module-argparse) 將我們給予選項的值當成字串，除然我們告訴他要怎麼做。所以我們來告訴 [`argparse`](https://docs.python.org/zh-tw/3/library/argparse.html#module-argparse) 將這個輸入值當成整數來使用：

```python
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("square", help="display a square of a given number",
                    type=int)
args = parser.parse_args()
print(args.square**2)
```

下面是運行這些代碼的結果：

```python
$ python3 prog.py 4
16
$ python3 prog.py four
usage: prog.py [-h] square
prog.py: error: argument square: invalid int value: 'four'
```

這樣很順利。現在程序在開始之前會因為錯誤的輸入而回報有用的訊息並結束掉。

## 介紹選項參數

到目前為止，我們一直在研究位置參數。讓我們看看如何添加可選的：

```python
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--verbosity", help="increase output verbosity")
args = parser.parse_args()
if args.verbosity:
    print("verbosity turned on")
```

接者是結果：

```python
$ python3 prog.py --verbosity 1
verbosity turned on
$ python3 prog.py
$ python3 prog.py --help
usage: prog.py [-h] [--verbosity VERBOSITY]

optional arguments:
  -h, --help            show this help message and exit
  --verbosity VERBOSITY
                        increase output verbosity
$ python3 prog.py --verbosity
usage: prog.py [-h] [--verbosity VERBOSITY]
prog.py: error: argument --verbosity: expected one argument
```

接者是發生的情況：

- 這個程式是寫成如果有指名 `--verbosity` 這個參數選項那才顯示些資訊，反之亦然。
- 不添加這一選項時程序沒有提示任何錯誤而退出，表明這一選項確實是可選的。注意，如果一個可選參數沒有被使用時，相關變量被賦值為 `None`，在此例中是 `args.verbosity`，這也就是為什麼它在 [`if`](https://docs.python.org/zh-tw/3/reference/compound_stmts.html#if) 語句中被當作邏輯假。
- Help 訊息稍微有些不一樣。
- 當使用 `--verbosity` 參數選項時必須要指定一個數值。

在上面的例子中 `--verbosity`，接受任意的整數，但對我們的程式來說只接受兩個輸入值， `True` 或 `False`。所以我們來修改一下程式碼使其符合：

```python
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--verbose", help="increase output verbosity",
                    action="store_true")
args = parser.parse_args()
if args.verbose:
    print("verbosity turned on")
```

接者是結果：

```python
$ python3 prog.py --verbose
verbosity turned on
$ python3 prog.py --verbose 1
usage: prog.py [-h] [--verbose]
prog.py: error: unrecognized arguments: 1
$ python3 prog.py --help
usage: prog.py [-h] [--verbose]

optional arguments:
  -h, --help  show this help message and exit
  --verbose   increase output verbosity
```

接者是發生的情況：

- 現在，這一選項更多地是一個標誌，而非需要接受一個值的什麼東西。我們甚至改變了選項的名字來符合這一思路。注意我們現在指定了一個新的關鍵詞 `action`，並賦值為 `"store_true"`。這意味著，當這一選項存在時，為 `args.verbose` 賦值為 `True`。沒有指定時則隱含地賦值為 `False`。
- 當你為其指定一個值時，它會報錯，符合作為標誌的真正的精神。
- 注意不同的 help 文件。

### 短選項

如果你很熟悉命令列的使用的話，你將會發現我還沒講到關於短參數。其實這很簡單：

```python
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose", help="increase output verbosity",
                    action="store_true")
args = parser.parse_args()
if args.verbose:
    print("verbosity turned on")
```

效果就像這樣：

```python
$ python3 prog.py -v
verbosity turned on
$ python3 prog.py --help
usage: prog.py [-h] [-v]

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  increase output verbosity
```

注意新的表示對於幫助文件也是一樣的

## 現在結合位置與選項參數

我們的程式成長的越來越複雜：

```python
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("square", type=int,
                    help="display a square of a given number")
parser.add_argument("-v", "--verbose", action="store_true",
                    help="increase output verbosity")
args = parser.parse_args()
answer = args.square**2
if args.verbose:
    print("the square of {} equals {}".format(args.square, answer))
else:
    print(answer)
```

然後現在的輸出結果：

```python
$ python3 prog.py
usage: prog.py [-h] [-v] square
prog.py: error: the following arguments are required: square
$ python3 prog.py 4
16
$ python3 prog.py 4 --verbose
the square of 4 equals 16
$ python3 prog.py --verbose 4
the square of 4 equals 16
```

- 我們帶回了一個位置參數，結果發生了報錯。
- 注意現在的順序對於程式來說已經不再重要了.

給我們的程序加上接受多個冗長度的值，然後實際來用用：

```python
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("square", type=int,
                    help="display a square of a given number")
parser.add_argument("-v", "--verbosity", type=int,
                    help="increase output verbosity")
args = parser.parse_args()
answer = args.square**2
if args.verbosity == 2:
    print("the square of {} equals {}".format(args.square, answer))
elif args.verbosity == 1:
    print("{}^2 == {}".format(args.square, answer))
else:
    print(answer)
```

接者是結果：

```python
$ python3 prog.py 4
16
$ python3 prog.py 4 -v
usage: prog.py [-h] [-v VERBOSITY] square
prog.py: error: argument -v/--verbosity: expected one argument
$ python3 prog.py 4 -v 1
4^2 == 16
$ python3 prog.py 4 -v 2
the square of 4 equals 16
$ python3 prog.py 4 -v 3
16
```

除了最後一個，看上去都不錯。最後一個暴露了我們的程序中有一個 bug。我們可以通過限制 `--verbosity` 選項可以接受的值來修復它：

```python
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("square", type=int,
                    help="display a square of a given number")
parser.add_argument("-v", "--verbosity", type=int, choices=[0, 1, 2],
                    help="increase output verbosity")
args = parser.parse_args()
answer = args.square**2
if args.verbosity == 2:
    print("the square of {} equals {}".format(args.square, answer))
elif args.verbosity == 1:
    print("{}^2 == {}".format(args.square, answer))
else:
    print(answer)
```

接者是結果：

```python
$ python3 prog.py 4 -v 3
usage: prog.py [-h] [-v {0,1,2}] square
prog.py: error: argument -v/--verbosity: invalid choice: 3 (choose from 0, 1, 2)
$ python3 prog.py 4 -h
usage: prog.py [-h] [-v {0,1,2}] square

positional arguments:
  square                display a square of a given number

optional arguments:
  -h, --help            show this help message and exit
  -v {0,1,2}, --verbosity {0,1,2}
                        increase output verbosity
```

注意這一改變同時反應在錯誤信息和幫助信息裡。

現在，讓我們使用另一種的方式來改變冗長度。這種方式更常見，也和 CPython 的可執行文件處理它自己的冗長度參數的方式一致（參考 `python --help` 的輸出）：

```python
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("square", type=int,
                    help="display the square of a given number")
parser.add_argument("-v", "--verbosity", action="count",
                    help="increase output verbosity")
args = parser.parse_args()
answer = args.square**2
if args.verbosity == 2:
    print("the square of {} equals {}".format(args.square, answer))
elif args.verbosity == 1:
    print("{}^2 == {}".format(args.square, answer))
else:
    print(answer)
```

我們已經介紹過另一個操作 "count" 用來計算指定的選項參數出現的次數。

```python
$ python3 prog.py 4
16
$ python3 prog.py 4 -v
4^2 == 16
$ python3 prog.py 4 -vv
the square of 4 equals 16
$ python3 prog.py 4 --verbosity --verbosity
the square of 4 equals 16
$ python3 prog.py 4 -v 1
usage: prog.py [-h] [-v] square
prog.py: error: unrecognized arguments: 1
$ python3 prog.py 4 -h
usage: prog.py [-h] [-v] square

positional arguments:
  square           display a square of a given number

optional arguments:
  -h, --help       show this help message and exit
  -v, --verbosity  increase output verbosity
$ python3 prog.py 4 -vvv
16
```

- 是的，它現在比前一版本更像是一個標誌（和 `action="store_true"` 相似）。這能解釋它為什麼報錯。
- 它也表現得與 “store_true” 的行為相似。
- 現在來秀一下 "count" 這個動作會給予什麼。你可能之前就有見過這種用法。
- 如果你不添加 `-v` 標誌，這一標誌的值會是 `None`。
- 應該要如預期那樣，就算給予長選項我們也要獲得一樣的輸出結果。
- 可惜的是，對於我們的腳本獲得的新能力，我們的幫助輸出並沒有提供很多信息，但我們總是可以通過改善文檔來修復這一問題（比如通過 `help` 關鍵字參數）。
- 最後一個輸出暴露了我們程序中的一個 bug。

讓我們來解決問題

```python
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("square", type=int,
                    help="display a square of a given number")
parser.add_argument("-v", "--verbosity", action="count",
                    help="increase output verbosity")
args = parser.parse_args()
answer = args.square**2

# bugfix: replace == with >=
if args.verbosity >= 2:
    print("the square of {} equals {}".format(args.square, answer))
elif args.verbosity >= 1:
    print("{}^2 == {}".format(args.square, answer))
else:
    print(answer)
```

而這也正是它給的：

```python
$ python3 prog.py 4 -vvv
the square of 4 equals 16
$ python3 prog.py 4 -vvvv
the square of 4 equals 16
$ python3 prog.py 4
Traceback (most recent call last):
  File "prog.py", line 11, in <module>
    if args.verbosity >= 2:
TypeError: '>=' not supported between instances of 'NoneType' and 'int'
```

- 第一組輸出很好，修復了之前的 bug。也就是說，我們希望任何 >= 2 的值儘可能詳盡。
- 第三個輸出不是這麼的好。

我們來修復這個錯誤：

```python
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("square", type=int,
                    help="display a square of a given number")
parser.add_argument("-v", "--verbosity", action="count", default=0,
                    help="increase output verbosity")
args = parser.parse_args()
answer = args.square**2
if args.verbosity >= 2:
    print("the square of {} equals {}".format(args.square, answer))
elif args.verbosity >= 1:
    print("{}^2 == {}".format(args.square, answer))
else:
    print(answer)
```

我們剛剛引入了又一個新的關鍵字 `default`。我們把它設置為 `0` 來讓它可以與其他整數值相互比較。記住，默認情況下如果一個可選參數沒有被指定，它的值會是 `None`，並且它不能和整數值相比較（所以產生了 [`TypeError`](https://docs.python.org/zh-tw/3/library/exceptions.html#TypeError) 異常）。

而且

```python
$ python3 prog.py 4
16
```

憑藉我們目前已學的東西你就可以做到許多事情，而我們還僅僅學了一些皮毛而已。 [`argparse`](https://docs.python.org/zh-tw/3/library/argparse.html#module-argparse) 模塊是非常強大的，在結束篇教程之前我們將再探索更多一些內容。

## 進行一些小小的改進

如果我們想要擴展我們的小程式做比範例更多的事：

```python
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("x", type=int, help="the base")
parser.add_argument("y", type=int, help="the exponent")
parser.add_argument("-v", "--verbosity", action="count", default=0)
args = parser.parse_args()
answer = args.x**args.y
if args.verbosity >= 2:
    print("{} to the power {} equals {}".format(args.x, args.y, answer))
elif args.verbosity >= 1:
    print("{}^{} == {}".format(args.x, args.y, answer))
else:
    print(answer)
```

結果：

```python
$ python3 prog.py
usage: prog.py [-h] [-v] x y
prog.py: error: the following arguments are required: x, y
$ python3 prog.py -h
usage: prog.py [-h] [-v] x y

positional arguments:
  x                the base
  y                the exponent

optional arguments:
  -h, --help       show this help message and exit
  -v, --verbosity
$ python3 prog.py 4 2 -v
4^2 == 16
```

請注意到目前為止我們一直在使用詳細級別來 *更改* 所顯示的文本。 以下示例則使用詳細級別來顯示 *更多的* 文本:

```python
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("x", type=int, help="the base")
parser.add_argument("y", type=int, help="the exponent")
parser.add_argument("-v", "--verbosity", action="count", default=0)
args = parser.parse_args()
answer = args.x**args.y
if args.verbosity >= 2:
    print("Running '{}'".format(__file__))
if args.verbosity >= 1:
    print("{}^{} == ".format(args.x, args.y), end="")
print(answer)
```

結果：

```python
$ python3 prog.py 4 2
16
$ python3 prog.py 4 2 -v
4^2 == 16
$ python3 prog.py 4 2 -vv
Running 'prog.py'
4^2 == 16
```

### 矛盾的選項

到目前為止，我們一直在使用 [`argparse.ArgumentParser`](https://docs.python.org/zh-tw/3/library/argparse.html#argparse.ArgumentParser) 實例的兩個方法。 讓我們再介紹第三個方法 `add_mutually_exclusive_group()`。 它允許我們指定彼此相互衝突的選項。 讓我們再更改程序的其餘部分以便使用新功能更有意義：我們將引入 `--quiet` 選項，它將與 `--verbose` 正好相反:

```python
import argparse

parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group()
group.add_argument("-v", "--verbose", action="store_true")
group.add_argument("-q", "--quiet", action="store_true")
parser.add_argument("x", type=int, help="the base")
parser.add_argument("y", type=int, help="the exponent")
args = parser.parse_args()
answer = args.x**args.y

if args.quiet:
    print(answer)
elif args.verbose:
    print("{} to the power {} equals {}".format(args.x, args.y, answer))
else:
    print("{}^{} == {}".format(args.x, args.y, answer))
```

我們的程序現在變得更簡潔了，我們出於演示需要略去了一些功能。 無論如何，輸出是這樣的:

```python
$ python3 prog.py 4 2
4^2 == 16
$ python3 prog.py 4 2 -q
16
$ python3 prog.py 4 2 -v
4 to the power 2 equals 16
$ python3 prog.py 4 2 -vq
usage: prog.py [-h] [-v | -q] x y
prog.py: error: argument -q/--quiet: not allowed with argument -v/--verbose
$ python3 prog.py 4 2 -v --quiet
usage: prog.py [-h] [-v | -q] x y
prog.py: error: argument -q/--quiet: not allowed with argument -v/--verbose
```

這應該很容易理解。 我添加了末尾的輸出這樣你就可以看到其所達到的靈活性，即混合使用長和短兩種形式的選項。

在我們結論之前，你可能想告訴你的用戶這個程式的主要目的，以防萬一他們不知道：

```python
import argparse

parser = argparse.ArgumentParser(description="calculate X to the power of Y")
group = parser.add_mutually_exclusive_group()
group.add_argument("-v", "--verbose", action="store_true")
group.add_argument("-q", "--quiet", action="store_true")
parser.add_argument("x", type=int, help="the base")
parser.add_argument("y", type=int, help="the exponent")
args = parser.parse_args()
answer = args.x**args.y

if args.quiet:
    print(answer)
elif args.verbose:
    print("{} to the power {} equals {}".format(args.x, args.y, answer))
else:
    print("{}^{} == {}".format(args.x, args.y, answer))
```

請注意用法文本中有細微的差異。 注意 `[-v | -q]`，它的意思是說我們可以使用 `-v` 或 `-q`，但不能同時使用兩者：

```python
$ python3 prog.py --help
usage: prog.py [-h] [-v | -q] x y

calculate X to the power of Y

positional arguments:
  x              the base
  y              the exponent

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose
  -q, --quiet
```

