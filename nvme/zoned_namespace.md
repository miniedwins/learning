---
tags: nvme
---

# Zoned Namesapce

## 名詞定義

### Zone

由連續的邏輯位址 (logic block address) 所組成，這些位址會被作業系統視為一個單位所使用，稱之為 Zone。

### Zone Size and Capacity

* Zone Size : 總空間大小
* Zone Capacity : 可使用空間大小，通常會小於等於 Zone Size

Unusable Blocks 為不可使用的空間 (官方網站定義)，不過 SEPC 上並沒有說明該空間的作用。該空間不會映射到任何邏輯位址。若是寫入或是讀取到這個空間都會發生錯誤。

![](https://github.com/miniedwins/learning/blob/main/nvme/pic/zone/zone_size%20and%20zone_capacity.png)

### Zone Namespace

* 由多個 Zone 所組成，稱為 Zone Namespaces。
* 每個 Zone 都會是以連續寫入的方式，將資料寫入。

![](https://github.com/miniedwins/learning/blob/main/nvme/pic/zone/zones_in_a_zoned_namespace.png)

### Zone Descriptor

每一個 Zone 都會有一個 Descriptor，描述該 Zone 的相關狀態或是屬性值。例如 : 目前的 Zone 是在位在哪一個狀態 (Zone State)，容量大小或是起始位置 (ZSLBA) 等之類的屬性值。

> Host 可以使用 `Zone Management Receive` 命令，取得一個或是多個 Zone Descriptor。

### Zone Characteristics

首先說明 `Write Pointer (WP)` 屬性，它是定義在 Zone Descriptor，表示 Zone 下一個可以寫入資料的 LBA，若是該 Zone 處在不可寫入的狀態，控制器則會回報錯誤。Zone Namespace 會對於每一個 Zone 區域維護 WP，所以當有資料寫入到，Zone會從當前所記錄的 WP 位址開始寫入。

下圖則是說明，如果開始為 ZSE 的狀態，WP 的位置則會是指向 ZSLBA，也就是該 Zone 的起始位置。若是寫入資料完成後，則會是指向下一個寫入的 LBA 位置。

![](https://github.com/miniedwins/learning/blob/main/nvme/pic/zone/zone_write_pointer.png)

> Host 可以使用 `Zone Management Receive` 命令取獲得目前的 WP 位址。

每次寫入操作都會增加 WP 屬性的值，因此在這幾個狀態 (ZSE, ZSIO, ZSEO, ZSC) 一但資料成功寫入後，都會增加 WP。主要原因是，寫入資料需要轉態到 Open 區域。

下圖說明當前的 Zone State 的狀態下，WP 在那些狀態是有效以及無效。

![](https://github.com/miniedwins/learning/blob/main/nvme/pic/zone/zone_characteristics.png)

可以先看到 ZSE (Empty State)，標示是有效的 WP，但是為什麼 Active & Open Resources 都是無效 ? 因為 ZSE 狀態下，尚未有任何資料寫入，並不會進入到 Active 或是 Open 區域，所以這兩個區域都會顯示無效的 WP。而當資料已經有被寫入到 Zone，這個時候的 ZSE 會轉狀態到 Active 或是 Open 區域，這個時候 WP 才會有是有效。

ZSF, ZSRO, ZSO 這幾種狀態它們的 WP 都不是有效的，因為這些狀態下它們都無法在寫入任何資料，WP 自然就會是無效。所以當在這幾個狀態下，如果發送出寫入命令，該命令會被控制器忽略(Abort) 並且回傳無效的狀態碼。

若是 Zone's WP 已經指向達最大可以寫入的位址 (LBA)，可以發送`Zone Management Send command`，設定參數 Zone Send Action 04h，表示要 Reset Zone。命令執行成功後，可以從 Zone Descriptor 觀察 WP 是否被設定成 ZSLBA。

***Zone 寫入與讀取命令的注意事項 :***

**寫入命令**

* 寫入命令 (Address-Specific Write) 的開始的 LBA，沒有等於 WP 所指向的位置
* 寫入命令 (Zone Append) 並且指定 ZSLBA，但是 ZSLBA 並不是 Zone 的最低起始位址

以上這兩點都會造成控制器忽略該命令，並且回傳無效的狀態碼。

**讀取命令**

* 如果目前在 ZSO 狀態內發送讀取命令，離線狀態是不能夠執行任何讀寫，則控制器會回傳狀態碼 (Zone offline)
* 如果 Across Zone Boundaries 設定為 "1"，則讀取的邏輯位址，可以讀取超過該 Zone 的邏輯位址，代表讀取的範圍可以超過該 Zone 的範圍，因此可以讀取更多的資料。

Across Zone Boundaries 參數，查詢 Identify Namespace(Zone Namespace) 可以找到相關設定說明 Optional Zoned Command Support (OZCS)。

* Bit 0: Across Zone Boundaries
    * "1" : 允許讀取的LBA範圍，超過該 Zone's LBA
    * "0" : 不允許讀取命令的LBA範圍，超過該 Zone's LBA

## Zone Descriptor Extension


## Zone Active Excursions

它是一個由廠商所定義的 Specific Action，可以讓 ZSIO、ZSEO、ZSC，在任何一個時間點轉態到 ZSF。如果控制器執行轉態的動作，Zone Attributes (ZA) 會被設定 Finish Zone Recommended (FZR=1)，並且產生一個 Zone Descriptor 事件的改變。

## 狀態機制

這是 Zone 的狀態圖，每一個 Zone 都一定會處在其中一個狀態，而系統會藉由不同狀態的切換來管理資源。所以在同一時間內資源是有限的，並且有部份的 Zones 可能會處在 ZSC 的狀態下，不過這個狀態下是可以讀取的。

![](https://github.com/miniedwins/learning/blob/main/nvme/pic/zone/zone_state_machine.png)

### Empty state (ZSE) 

一開始初始化的 Zone 都會進入到 ZSE 狀態，這也代表儲存空間沒有任何寫入資料。

***(待確認行為是否為真)***
Zone 可以有效地轉換到各個狀態之前，前提需要格式化 (Format CMD)，或是執行建立 Namespace (Namespace Managent CMD)，因此初始化的狀態可能會是 ZSE 或是 ZSO。

### Closed state (ZSC) 

處在關閉的狀態下，可以讀取資料但無法寫入資料。若是需要寫入資料就必須要轉態到 ZSIO or ZSEO。

### Full state (ZSF) 

寫入的 (LBAs) 已經達到 Zone 的容量上限，就會自動進入 Full 狀態。

若是 Zoned Namespace 轉變成寫入保護 (write protected) 的狀態， 則在活動區所有的 Zones 都會轉態成 ZSF。

### Read Only state (ZSRO)

此狀態僅能夠讀取，但沒有說明是不是能夠切換到其它狀態。

### Offline state (ZSO)

此狀態無法再轉換到其它狀態，代表該 Zone 生命週期結束。

### Implicitly Opened (ZSIO) 

當系統直接發送寫入命令，當前 Zone 會自動進入到 ZSIO 狀態，關閉的方式也會是自動。這麼做的原因是控制器可以隨時轉換其它態，有效的管理資源，避免資源使用不足。

### Explicitly Opened (ZSEO) 

通過管理命令 (Zone Management Send command) 透過顯示打開的方式進入到 ZSEO 狀態，不過關閉的時候，需要使用管理命令關閉 Zone。

如果打開的區域數量的 Zone 達到最大值，並且它們都是顯式打開的，那麼任何一個隱式或是顯式打開的 Zone 都將失敗。

如果其中一些 Zone 只是隱式打開，那麼嘗試打開隱式或是顯式的 Zone，將會導致SSD關閉其中一個隱式打開的Zone。

> 備註 : 控制器不會主動切換在打開區域的 ZSEO，需要發管理命令切換。

## 資源管理

它的定義在於可以使用 Zones 的最大數量，以及最大可以開啟多少個 Zones 資源。根據 Zone 狀態圖表示，並非可以無限地打開資源，因此會管理與限制資源的使用。

![](https://github.com/miniedwins/learning/blob/main/nvme/pic/zone/zone_resource.png)

* Active : 表示最大有多少個 Zones 的資源可以使用
* Opend : 表示最大可以打開多少個 ZSIO & ZSEO 數量
* Maximum : (Opend Zones + Closed Zones) <= Active Zones

整體的資源管理，主要的概念區分 Active 以及 Opend Zone，只要是進入到這兩個區域，使用的資源就會增加，離開 Active 或是 Opend Zone 以外的區域，使用的資源就會減少。Active 代表整體總共可以使用的資源，Opend 則是在這整個資源中，有多少可以打開的資源。

例如 : 如果控制器處理一個命令，需要將 Zone 轉態到 ZSIO、ZSEO、ZSC，如果已經沒有可使用空間，若是打開超過 Active 或是 Opend 的最大限制，則控制器會終止命令，並且回傳錯誤的狀態碼 (e.g.：Too Many Active Zones or Too Many Open Zones)。

控制器管理資源的目的，就是將那些在 Opend 區域裡的 ZSIO 轉態到 ZSC 狀態，藉由這個方式來釋放資源，能夠讓其它需要的使用的 Zone 進入到 Opend 區域。ZSEO 是屬於透過管理命令方式打開，並非由控制器自動切換到 ZSIO，ZSEO 狀態是無法自動的切換，因此需要使用管理命令將其轉態。

## 狀態轉換

每個 Zone 狀態可以轉換到不同的狀態，但是並不是每個狀態都可以允許轉換，像是 ZSO 就無法轉換到其他的狀態。有些 Zone 的狀態，若是要轉換到其它的狀態就有需要透過管理命令 (Zone Management Send command) 的方式執行轉換，而有些則是控制器自動轉換。

另外要轉態到 Active 或是 Open，都會檢查這兩個區域內的 Resouces 是不是有足夠的資源可以轉態過去，若是沒有可用資源則是回傳狀態碼 (Too Many Active or Opend Zones)。

> 轉換原則 : 
> 1. 無法由控制器自動轉換的，就是需要透過管理命令轉換
> 2. 某一些條件達成後，會自動轉換狀態

### ZSE

* ZSE -> ZSIO : Controller Transition (write operation)
* ZSE -> ZSEO : Zone Send Action of Open Zone
* ZSE -> ZSC  : Set Zone Descriptor Extension
* ZSE -> ZSF  : Zone Send Action of Finish Zone

***ZSE -> ZSEO (暫時未了解)***

### ZSIO

* ZSIO -> ZSE  : Zone Send Action of Reset Zone
* ZSIO -> ZSEO : Zone Send Action of Open Zone
* ZSIO -> ZSC  : 
    * Zone Send Action of Close Zone
    * Controller Transition (Managing resources)
* ZSIO -> ZSF  : 
    * Zone Send Action of Finish Zone
    * Zone already reach its writeable zone capacity
    * Zoned namespace becomes write protected

### ZSEO
* ZSEO -> ZSE : Zone Send Action of Reset Zone
* ZSEO -> ZSC : Zone Send Action of Close Zone
* ZSEO -> ZSF :
    * Zone Send Action of Finish Zone
    * Zone already reach its writeable zone capacity
    * Zoned namespace becomes write protected

### ZSC
* ZSC -> ZSE  : Zone Send Action of Reset Zone
* ZSC -> ZSIO : Controller Transition (write operation)
* ZSC -> ZSEO : Zone Send Action of Open Zone
* ZSC -> ZSF  : 
    * Zone Send Action of Finish Zone
    * Zone Active Excursion
    * Zoned namespace becomes write protected

### ZSF
* ZSF -> ZSE : Zone Send Action of Reset Zone

### ZSRO
* ZSRO -> ZSO : Zone Send Action of offline Zone

### ZSO
* There are no transitions from the ZSO:Offline state to any other zone state.

## 管理命令


## 疑問待了解 

1. 每個 NS's Zone 編號都依順序編號 ? 
2. 為什麼 ZSRO 只能轉到 ZSO，不能轉態到其它區域 ?

## 待確認行為是否為真

1. 若是當前寫入的資料，已達該 Zone 最大的邏輯位址，就無法再繼續寫入資料，並且該狀態會轉變成 Read Only state (ZSRO)。 
