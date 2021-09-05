# Windows Boot Process

Windows Boot Process consist of several phases

## Phase I : BIOS initialization

- The firmware identifies and initialize hardware devices and then runs the POST [Power On Self Test].
- After BIOS detects a valid system disk and reads MBR , POST process ends and Start Bootmgr.exe
- Bootmgr.exe finds and runs Winload.exe on Boot partition which is begining of II Phase OS Loader Phase

## Phase II : OS Loader

- Winload.exe [Windows Loader] loads essential system drivers that are required for reading data from disk.
- It initializes windows so that kernel execution should start.
- Once kernel starts OS Loader loads registry hive and additional drivers which are marked as BOOT START.

## Phase III : OS Initialization

OS Initialization phase can be divided into four sub-phases.

### Phase III A : Kernal Initialization [PreSMSS]

- Kernal initializes data structure and components.
- Starts PnP [Plug and Play] manager .
- PnP Manager initializes the Boot Start drivers which was loaded during PHASE II [OS Loader]

### Phase III B : Session Initialization [SMSSInit]

- Kernal passes control from Kernal Initialization[Phase III A ] to Session Manager process [Smss.exe]
- System initializes registry, loads and start the drivers other than Boot Start.
- Starts the subsystem process.
- Control is passed to Winlogon.exe

### Phase III C : Winlogon Initialization [WinLogonInit]

- Winlogon.exe start with User Logon Screen .
- Service control manager starts services.
- Group policy script run during winlogon initialization.

### Phase III D : Explorer Initialization [ExplorerInit]

- This sub-phse starts when Winlogon process passes control to Explorer process [Explorer.exe].
- Subsystem creates Desktop Windows Manager [DWM] process.
- DWM initializes desktop and display for the first time on screen.