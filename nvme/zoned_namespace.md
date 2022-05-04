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

> Host 可以使用 `Zone Management Receive` 命令，取得一個或是多個 Zone Descriptor。

### Zone Characteristics

首先說明 `Write Pointer (WP)` 屬性，它是定義在 Zone Descriptor，表示 Zone 下一個可以寫入資料的邏輯地址，若是該 Zone 處在不可寫入的狀態，控制器則會回報錯誤。Zone Namespace 會對於每一個 Zone 區域維護 WP，所以當有資料寫入到，Zone會從當前所記錄的 WP 位址開始寫入。

> Host 可以使用 `Zone Management Receive` 命令取獲得目前的 WP 位址。

***(待確認行為是否為真)***
每次寫入操作都會增加 WP 屬性的值，因此在這幾個狀態 (ZSE, ZSIO, ZSEO, ZSC) 一但資料成功寫入後，都會增加 WP。若是當前寫入的資料，已達該 Zone 最大的邏輯位址，就無法再繼續寫入資料，並且該狀態會轉變成 Read Only state (ZSRO)。 

下圖說明當前的 Zone State 的狀態下，WP 在那些狀態是有效以及無效。

![](https://github.com/miniedwins/learning/blob/main/nvme/pic/zone/zone_characteristics.png)

可以先看到 ZSE (Empty State)，標示是有效的 WP，但是為什麼 Active & Open Resources 都是無效 ? 因為還在 ZSE 狀態下，尚未有任何資料寫入，因此 Active & Resource 都是無效的 WP。而當資料已經有被寫入到 Zone，這個時候的 Zone State，會轉狀態到 Active OR Open，這個時候 WP 才會有是有效。

ZSF, ZSRO, ZSO 這幾種狀態它們的 WP 都不是有效的，因為這些狀態下它們都無法在寫入任何資料，WP 自然就會是無效。所以當在這幾個狀態下，如果發送出寫入命令，該命令會被控制器忽略(Abort) 並且回傳無效的狀態碼。

若是 Zone's WP 已經指向達最大可以寫入的位址 (LBA)，可以發送`Zone Management Send command`，設定參數 Zone Send Action 04h，表示要 Reset Zone，命令執行成功後，可以從 Zone Descriptor 觀察 WP 是否被設定成 ZSLBA。

***Zone 寫入與讀取命令的注意事項 :***

**寫入命令**

* 寫入命令 (Address-Specific Write) 的開始邏輯位址，沒有等於 WP 所指定的位置
* 寫入命令 (Zone Append) 並且指定 ZSLBA，但是 ZSLBA 並不是 Zone 的最低起始位址

以上這兩點都會造成控制器忽略該命令，並且回傳無效的狀態碼。

**讀取命令**

* 如果在 ZSO (Zone offline) 發送讀取命令，則控制器會回傳狀態碼 (Zone offline)
* 如果 Across Zone Boundaries 設定為 "1"，則讀取的邏輯位置，可以讀取超過該 Zone 的邏輯位址。代表可以讀取的範圍可以超過該 Zone 的範圍，因此可以讀取更多的資料 ***(尚未確定功能是否可行)***

## 狀態機制

這是 Zone 的狀態機制圖，每一個 Zone 都一定會處在其中一個狀態，而系統會藉由不同狀態的切換來管理資源。所以在同一時間內資源是有限的，並且有部份的 Zones 可能會處在不可以寫入的狀態下，不過它是可以讀取的。

![](https://github.com/miniedwins/learning/blob/main/nvme/pic/zone/zone_state_machine.png)

### Empty state (ZSE) 

一開始初始化的 Zone 都會進入到 ZSE 狀態，這也代表儲存空間沒有任何寫入資料。

***(待確認行為是否為真)***
Zone 可以有效地轉換到各個狀態之前，前提需要格式化 (Format CMD)，或是執行建立 Namespace (Namespace Managent CMD)，因此初始化的狀態可能會是 ZSE 或是 ZSO。

### Closed state (ZSC) 

處在關閉的狀態下，可以讀取資料但無法寫入資料。若是需要寫入資料就必須要轉態到 ZSIO or ZSEO。

### Full state (ZSF) 

可寫入的邏輯位址 (LBA) 已經達到 Zone 的容量上限，就會進入 Full 狀態。

### Read Only state (ZSRO)

在這個狀態下，無法寫入只可以讀取資料。

### Offline state (ZSO)

處在離線的狀態，無法讀寫任何資料。

### Implicitly Opened (ZSIO) 

當系統直接發送寫入命令，當前 Zone 會自動進入到 ZSIO，關閉的方式也會是自動。這麼做的原因是控制器可以隨時關閉此區，有效的管理資源，避免資源使用不足。

### Explicitly Opened (ZSEO) 

通過管理命令 (Zone Management Send command) 透過顯示打開的方式進入到 ZSEO 區域，不過關閉的時候，需要使用管理命令關閉 Zone。

***(待確認行為是否為真)***
如果打開的區域數量達到最大值，並且它們都是顯式打開的，那麼任何打開新區域的嘗試都將失敗。如果其中一些區域只是隱式打開的，那麼嘗試打開一個新區域將導致SSD關閉其中一個隱式打開的區域。

> 備註 : 控制器並不會自動關閉 ZSEO 區域

## 資源管理

* Active : 表示最大有多少個 Zones 的資源可以使用
* Opend : 表示最大可以打開多少個 ZSIO & ZSEO 數量
* Maximum : (Opend Zones + Closed Zones) <= Active Zones

![](https://github.com/miniedwins/learning/blob/main/nvme/pic/zone/zone_resource.png)

例如 : 如果控制器處理一個命令，需要將 Zone 轉態到 ZSIO、ZSEO、ZSC，如果 Resource 已經沒有可使用空間，若是打開超過 Active 或是 Opend 的最大限制，則控制器會終止命令，並且回傳錯誤的狀態碼 (e.g.：Too Many Active Zones or Too Many Open Zones)

若是 Zoned namespace 轉變成寫入保護 (write protected) 的狀態， 則在活動區所有的 Zones 都會轉態成 ZSF。


## 狀態轉換

ZSE:Empty state

ZSIO:Implicitly Opened state

ZSEO:Explicitly Opened state

ZSC:Closed state

ZSF:Full state

ZSRO:Read Only state

ZSO:Offline state

* 沒有任何狀態可以從 `ZSO` 轉到其它的 `zone state`

> 備註 : ZSE 可以轉變到到任何的 zone state。不過，一個命令被控制器處理也會造成不同狀態轉換，例如 : 處理一個寫入命令後，會從 ZSC:ZSIO，然後再從 ZSIO:ZSF (可以參考 Zone State Machine)。

(需要修改內容)

* 如果一個 `zoned namespace` 被兩個其中一個命令所執行(Format NVM 或是 NS Management)，zone namespace 初始化後，就會進入到 ZSO 或是 ZSE 其中一個狀態 

* zone namespace 在可以有效地轉換到各個狀態之前，前提需要有被執行 formatted 或是 created by NS managemnt 才可以轉換到各個狀態

---

## Zone Management Send command

---

A ZNS SSD may impose a limit on the maximum number of zones that can be active. This limit is always equal or larger than the limit on the maximum number of open zones.

This new limit imposes new constraints on user applications. While the maximum number of open zones of a namespace only limits the number of zones that an application can simultaneously write, the maximum number of active zones imposes a limit on the number of zones that an application can choose for storing data. If the maximum number of active zones is reached, the application must either reset or finish some active zones before being able to chose other zones for storing data.

(說明) ZNS 限制  an applications 可以同時寫入 open zones 最大數量，以及 an applications 可以選擇 active zones 最大數量。如果 active zones 已經達到最大數量，若是該應用程式想要選擇其它的 zones 操作， 必須要先執行 `reset` 或是 `finish` some active zones 

Similar to the limit on the maximum number of open zones, a limit on the maximum number of active zones for a namespace does not affect read operations. Any zone that is not offline can always be accessed for reading regardless of the current number of open and active zones.

(說明) 最大 active zones 數量的限制，並不會影響讀取操作。無論目前是 open and active zones 數量是多少，任何一個 zone 只要不是在 offline 狀態下，都可以讀取資料。

---

## 疑問待了解 

* 若是成立，每個 NS's Zone 編號都依順序編號 ?
  * NS1 : zone 1, 2, 3, 4, 5
  * NS2 : zone 1, 2, 3, 4, 5
* Implicitly and Explicitly Opend 是不是只有 Implicitly Opend 可以寫入資料 ?

