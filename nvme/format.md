# Secure Erase



## 基本介紹

### 內容說明

Secure Erase 是透過 `format NVM` 命令執行操作，是使用低階 (low level) 的方式清除 NVM media，因此它會破壞資料 (data) 以及元數據 (metadata)，我們可以指定所有的 namespaces 或是個別指定 namespace 的資料被清除。

**注意事項 :** 

* 如果某一個 NS 正在執行 I/O ，若是發送 `format NVM` 命令，則該命令可能會被 `aborted`
* 如果 `format NVM` 命令正在執行中，若是提交 I/O 命令 ，則該命令可能會被 `aborted`



### 支援兩種格式化類型 

* `User Data Erase` : 移除使用者所有的資料 (NVM Subsystem)
* `Cryptographic Erase` : 透過刪除加密的金鑰方式移除使用者的資料 (前提 : 使用者的資料必須要被加密)



### Format NVM 屬性說明

524 Bytes (FNA) : 

* Bit 2 : 代表是否支援 `cryptographic erase`
  * 0 : Don't Support
  * 1 : Support
* Bit 1 : 代表是否支援 `all namespaces` 或是 `particular namespace`
  * 0 : Don't support all namespaces
  * 1 : Supprot all namespaces
* Bit 0 : 不翻譯，保留原文說明 
  * 有部分內容暫時無法了解

![](https://github.com/miniedwins/learning/blob/main/nvme/pic/identify_controller/Identify_Controller_FNA.png)



### 格式化操作範圍 (format operation)

Secure Erase 操作它會根據控制器 `Identify` 所支援的屬性 `FNA` 決定 `format NVM` 操作行為。

如下圖所示，FNA Bit 數值會對應所指定 NSID，執行不同的 format operation，例如 : `FNA=1` 代表可以進行任何 `allocated namespaces` 的任一個或是所有 NS 的格式化操作。

![](https://github.com/miniedwins/learning/blob/main/nvme/pic/format_nvm_operation_scope.png)



### 如何區別  Sanitize

* `format` : 可以對多個 NS 或是指定單一個 NS 執行操作
* `sanitize` : 它是針對所有的 Namespaces 執行操作

> 備註 : Sanitize 以及 Secure Erase 都可以安全地清除 SSD 所有的資料，並且清除後的資料會永久無法恢復。



## 檢查控制器支援

說明 : 

發送命令 : 

~~~shell

~~~



## 如何使用功能 

說明 : 

發送命令 : 

~~~shell
~~~

