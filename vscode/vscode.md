# VSCode

# 設定說明 (Setting)

`User Setting` :  代表全域的設定

`Workspace Setting` : 代表個人目錄的設定 (檔案設定後會放在 .vscode 資料夾)

`Note` : 當兩個設定檔有重複的時候，`Workspace setting` 會覆蓋 `User Setting`



## setting.json

### User Setting

~~~shell
 // Window
"window.zoomLevel": 1, 					// 視窗縮放
 
 // Editor
 "editor.fontSize": 22,					// 字體大小
 "editor.fontFamily": "Fira Code Light",		// 設定字型
 "editor.fontWeight": "500",				// 字體寬度
 "editor.fontLigatures": true				// 開啟連字號 (ex: => 變成箭頭)
 "editor.formatOnSave": true, 				// 儲存時，自動排版
 "editor.lineHeight": 26,				// 每個行之間的上下高度
 "editor.renderIndentGuides": true			// 顯示縮排線

 // Files
 "files.autoSave": "onFocusChange", 			// 離開視窗焦點時自動儲存
 "files.encoding": "utf8",				// 預設編碼格式
 "files.trimTrailingWhitespace": true,			// 儲存後，會將多餘的空白去除
 "files.autoGuessEncoding": false, 			// 自動猜測檔案的編碼
 "files.defaultLanguage": "markdown" 			// 設定預設文件語言類型 ( VS Code 當作預設的 Markdown 編輯器)
 
 // git
 "git.autofetch": true 					// VSCode 在背景自動執行 git fetch
 "git.enableSmartCommit": true				// 如果所有變更都還沒有 git add ( Stage ) 的話
 							// 預設會自動全部 Commit，不會再先問過。
 "git.confirmSync": false 				// 當要同步 Git 遠端儲存庫時，不需要再提問
 
 // Terminal
 "terminal.integrated.fontSize": 30, 			// terminal 字體大小
 "terminal.integrated.shell.windows": 			// 指定使用哪種終端機 (cmd or powershell)
 "C:\\WINDOWS\\System32\\cmd.exe",
 "C:\\Windows\\sysnative\\WindowsPowerShell\\v1.0\\powershell.exe",
 
  // SSH Remote (remote ssh package)
 "remote.SSH.remotePlatform": {				// 遠端連線位址
        "192.168.88.94": "linux",
        "192.168.88.73": "linux"
 },

 // Extensions
 "extensions.ignoreRecommendations": false,		// 是否忽略建議套件
 "extensions.autoCheckUpdates": true,			// 自動確認新的版本

 // Theme and Icon
 "workbench.colorTheme": "Cobalt2",			// 主題
 "workbench.iconTheme": "material-icon-theme",		// 圖示
 "workbench.welcome.enabled": false, 			// 歡迎的顯示頁面
 "workbench.editor.enablePreview": false,
~~~

### Workspace Setting

#### Python

~~~shell
// VS Code 左下角可以自由調整，會將自動調整這個設定值
"python.pythonPath": 								// 設定 "env" or "real env" python 執行檔
"C:\\Users\\edwin\\work\\venv\\venv_demo\\Scripts\\python.exe",
"C:\\Users\\copol\\AppData\\Local\\Programs\\Python\\Python38\\python.exe",

"python.venvPath": "C:\\Users\\edwin\\work\\venv",				// 設定你放全部的 venvs 環境的根目錄資料夾
"python.terminal.activateEnvironment": true,					// 自動啟動 env 環境

// Auto Import (ImportMagic Package)
// 需要指定官方、第三方，以及自己的函式庫路徑
// 指定好路徑儲存後，該套件會自動掃描 (時間會比較久)
"python.autoComplete.extraPaths" : ["C:\\wrokspace\\python\\"],			// 自動導入套件	
"python.autoComplete.addBrackets": true,					// 自動補括號
 
// pylint
"python.linting.pylintEnabled": true,  							
"python.linting.enabled": true,					
~~~

**TestExplorer**

~~~shell
"pythonTestExplorer.testFramework": "pytest", 					// 指定測試模組
"testExplorer.hideEmptyLog": true, 						// 輸出為空字串時，顯示空的日誌
"testExplorer.codeLens": true,
~~~

**Python Testing**

~~~shell
"python.testing.unittestEnabled": false,					// 不啟用 Unittest
"python.testing.nosetestsEnabled": false,					// 不啟用 nosetest
"python.testing.pytestEnabled": true, 						// 啟用 pytest

// 這個參數可能會覆蓋 pytest.ini，暫時先使用 pytest.ini
// TestExpoler and PytTesting (Debug mode: 會共用這個參數)
"python.testing.pytestArgs": ["-s", "-v", "test_script"]	 		// pytest 額外參數設定

"python.testing.autoTestDiscoverOnSaveEnabled": false,				// 儲存一個測試檔案後，會自動運行測試項目
~~~



## task.json

* tasks :
  * `label` : 任務列表中看到的的名稱
  * `type` : 任務的類型，可以是 shell 或是 process
    * `shell` :  若是設定 shell，command 選項需要指定檔案路徑
    * `process` : 執行檔名稱
  * `command` : 執行的實際命令 (ex. python, gcc)
  * `args` (list) : 傳遞給程式的命令參數 

## launch.json

* configurations : 設定檔
  * `name` (string) : 偵錯列表中看到的的名稱
  * `type` (string) : 執行偵錯的程式語言
  * `request` (string) : 啟動執行的方式
    * `test` :  單元測試
    * `launch` :  除錯模式
    * `attach` : 使用在網路方面 (暫時用不到)
  * `program` (string) : 指定要偵錯的檔案名稱以及路徑
    * `${file} ` : 目前程式所開啟的檔案名稱
    * `${workspaceFolder}` : 目前的檔案路徑 
  * `cwd` (string) : 偵錯模式時的工作目錄
  * `args` (list) :  傳遞給程式的命令參數，若是沒有參數可以留空
  * `justMyCode` (bool) : 偵錯模式時，單步執行可以進入原始碼
  * `stopOnEntry` (bool) : 程式執行第一行的時候就想要進入偵錯
  * `internalConsoleOptions` (string) : 每次進入偵錯時都會開啟偵錯主控台視窗
    * `openOnSessionStart` : 開啟
    * `neverOpen` : 永不開啟
  * `console` (string) : 要啟用哪一個控制台
    * `integratedTerminal` :   執行在偵錯主控台中 Terminal 視窗
    * `externalTerminal ` :  執行的過程中會獨立開啟另外一個 Terminal 視窗介面

# 設定檔案 (Example)

## task.json

### C/C++

~~~shell
{
    "version": "2.0.0",
    "tasks": [
        {
            "type": "cppbuild",
            "label": "C/C++: gcc.exe build active file",
            "command": "C:\\MinGW\\bin\\gcc.exe",
            "args": [
                "-g",
                "${file}",
                "-o",
                "${fileDirname}\\${fileBasenameNoExtension}.exe"
            ],
            "options": {
                "cwd": "C:\\MinGW\\bin"
            },
            "problemMatcher": [
                "$gcc"
            ],
            "group": "build",
            "detail": "compiler: C:\\MinGW\\bin\\gcc.exe"
        }
    ]
}
~~~

說明 : 

`command` : 編譯出來的exe檔名和原始檔一樣

`problemMatcher` :  使用 `gcc` 捕獲錯誤



### Python

~~~shell
{
    "version": "2.0.0",
    "tasks": [
        {
            "label": "python task",
            "type": "process",
            "command": "python",
            "args": ["'${file}'"]
        }
    ]
}
~~~



### Golang

~~~shell
~~~



### Shell

~~~shell
~~~





## launch.json

### C/C++

~~~shell
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "gcc.exe - build and debug",
            "type": "cppdbg",
            "request": "launch",
            "program": "${fileDirname}\\${fileBasenameNoExtension}.exe",            
            "args": [],
            "stopAtEntry": true,            
            "cwd": "${workspaceFolder}",
            "environment": [],
            "externalConsole": false,
            "MIMode": "gdb",
            "miDebuggerPath": "C:\\MinGW\\bin\\gdb.exe",
            "setupCommands": [
                {
                    "description": "Enable pretty-printing for gdb",
                    "text": "-enable-pretty-printing",
                    "ignoreFailures": true
                }
            ],
            "preLaunchTask": "C/C++: gcc.exe build active file"
        }
    ]
}
~~~

說明 : 

* `program` : 指定偵錯的執行檔名稱
* `stopAtEntry` : 啓動偵錯時在`main`方法上停止 (停留在第一行)
* `cwd` : 編譯後的檔案會放在這個指定的工作目錄上 (沒有設定指定的目錄，程式會報錯誤訊息)
* `MIMode` : 指示VS程式碼將連線到的偵錯程式。 必須設定為`gdb`或`lldb`。
* `miDebuggerPath` :  安裝 `MinGW` 的路徑相符
* `externalConsole` : 指定是否需要開啟外部控制台 
* `preLaunchTask` : 
  * 啓動前要執行的任務前，會自動先編譯主程式 (確保 `task.json` 檔案標籤設定一致)
  * 如果不設定，執行偵錯前必須先手動執行編譯主程式，等編譯完後再執行偵錯



### Python

~~~shell
{
	"version": "0.2.0",
    "configurations":[
        {
            "name": "python debug",
            "type": "python",
            "request": "launch",
            "cwd": "${workspaceFolder}",
			"program": "${file}",
            "justMyCode": false,
            "console": "integratedTerminal"
        },
        {
            "name": "pytest",
            "type": "python",
            "request": "test",
            "justMyCode": false,
            "console": "integratedTerminal"
        }
    ]
}
~~~

# 變數說明 (File)

- **${workspaceFolder}** - 當前工作目錄(根目錄)

  - /home/your-username/your-project

- **${workspaceFolderBasename}** - 當前工作資料夾的父目錄

  - your-project
  
- **${file}** - 當前打開的檔案名稱(完整路徑)

  - /home/your-username/your-project/folder/file.txt 

- **${relativeFile}** - 當前根目錄到當前打開檔案的相對路徑(包括檔案名稱)

  - folder/file.txt
  
- **${relativeFileDirname}** - 當前根目錄到當前打開檔案的相對路徑(不包括檔案名稱)

  - folder
  
- **${fileBasename}** - 當前打開的檔案名稱(包括副檔名)

  - file.txt
  
- **${fileBasenameNoExtension}** - 當前打開的檔案名稱(不包括副檔名)

  - file

- **${fileDirname}** - 當前打開檔案的目錄名稱

  - /home/your-username/your-project/folder

  

- **${fileExtname}** - 當前打開檔案的副檔名

  - .ext

