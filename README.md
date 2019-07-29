# Copyright
Copyright(c) xiezhulin\<zdld99170@126.com>

# Description
Run the defined commands on Linux/Cygwin, and execute on Windows
[Usage](https://github.com/xiezhulin/cmd2win/blob/master/cmd2win)

# Installation
## On Windows
    Run 'cmd2win_server.py', you can choose any one of the following method
    1. double click
    2. by cmd(details with '--help')
    3. put 'cmd2win_server.py' into 'C:\Users\Administrator\AppData\Roaming\Microsoft\Windows\Start Menu\Programs',
       ensure the server can started when windows bootcompleted, but maybe different path in your computer.
## On Linux
### 1. Put 'cmd2win' into your PATH directory, ensure cmd2win can run in any directory
### 2. Set envrironment, it's optional, such as append the following content to ~/.bashrc
#### 1) Set alias(Let's say your Windows IP is 192.168.1.1)
     $ cmd2win_cmd_prefix="cmd2win --host 172.25.124.179"
     $ alias so="$cmd2win_cmd_prefix open"
     $ alias sod="$cmd2win_cmd_prefix open_parent_dir"
     $ alias scu="$cmd2win_cmd_prefix custom"
     $ alias sc="$cmd2win_cmd_prefix cmp"
     $ alias scl="$cmd2win_cmd_prefix clip"
#### 2) Change defaults
     Text editor defaults to notepad, ensure "gvim" can run by windows cmd
     $ export SMB_TXT_EDITOR="gvim"
     $ export SMB_TXT_EDITOR_SUPPORT_MULTI_FILES=True
     Config windows compare tools, and add the tools to windows' environment, defaults to fc, ensure "Bcompare" can
     run by windows cmd
     $ export SMB_COMPARER="Bcompare"
