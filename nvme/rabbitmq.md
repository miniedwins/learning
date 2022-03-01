---
tags: rabbitmq
---

# Rabbitmq 基本介紹

## 簡介

RabbitMq 是實現了高級消息隊列協議（AMQP）。它是一種應用程序對應用程序的通訊方式，應用程序通過寫入訊息到佇列中，將訊息傳遞到佇列中，然後由另一應用程序讀取。

## 工作模式

基本模式如下: 
- Direct
- Worker
- Publish/Subscribe
- Routing
- Topics
- RPC

### **Direct**

簡單的工作模式，只有會一個 `Producer` 會發送訊息到 Queue，而只有一個 `Consumer` 會從 Queue 中拿取消費。

![](https://i.imgur.com/ZkcluxG.png)

### **Worker**

該工作模式中只有一個 `Producer` 會發訊息到 Queue，但是同時可以有多個 `Consumer` 會去消費 Queue 裡的訊息，這個模式可以加快工作的速度。

![](https://i.imgur.com/nITGfgT.png)

一旦有很多非同步的工作，就可以使用該模式部署多台電腦做分散式架構處理。


### **Publish/Subscribe**

先前的模式都是直接發送訊息到 Queue，從這個模式開始會使用到 `Exchange`，中間多了一個代理層。Producer 傳遞的訊息不再是直接傳到 Queue，而是直接發送到 Exchange，然後由 Exchange 決定要將這個訊息傳遞到哪個 Queue。

![](https://i.imgur.com/2BcjaHF.png)

Exchange 分成下列幾種類型 : 
- direct
- topic
- fanout
- headers 

Publish/Subscribe 模式中，Exchange 使用的是 `type=fanout`，它的運作行為是一種廣播模式，當 Producer 將訊息傳遞給 Exchange，然後 Exchange 會把這個訊息傳遞給所有跟 Exchange 有綁定的 Queue。

### **Routing**

Routing 模式中，Exchange 使用的是 `type=direct`，當 Producer 將訊息帶有 routing key 傳遞丟給 Exchange，它就會根據這個 routing key 將訊息正確傳遞到指定的 Queue。

需要注意的是，Queue 在綁定 Exchange 的時候，必須要設定 routing key， 這樣 Exchange 才能夠知道要將這些訊息傳遞到哪個 Queue。

![](https://i.imgur.com/VQUVPRU.png)

Routing 其實是一種路由模式，Queue 它可以個綁定多個 routing key，若是 Producer 傳遞的訊息帶有其中一個 routing key，Exchange 都會將這些訊息傳遞到綁定的 Queue。

### Topics

Topics 模式中，Exchange 使用的是 `type=topic`，它是基於 Routing 模式一樣的行為，並且在 routing key 加入模糊綁定，Exchange 只要匹配關鍵字串，就會傳遞到相對應的 Queue。

![](https://i.imgur.com/ggSOM5T.png)