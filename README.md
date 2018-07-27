###
# Copyright (c) Guangdong vivo software technology CO.,LTD. Unpublished
#
# Guangdong vivo software technology CO.,LTD.
# Proprietary & Confidential
#
# This source code and the algorithms implemented therein constitute
# confidential information and may comprise trade secrets of vivo
# or its associates, and any use thereof is subject to the terms and
# conditions of the Non-Disclosure Agreement pursuant to which this
# source code was originally received.
#
# Description:
#    Do operations based on samba quickly on windows by using custom commands on linux terminal
#
# Author:
#       Ronny<xiezhulin@vivo.com>
#

###
# Support commands
#
See Usage

###
# Usage
#
$ dosmb -h
$ dosmb --help 

dosmb [Optinos] [Args]
Args:
    cmp <src> <dst>
        cmp two files or directories

    open [file/directory] [...]
        open files or directories, defaults to the current directory

    open_parent_dir [file/directory] [...]
        open the parent directory of given files or directories, defaults to the current directory

    custom <"windows command"> [file/directory] [...]
        run windows command, file and directory can be converted to smb path(s), defauls to the
        current directory if file/directory no given
        .e.g:
            dosmb --host 172.25.105.45 custom "adb install -r" ./build/testdemo.apk

    clip <file/directory/content>
        copy content or a smb path of the given file/directory to window's clipboard, defaults to the current directory

Options:
  -h, --help            show this help message and exit
  --host=HOST           server host, defaults to 192.168.8.8
  -p PORT, --port=PORT  server port, defaults to 8090
  -v, --verbose         verbosely list processed

###
# Installation
#
On Windows
    put 'smb_monitor.py' into 'C:\Users\Administrator\AppData\Roaming\Microsoft\Windows\Start Menu\Programs', ensure the server
    can start when windows bootcompleted

On Linux
    1. put 'dosmb' into under PATH on your's linux, ensure dosmb command can run in any path
    2. The step is optional, set the following content in envrironment in your way(append the following content to ~/.bashrc)
        1) set alias command
            alias so="dosmb --host 172.25.105.45 open"
            alias sod="dosmb --host 172.25.105.45 open_parent_dir"
            alias scu="dosmb --host 172.25.105.45 custom"
            alias sc="dosmb --host 172.25.105.45 cmp"
            alias scl="dosmb --host 172.25.105.45 clip"
        2) change defaults
            ###
            # Smb map dirve on windows network
            # defaults to ip-address for your linux(unix) server
            #
            export SMB_MAP_DRIVE="y:\\"
            
            ###
            # Text editor
            # defaults to notepad
            #
            export SMB_TXT_EDITOR="gvim"
            export SMB_TXT_EDITOR_SUPPORT_MULTI_FILES=True
            
            ###
            # Config windows compare tools, and add the tools to windows' environment
            # defaults to fc
            #
            export SMB_COMPARER="Bcompare"
        
