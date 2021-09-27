# pip 套件使用方法



## 使用說明

* pip 用來管理 python 2.x 用的 package，而 pip3 用來管理 python 3.x 用的 package
* 各自獨立，pip 升級不會變成 pip3，要裝 pip3 也不需要先有 pip

##   操作命令 

* 說明 : 
  * Windows 可以直接使用 pip 安裝套件
  * Ubuntu 需要先指定安裝 python3-pip

* `安裝` : 
  
  * pip install packages
  * pip install -v  package==1.0 (指定套件版本)
  
* `不同版本安裝` :

  * 說明

    * `Python` 版本都有自己的 `site-packages`，使用哪個版本開發，就要用該版本安裝套件

      以避免不同 `Python`版本切換，而無法使用套件 。

  * 指定 `Python`版本安裝套件 : 

    * 當前的使用者可以使用 (安裝在 `/home/user`)
      * /usr/bin/python3.x.x -m pip install package --user
        * /home/edwin/.local/bin/flask
        * /home/edwin/.local/lib/python3.8/site-packages/flask
    * 所有使用者可以使用 (安裝在 `/usr/local`)
      * sudo /usr/bin/python3.x.x -m pip install  package
        * /usr/local/bin/flask
        * /usr/local/lib/python3.8/dist-packages/flask

* `更新` : pip install --upgrade package

* `更新 PIP` : 
  
  * `Ubuntu` : python -m pip install --upgrade pip 
  * `Windows` : python.exe -m pip install --upgrade pip
  
* `移除` : pip uninstall package

* `查看版本` : pip -version

* `查看已安裝套件` :  pip list



## 如何建立套件清單

PIP / PIP3 安裝很多套件(Library)，但是要移植到其它機器上 (避免升級造成程式問題)，可以使用 requirements.txt 來限定套件與版本 。

~~~shell
pip freeze > requirements.txt
~~~



## 如何安裝多個套件

需要先建立 `requirements` 套件清單才可以安裝，使用在團體共享開發或是建立其它環境中使用

```bash
pip install -r requirements.txt 
```



---

# pipenv 虛擬環境



## 如何建立虛擬環境

### 安裝套件

~~~bash
pip install pipenv
~~~

### 建立虛擬環境

~~~bash
# 建立pipenv資料夾
mkdir pipenv

# 進入pipenv資料夾
cd pipenv

# 當前目錄下會產生 "Pipfile" and "Pipfile.lock"
pipenv --python 3
pipenv install --python 3.6.5  更精確的指定版本

# 建立完成後會產生 Virtualenv location :
# C:\Users\copol\.virtualenvs\pipenv-LAdtM08T 
# 存放所有虛擬環境套件的地方
~~~

### 查看虛擬環境目錄

~~~shell
pipenv --venv
~~~

輸出結果 : 

~~~shell
# 在虛擬環境下安裝的套件，都會安裝到此目錄中
C:\Users\copol\.virtualenvs\pipenv-LAdtM08T
~~~



## 虛擬環境操作方法

### 如何進入到虛擬環境

在當前的虛擬環境目錄下執行

~~~shell
pipenv shell
~~~

輸出結果 : 

前端會顯示類似這樣的字串，代表已進入虛擬環境中

~~~shell
(pipenv-LAdtM08T) D:\pipenv>
~~~



### 安裝套件

建立虛擬環境完成後，Pipenv 會自動產生一個 Pipfile，用來記錄所安裝的套件

**安裝命令** : 

* pipenv install your-packags (for packages)
* pipenv install --dev your-packags (dev-package)

下面是 `Pipfile` 內容

~~~bash
[[source]]
name = "pypi"
url = "https://pypi.org/simple"
verify_ssl = true

[dev-packages]	# 開發中安裝套件
pytest = "*"

[packages]		# 部署用的套件
flask = "*"

[requires]
python_version = "3.8"
~~~



### 查看安裝套件

~~~bash
# 透過 pipenv shell 進入虛擬環境
pipenv shell

# pipenv shell 環境下，就可以找到剛剛安裝的套件 flask
pip list
~~~



### 顯示套件相依性

~~~bash
pipenv graph
pipenv graph --bare #最小輸出(雖然官方文檔這樣寫，但實際上會輸出所有的套件)
pipenv graph --json #用json格式輸出
pipenv graph --reverse #內外翻轉輸出
~~~



### 如何在虛擬環境中運行程式

建立一個檔案在虛擬環境目錄中 (在該環境中安裝 `requests`)

~~~python
import requests
print("Hello World")
~~~

虛擬環境下執行的結果 : 

~~~shell
D:\pipenv>pipenv run python main.py
Hello World
~~~

真正環境下執行的結果 : 

* 一切安裝的套件都在虛擬環境中，而真實環境並沒有安裝 `requests` 套件

* 因為沒有安裝套件 `requests`，所以會回報錯誤訊息

~~~shell
D:\pipenv>python main.py
Traceback (most recent call last):
  File "main.py", line 1, in <module>
    import requests
ModuleNotFoundError: No module named 'requests'
~~~



### 團隊內項目共享

**複製團隊內的 pipfile**

 如果不想安裝 (dev-packages)，拿掉 `--dev` 參數

~~~bash
# 安裝部署 (packages)
# 開發 (dev-packages)
pipenv install --dev

# 安裝完成後進入虛擬環境
pipenv shell

# 檢查剛剛安裝的套件
pip list
~~~



### 刪除虛擬環境

執行刪除命令

~~~bash
pipenv --rm
~~~

輸出結果 

~~~shell
Removing virtualenv (C:\Users\copol\.virtualenvs\pipenv2-xlLQpVLn)
~~~



## 解決 VS Code 無法登入虛擬環境

使用 `PowerShell ` 執行下列命令 : 

~~~shell
Set-ExecutionPolicy RemoteSigned
~~~

輸出結果 :

~~~shell
執行原則變更
執行原則有助於防範您不信任的指令碼。如果變更執行原則，可能會使您接觸到 about_Execution_Policies 說明主題 (網址為
https:/go.microsoft.com/fwlink/?LinkID=135170) 中所述的安全性風險。您要變更執行原則嗎?
[Y] 是(Y)  [A] 全部皆是(A)  [N] 否(N)  [L] 全部皆否(L)  [S] 暫停(S)  [?] 說明 (預設值為 "N"): y
~~~

