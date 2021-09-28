# Device self-test



## 基本介紹

裝置自檢 (self-test)，主要定義一系列 SSD 自我檢測的驗證項目，但是內部實現的測試方法是由廠商自定義。

這邊要注意的是，當前 SSD 若是正在運行自檢期間，如果控制器收到任何命令，應進行下列動作 :

* suspend the device self-test operation  (暫停目前的自檢操作)
* process and complete that command (處理收到的命令，並完成命令執行)
* resume the device self-test operation (回到剛剛自檢的操作)

> 備註 : 另外控制器若是沒有自檢，可能會造成效能降低的問題。

下列圖示 Device Self-test Operation (Informative)

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
# 待確認
nvme id-ctrl /dev/nvme0 | grep DSTO
~~~



## 發送自檢測試命令

說明 : 指定 Namespace Id 以及 Self-test Code (STC)，發送自檢命令給控制器執行操作。

![](https://github.com/miniedwins/learning/blob/main/nvme/pic/admin_command_set/device_self_test_dw_10.png)

備註 :  發送命令前需要了解，**Namespace Test Action** 所描述的說明。

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

說明 : 

~~~shell
# 待確認
~~~



## 查看 EDSTT 測試時間

說明 : 發送 **Identify Controller** 命令來確認 **Extended Self-Test** 需要多少時間內完成測試。

> 備註 : 如果沒有控制器沒有支援，這個欄位就是保留狀態。

Controller Attributes (CTRATT) :

- 317:316 Bytes :  Extended Device Self-test Time (EDSTT)
  - 欄位需要轉換成 10 進制，取得真正的測試時間

![](https://github.com/miniedwins/learning/blob/main/nvme/pic/identify_controller/Identify_Controller_EDSTT.png)

~~~shell
# 待確認
nvme id-ctrl /dev/nvme0 | grep EDSTT
~~~



一.Device self-test命令在Command DW 10字段中定義了診斷的操作類型，而所有其他命令指定的字段都要保留。

![img](https://files.sekorm.com/opt/fileStore/cms/nps/editor/20210521/1621582300536061353th.png)



如上圖所示，目前支持的操作類型有4種，

1.開始一個短診斷操作；短診斷的完成時間不能大於2min。

2.開始一個長診斷操作；長診斷的完成時間由Identify Controller的字段EDSTT定義，單位是分鐘。

3.開始一個廠商自定義操作;

4.中斷一個診斷操作;



二.中斷一個自檢命令的操作有:

1.Controller reset

2.NVMe Format Command

3.一個STC為F的Device self-test命令

4.一個刪除對應的ns的操作

5.Sanitize命令



三.觸發自檢命令之後，FW會按照相應的序列順序執行，命令運行的情況在device self-test log中顯示，這個log可通過get log page命令的LID=6來獲取。

1.Current Device Self-Test Operation 表示當前的診斷操作類型

2.Current Device Self-Test Completion 表示當前的診斷操作進度

3.Self-test Result Data Structure 總共有20條記錄，記錄了歷史的自檢結果，主要關注兩個點：

●Device Self-test Status:這裡顯示了自檢的結果，成功或者失敗。

● Segment Number:這裡顯示了失敗在哪個序列操作。
