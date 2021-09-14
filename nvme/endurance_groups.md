# Endurance Groups



## 檢查是否支援

* 檢查控制器是否有支援 Endurance Groups
* Controller Attributes (CTRATT) : 
  * Bit 4 (Endurance_Groups)
    * 0 : Support
    * 1 : Don't support

![endurance_group](https://github.com/miniedwins/learning/blob/main/nvme/pic/identify_controller/Identify_Controller_CTRATT_Bit4_Endurance_Groups.png)

發送命令 : 

~~~shell
nvme id-ctrl | grep CTRATT
~~~



