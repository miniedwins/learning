# Secure Erase



## 基本介紹

Secure Erase 是透過 `format NVM` 命令執行操作，是使用低階 (low level) 的方式清除 NVM media，因此它會破壞資料 (data) 以及元數據 (metadata)，我們可以指定所有的 namespaces 或是個別指定 namespace 的資料被清除。



**Secure Erase 支援兩種格式化類型 :**

* `User Data Erase` : 移除使用者所有的資料 (NVM Subsystem)
* `Cryptographic Erase` : 透過刪除加密的金鑰方式移除使用者的資料 (前提 : 使用者的資料必須要被加密)

---

**Format NVM – Operation Scope**

Secure Erase 操作它會根據控制器 `Identify` 所支援的屬性 `FNA` 決定 `format NVM` 的操作行為。

如下圖所示，FNA Bit 數值會對應所指定 NSID，執行不同的 format 操作。

![](https://github.com/miniedwins/learning/blob/main/nvme/pic/format_nvm_operation_scope.png)

---

**如何區別 Secure Erase & Sanitize : **

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

