# sanitize



## 基本介紹

主要的功能就是清除 NAND Flash 資料，支援三個操作類型 : `Block Erase`、`Overwrite`、`Crypto Erase`。所有的操作類型都在背景運行，我們可以在執行的途中或是完成後，透過 `Sanitize Status Log` 來檢查執行的進度或是狀態。

* `Block Erase` : 清除所有物理上 Block 資料，一旦被清除就無法再恢復資料
* `Overwrite` : 使用特定資料格式去複寫現有已存在的資料
* `Crypto Erase` : 通過刪除密鑰的方式讓資料無法再被識別，因為沒有金鑰就無法取得真正的資料內容

**當命令 (Sanitize) 開始運作的時候，控制器需要有以下動作 :** 

* 清除任何一個事件 *(備註 : 目前還不是很熟悉事件處理的機制)*
  * Sanitize Operation Completed asynchronous event
  * Sanitize Operation Completed With Unexpected Deallocation asynchronous event
* 將目前執行的狀態更新到日誌中
  * *Reference : Sanitize Status log*
* 忽略任何一個已提交過的命令或是正在執行的時候所收到的命令 
  * *Reference : Sanitize Command Restrictions (備註 : 內容較多，不花時間閱讀)*
* 終止正在執行的自檢 (self-test) 操作
* 暫時停止 `APST` Management，避免執行過程中進入到省電模式
* Shall release stream identifiers for any open streams. *(備註 : 目前還不清楚 streams)*

**控制器會中止任何一個 Sanitize command，動作如下** 

* If controller unsupported Sanitize command
  * (原文) Controller shall abort the command with a status of Invalid Field in Command.
  * (說明) 控制器若是不支援 Sanitize 命令，當收到命令後，控制器會回覆一個不是有效的命令
* If any Persistent Memory Region (PMR) is enabled
  * (原文) Controller shall abort any Sanitize command with a status of Sanitize Prohibited.
  * (說明) 當啟用 PMR 功能，Sanitize 操作會被禁止使用
* If a firmware activation with reset is pending
  * *備註 : 不太清楚原文表達 reset 的狀態說明*
* Activation of new firmware is prohibited during a sanitize operation



## 檢查控制器支援

說明 : 發送 **Identify Controller** 命令來確認支援哪幾種模式。

Controller Attributes (CTRATT) :

* 331:328 Bytes :  Sanitize Capabilities (SANICAP)
  * `Bit0 (value=1)` : Crypto Erase Support 
  * `Bit1 (value=1)` : Block Erase Support 
  * `Bit2 (value=1)` : Overwrite Support

![](https://github.com/miniedwins/learning/blob/main/nvme/pic/identify_controller/Identify_Controller_SANICAP_Bit0_Bit1_Bit2.png)

執行命令 : 

~~~shell
nvme id-ctrl /dev/nvme0 | grep sanicap
# sanicap : 0x3
~~~



## 如何執行 Sanitize

說明 : 使用 `Block Erase` 模式清除使用者資料。

備註 : `Sanitize` 是運作在背景下執行，所以執行後必須要取得日誌內容，才可以確認成功或是失敗。

![](https://github.com/miniedwins/learning/blob/main/nvme/pic/admin_command_set/sanitize_cmd_dw10.png)

![](https://github.com/miniedwins/learning/blob/main/nvme/pic/admin_command_set/sanitize_cmd_dw11.png)

執行命令 : 

~~~shell
# Block Erase
nvme sanitize -a 0x02 /dev/nvme0
~~~



## 查看 Sanitize 日誌

說明 : 當控制器執行 `Sanitize` 命令後 ，就可以透過日誌可以清楚的了解執行的狀態。

日誌解釋 :

* Sanitize Progress : 表示執行的進度
  * 01:00 Bytes
    * 執行過程中，該值會持續變動到命令執行完成，最後該值為變成 `65535` or `0xFFFFh`
    * 可以從每次日誌所取得值，計算執行進度，如下計算方法 : 
      * 第一次執行 : (3761 / 65535) x 100 = `5.7%`
      * 第二次執行 : (32754 / 65535) x 100 = `49.9%`
      * 第三次執行 : (65535 / 65535) x 100 = `100%`
* Sanitize Status : 表示執行狀態
  * 03:02 Bytes 
    * 第一次執行 : `0x02` (表示 : 目前正在操作 Sanitize)
    * 第二次執行 : `0x02` (表示 : 目前正在操作 Sanitize)
    * 第三次執行 : `0x101`
      * 7:0 Bits : `0x01` (表示 : Sanitize 操作成功)
      * 15:8 Bits : `0x01` 
        * NS 沒有任何資料被寫入，可以解釋資料已被清空
        * PMR 功能沒有被啟用
    * 如果該值是 : `0x03` (表示 : Sanitize 操作失敗)
* Sanitize Command Dword 10 Information :

執行命令 : 

~~~shell
nvme sanitize-log /dev/nvme0
~~~

第一次執行的結果

~~~shell
Sanitize Progress                      (SPROG) :  3761
Sanitize Status                        (SSTAT) :  0x2
Sanitize Command Dword 10 Information (SCDW10) :  0x2
Estimated Time For Overwrite                   :  4294967295 (No time period reported)
Estimated Time For Block Erase                 :  4294967295 (No time period reported)
Estimated Time For Crypto Erase                :  4294967295 (No time period reported)
Estimated Time For Overwrite (No-Deallocate)   :  0
Estimated Time For Block Erase (No-Deallocate) :  0
Estimated Time For Crypto Erase (No-Deallocate):  0
~~~

第二次執行的結果

~~~shell
Sanitize Progress                      (SPROG) :  32754
Sanitize Status                        (SSTAT) :  0x2
Sanitize Command Dword 10 Information (SCDW10) :  0x2
Estimated Time For Overwrite                   :  4294967295 (No time period reported)
Estimated Time For Block Erase                 :  4294967295 (No time period reported)
Estimated Time For Crypto Erase                :  4294967295 (No time period reported)
Estimated Time For Overwrite (No-Deallocate)   :  0
Estimated Time For Block Erase (No-Deallocate) :  0
Estimated Time For Crypto Erase (No-Deallocate):  0
~~~

第三次執行的結果

~~~shell
Sanitize Progress                      (SPROG) :  65535
Sanitize Status                        (SSTAT) :  0x101
Sanitize Command Dword 10 Information (SCDW10) :  0x2
Estimated Time For Overwrite                   :  4294967295 (No time period reported)
Estimated Time For Block Erase                 :  4294967295 (No time period reported)
Estimated Time For Crypto Erase                :  4294967295 (No time period reported)
Estimated Time For Overwrite (No-Deallocate)   :  0
Estimated Time For Block Erase (No-Deallocate) :  0
Estimated Time For Crypto Erase (No-Deallocate):  0
~~~





