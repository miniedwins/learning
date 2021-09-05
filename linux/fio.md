# Linux FIO



## 主要功能

- Performance Test
- Build Test Script
- BurinIn Test
- Quality of Service



## 參數說明

### Main 

~~~shell
[--name=str]
測試的專案名稱, 必需要加該參數

[--filename=str]
測試端的磁碟掛載點 ("/dev/sda"), 或是指定掛載點的目錄結構("/home/hero/test_file")

[--numjobs=int ] (defaults=1)
設定要開啟多少個線程數, 通常搭配 --thread 使用

[--iodepth=int]
一個時間內可以產生多少個 I/O (default=1), 通常會配合 numjobs 
example: --thread --numjobs=4 --iodepth=8 (total=4*8=32)

[--thread]
使用多線程模式

[--runtime=int]
測試的時間, 基本單位 (s, h, m, H, M), 若沒有設定則會依據磁碟掛載點的容量, 然後讀/寫完後停止

[--size=int]
測試的檔案大小為, 或是百分比(%)來表示寫入資料大小, 若沒有設定則會依據磁碟掛載點的容量, 然後讀/寫完後停止
Example: 100G or 100%

[--time_based]
直到runtime時間結束才會停止 (即使所有capacity都已經完全被讀/寫完)

[--group_reporting]
測試的結果會一次整合所有的數據, 並不會分散顯示報告 (若是有開多個任務參數 --numjobs, 最好是設定該參數)
~~~



### I/O Type

~~~shell
[--direct=int] (defaults=1)
If value is true, use non-buffered I/O. This is usually O_DIRECT

[buffered=bool] (Defaults=true)
If value is true, use buffered I/O. This is the opposite of the direct option.

[--ioengine=str]
Defines how the job issues I/O to the file.

libaio :
Linux native asynchronous I/O. Note that Linux may only support queued behavior with non-buffered I/O (set direct=1 or buffered=0). This engine defines engine specific options.

sync : 
Basic read(2) or write(2) I/O. lseek(2) is used to position the I/O location. See fsync and fdatasync for syncing write I/Os. (若是需要此用 fsync or fdatasync, I/O Engine 就必須要使用 sync)

[--rw="str"]
read : Sequential reads
write  Sequential writes
randread : Random reads 
randwrite : Random writes
rw, readwrite : Mixed sequential reads and writes
randrw: Mixed random reads and writes

[rwmixread=int]
mixed read 的比例為多少, default=50% (50% read + 50% write)
Example: rwmixread=30 (Read=30%, Write=70%)

[rwmixwrite=int ]
mxied write 的比例為多少, default=50% (50% write + 50% read)
Example: rwmixwrite=30 (Write=30%, Read=70%)

[--offset=int]
指定想要移動到哪個位置 (offset) 讀取或是寫入

Example: 
(1) offset=20%
(1) offset=1G

[--overwrite=bool] (Default=0)
If true, writes to a file will always overwrite existing data. If the file doesn’t already exist, it will be created before the write phase begins. If the file exists and is large enough for the specified write phase, nothing will be done.

[--randrepeat=bool] (Default=1)         
Seed the random number generator used for random I/O patterns in a predictable way so the pattern is repeatable across runs. Default: true.

[--randseed=int]
Seed the random number generators based on this seed value, to be able to control what sequence of output is being generated. If not set, the random sequence depends on the randrepeat setting.

[--norandommap]
Normally fio will cover every block of the file when doing random I/O. If this option is given, fio will just get a new random offset without looking at past I/O history.This means that some blocks may not be read or written, and that some blocks may be read/written more than once.
~~~



### I/O  Size

~~~shell
===============================================
[--bs=int] (default=4k)
blocksize or I/O size 
若是有包含寫入行為, 需要設定混合寫入 --rw=rw or randw

Example : 
(1) bs=256k (means 256k for reads, writes and trims.)
(2) bs=8k,32k (means 8k for reads, 32k for writes and trims.)
(3) bs=8k,32k, (means 8k for reads, 32k for writes, and default for trims.)
(4) bs=,8k (means default for reads, 8k for writes and trims.)
(5) bs=,8k, (means default for reads, 8k for writes, and default for trims.)

===============================================
--bsrange=irange[,irange]
設定一個區間, 若是有包含寫入行為, 需要設定混合寫入 --rw=rw or randw

Example : 
(1) bsrange=1k-4k,2k-8k # (read, write)

===============================================
[--bssplit=str] (blocksize/percentage)
依百分比例的方式來設定, 若是有包含寫入行為, 需要設定混合寫入 --rw=rw or randw

Example:
(1) bssplit=4k/10:64k/50:32k/40 (10% 4k blocks, 50% 64k blocks, 40% 32k blocks)
(2) bssplit=4k/50:1k/:32k/ (50% 4k ios, and 25% 1k and 32k ios)
(3) bssplit=2k/50:4k/50,4k/90:8k/10 (50% 2k reads and 50% 4k reads, 90% 4k writes and 10% 8k writes)
~~~



### I/O Rate

~~~shell
[--rate=int[int,int]]
固定輸出頻寬(BW)

Example :
(1) --rw=rard --rate=500k (r=1024KiB/s)
(2) --rw=rw --rate=1m,500k (r=1032KiB/s,w=496KiB/s)

[--rate_iops=int]
固定輸出的吞吐量(IOPS)

Example :
(1) --bs=4k --rw=write --rate_iops=1000 (IOPS=0-1000)
(1) --bs=4k --rw=rw --rate_iops=1000 (IOPS=0-2000)
~~~



### Verification

~~~shell
[--verify=str] (md5, crc64, crc32, ..., pattern, null)
I/O Stress, 可以使用該參數驗證資料是否有錯誤, 有很多驗證方法, 沒有全列
md5= "Use an md5 sum of the data area and store it in the header of each block."
pattern= "使用指定的 pattern 驗證資料是否有誤, 搭配參數 --verify_pattern=str"

[--verify_pattern=str]
指定一組固定的 pattern, 驗證資料是否正確

Example :
(1) buffer_pattern="0x55AA"
(2) buffer_pattern="abcd"
(3) buffer_pattern=-12

[do_verify=bool] (default=true)
執行 write 之後做資料的驗證 (官方只有指定 write 有效, random write 不確定是否有效)
~~~



### Buffers and memory

~~~shell
[--buffer_pattern=str]
指定只寫入一組固定的 pattern
Example :
(1) buffer_pattern="0x55AA"
(2) buffer_pattern="abcd"
(3) buffer_pattern=-12

[--refill_buffers]
默認情況下，fio 會在測試開始時創建用於產生成測試文件的資料，並一直重用這些數據。
如果設定這個參數後，會在每次 I/O 提交後重新產生新的資料，保證測試文件內容有充分的隨機性。

[invalidate=bool]
Invalidate the buffer/page cache parts of the files to be used prior to starting I/O if the platform and file type support it. Defaults to true. This will be ignored if pre_read is also specified for the same job.
~~~



### Target file and device

~~~shell
[nrfiles=int] (Defaults=1)
Number of files to use for this job. Defaults to 1. 
說明 : 執行時不要指定 --filename=str，否則只會產生單一個檔案

Example1 : --name=test --numjobs=2 --size=100M --nrfiles=5
說明 : 每個執行的任務建立五個檔案，所以總共產生10個檔案 (2*5=10)，並且同時寫入資料
備註 : 每個檔案平均會分配大小為 20MBytes (100M/5)

Example2 : --name=test --numjobs=2 --size=100M --nrfiles=1
說明 : 每個執行的任務建立一個 100M 檔案，所以總共產生2個檔案(2*1=2)，並且同時寫入資料

[openfiles=int]
Number of files to keep open at the same time. Defaults to the same as nrfiles, can be set smaller to limit the number simultaneous opens.

Example : --name=test --numjobs=1 --size=100M --nrfiles=5 openfiles=1
說明 : 限制每個執行的任務只能依序一次寫入一個檔案內容 (file.0 -> file.1 -> file.2)
~~~



### Other

~~~shell
[--ramp_time=int]
設定 ramp_time 會讓測試開始的一段時間不統計到整體效能裡, 主要是為了避開快取, 影響真正統計效能.

[--bwavgtime=int]
設定測試時間的平均值, 以millisecond(ms)為單位。
~~~



## 測試腳本

### test-mysql

~~~shell
[global]
runtime=86400
time_based
group_reporting
directory=/your_dir
ioscheduler=deadline
refill_buffers

[mysql-binlog]
filename=test_mysql_bin.log
bsrange=512-1024
ioengine=sync
rw=write
size=24G
sync=1
rw=write
overwrite=1
fsync=100 
rate_iops=64
invalidate=1
numjobs=64

[innodb-redolog]
filename=test_innodb_redo.log
bsrange=512-2048
ioengine=sync
rw=write
fsync=1
size=2G
rate_iops=64
overwrite=1
nrfiles=2
openfiles=1
invalidate=1
numjobs=2

[innodb-trxlog]
filename=test_innodb_undo.log
bsrange=512-2048
ioengine=sync
rw=write
size=8G
fsync=1
overwrite=1
rate_iops=64
invalidate=1
numjobs=2

[innodb-data]
filename=test_innodb.dat
bs=16K
ioengine=psync
rw=randrw
size=220G
direct=1
rwmixread=80
numjobs=4

thinktime=600
thinktime_spin=200
thinktime_blocks=2
~~~
