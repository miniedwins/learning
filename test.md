# Firmware Download



## Introduction

`Firmware Command` 分為以下兩種命令 : 

1. Firmware Image Download
2. Firmware Commit



## Firmware Image Download 

此功能主要是用來更新全部或是部份的資料 (image) 到控制器上(controller)，也就是可以將新的韌體資料上傳到控制器上，由此方式更新韌體。更新的過程中需要將該更新的資料分成一小部份的方式作為傳遞，每一份傳遞資料都包含了 `NUMD` and `OFST` ，所以 `host` 必須要確保資料傳遞的 `NUMD` and `OFST`是否有符合 `FWUG `，可以透過 `identify-ctrl` 取得，若是沒有符合 `FWUG` 就會造成韌體更新錯誤。

當所有的資料傳遞完成後，並不會馬上被啟用 `active`，`host ` 還需要發送 `Firmware Commit Commad`，並且在其它 `downloading image` 之前發送該命令，這個時候控制器就會處理第一次 `Firmware Commit` 前的 `Firmware Image`。

如果在執行 `Firmware image download or Commit` 的期間，發生系統斷電或式控制器被重置等突發事件後，先前傳遞的資料都會被控制器給移除。

*備註 : 建議要越小越好，目前 `FADU Sample` 所提供的 `FWUG value = 1` 。*

<img src="../../res/Firmware_Update_Granularity.png" style="zoom:80%;" align="left"/>

### NUMD (Number of  Dwords)

這裡是設定傳遞資料的大小，可以由 `NUMD` 設定較大的傳輸資料 `128k bytes`，最小要設定成 `4k bytes` 大小，不過最後都要符合 `FWUG` 所要求的規範。

<img src="../../res/number of dwords.png" style="zoom:80%;" align="left"/>

### OFST (Offset)

開始傳遞的資料都會是由 `OFST=0h` 開始，它必需要隨者傳遞的資料做偏移。也就是每次傳遞的 `OFST` 位置會不同。例如 : 傳遞資料大小每次為 `4k bytes`，第一次 `OFST` 位置就會是 `0h`，第二次傳遞的資料 `OFST` 位置就會是 `1000h` ，這個數值就是 `4096(hex)`，以此方式遞增到傳遞資料結束。

<img src="../../res/offset.png" style="zoom:80%;" align="left"/>

```
print(set4)
print(set5)
```



## Firmware Commit Command

主要功能是用來更動 `Firmware image or Boot Partitions`。當韌體被更動後，`Firmware Commit` 會去驗證剛剛 `download image` 並且修訂所指定的 `firmware slot`。此時還無法使用當前下載 `firmware image`，需要等下一次 `Controller Level Rest` 完成後，所指定的 `firmware slot` 才會被啟動。 

> `firmware slot` 是存放韌體的位置，須看控制器所支援的數量，最大支援七個數量

host 會在下一次 `Controller Level Rest` 去檢查兩件事情， 如下 :

1. 檢查目前所使用的 `firmware revsion (FR)`
2. 檢查 `firmware slot information` 

`host` 檢查下列表格就可以得知，下一次控制器重置後，是否需要 active firmware slot

<img src="../../res/Firmware Slot Information log page.png" style="zoom:80%;" align="left"/>



### Commit Action (CA)

當然`firmware commit` 的功能，不只有以上基礎使用方法，例如 : 

1. 更新韌體後，下一次控制器重置，不啟用先前更新的韌體。
2. 不更新韌體，下一次控制器重置，指定啟用當前已存在的 `firmware slot`。

下列表格代表者執行 `firmware commit` 命令所需要指定的參數 :

1. Commit Action (CA)
2. firmware slot (FS)

<img src="../../res/Firmware Commit.png" style="zoom:80%;" align="left"/>

![](https://i.imgur.com/8pzbBDX.png)




