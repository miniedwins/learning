# NVM Set

## 基本介紹

NVM Set 就是一組邏輯上與物理上的集合，每一個 Set 可以集合單一個 namespace 或是多個不同的 namespaces。而一個 namesapce 只允許在一個 NVM Set 裡面，不能同時存在多個 Sets 之中。

下圖顯示不同 NVM Set 所包含的 namespaces，NVM Set A 包含了 (NS A1, NS A2, NS A3)，而 NVM Set B 包含了 (NS B1 and NS B2)，最後 NVM Set C 只包含了 (NS C1)。而且每一個 Set 都可以包含未分配的 namespace 空間。

**NVM Sets and Associated Namespaces**

![NVM Sets](https://github.com/miniedwins/learning/blob/main/nvme/pic/NVM_Sets_and_Associated_Namespaces.png)



## 檢查控制器是否支援

說明 : 發送 Identify Controller 命令來確認是否有支援 NVM Sets。

- Controller Attributes (CTRATT) :
  - 99:96 Bytes : Bit 2 (NVM Sets)
    - 0 : Don't Support
    - 1 : Support

![](https://github.com/miniedwins/learning/blob/main/nvme/pic/identify_controller/Identify_Controller_CTRATT_Bit2_NVM_Sets.png)

發送命令 : 

~~~python
# 備註: 尚未驗證命令是否有誤 !!!

nvme id-ctrl | grep CTRATT
~~~

