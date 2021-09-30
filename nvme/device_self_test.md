# Device self-test



## 基本介紹

裝置自檢 (self-test)，主要定義一系列 SSD 自我檢測的驗證項目，但是內部實現的測試方法是由廠商自定義。

這邊要注意的是，當前 SSD 若是正在運行自檢期間，如果控制器收到任何命令，應進行下列動作 :

* suspend the device self-test operation  (暫停目前的自檢操作)
* process and complete that command (處理收到的命令，並完成命令執行)
* resume the device self-test operation (回到剛剛自檢的操作)

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
* 檢的進度與測試的情況，可以從 Device Self-Test 日誌取得資訊內容

**當自檢 (Extended Self-Test) 時發生 Controller Level Reset，應當會有下列的運作行為 :**

* 控制器重置或是任何電源重新上斷電執行完成後，需要回到先前自檢的操作
* 回到先前自檢未完成的操作項目，這部份可以由廠商定義
* 未完成的操作項目，應當重新清除，然後再重新測試

**中斷自檢操作命令如下 :**

* shall be aborted by **a Format NVM**
  * 收到 Format NVM 命令
* shall be aborted when **a sanitize operation is started**
  * 開始執行 Sanitize 操作已經開始
* shall be aborted if a Device Self-test command with the **Self-Test Code field set to Fh** is processed
  * STC 欄位為 device self-test 命令參數，若是被設定成 **0xFh**，代表是停止自檢測試
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

為了避免設備掉電影響資料遺失，必須要加入多個電容零件，保護在發生掉電後，在一定的時間內有足夠的電力將所有緩存在 DRAM 的資料刷新到 NAND Flash。

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

~~~shell
# 待確認
# Short self-test
nvme device-self-test /dev/nvme0 --namespace-id=1 --self-test-code=1

# Extended self-test
nvme device-self-test /dev/nvme0 --namespace-id=1 --self-test-code=2
~~~

說明 : 停止自檢操作命令

~~~shell
# 待確認
# Abort the device self-test
nvme device-self-test /dev/nvme0 --namespace-id=1 --self-test-code=0xf
~~~



## 查看自檢日誌

說明 : 日誌格式，可以讓我們知道自檢運行的進度以及結果。

* 一個日誌總共佔 (28 bytes)，控制器可以儲存 20 條日誌訊息，所以總共日誌資料為 563 Bytes
* 若是超過最大儲存，理應當覆蓋 **(最舊)** 的日誌，並且維持在 **(最新)** 的日誌訊息

日誌內容說明 : 

* Current Device Self-Test Operation : 代表屬於那一種自檢測試
* Current Device Self-Test Completion : 測試進度百分比

![](https://github.com/miniedwins/learning/blob/main/nvme/pic/log_page/log_page_self_test.png)

~~~shell
nvme self-test-log /dev/nvme0 -o "normal"
nvme self-test-log /dev/nvme0 -o "json"
~~~

日誌結果 :

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

若是要取得更詳細的資訊 (搭配 SPEC 找出相對欄位的描述內容)，需要執行下列命令 : 

~~~shell
nvme self-test-log /dev/nvme0 -o "binary" > self_test.log

# show binary log
hexdump -C -n 512 self_test.log
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



三.觸發自檢命令之後，FW會按照相應的序列順序執行，命令運行的情況在device self-test log中顯示，這個log可通過get log page命令的LID=6來獲取。

1.Current Device Self-Test Operation 表示當前的診斷操作類型

2.Current Device Self-Test Completion 表示當前的診斷操作進度

3.Self-test Result Data Structure 總共有20條記錄，記錄了歷史的自檢結果，主要關注兩個點：

●Device Self-test Status:這裡顯示了自檢的結果，成功或者失敗。

● Segment Number:這裡顯示了失敗在哪個序列操作。
