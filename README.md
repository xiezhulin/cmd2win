# Copyright
Copyright(c) Guangdong vivo software technology CO.,LTD. Unpublished

Guangdong vivo software technology CO.,LTD.Proprietary & Confidential

This source code and the algorithms implemented therein constitute
confidential information and may comprise trade secrets of vivo
or its associates, and any use thereof is subject to the terms and
conditions of the Non-Disclosure Agreement pursuant to which this
source code was originally received.

# Description
Do operations based on samba quickly on windows by using custom commands on linux terminal<br>
[Usage](https://github.com/xiezhulin/dosmb/blob/master/dosmb)

# Installation
## On Windows
    Put 'smb_monitor.py' into 'C:\Users\Administrator\AppData\Roaming\Microsoft\Windows\Start Menu\Programs',
    ensure the server can started when windows bootcompleted
## On Linux
### 1. Put 'dosmb' into your PATH directory, ensure dosmb can run in any directory
### 2. Set envrironment, it's optional, such as append the following content to ~/.bashrc)
#### 1) Set alias
     $ alias so="dosmb --host 172.25.105.45 open"
     $ alias sod="dosmb --host 172.25.105.45 open_parent_dir"
     $ alias scu="dosmb --host 172.25.105.45 custom"
     $ alias sc="dosmb --host 172.25.105.45 cmp"
     $ alias scl="dosmb --host 172.25.105.45 clip"
 #### 2) Change defaults
     Samba map dirve on windows network defaults to ip-address for your linux(unix) server
     $ export SMB_MAP_DRIVE="y:\\"
     Text editor defaults to notepad
     $ export SMB_TXT_EDITOR="gvim"
     $ export SMB_TXT_EDITOR_SUPPORT_MULTI_FILES=True
     Config windows compare tools, and add the tools to windows' environment, defaults to fc
     $ export SMB_COMPARER="Bcompare"

