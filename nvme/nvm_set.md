# NVM Set

## 基本介紹

NVM Set 就是一組邏輯上與物理上的集合，每一個 Set 可以集合單一個 namespace 或是多個不同的 namespaces。而一個 namesapce 只允許在一個 NVM Set 裡面，不能同時存在多個 Sets 之中。

下圖顯示不同 NVM Set 所包含的 namespaces，NVM Set A 包含了 (NS A1, NS A2, NS A3)，而 NVM Set B 包含了 (NS B1 and NS B2)，最後 NVM Set C 只包含了 (NS C1)。而且每一個 Set 都可以包含未分配的 namespace 空間。

**NVM Sets and Associated Namespaces**

![NVM Sets](https://github.com/miniedwins/learning/blob/main/nvme/pic/NVM_Sets_and_Associated_Namespaces.png)