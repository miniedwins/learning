# Device self-test



## 基本介紹

裝置自檢 (self-test)，主要定義一系列 SSD 自我檢測的驗證項目，但是內部實現的測試方法是由廠商自定義。

這邊要注意的是，當前 SSD 若是正在運行自檢期間，如果控制器收到任何命令，應進行下列動作 :

* suspend the device self-test operation  (暫停目前的自檢操作)
* process and complete that command (處理收到的命令，並完成命令執行)
* resume the device self-test operation (回到剛剛自檢的操作項目)

> 備註 : 另外控制器若是沒有自檢，可能會造成效能降低的問題。

**Example Device Self-test Operation (Informative)**

![](https://github.com/miniedwins/learning/blob/main/nvme/pic/device_self_test_informative.png)



## 自檢類型

### short device self-test

* 一個自檢測試 (short self-test) 必須要在兩分鐘內或是更少的時間完成測試
* 自檢的進度與測試的情況，可以從 Device Self-Test 日誌取得資訊內容

### extended device self-test

* 一個自檢測試 (extended self-test) 會依據 EDSTT 所指定的時間內完成測試
  * EDSTT : Extended Device Self Test Time (單位 : 分鐘)
* 檢測進度與測試的情況，可以從 Device Self-Test 日誌取得資訊內容

**當自檢 (Extended Self-Test) 時發生 Controller Level Reset，應當會有下列的運作行為 :**

* 控制器重置或是任何電源重新上斷電執行完成後，需要回到先前自檢的操作
* 回到先前自檢未完成的操作項目，這部份可以由廠商定義
* 未完成的操作項目，應當重新清除，然後再重新測試

**什麼命令會中斷自檢動作 :**

* shall be aborted by **a Format NVM**
  * 收到 Format NVM 命令
* shall be aborted when **a sanitize operation is started**
  * 已經開始執行 Sanitize 操作
* shall be aborted if a Device Self-test command with the **Self-Test Code field set to Fh** is processed
  * 發送 device self-test 命令，需要設定 **STC** 欄位參數，它是用來設定哪個測試類型 (e.g., short, extended, and stop)
  * 若是被設定成 **0xFh**，代表是停止自檢測試
* may be aborted if the specified **namespace is removed** from the namespace inventory.
  * 若是指定的 Namespace 已經被控制器移除

**Format NVM command Aborting a Device Self-Test Operation**

![](https://github.com/miniedwins/learning/blob/main/nvme/pic/device_self_test_aborting_operation.png)



## 自檢說明

### DRAM Check

DRAM 作用是來做資料的緩存，或許會存放了部分代碼和重要的數據，所以需要讀寫校驗 DRAM 好壞。

### SMART Check

檢查 SMART LOG 健康狀態並確認 Critical Warning bit set to 1，若是設定為 "1" 代表測試失敗。

### Volatile Memory Backup (重要) 

為了避免設備掉電影響資料遺失，必須要加入多個電容零件，保護在發生掉電後，一定的時間內有足夠的電力將所有緩存在 DRAM 的資料刷新到 NAND Flash。

該測試主要針對電容壽命檢測，以避免電容因為長期使用造成損壞或是容值下降不足，原因如下 : 

* 如果容值變低，則會影響SSD的掉電時間，可能會無法保證一定的時間內刷新所有的資料
* 不能針對電容檢測太過於頻繁，會影響電容的使用壽命

### Metadata Validation

讀取並確認所有已寫入 Metadata 的資料完整性。因為有些資料可能很久都不會再更新，如果那些資料量很大，長時間下來會造成元數據不完整的可能性，所以韌體必須要定期或是透過自檢的方式去讀取校驗，確保元數據完整性。

### NVM Integrity

讀寫每一個 NVM 保留區域，確保每一個讀寫 (channel) 都能夠正常，並不會造成資料遺失。

### Data Integrity (Extended only)

該測試需要在背景下執行，主要確保所有使用者儲存的資料完整性。

### Media Check

隨機讀取每一個可用的儲存空間，並作讀寫校驗。

### Drive Life

檢查 SSD 壽命是否已經快要結束了。



## 檢查控制器支援

說明 : 發送 **Identify Controller** 命令來確認是否有支援 Device Self-Test。

- Controller Attributes (CTRATT) :
  - 318 Bytes : Bit 0
    - 0 : Don't Support
    - 1 : Support

![](https://github.com/miniedwins/learning/blob/main/nvme/pic/identify_controller/Identify_Controller_DSTO.png)

~~~shell
nvme id-ctrl /dev/nvme0 | grep dsto
# dsto: 1
~~~



## 發送自檢測試命令

說明 : 指定 Namespace Id 以及 Self-test Code (STC)，發送自檢命令給控制器執行操作。

![](https://github.com/miniedwins/learning/blob/main/nvme/pic/admin_command_set/device_self_test_dw_10.png)

備註 :  發送命令前需要了解 **Namespace Test Action** 所描述的說明。

**Device Self-test Namespace Test Action**

![](https://github.com/miniedwins/learning/blob/main/nvme/pic/admin_command_set/device_self_test_namespace_test_action.png)

說明 : 指定哪一個自檢類型。

~~~shell
# Short self-test
nvme device-self-test /dev/nvme0 --namespace-id=1 --self-test-code=1

# Extended self-test
nvme device-self-test /dev/nvme0 --namespace-id=1 --self-test-code=2
~~~

說明 : 停止自檢操作命令。

~~~shell
# Abort the device self-test
nvme device-self-test /dev/nvme0 --namespace-id=1 --self-test-code=0xf
~~~



## 查看自檢日誌

說明 : 日誌格式，可以讓我們知道自檢運行的進度以及結果。

* 一個日誌總共佔 (28 bytes)，控制器可以儲存 20 條日誌訊息
  * 1:0 Bytes : **(永遠表示)** 當前自檢的類型與進度 
  * 3:2 Bytes : 保留位元
  * 全部日誌資料 :  3 + 560 (28 x 20) = 563 Bytes
* 若是超過最大儲存，最後一個 (20th) 日誌會被前一個 (19th) 取代，最新自檢的日誌會放在第一個 (1st)

注意事項 : 

* 31:4 Bytes : 表示第一個日誌的內容
* 563:536 Bytes : 表示最後一個日誌

**Device Self-test Log**

說明 (Self-test Log) : 

* Current Device Self-Test Operation : 目前執行那一種自檢測試
* Current Device Self-Test Completion : 目前測試進度百分比

![](https://github.com/miniedwins/learning/blob/main/nvme/pic/log_page/log_page_self_test.png)

**Self-test Result Data Structure**

![](https://github.com/miniedwins/learning/blob/main/nvme/pic/log_page/log_page_self_test_result_data_structure_01.png)

![](https://github.com/miniedwins/learning/blob/main/nvme/pic/log_page/log_page_self_test_result_data_structure_02.png)

nvme-cli 可以選擇那一種顯示方式，較為方便閱讀日誌。

~~~shell
# NORMAL 格式輸出
nvme self-test-log /dev/nvme0 -o "normal"

# JSON 格式輸出
nvme self-test-log /dev/nvme0 -o "json"
~~~

日誌結果 :  下列每一條日誌所輸出的結果並非日誌完整的訊息，nvme-cli 只挑選比較重要的內容顯示。

~~~shell
Device Self Test Log for NVME device:nvme0
Current operation  : 0
Current Completion : 0%
Self Test Result[0]:
  Operation Result             : 0
  Self Test Code               : 2
  Valid Diagnostic Information : 0
  Power on hours (POH)         : 0x288
  Vendor Specific              : 0 0
Self Test Result[1]:
  Operation Result             : 0
  Self Test Code               : 1
  Valid Diagnostic Information : 0
  Power on hours (POH)         : 0x288
  Vendor Specific              : 0 0
Self Test Result[2]:
  Operation Result             : 0
  Self Test Code               : 1
  Valid Diagnostic Information : 0
  Power on hours (POH)         : 0x288
  Vendor Specific              : 0 0
Self Test Result[3]:
  Operation Result             : 0xf
Self Test Result[4]:
  Operation Result             : 0xf
Self Test Result[5]:
  Operation Result             : 0xf
...
Self Test Result[20]:
  Operation Result             : 0xf
~~~

若是要取得更詳細的資訊，需要執行下列命令 : 

~~~shell
# 將日誌以二進位輸出到 "self_test.log" 檔案
nvme self-test-log /dev/nvme0 -o "binary" > self_test.log

# 使用 hexdump 命令，它會以16進位的方式顯示
hexdump -C -n 512 self_test.log

# 或是直接使用 get-log
nvme get-log -i 0x06 -l 563
~~~

日誌結果 :

~~~shell
00000000  00 00 00 00 20 00 00 00  88 02 00 00 00 00 00 00  |.... ...........|
00000010  01 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
00000020  10 00 00 00 88 02 00 00  00 00 00 00 01 00 00 00  |................|
00000030  00 00 00 00 00 00 00 00  00 00 00 00 10 00 00 00  |................|
00000040  88 02 00 00 00 00 00 00  01 00 00 00 00 00 00 00  |................|
00000050  00 00 00 00 00 00 00 00  0f 00 00 00 00 00 00 00  |................|
00000060  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
00000070  00 00 00 00 0f 00 00 00  00 00 00 00 00 00 00 00  |................|
00000080  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
00000090  0f 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
000000a0  00 00 00 00 00 00 00 00  00 00 00 00 0f 00 00 00  |................|
000000b0  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
000000c0  00 00 00 00 00 00 00 00  0f 00 00 00 00 00 00 00  |................|
000000d0  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
000000e0  00 00 00 00 0f 00 00 00  00 00 00 00 00 00 00 00  |................|
000000f0  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
00000100  0f 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
00000110  00 00 00 00 00 00 00 00  00 00 00 00 0f 00 00 00  |................|
00000120  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
00000130  00 00 00 00 00 00 00 00  0f 00 00 00 00 00 00 00  |................|
00000140  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
00000150  00 00 00 00 0f 00 00 00  00 00 00 00 00 00 00 00  |................|
00000160  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
00000170  0f 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
00000180  00 00 00 00 00 00 00 00  00 00 00 00 0f 00 00 00  |................|
00000190  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
000001a0  00 00 00 00 00 00 00 00  0f 00 00 00 00 00 00 00  |................|
000001b0  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
000001c0  00 00 00 00 0f 00 00 00  00 00 00 00 00 00 00 00  |................|
000001d0  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
000001e0  0f 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
000001f0  00 00 00 00 00 00 00 00  00 00 00 00 0f 00 00 00  |................|
~~~

下面圖示使用上面日誌結果說明對應關係，第二個到最後一個日誌以此類推

說明 : 

* 當前因為沒有在運行自檢測試，狀態都為 **0x00**
* 主要觀察日誌的重點 
  * Device Self-test Status : 測試的結果，成功或者失敗
  * Segment Number : 若是測試失敗，會是在哪個項目出錯
  * Namespace Identifier : 若是有指定一個以上的 NS，發生在哪一個 NS Id

![](https://github.com/miniedwins/learning/blob/main/nvme/pic/log_page/self_test_log_description.png)



## 查看 EDSTT 測試時間

說明 : 發送 **Identify Controller** 命令來確認 **Extended Self-Test** 需要多少時間內完成測試。

> 備註 : 如果沒有控制器沒有支援，這個欄位就是保留狀態。

Controller Attributes (CTRATT) :

- 317:316 Bytes :  Extended Device Self-test Time (EDSTT)
  - 欄位需要轉換成 10 進制，取得真正的測試時間

![](https://github.com/miniedwins/learning/blob/main/nvme/pic/identify_controller/Identify_Controller_EDSTT.png)

~~~shell
nvme id-ctrl /dev/nvme0 | grep edstt
# edstt: 5
~~~
