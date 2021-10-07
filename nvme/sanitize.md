# sanitize



## 基本介紹

主要的功能就是清除 NAND Flash 資料，支援三個操作類型 : `Block Erase`、`Overwrite`、`Crypto Erase`。

當執行中或是執行完成的時候，我們可以透過 `Sanitize Status Log` 來檢查執行的進度或是狀態。

* Block Erase : 清除所有物理上 Block 資料，一旦被清除就無法再恢復資料
* Overwrite : 使用特定資料格式去複寫現有已存在的資料
* Crypto Erase : 通過刪除密鑰的方式讓資料無法再被識別，因為沒有金鑰就無法取得真正的資料內容

> 備註 : Sanitize 三個操作類型，都是運作在背景執行。



## 檢查控制器支援

說明 : 

執行命令 : 

~~~shell
~~~



## 如何執行 Sanitize

說明 : 

執行命令 : 

~~~shell
~~~



