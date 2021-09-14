# Endurance Groups

Endurance 可以管理 Single NVM Set 或是管理多個 NVM Sets，每一個 Group 都會有一個 ID 編號，標示目前有哪些 NVM Sets 是位在該哪一個 Group，而每一個 NVM Set 的屬性 (Endurance Group Identifier)，描述是屬於哪一個 Endurance Group。

NVMe Group ID 的設置，這個可以讓SSD進行磨損均衡的管理。如果只有一個NVM Set 和 Endurance Group ID關聯，磨損均衡范圍不能跨越該Set，也就是多個 Sets 只能可以被一個 Group 管理，但是主機端可以選擇跨 Set 進行壽命管理。

**NVM Sets and Associated Namespaces**

![Endurance Groups](https://github.com/miniedwins/learning/blob/main/nvme/pic/NVM_Sets_and_Associated_Namespaces.png)



## 檢查是否支援

說明 : 發送 Identify Controller 來確認是否有支援 Endurance Groups

* 檢查控制器是否有支援 Endurance Groups
* Controller Attributes (CTRATT) : 
  * 99:96 Bytes : Bit 4 (Endurance_Groups)
    * 0 : Support
    * 1 : Don't support

![endurance_group](https://github.com/miniedwins/learning/blob/main/nvme/pic/identify_controller/Identify_Controller_CTRATT_Bit4_Endurance_Groups.png)

發送命令 : 

~~~shell
nvme id-ctrl | grep CTRATT
~~~



## 確認最大支援數量

說明 : 每個 Groups 都會擁有一組 Id 編號，發送 Identify Controller 來確認該控制器最大支援多少個數量

* 檢查控制器最大支援數量 Endurance Group Identifier Maximum
  * 341:340 Bytes : Endurance Group Identifier Maximum (ENDGIDMAX)

![Identifier Maximum](https://github.com/miniedwins/learning/blob/main/nvme/pic/identify_controller/Identify_Controller_Endurance_Group_Identifier_Maximum.png)

發送命令 : 

~~~shell
nvme id-ctrl | grep ENDGIDMAX
~~~

