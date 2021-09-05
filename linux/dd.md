# Linux DD



## 主要功能

- Performance Test (Simple)

- Read & Write Sectors

- Dump Sector Data

- Backup & Recovery Disk Data or Parttion

  

## 常用參數

### option

- `if=FILE`： read from FILE instead of stdin
- `of=FILE`：write to FILE instead of stdout
- `ibs=BYTES`：read up to BYTES bytes at a time (default: 512)。
- `obs=BYTES`：write BYTES bytes at a time (default: 512)
- `bs=BYTES`： read and write up to BYTES bytes at a time (default: 512); overrides ibs and obs
- `count=N`： copy only N input blocks
- `iflag=FLAGS` : read as per the comma separated symbol list
- `oflag=FLAGS` ： write as per the comma separated symbol list
- `seek=N`：skip N obs-sized blocks at **start of output**
- `skip=N`：skip N ibs-sized blocks at **start of input**

### flag & conv

- **iflag=nocache**

  Request to drop cache. 

  

- **oflag=sync**

  Use synchronized I/O for **both data and metadata**.

  備註 : 每次 **write** 調用會自動將 **data 和 metadata** 同步到儲存裝置

  

- **oflag=dsync**

  Use synchronized I/O for data. For the output file, this forces a physical write of **output data on each write**. 

  備註 : 僅當檔案屬性需要更新以反映檔案資料變化（例如，更新檔案大小以反映檔案中包含了更多資料）時，O_DSYNC標誌才影響檔案屬性。

  

- **oflag=fsync** 

  Synchronize output **data and metadata** **just before finishing**. This forces a physical write of **output data and metadata**.

  備註 : 

  - 除了同步檔案的修改內容（dirty page），fsync還會同步檔案的描述資訊（metadata，包括size、訪問時間等等），因為檔案的資料和metadata通常存在硬碟的不同地方，因此fsync至少需要兩次IO寫操作，多餘的一次IO操作
  - 為了滿足事務要求，資料庫的日誌檔案是常常需要同步IO的。由於需要同步等待硬碟IO完成，所以事務的提交操作常常十分耗時，成為效能的瓶頸
  - fsync效能較低。但是如果需要使用 **fdatasync** 減少對 **metadata** 更新，需要確保檔案的大小在寫入前後沒有發生變化。

  

- **oflag=fdatasync**

  Synchronize output data **just before finishing**. This forces a physical write of **output data**.

  備註 : 

  - fdatasync does not flush modified metadata unless that metadata is needed in order to allow a subsequent data retrieval to be corretly handled.

    

- **oflag=direct** 

  **Use direct I/O for data, avoiding the buffer cache.** Note that the kernel may impose restrictions on read or write buffer sizes.
  
  

## 磁碟操作

### Write

#### 備份整顆硬碟

~~~shell
dd if=/dev/sda of=/dev/sdb
~~~

#### 備份 MBR 分區

~~~shell
dd if=/dev/sda of=mbr.img bs=446 count=1
~~~

#### 恢復 MBR 分區

~~~shell
dd if=mbr.img of=/dev/sda
~~~

#### 建立固定大小檔案

~~~shell
dd if=/dev/urandom of=tmp.dat bs=4096 count=1
~~~

#### 寫入固定大小資料

沒有指定從哪個地方開始寫入資料，會從 LBA=0 開始

~~~shell
dd if=/dev/urandom of=/dev/sda bs=4096 count=1
~~~

#### 寫入資料到指定的 LBA (seek)

~~~shell
sudo dd if=/dev/urandom of=/dev/sdb bs=512 seek=1 count=1
~~~

使用 hexdump 查詢剛剛寫入到磁碟  `sdb` 的結果

~~~shell
hexdump -C -n 4096 /dev/sdb
~~~

輸出結果 : 寫入的時候跳過一個 LBA，所以 LBA=0 是沒有任何資料的

~~~shell
00000000  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
*
00000200  d6 33 81 d8 b5 4b f3 4d  04 d8 e1 4b 3e 35 c5 43  |.3...K.M...K>5.C|
00000210  93 04 be fe 37 48 6b 0a  1d ad 8c 6d 1b 13 6b c8  |....7Hk....m..k.|
00000220  34 7a 61 22 68 89 7a be  71 a3 1d e5 5d 1c c6 06  |4za"h.z.q...]...|
00000230  e9 25 8b 1b d7 62 1e 2c  a7 a1 85 d6 8b f8 ec 7e  |.%...b.,.......~|
00000240  29 f8 9b 0e 35 20 e0 c7  1a 1c 9b e9 f6 82 c0 a9  |)...5 ..........|
00000250  cf 1f 39 b0 83 50 10 55  36 aa 86 50 23 72 59 e7  |..9..P.U6..P#rY.|
00000260  25 b2 3f 4c 82 49 6e b4  58 e4 51 9f 34 74 b6 79  |%.?L.In.X.Q.4t.y|
00000270  c4 1e 9f 07 2a b6 32 e0  95 4e fb 2a 44 02 3f 83  |....*.2..N.*D.?.|
00000280  9b bf 6d 35 7e 69 a6 e0  d7 11 07 d0 de 29 76 1e  |..m5~i.......)v.|
00000290  0c 8a ec d4 87 2e c9 41  6c 9b 15 cc 19 78 ff 66  |.......Al....x.f|
000002a0  67 70 63 a1 bf 98 04 3d  10 08 7e 6a 55 45 3f d2  |gpc....=..~jUE?.|
000002b0  c1 e3 88 80 4f 4f 16 67  8b 15 2a ba e2 6e 45 b2  |....OO.g..*..nE.|
000002c0  85 1b 94 ef 26 a7 42 71  25 3e d0 91 81 71 3d 60  |....&.Bq%>...q=`|
000002d0  9b 09 48 6d 3b c1 7c 78  24 47 24 ab c7 04 cb 66  |..Hm;.|x$G$....f|
000002e0  97 98 63 0a cc e9 e8 fc  6d 35 84 cf 8a 61 a5 84  |..c.....m5...a..|
000002f0  58 ed a2 15 f9 79 4a dd  ab 80 5d 49 f4 3f 50 9d  |X....yJ...]I.?P.|
00000300  33 e7 53 9e b2 1f 12 2d  d7 1e 65 de 32 8a da a7  |3.S....-..e.2...|
00000310  0e 41 c2 8b fb 28 29 ac  d2 8c 2e 7f 8c 6b 28 7c  |.A...()......k(||
00000320  53 28 bd 08 a3 31 be ce  93 1e ef 7b a2 97 e0 d9  |S(...1.....{....|
00000330  5c 3a 6d 05 f2 83 b6 18  0f 53 29 7f 63 7e 93 89  |\:m......S).c~..|
00000340  20 c8 14 ac 81 20 b4 03  84 16 28 42 6a 85 af 43  | .... ....(Bj..C|
00000350  43 98 42 d8 b8 71 d7 a4  56 b0 d4 ef f3 d4 8c ba  |C.B..q..V.......|
00000360  a1 e3 f2 89 d2 20 14 12  0e 05 44 f0 11 45 5c 25  |..... ....D..E\%|
00000370  bb 05 0e 34 b1 13 81 30  af 69 58 f7 4d 46 62 4a  |...4...0.iX.MFbJ|
00000380  67 4e 51 03 d4 ae 0a a0  36 4d 21 df 78 1d 51 14  |gNQ.....6M!.x.Q.|
00000390  6f f7 53 97 3d 13 14 33  50 52 24 11 a6 a0 03 17  |o.S.=..3PR$.....|
000003a0  18 1d ee 0b c1 36 ec 4e  eb 4b 79 11 59 94 86 82  |.....6.N.Ky.Y...|
000003b0  23 3e 4e ab 2b e6 8d 8b  61 45 1e 28 c3 e1 a5 ac  |#>N.+...aE.(....|
000003c0  0f 0c 2f 46 2d 0e 0c a5  d1 0b bb 59 7b 41 ca 18  |../F-......Y{A..|
000003d0  b5 c5 51 f7 67 d5 f0 74  b5 7f 6e 82 f8 62 a9 53  |..Q.g..t..n..b.S|
000003e0  2c 99 d3 8b cf f7 44 99  20 9c 0f 29 5c d4 4e 64  |,.....D. ..)\.Nd|
000003f0  32 ca 9e e2 77 3a 30 4a  72 fd fd 9b c0 37 fd 74  |2...w:0Jr....7.t|
00000400  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
*
00001000
~~~



### Read

#### 讀取 LBA 資料 

沒有指定從哪個地方開始讀取資料，會從 LBA=0 開始

~~~shell
dd if=/dev/sda of=lba.dat bs=4096 count=1
1+0 records in
1+0 records out
4096 bytes (4.1 kB, 4.0 KiB) copied, 0.00032281 s, 12.7 MB/s
~~~



#### 讀取 LBA資料 (skip)

skip=value 就是忽略多少個 LBA，然後在讀取資料

~~~shell
dd if=/dev/sdb of=test.dat bs=512 skip=1 count=1
~~~

使用 hexdump 查詢剛剛讀取 `test.dat`資料的結果

~~~shell
 hexdump -C -n 512 test.dat
~~~

輸出結果 : 先前寫入

~~~shell
00000000  d6 33 81 d8 b5 4b f3 4d  04 d8 e1 4b 3e 35 c5 43  |.3...K.M...K>5.C|
00000010  93 04 be fe 37 48 6b 0a  1d ad 8c 6d 1b 13 6b c8  |....7Hk....m..k.|
00000020  34 7a 61 22 68 89 7a be  71 a3 1d e5 5d 1c c6 06  |4za"h.z.q...]...|
00000030  e9 25 8b 1b d7 62 1e 2c  a7 a1 85 d6 8b f8 ec 7e  |.%...b.,.......~|
00000040  29 f8 9b 0e 35 20 e0 c7  1a 1c 9b e9 f6 82 c0 a9  |)...5 ..........|
00000050  cf 1f 39 b0 83 50 10 55  36 aa 86 50 23 72 59 e7  |..9..P.U6..P#rY.|
00000060  25 b2 3f 4c 82 49 6e b4  58 e4 51 9f 34 74 b6 79  |%.?L.In.X.Q.4t.y|
00000070  c4 1e 9f 07 2a b6 32 e0  95 4e fb 2a 44 02 3f 83  |....*.2..N.*D.?.|
00000080  9b bf 6d 35 7e 69 a6 e0  d7 11 07 d0 de 29 76 1e  |..m5~i.......)v.|
00000090  0c 8a ec d4 87 2e c9 41  6c 9b 15 cc 19 78 ff 66  |.......Al....x.f|
000000a0  67 70 63 a1 bf 98 04 3d  10 08 7e 6a 55 45 3f d2  |gpc....=..~jUE?.|
000000b0  c1 e3 88 80 4f 4f 16 67  8b 15 2a ba e2 6e 45 b2  |....OO.g..*..nE.|
000000c0  85 1b 94 ef 26 a7 42 71  25 3e d0 91 81 71 3d 60  |....&.Bq%>...q=`|
000000d0  9b 09 48 6d 3b c1 7c 78  24 47 24 ab c7 04 cb 66  |..Hm;.|x$G$....f|
000000e0  97 98 63 0a cc e9 e8 fc  6d 35 84 cf 8a 61 a5 84  |..c.....m5...a..|
000000f0  58 ed a2 15 f9 79 4a dd  ab 80 5d 49 f4 3f 50 9d  |X....yJ...]I.?P.|
00000100  33 e7 53 9e b2 1f 12 2d  d7 1e 65 de 32 8a da a7  |3.S....-..e.2...|
00000110  0e 41 c2 8b fb 28 29 ac  d2 8c 2e 7f 8c 6b 28 7c  |.A...()......k(||
00000120  53 28 bd 08 a3 31 be ce  93 1e ef 7b a2 97 e0 d9  |S(...1.....{....|
00000130  5c 3a 6d 05 f2 83 b6 18  0f 53 29 7f 63 7e 93 89  |\:m......S).c~..|
00000140  20 c8 14 ac 81 20 b4 03  84 16 28 42 6a 85 af 43  | .... ....(Bj..C|
00000150  43 98 42 d8 b8 71 d7 a4  56 b0 d4 ef f3 d4 8c ba  |C.B..q..V.......|
00000160  a1 e3 f2 89 d2 20 14 12  0e 05 44 f0 11 45 5c 25  |..... ....D..E\%|
00000170  bb 05 0e 34 b1 13 81 30  af 69 58 f7 4d 46 62 4a  |...4...0.iX.MFbJ|
00000180  67 4e 51 03 d4 ae 0a a0  36 4d 21 df 78 1d 51 14  |gNQ.....6M!.x.Q.|
00000190  6f f7 53 97 3d 13 14 33  50 52 24 11 a6 a0 03 17  |o.S.=..3PR$.....|
000001a0  18 1d ee 0b c1 36 ec 4e  eb 4b 79 11 59 94 86 82  |.....6.N.Ky.Y...|
000001b0  23 3e 4e ab 2b e6 8d 8b  61 45 1e 28 c3 e1 a5 ac  |#>N.+...aE.(....|
000001c0  0f 0c 2f 46 2d 0e 0c a5  d1 0b bb 59 7b 41 ca 18  |../F-......Y{A..|
000001d0  b5 c5 51 f7 67 d5 f0 74  b5 7f 6e 82 f8 62 a9 53  |..Q.g..t..n..b.S|
000001e0  2c 99 d3 8b cf f7 44 99  20 9c 0f 29 5c d4 4e 64  |,.....D. ..)\.Nd|
000001f0  32 ca 9e e2 77 3a 30 4a  72 fd fd 9b c0 37 fd 74  |2...w:0Jr....7.t|
00000200
~~~



### flag  and conv

#### oflag=dsync

每一次的寫入都會同步 **data** 到存儲裝置， **sync** 是會同步 **data and metadata** 到存儲裝置

~~~shell
dd if=/dev/zero of=test.iso bs=1024k count=1k oflag=dsync
1024+0 records in
1024+0 records out
1073741824 bytes (1.1 GB, 1.0 GiB) copied, 15.979 s, 67.2 MB/s
~~~

#### oflag=direct

不使用核心的快取，直接往 Block I/O Layer 發送 I/O requested

~~~shell
dd if=/dev/zero of=test.iso bs=1024k count=1k iflag=nocache oflag=direct                    
1024+0 records in
1024+0 records out
1073741824 bytes (1.1 GB, 1.0 GiB) copied, 5.81441 s, 185 MB/s
~~~

#### conv=fsync

命令執行完前，會一次性的同步 **data and metadata** 到存儲裝置

~~~shell
dd if=/dev/zero of=test bs=1024k count=1k conv=fsync
1024+0 records in
1024+0 records out
1073741824 bytes (1.1 GB, 1.0 GiB) copied, 6.00116 s, 179 MB/s
~~~
