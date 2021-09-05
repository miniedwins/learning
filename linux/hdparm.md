# Linux Hdparm

## 主要功能

- Identification
- Performance Test (Simple)
- Read & Write & Trim Sector
- Firmware Download
- ATA Security Feature Set 
- Immediate & Standby & Sleep Command



## 顯示資訊

#### 讀取硬碟資訊 (-i)

**說明** : 顯示的訊息會較為簡易

**命令** : hdparm -i /dev/sda

~~~shell
/dev/sda:

 Model=Micron_M510_MTFDDAK128MAZ, FwRev=MU02, SerialNo=1340039B9B57
 Config={ Fixed DTR>10Mbs }
 RawCHS=16383/16/63, TrkSize=0, SectSize=0, ECCbytes=0
 BuffType=unknown, BuffSize=unknown, MaxMultSect=16, MultSect=off
 CurCHS=16383/16/63, CurSects=16514064, LBA=yes, LBAsects=250069680
 IORDY=on/off, tPIO={min:120,w/IORDY:120}, tDMA={min:120,rec:120}
 PIO modes:  pio0 pio3 pio4
 DMA modes:  mdma0 mdma1 mdma2
 UDMA modes: udma0 udma1 udma2 udma3 udma4 udma5 *udma6
 AdvancedPM=yes: unknown setting WriteCache=enabled
 Drive conforms to: unknown:  ATA/ATAPI-3,4,5,6,7

 * signifies the current active mode
~~~



#### 讀取硬碟資訊 (-I)

**說明** :  顯示的訊息會比較完整

**命令** :  hdparm -I /dev/sda

~~~shell
ㄥdev/sda:

ATA device, with non-removable media
        Model Number:       Micron_M510_MTFDDAK128MAZ
        Serial Number:      1340039B9B57
        Firmware Revision:  MU02
        Transport:          Serial, ATA8-AST, SATA 1.0a, SATA II Extensions, SATA Rev 2.5, SATA Rev 2.6, SATA Rev 3.0
Standards:
        Used: unknown (minor revision code 0x0028)
        Supported: 9 8 7 6 5
        Likely used: 9
Configuration:
        Logical         max     current
        cylinders       16383   16383
        heads           16      16
        sectors/track   63      63
        --
        CHS current addressable sectors:    16514064
        LBA    user addressable sectors:   250069680
        LBA48  user addressable sectors:   250069680
        Logical  Sector size:                   512 bytes
        Physical Sector size:                  4096 bytes
        Logical Sector-0 offset:                  0 bytes
        device size with M = 1024*1024:      122104 MBytes
        device size with M = 1000*1000:      128035 MBytes (128 GB)
        cache/buffer size  = unknown
        Form Factor: 2.5 inch
        Nominal Media Rotation Rate: Solid State Device
Capabilities:
        LBA, IORDY(can be disabled)
        Queue depth: 32
        Standby timer values: spec'd by Standard, with device specific minimum
        R/W multiple sector transfer: Max = 16  Current = 16
        Advanced power management level: 254
        DMA: mdma0 mdma1 mdma2 udma0 udma1 udma2 udma3 udma4 udma5 *udma6
             Cycle time: min=120ns recommended=120ns
        PIO: pio0 pio1 pio2 pio3 pio4
             Cycle time: no flow control=120ns  IORDY flow control=120ns
Commands/features:
        Enabled Supported:
           *    SMART feature set
           *    Power Management feature set
           *    Write cache
           *    Look-ahead
           *    Host Protected Area feature set
           *    WRITE_BUFFER command
           *    READ_BUFFER command
           *    NOP cmd
           *    DOWNLOAD_MICROCODE
           *    Advanced Power Management feature set
                SET_MAX security extension
           *    48-bit Address feature set
           *    Device Configuration Overlay feature set
           *    Mandatory FLUSH_CACHE
           *    FLUSH_CACHE_EXT
           *    SMART error logging
           *    SMART self-test
           *    General Purpose Logging feature set
           *    WRITE_{DMA|MULTIPLE}_FUA_EXT
           *    64-bit World wide name
           *    IDLE_IMMEDIATE with UNLOAD
                Write-Read-Verify feature set
           *    WRITE_UNCORRECTABLE_EXT command
           *    {READ,WRITE}_DMA_EXT_GPL commands
           *    Segmented DOWNLOAD_MICROCODE
           *    Gen1 signaling speed (1.5Gb/s)
           *    Gen2 signaling speed (3.0Gb/s)
           *    Gen3 signaling speed (6.0Gb/s)
           *    Native Command Queueing (NCQ)
           *    Phy event counters
           *    NCQ priority information
           *    READ_LOG_DMA_EXT equivalent to READ_LOG_EXT
           *    DMA Setup Auto-Activate optimization
                Device-initiated interface power management
                Asynchronous notification (eg. media change)
           *    Software settings preservation
                Device Sleep (DEVSLP)
           *    SMART Command Transport (SCT) feature set
           *    SCT Write Same (AC2)
           *    SCT Features Control (AC4)
           *    SCT Data Tables (AC5)
           *    reserved 69[4]
           *    reserved 69[7]
           *    Data Set Management TRIM supported (limit 8 blocks)
           *    Deterministic read ZEROs after TRIM
Logical Unit WWN Device Identifier: 500a0751039b9b57
        NAA             : 5
        IEEE OUI        : 00a075
        Unique ID       : 1039b9b57
Device Sleep:
        DEVSLP Exit Timeout (DETO): 50 ms (drive)
        Minimum DEVSLP Assertion Time (MDAT): 10 ms (drive)
~~~



#### 讀取硬碟溫度 (-H)

**命令** : hdparm -H /dev/sda

~~~shell
/dev/sda:
SG_IO: bad/missing sense data, sb[]:  70 00 05 00 00 00 00 0a 04 51 40 00 21 04 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
 drive temperature (celsius) is:  -18
 drive temperature in range:  yes
~~~



## 磁碟操作

### Read sector

**說明** : Read sector or LBA value 

**命令** : hdparm --read-sector /dev/sda

~~~shell
reading sector 100: succeeded
fef4 22b4 ae9d 4fe7 0145 0b45 137e d045
4419 c224 a78f d536 6c5d 3fe1 d557 474f
e731 663a 8091 ee18 f73d 86a8 de4d 88b1
ac66 327a 85de 2210 8cd9 4a48 fc15 a084
fb15 aac3 614d bbd4 8ede 558b d404 a4eb
eb84 81dd 885d d6e3 96a7 e8c3 99eb b351
7d24 5349 86ac cd5c 45cb 8f18 66d9 fcc3
3705 5b46 bc94 6026 88b4 a94d 8d35 060f
ab3d bada 6ed1 1c45 46ea f854 1ab1 49a5
babd ab7a 3111 2b49 f983 75c0 d65a 2c44
c3d8 512c 0a4e 40b6 d3f4 e1ae 1fc6 7a80
28ac 1e14 0335 67e8 598c 8fe2 7d39 5f32
0eee bb08 ff42 b279 8a78 fb64 ae26 46c2
c0e3 b042 6b54 83e9 b174 4255 f933 0e74
602d b419 b22c 5a73 19db 965c 2f67 3e30
a4eb 4f6a ba2d 6f30 ffaa bb39 1d21 91e1
c564 1392 5854 e0b5 0ba4 a2be 8165 4b67
518d a706 509a a103 a300 b739 aad9 0aab
83bd e8d4 750c b241 df02 226b 10e7 b70c
fb5b 20cb c07d f850 ab89 bffc e243 f817
4da7 2e7e 0f8a 70d9 f041 e49d d593 8f95
568d 8361 169e b18e 9134 bd81 b1e3 252d
5fdc 7235 7ad3 0934 bb7e 2d17 778c 7d45
4917 13ae b45f e0b7 e6e2 c737 e10a 5ba9
56c4 b9f1 aad5 9c3f efd8 5f7b 0d11 54db
d41f 81b7 419e 95e3 e82e 43ec 2e29 5adc
782f 3376 dcde 2306 35c6 81f7 22b9 337e
3bb7 d05f bd3b c50b 3d89 e7fd 78d8 f3be
e563 2dc4 91ed 2a57 a4f7 d6fc 0a4e 455c
162b a20c acf7 4b09 07aa 5521 1b75 a888
6d41 8e17 b8eb 1cb7 aafb bbdc 74f3 0523
a685 aaef bf97 02cb f500 6275 46e3 9274
~~~



### Idle immediate

**說明** : Issue idle immediate

**命令** : hdparm --idle-immediate /dev/sda

~~~shell
/dev/sda:
 issuing idle_immediate command
~~~



### Standby mode (-y)

**說明** : Issue standby cmd

**命令** : hdparm -y /dev/sda

~~~shell
/dev/sda:
 issuing standby command
~~~



### Sleep mode (-Y)

**說明** : Issue sleep cmd

**命令** : hdparm -Y /dev/sda

~~~shell
/dev/sda:
 issuing sleep command
~~~



### Secure Erase

設定 user-master 密碼

~~~shell
hdparm --user-master u --security-set-pass 1234 /dev/sda
~~~

然後使用相同的密碼執行

~~~shell
hdparm --user-master u --security-erase 1234 /dev/sda
~~~



### Write Cache Feature (-W)

**說明** : 讀取或是寫入 Write Cache Feature

**命令** : 

- Read : hdparm -W /dev/sda

  ~~~shell
  /dev/sda:
   write-caching =  1 (on)
  ~~~

- Enable : hdparm -W 1 /dev/sda

  ~~~shell
  /dev/sda:
   setting drive write-caching to 1 (on)
   write-caching =  1 (on)
  ~~~

- Disable : hdparm -W 0 /dev/sda

  ~~~shell
  /dev/sda:
   setting drive write-caching to 0 (off)
   write-caching =  0 (off)
  ~~~

  

## 效能測試

#### 測試硬碟讀取速度 (-t)

說明 : This displays the speed of reading through the buffer cache to the disk  without any prior caching of data.

命令 : hdparm -t /dev/sda

~~~shell
/dev/sda:
 Timing buffered disk reads: 302 MB in  3.05 seconds =  99.11 MB/sec
~~~



#### 測試硬碟讀取速度 (-T)

說明 : This displays the speed of reading directly from the Linux buffer cache without disk access.

命令 : hdparm -T /dev/sda

~~~shell
/dev/sda:
 Timing cached reads:   4970 MB in  1.99 seconds = 2495.91 MB/sec
~~~



#### 測試硬碟速度 (-direct)

說明 : Use the kernel´s "O_DIRECT" flag when performing a -t timing test.  This bypasses the page cache, causing the reads to go directly from the drive into hdparm's buffers, using so-called "raw" I/O

命令 : hdparm -t --direct /dev/sda

~~~shell
/dev/sda:
 Timing O_DIRECT disk reads: 1696 MB in  3.00 seconds = 565.26 MB/sec
~~~

