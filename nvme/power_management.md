# Power Management



## 電源管理介紹

主要功能是允許主機 (Host) 可以靜態或是動態管理 **NVM Subsystem Power**。

下列說明靜態與動態之間的不同 : 

* `Static Power Management ` 

  靜態電源管理由主機 (Host) 決定分配 NVM subsystem 的最大電源，並將 NVM Express 的電源狀態設定成該耗電量或更少的電量模式。

  

* `Dynamic Power Management`

  動態電源管理由主機 (Host) 決定切換到最適合的電源狀態。Power Manager 會根據這 Power Objective & Performance Objective 做為參考標準，並動態的切換符合的電源模式。

  

  ![](https://github.com/miniedwins/learning/blob/main/nvme/pic/dynamic_power_management.png)



## 電源階段描述 (Power State)

描述各個電源階段表格，說明每個階段有不同的最大電源消耗 (MP)，進入 (Enter) 或是離開 (Exit) 該電源階段的延遲時間，以及不同階段的 `I/O` 效能 (Performance) 與延遲 (Latency) 時間的處理能力。數字越小代表者效能越好，相對的功耗也會越大。

下圖表格是描述各個電源階段的功耗與效能 (參考表格並非真實數據)

![](https://github.com/miniedwins/learning/blob/main/nvme/pic/power_state_descriptor_table.png)

一個控制器最大可以支援 32 個電源狀態，可以發送命令 identify controller 取得 **Number of Power States Supported (NPSS)** 控制器支援數量。目前現階段的應用並不會使用這麼多，根據目前大廠所支援的狀態大多都是 `PS0 ~ PS4`。 `PS0`模式代表最大電源消耗，意思就是說處在這個電源模式下可以發揮工作最大效率，`PS3 & PS4` 模式表示低電源消耗，又稱為 Non-Operational Power States (NOPS) ，若是處在 `PS4` 電源狀態下，則該電源消耗是最低的。

*備註 : 每個控制器最少都要支援一個電源狀態，那就是 PS0。*

> 補充 : 有些廠商的控制器韌體只有支援 PS0，可能的原因那就是客戶不考慮耗電量的問題，希望在工作效率上能夠全速運行，並且能夠維持在相對的效能。



若是要了解控制器提供表格的內容，可以發送命令 identify controller 取得電源資訊內容，以下是部份電源表格結構 : 

![](https://github.com/miniedwins/learning/blob/main/nvme/pic/identify_controller/Identify_Controller_Power_State_Descriptor.png)

然後再去尋找每個電源狀態的資料結構的說明，如下圖是部份表格 :

![](https://github.com/miniedwins/learning/blob/main/nvme/pic/identify_controller/Identify_Controller_Power_State_Descriptor_Data_Structure.png)



## 非操作電源模式 (NOPS)

Non-Oprtaional Power States (NOPS)，定義是當控制器沒有任何 I/O 命令需要處理，並且閒置了一段時間後，就會進入到非操作電源模式。因為是主機 (Host) 自動切換電源狀態，前提條件下必須要啟用 `APST Feature`。

從主機的角度來看，就是沒有任何 `Pending I/O` 提交到控制器，主機就會發送 `Set Features Cmd` 切換目前的 **power state to non-operational power state**，在這段命令還沒執行完畢前，是不會再提交任何的 I/O 命令。因為控制器是平行處理 (parallel) 各種不同的命令，若是同時執行 `Admin & IO` 命令 ，可能會導致切換到不可預期電源狀態。

值得注意的一點，無論 `APST`是否有被啟用， 一旦電源狀態位在 `NOPS` 狀態下，當有任何的 I/O 命令被提交，控制器必須要切換到最近的 **operational power state**。

例如 : 電源狀態位在 `PS4` 的時候，若是控制器有收到 I/O 命令，就可能會將目前的電源狀態切換到 `PS0` 或其它能夠運行 I/O 命令的電源狀態，因為`NOPS` 狀態是不允許處理 I/O 命令 。比較正確的說法，當有一個 **I/O Submission Queue Tail Doorbell** 暫存器的值被主機寫入，代表有 I/O 命令需要被控制器提取以及處理。

當位在 NOPS 狀態，控制器還是可以運行其它非 I/O 命令，例如 : 閒置時候的背景操作，這個時候可能會超過控制器宣告該電源狀態的最大功耗(MP)，以下的操作是可以在 NOPS 狀態中運行 :

- servicing a memory-mapped I/O (MMIO) 
- configuration register access
- processing a command submitted to the Admin Submission Queue 

根據上述的結論，若是控制器有支援 **Non-Operational Power State Permissive Mode**，是可以允許控制器暫時超過該電源階段所宣告的最大功耗 (MP)。它的條件是在 `NOPS` 狀態下，允許背景執行以上所說的非 I/O 操作。

![](https://github.com/miniedwins/learning/blob/main/nvme/pic/non_operational_power_state_config.png)

*備註 : Non-Operational Power State Permissive Mode Disable 暫時看不懂*



## 自動電源狀態切換 (APST)

**Autonomous Power State Transitions (APST)** 提供主機一個電源狀態自動切換的機制，能讓主機可以切換電源階段 (a non-operational power state may autonomously transition to another non-operational power state)。它的進入的條件是當控制器連續閒置 (Idle) 一段時間，並且超過所指定的閒置時間，主機就會轉換電源狀態到 `NOPS`。

注意 : 如果電源階段是在 **Non-Operational States (NOPS)**，這個時候控制器可能會去運行像是 **Device Self-Test (DST)** 操作，那就可能會超過控制器所宣告該電源階段的最大功耗值 (MP)，此時控制器不應該切換到 NOPS。

*備註 : Controller idle means that there are no commands outstanding to any I/O Submission Queue*

