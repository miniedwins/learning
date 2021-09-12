# Git 基本設定



## 初始化前設定

* git config --global user.name "your name"
* git config --global user.email "your e-mail"
* git config --global color.ui true



## 建立 SSH 連線

產生金鑰

~~~shell
ssh-keygen -t rsa -b 4096 -C "your e-mail"
~~~

拷貝公鑰內容 並且上傳公鑰至 GitHub

**Github > Settings > SSH and GPG keys >  New SSH Key > add your public ssh keys**

~~~shell
cd ~/.ssh
cat id_rsa.pub
~~~



## 設定命令縮寫 (alias)

**命名方法**

* git config --global alias.[name] [command_name]

**常用命名縮寫**

* git config --global alias.cm commit
* git config --global alias.co checkout
* git config --global alias.br branch
* git config --global alias.st status
* git config --global alias.lg 'log --oneline --graph'

**檢查設定檔** 

* git config -l

# 常用命令 

## 遠端數據庫操作



### 更新遠端數據庫

`-u` : 預設會將資料推送到遠端數據庫

`origin` : 遠端數據庫名稱

將本地端的資料推送一份到遠端 `origin`節點，並生成一個 `master`分支

~~~shell
$ git push -u origin master:master
~~~

### 建立遠端數據庫節點

~~~shell
$ git remote add origin "your git website project"
~~~

### 顯示遠端數據庫節點

~~~shell
$ git remote -v
origin  https://github.com/miniedwins/nvme-cli.git (fetch)
origin  https://github.com/miniedwins/nvme-cli.git (push)
upstream        https://github.com/linux-nvme/nvme-cli.git (fetch)
upstream        https://github.com/linux-nvme/nvme-cli.git (push)
~~~

### 顯示本地與遠端所有分支

~~~shell
$ git br -a
* master
  remotes/origin/1.11-stable
  remotes/origin/HEAD -> origin/master
  remotes/origin/integration-libnvme
  remotes/origin/libnvme-int-3.4.2021
  remotes/origin/master
  remotes/upstream/1.11-stable
  remotes/upstream/integration-libnvme
  remotes/upstream/libnvme-int-3.4.2021
  remotes/upstream/master
~~~

# 操作範例 : 

## 如何下載遠端分支

git clone 並不會將建立遠端分支，所以從本地端看不到其它分支

~~~shell
$ git br -l
* master
~~~

顯示遠端所有的分支

星星 (*) : 代表目前本地端所在分支

~~~shell
$ git br -a
* master
  remotes/origin/HEAD -> origin/master
  remotes/origin/dev
  remotes/origin/master
~~~

取遠端數據庫的分支，建立本地端數據庫的分支

~~~shell
$ git br dev remotes/origin/dev
Branch 'dev' set up to track remote branch 'dev' from 'origin'.
~~~

然後檢查目前本地端的分支

~~~shell
$ git br -l
  dev
* master
~~~



## 如何刪除遠端分支

首先顯示遠端分支名稱

~~~shell
$ git br -a
  dog
* main
  remotes/origin/HEAD -> origin/main
  remotes/origin/circleci-project-setup
  remotes/origin/dog
  remotes/origin/main
~~~

找到刪除遠端分支的名稱

~~~shell
git push origin :circleci-project-setup
~~~

結果顯示

~~~shell
$ git push origin :circleci-project-setup
To https://github.com/miniedwins/foo-cli.git
 - [deleted]         circleci-project-setup
~~~



## 修改已提交的紀錄

說明 : 已經提交的 commit 想要再補充解釋，但是只想要修改 commit 訊息

備註 : `--amend`  參數只能處理最後一次

修改前 :

~~~shell
$ git log --oneline
3e7a7a2 (HEAD -> master, origin/master, origin/HEAD) update README.md
0782f7e init
~~~

執行 --amend

~~~shell
$ git commit --amend -m "study --amend command"
[master fd5824c] study --amend command
 Author: miniedwins <miniedwins@gmail.com>
 Date: Thu May 20 14:18:46 2021 +0800
 1 file changed, 1 insertion(+)
~~~

修改後 : 

~~~shell
$ git log --oneline
fd5824c (HEAD -> master) study --amend command
0782f7e init
~~~



## 同步原作專案進度

先建立原作專案節點

~~~shell
$ git remote add upstream https://github.com/linux-nvme/nvme-cli.git
~~~

顯示目前的節點

`origin` 從原作專案 Fork 到自己的本地專案節點

`upstream` 原作專案節點

~~~shell
$ git remote -v
origin  https://github.com/miniedwins/nvme-cli.git (fetch)
origin  https://github.com/miniedwins/nvme-cli.git (push)
upstream        https://github.com/linux-nvme/nvme-cli.git (fetch)
upstream        https://github.com/linux-nvme/nvme-cli.git (push)
~~~

取得原作專案最新版的內容

~~~shell
$ git fetch upstream
From https://github.com/linux-nvme/nvme-cli
 * [new branch]      1.11-stable          -> upstream/1.11-stable
 * [new branch]      integration-libnvme  -> upstream/integration-libnvme
 * [new branch]      libnvme-int-3.4.2021 -> upstream/libnvme-int-3.4.2021
 * [new branch]      master               -> upstream/master
~~~

如果遠端資料與本地端不一樣，就會同步更新 (三種不同的更新方法)

~~~shell
# git pull = fetch + merge upstream/master
git pull upstream master 
git merge upstream/master
git rebase upstream/master
Already up to date.
~~~

然後再推回去自己的專案內容，保持自己本地端 `Fork` 的內容與專案同步

~~~shell
$ git push origin master
Everything up-to-date
~~~



## 如何移動分支標籤

~~~shell
$ git l
384ea2f (HEAD -> feature) update README.md
599f220 update main.py file
74eee63 add main.py file
4245a5b add f1, f2, f3
100a5c9 add m3
14624ca add m2
533800c add m1
3381c06 init

~~~

將標籤指向別的 commit 物件

~~~shell
$ git br -f master 3381c06
~~~

此時分支標籤的位置就會被更改了

~~~shell
$ git l
384ea2f (HEAD -> feature) update README.md
599f220 update main.py file
74eee63 add main.py file
4245a5b add f1, f2, f3
100a5c9 add m3
14624ca add m2
533800c add m1
3381c06 (master) init
~~~



## 如何使用標籤 (Tag)

### 新增標籤

* `-a` 標籤名稱 
* `-m` 標籤說明

~~~shell
git tag -a v1.0.1 -m "Relase v1.0.1"
~~~

### 刪除標籤

**-d** :  標籤名稱

~~~shell
$ git tag -d v1.0.1
Deleted tag 'v1.0.1' (was 734dfeb)
~~~

### 列出既有標籤

~~~shell
$ git tag -l
v1.0.0
v1.0.1
~~~

### 上傳標籤到遠端

~~~shell
$ git push origin v1.0.1
Enumerating objects: 1, done.
Counting objects: 100% (1/1), done.
Writing objects: 100% (1/1), 161 bytes | 161.00 KiB/s, done.
Total 1 (delta 0), reused 0 (delta 0), pack-reused 0
To https://github.com/miniedwins/foo.git
 * [new tag]         v1.0.1 -> v1.0.1
~~~



## 清空工作目錄

新增檔案，並且沒有被 Git 列入追蹤的狀態有效

* `git clean -f`  清空工作目錄
* `git clean -n`  顯示會被清空的資料
