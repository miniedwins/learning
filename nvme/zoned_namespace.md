---
tags: nvme
---

# Zoned Namesapce

## 名詞定義

### Zone

由連續的邏輯位址 (logic block address) 所組成，這些位址會被作業系統視為一個單位所使用，稱之為 Zone。

### Zone Size

代表一個 Zone 的總容量大小。

### Zone Capacity

代表每一個 Zone 可以使用的邏輯區塊，該空間通常是小於或是等於 Zone Size。

### Zone Namespace

由多個 Zone 所組成，稱為 Zone Namespaces。

### Zone Descriptor

每一個 Zone 都會有一個 Descriptor，描述該 Zone 的相關狀態或是屬性值。例如 : 目前的 Zone 是在位在哪一個狀態 (Zone State)，容量大小或是起始位置 (ZSLBA) 等之類的屬性值。

> Host 可以透過發送 `Zone Management Receive` 命令，取得一個或是多個 Zone Descriptor。

### Zone Characteristics

首先說明 `Write Pointer (WP)` 屬性，它是定義在 Zone Descriptor，表示 Zone 下一個可以寫入資料的邏輯地址，若是該 Zone 處在不可寫入的狀態，控制器則會回報錯誤。Zone Namespace 會對於每一個 Zone 區域維護 WP，所以當有資料寫入到，Zone會從當前所記錄的 WP 位址開始寫入。

> Host 可以使用 `Zone Management Receive` 命令取獲得目前的 WP 位址。

每次寫入操作都會增加 WP 屬性的值，因此在這幾個狀態 (ZSE, ZSIO, ZSEO, ZSC) 一但資料成功寫入後，都會增加 WP。若是當前寫入的資料，已達該 Zone 最大的邏輯位址，就無法再繼續寫入資料，並且該狀態會轉變成 Read Only state (ZSRO)。 ***(待確認)***

下圖說明當前的 Zone State 的狀態下，WP 在那些狀態是有效以及無效。

![](https://github.com/miniedwins/learning/blob/main/nvme/pic/zone/zone_characteristics.png)

可以先看到 ZSE (Empty State)，標示是有效的 WP，但是為什麼 Active & Open Resources 都是無效 ? 因為還在 ZSE 狀態下，尚未有任何資料寫入，因此 Active & Resource 都是無效的 WP。而當資料已經有被寫入到 Zone，這個時候的 Zone State，會轉狀態到 Active OR Open，這個時候 WP 才會有是有效。

ZSF, ZSRO, ZSO 這幾種狀態它們的 WP 都不是有效的，因為這些狀態下它們都無法在寫入任何資料，WP 自然就會是無效。所以當在這幾個狀態下，如果發送出寫入命令，該命令會被控制器忽略(Abort) 並且回覆無效的 Status Code。

若是 Zone's WP 已經指向達最大可以寫入的位址 (LBA)，可以發送`Zone Management Send command`，設定參數 Zone Send Action 04h，表示要 Reset Zone，命令執行成功後，可以從 Zone Descriptor 觀察 WP 是否被設定成 ZSLBA。

Zone 寫入命令的注意事項 : 

* 寫入命令 (Address-Specific Write) 的開始邏輯位址，沒有等於 WP 所指定的位置
* 寫入的命令 (Zone Append) 並且指定 ZSLBA，但是 ZSLBA 並不是 Zone 的最低起始位址

以上這兩點都會造成控制器忽略該命令，並且回覆無效的 Status Code。


## 狀態機制

The state machine consists of the following states: ZSE:Empty, ZSIO:Implicitly Opened, ZSEO:Explicitly Opened, ZSC:Closed, ZSF:Full, ZSRO:Read Only, and ZSO:Offline.

![](https://github.com/miniedwins/learning/blob/main/nvme/pic/zone/zone_state_machine.png)

### Empty state (ZSE) 

儲存空間沒有任何資料

* if the write pointer is valid, the write pointer points to the lowest LBA in the zone
* Zone Descriptor Extension Valid bit is cleared to ‘0’

### Closed state (ZSC) 

關閉的狀態

### Full state (ZSF) 

持續寫入區塊 (blocks) 的數量達到一個 Zone Capacity 的上限之後，就會進入 Full 狀態。

### Read Only state (ZSRO)

只可以讀取資料

### Offline state (ZSO)

該區域屬於關閉狀態，無法讀寫任何資料

* if the write pointer is valid and does not point to the lowest LBA in the zone
* if the write pointer is valid and the Zone Descriptor Extension Valid bit is set to ‘1’

### Implicitly Opened (ZSIO)  

隱式

### Explicitly Opened (ZSEO) 

顯式


### Active Zones

根據 (Zone State Machine) 表示，位在該區域的 Zone 狀態為下列三種 : 

* ZSIO : Implicitly Opened state (隱式打開)
* ZSEO : Explicitly Opened state (顯式打開)
* ZSC  : Closed state (關閉)

在這裡活動的 Zone 是可以隨時被系統隱式打開或是關閉。

---

以下狀態 (zone state)，控制器會中止寫入命令 :

* Zone Full
* Zone Read Only
* Zone Offline
* ZSE ZSIO ZSEO ZSC :
  * a) if an Address-Specific Write Command specifies a Starting LBA field that is not equal to the write pointer for that zone, then the controller shall abort that command with a status code of Zone Invalid Write;
  * b) if a Zone Append command specifies a ZSLBA that is not the lowest logical block address in that zone, then the controller shall abort that command with a status code of Invalid Field in Command.

---

## Zone Resources

*  Rsource
  * Active : 表示最大有可以使用多少 Active Zones
  * Open : 表示最大可以打開 (Implicitly & Explicitly) 多少個 Active Zones

如果控制器處理一個命令，需要將 zone 轉態到 ZSIO、ZSEO、ZSC，如果 Resource 已經沒有可使用空間，若是打開超過 Active 或是 Opend 的最大限制，則控制器會終止命令，並且回傳錯誤的狀態碼 (例如：Too Many Active Zones or Too Many Open Zones)

若是 zoned namespace 轉變成寫入保護 (write protected) 的狀態， 則在活動區所有的 Zones 都會轉態成 ZSF。

如果打開的區域數量達到最大值，並且它們都是顯式打開的，那麼任何打開新區域的嘗試都將失敗。但是，如果其中一些區域只是隱式打開的，那麼嘗試打開一個新區域將導致SSD關閉其中一個隱式打開的區域。

---

## 狀態轉換

(未完成)

### ZSE:Empty state

### ZSIO:Implicitly Opened state

### ZSEO:Explicitly Opened state

### ZSC:Closed state

### ZSF:Full state

### ZSRO:Read Only state

### ZSO:Offline state

* 沒有任何狀態可以從 `ZSO` 轉到其它的 `zone state`

> 備註 : ZSE 可以轉變到到任何的 zone state。不過，一個命令被控制器處理也會造成不同狀態轉換，例如 : 處理一個寫入命令後，會從 ZSC:ZSIO，然後再從 ZSIO:ZSF (可以參考 Zone State Machine)。

(需要修改內容)

* 如果一個 `zoned namespace` 被兩個其中一個命令所執行(Format NVM 或是 NS Management)，zone namespace 初始化後，就會進入到 ZSO 或是 ZSE 其中一個狀態 

* zone namespace 在可以有效地轉換到各個狀態之前，前提需要有被執行 formatted 或是 created by NS managemnt 才可以轉換到各個狀態

---

## Zone Management Send command

(說明) Host 可以透過 `Zone Management Send` 控制 Zone State 切換到不同的狀態。

(用途) 

(尚未完成 ...)

### Zone Send Actions

#### Close Zone

說明 : 

* Select All Bit 
  * 1 : 
  * 0 : 



---

A ZNS SSD may impose a limit on the maximum number of zones that can be active. This limit is always equal or larger than the limit on the maximum number of open zones.

This new limit imposes new constraints on user applications. While the maximum number of open zones of a namespace only limits the number of zones that an application can simultaneously write, the maximum number of active zones imposes a limit on the number of zones that an application can choose for storing data. If the maximum number of active zones is reached, the application must either reset or finish some active zones before being able to chose other zones for storing data.

(說明) ZNS 限制  an applications 可以同時寫入 open zones 最大數量，以及 an applications 可以選擇 active zones 最大數量。如果 active zones 已經達到最大數量，若是該應用程式想要選擇其它的 zones 操作， 必須要先執行 `reset` 或是 `finish` some active zones 

Similar to the limit on the maximum number of open zones, a limit on the maximum number of active zones for a namespace does not affect read operations. Any zone that is not offline can always be accessed for reading regardless of the current number of open and active zones.

(說明) 最大 active zones 數量的限制，並不會影響讀取操作。無論目前是 open and active zones 數量是多少，任何一個 zone 只要不是在 offline 狀態下，都可以讀取資料。

---

## 疑問待了解 

* 所以可以建立多個 Zoned NS，每個 NS 都可以包含多個 Zone
* 若是成立，每個 NS's Zone 編號都依順序編號 ?
  * NS1 : zone 1, 2, 3, 4, 5
  * NS2 : zone 1, 2, 3, 4, 5
* Implicitly and Explicitly Opend 是不是只有 Implicitly Opend 可以寫入資料 ?

