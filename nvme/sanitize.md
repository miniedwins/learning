# sanitize



## 基本介紹

主要的功能就是清除 NAND Flash 資料，支援三個操作類型 : `Block Erase`、`Overwrite`、`Crypto Erase`。

所有的操作類型都在背景運行，我們可以在執行的途中或是完成的時候，透過 `Sanitize Status Log` 來檢查執行的進度或是狀態。

* `Block Erase` : 清除所有物理上 Block 資料，一旦被清除就無法再恢復資料
* `Overwrite` : 使用特定資料格式去複寫現有已存在的資料
* `Crypto Erase` : 通過刪除密鑰的方式讓資料無法再被識別，因為沒有金鑰就無法取得真正的資料內容

**當命令 (Sanitize) 開始運作的時候，控制器需要有以下動作 :** 

* 清除任何一個事件 *(備註 : 還不太了解事件如何處理)*
  * Sanitize Operation Completed asynchronous event
  * Sanitize Operation Completed With Unexpected Deallocation asynchronous event
* 將目前執行的狀態更新到日誌中
  * *Reference : Sanitize Status log*
* 忽略任何一個已提交過的命令或是正在執行的時候所收到的命令 
  * *Reference : Sanitize Command Restrictions(內容較多，不花時間閱讀)*
* 終止正在執行的自檢 (self-test) 操作
* 暫時停止 `APST` Management，避免執行過程中進入到省電模式
* Shall release stream identifiers for any open streams.
  * *備註 : 暫時還不清楚解原文說明*

**下列的動作控制器會中止任何一個 Sanitize command** 

* If controller unsupported Sanitize command
  * Controller shall abort the command with a status of Invalid Field in Command.
* If any Persistent Memory Region (PMR) is enabled
  * Controller shall abort any Sanitize command with a status of Sanitize Prohibited.
* If a firmware activation with reset is pending
  * *備註 : 不是很了解原文所表達的狀態說明 (reset status after commit action?)*
* Activation of new firmware is prohibited during a sanitize operation



## 檢查控制器支援

說明 : 發送 **Identify Controller** 命令來確認是否支援 `Sanitize` 模式。

Controller Attributes (CTRATT) :

* 331:328 Bytes :  Sanitize Capabilities (SANICAP)
  * `Bit0 (value=1)` : Crypto Erase Support 
  * `Bit1 (value=1)` : Block Erase Support 
  * `Bit2 (value=1)` : Overwrite Support

執行命令 : 

~~~shell
nvme id-ctrl /dev/nvme0 | grep sanicap
# sanicap : 0x3 (代表支援三個 Erase Mode)
~~~



## 如何執行 Sanitize

說明 : 使用 Block Erase 清除使用者資料

執行命令 : 

~~~shell
# Block Erase
nvme sanitize -a 0x02 /dev/nvme0
~~~



## 查看 Sanitize 日誌

說明 : 

執行命令 : 

~~~shell
nvme sanitize-log /dev/nvme0
~~~





