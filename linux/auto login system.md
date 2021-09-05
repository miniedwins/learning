# 使用者帳號自動登入

首先編輯檔案 `getty@.service`  

~~~shell
sudo vim /lib/systemd/system/getty@.service
~~~

找到後註解此行

~~~shell
ExecStart=-/sbin/agetty -o '-p -- \\u' --noclear %I $TERM
~~~

將以下列設定寫入到檔案中

myusername : 更改成登入的使用者帳號

*注意 : 如果是登入帳號是 `root`，需要先設定`root`密碼*

~~~bash
ExecStart=-/sbin/agetty --noissue --autologin myusername %I $TERM
~~~

啟動服務後，然後重新開機生效。

~~~bash
sudo systemctl start getty@ttyN.service
sudo reboot
~~~

