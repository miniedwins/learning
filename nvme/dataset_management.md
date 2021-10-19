# Dataset Management



## DSM 介紹

**Dataset Management (DSM) :** 由主機來決定執行 `dsm` 命令，可以改善效能與穩定性，以及對邏輯區塊 (logic block) 執行像是 `Trim` 的行為，因此它才是真正的 Trim 的名詞解釋。它提供 Range Definition，最大可以支援 Range 0-255 (256*16 = 4096 Bytes)，每個 Range 的組成包含 Starting LBA, Length in logical blocks, Context Attributes。主機可以透過 dsm 命令，指定每個 `Range Field Attributes`，而控制器會根據該 `Range` 所指定的內容去執行 。

例如 : 主機要執行 `Trim` 功能，主機發送 dsm 命令就會設定 Attribute Deallocate (AD) 以及將 Range Definition Data 傳給控制器，當控制器執行完畢後，那些指定的 block range 就會變成 `deallocate` or `unwritten logical block`。

**dsm 可以設定的功能有 AD, IDW, IDR**

![](https://github.com/miniedwins/learning/blob/main/nvme/pic/nvm_command_set/dataset_management_dw11.png)

**Range Definition : 指定開始的邏輯區塊位置與長度，還有屬性 (Context Attributes)**

![](https://github.com/miniedwins/learning/blob/main/nvme/pic/dataset_management_range_definition.png)

## 相關名詞解釋

### Deallocate

該定義代表一個邏輯區塊的狀態，如下所述 : 

* 從未被寫過的邏輯區塊 (unwritten logical lock)，對主機而言就是一個乾淨的邏輯區塊
* 該邏輯區塊 (logical block) 已經有執行過 dsm with deallocated 
* (原文) Write Zeroes Command or Sanitize command is called deallocated or unwritten logical block
  * (說明) 執行上述這兩個命令，基本上會讓邏輯區塊清除為零，可以稱為 deallocated or unwritten logical block

> 備註 : The operation of the Deallocate function is similar to the ATA DATA SET MANAGEMENT with Trim feature

### Error Recovery

(原文) The controller shall fail Read, Verify, or Compare commands that include deallocated or unwritten blocks with a status of Deallocated or Unwritten Logical Block if that error has been enabled using the DULBE bit in the Error Recovery feature.

*備註 : Legacy software may not handle an error for this case.*

![](https://github.com/miniedwins/learning/blob/main/nvme/pic/feature/error_recovery_id_05.png)

###  DULBE

當主機讀取 deallocated or unwritten block，控制器根據 Deallocate Logical Block Features (Bits 2:0) 設定，參考 Identify Namespace Data Structure (DLFEAT)，當讀取到 deallocated or unwritten block，控制器應該需要回傳那一種數值。

回覆下列其中一種數值 : 

* 0x00h
* 0xFFh
* either 0x00h or 0xFFh

![](https://github.com/miniedwins/learning/blob/main/nvme/pic/identify_namesapce/Identify_Namespace_DLFEAT.png)



## 如何執行命令

### 檢查控制器是否支援

說明 : 檢查控制器有沒有支援 **Dataset Management** 命令，沒有支援就沒有辦法做 **Trim**

![](https://github.com/miniedwins/learning/blob/main/nvme/pic/identify_controller/Identify_Controller_ONCS_Bit2.png)

執行命令 : 

~~~shell
nvme id-ctrl /dev/nvme0 | grep oncs
# oncs: 0x1e
~~~



### 確認是否支援 Deallocate

說明 : 檢查控制器有沒有支援 Deallocated or Unwritten Logical Block error for this namespace

取得方法 : 

* 查看 Namesapce Data Struct，並檢查 `DLFEAT` 該屬性質
* nvme-cli 並沒有把 `DLFEAT` 顯示出來，因此需要發送 `admin-passthru` 命令取得 `Raw Data`
* 長度可以設定 512 bytes 即可，目的只是要確認 `Bits 2:0`

![](https://github.com/miniedwins/learning/blob/main/nvme/pic/identify_namesapce/Identify_Namespace_NSFEAT.png)

執行命令 : 

~~~shell
nvme admin-passthru /dev/nvme0 --namespace-id=1 --opcode=0x06 --cdw10=0x00 --data-len=512 --read
~~~

執行結果 : 

~~~shell
NVMe command result:00000000
       0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
0000: b0 44 f2 1b 00 00 00 00 b0 44 f2 1b 00 00 00 00 ".D.......D......"
0010: b0 44 f2 1b 00 00 00 00 00 01 00 00 00 00 00 00 ".D.............."
0020: 00 00 ff 00 00 00 00 00 ff 00 00 00 00 00 00 00 "................"
~~~



### 檢查啟用或停用 DUBLE 

說明 : 檢查目前的控制器是否有啟用或是停用 **DUBLE**

![](https://github.com/miniedwins/learning/blob/main/nvme/pic/feature/error_recovery_id_05.png)

~~~shell
nvme get-feature --feature-id=0x05 /dev/nvme0n1 
# get-feature:0x5 (Error Recovery), Current value:00000000
~~~

