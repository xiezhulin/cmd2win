#!/usr/bin/env python2
# coding: UTF-8
#
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
#     monitor and do smb operation, it run on windows
#
# Version    Author                          Date
#  1.0.0     Ronny<xiezhulin@vivo.com>    Mar 8, 2016
#

import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import time
import socket
import optparse
import threading


class SmbMonitor():
    s = None
    default_port = 8090
    backlog = 5
    size = 1024
    interval = 0.25

    usage = "%s [Optinos]" % sys.argv[0]
    description = """Copyright (c) Guangdong vivo software technology CO.,LTD.
smb command server run on windows by Ronny<xiezhulin@vivo.com> Mar 8, 2016
"""

    def __init__(self):
        self.verbose = True

        hostname = socket.gethostname()
        self.host = socket.gethostbyname(hostname)
        self.port = 8090

        self.parse_otpions()
        print('hostname: %s\nhost: %s\nport:%d' %(hostname, self.host, self.port))
        self.run()

    def parse_otpions(self):
        p = optparse.OptionParser(usage=self.usage, description=self.description)
        p.add_option('-p', '--port',
                        dest='port',
                        help='server port, defaults to %d' % self.default_port,
                        metavar='PORT',
                        default=self.default_port)

        opt, _ = p.parse_args()
        if opt.port:
            self.port = int(opt.port)

    def executor(self, cmd):
        os.system(cmd)

    def run(self):
        self.s = socket.socket()
        self.s.bind((self.host, self.port))
        self.s.listen(self.backlog)
        while True:
            conn, addr = self.s.accept()
            buf = conn.recv(self.size)
            if buf:
                if self.verbose:
                    print("receive: [%s]" % (buf, ))
                thread = threading.Thread(target=self.executor, args=(buf.encode('gbk'), ))
                thread.setDaemon(True)
                thread.start()

        time.sleep(self.interval)

    def __del__(self):
        if self.s:
            print('delete')
            self.s.close()

if __name__ == '__main__':
    SmbMonitor()

