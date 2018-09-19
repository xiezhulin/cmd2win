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
#  2.0.0     Ronny<xiezhulin@vivo.com>    Sep 15, 2018
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
    DEFAULT_PORT = 8090
    BACKLOG = 5
    SIZE = 1024

    usage = "%s [Optinos]" % sys.argv[0]
    description = """Copyright (c) Guangdong vivo software technology CO.,LTD.
dosmb server run on windows by Ronny<xiezhulin@vivo.com>.
v1.0 (Mar 8, 2016) first version.
v2.0 (Sep 15, 2018) improve codestyle, add grant ip to prevent attacks within the LAN
then remove interval after receiving a message.
v3.0 (Sep 19, 2018) convert net remote to local driver if mapped
v3.1 TODO:check client ip.
"""
    socket = None;
    grant_ip = []

    def __init__(self):
        self.verbose = True

        hostname = socket.gethostname()
        self.host = socket.gethostbyname(hostname)

        self.parse_otpions()
        print('hostname: %s\nhost: %s\nport:%d' %(hostname, self.host, self.port))
        self.net_maps = self.get_net_map_drivers()
        self.run()

    def parse_otpions(self):
        p = optparse.OptionParser(usage=self.usage, description=self.description)
        p.add_option('-p', '--port',
                        dest='port',
                        help='server port, defaults to %d' % self.DEFAULT_PORT,
                        metavar='PORT',
                        default=self.DEFAULT_PORT)
        p.add_option('-g', '--grant-ip',
                        dest='grant_ip',
                        help='grant client ip(s) separated by commas, defaluts to grant all ips',
                        metavar='GRANT_IP',
                        default='')

        opt, _ = p.parse_args()
        if opt.port:
            self.port = int(opt.port)
        else:
            self.port = self.DEFAULT_PORT

        if opt.grant_ip:
            self.grant_ip = opt.grant_ip.split(',')
            if self.verbose:
                for s in self.grant_ip:
                    print('grant ip: %s' % (s, ))
        else:
            print('grant all client ip!')

    def get_net_map_drivers(self):
        COLUMN_NAMES = ('status', 'local', 'remote', 'network')
        records = []
        try:
            f = os.popen('net use')
            content = f.read()
            for line in content.splitlines():
                line = line.strip()
                if line.startswith('OK'):
                    record = line.split()
                    if len(record) < len(COLUMN_NAMES):
                        raise Exception("invalid result for 'net use'")
                    else:
                        # only to get local and remote
                        records.append((record[1], record[2]))
        finally:
            f.close()
        return records

    def executor(self, cmd):
        os.system(cmd)

    def run(self):
        self.socket = socket.socket()
        self.socket.bind((self.host, self.port))
        self.socket.listen(self.BACKLOG)
        while True:
            conn, addr = self.socket.accept()
            client_ip = addr[0]
            if self.grant_ip and client_ip not in self.grant_ip:
                print("%s: no grant permission, ignore!" % (client_ip, ))
                continue
            buf = conn.recv(self.SIZE)
            if buf:
                if self.verbose:
                    print("receive: [%s]" % (buf, ))
                found = 0
                for local, remote in self.net_maps:
                    if buf.find(remote) != -1:
                        buf = buf.replace(remote, local)
                        found = 1
                        # continue to replace, no break
                if self.verbose and found == 1:
                    print("convert: [%s]" % (buf, ))

                thread = threading.Thread(target=self.executor, args=(buf.encode('gbk'), ))
                thread.setDaemon(True)
                thread.start()

    def __del__(self):
        if self.socket:
            print('delete')
            self.socket.close()

if __name__ == '__main__':
    SmbMonitor()

