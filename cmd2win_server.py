#!/usr/bin/env python3
# coding: UTF-8
#
# Copyright (c) xiezhulin<zdld99170@126.com>
#
# Description:
#     cmd2win server it run on windows, execute cmd2win some commands supported
#
# Author:
#       Ronny<zdld99170@126.com>
#
# Version infomation:
#     Version  Date            Description
#     v1.0     Mar 08, 2016    first version
#     v1.1     Jul 22, 2019    optimize code (name and format)
#

import os
import sys
import time
import socket
import optparse
import threading
if sys.version_info.major < 3:
    print("python 2")
    reload(sys)
    sys.setdefaultencoding('utf-8')
else:
    print("python 3+")


class Cmd2WinServer(object):
    _DEFAULT_PORT = 8090
    _BACKLOG = 5
    _SIZE = 1024

    _USAGE = "%s [Optinos]" % sys.argv[0]
    description = """Copyright (c) xiezhulin<zdld99170@126.com>
cmd2win server run on windows by Ronny
v1.0 (Mar 8, 2016) first version.
v2.0 (Sep 15, 2018) improve codestyle, add grant ip to prevent attacks within the LAN
then remove interval after receiving a message.
v3.0 (Sep 19, 2018) convert net remote to local driver if mapped
"""
    _socket = None;
    _grant_ip = []
    _verbose = True

    def __init__(self):

        hostname = socket.gethostname()
        #self.host = socket.gethostbyname(hostname)
        self.host = self.__get_host_ip()

        self.parse_otpions()
        print('hostname: %s\nhost: %s\nport:%d' %(hostname, self.host, self.port))
        self.net_maps = self.get_net_map_drivers()
        self.run()

    def parse_otpions(self):
        p = optparse.OptionParser(usage=self._USAGE, description=self.description)
        p.add_option('-p', '--port',
                        dest='port',
                        help='server port, defaults to %d' % self._DEFAULT_PORT,
                        metavar='PORT',
                        default=self._DEFAULT_PORT)
        p.add_option('-g', '--grant-ip',
                        dest='grant_ip',
                        help='grant client ip(s) separated by commas, defaluts to grant all ips',
                        metavar='GRANT_IP',
                        default='')

        opt, _ = p.parse_args()
        if opt.port:
            self.port = int(opt.port)
        else:
            self.port = self._DEFAULT_PORT

        if opt.grant_ip:
            self._grant_ip = opt.grant_ip.split(',')
            if self._verbose:
                for s in self._grant_ip:
                    print('grant ip: %s' % (s, ))
        else:
            print('grant all client ip!')

    def get_net_map_drivers(self):
        COLUMN_NAMES = ('status', 'local', 'remote')
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

    def __get_host_ip(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))
            ip = s.getsockname()[0]
        finally:
            s.close()
        return ip

    def executor(self, cmd):
        os.system(cmd)

    def run(self):
        self._socket = socket.socket()
        self._socket.bind((self.host, self.port))
        self._socket.listen(self._BACKLOG)

        while True:
            conn, addr = self._socket.accept()
            client_ip = addr[0]
            if self._grant_ip and client_ip not in self._grant_ip:
                print("%s: no grant permission, ignore!" % (client_ip, ))
                continue
            buf = conn.recv(self._SIZE)
            if buf:
                if sys.version_info.major >= 3:
                    buf = buf.decode()

                if self._verbose:
                    print("receive: [%s]" % (buf, ))

                found = 0
                for local, remote in self.net_maps:
                    if buf.find(remote) != -1:
                        buf = buf.replace(remote, local)
                        found = 1
                        # continue to replace, no break
                if self._verbose and found == 1:
                    print("convert: [%s]" % (buf, ))

                if sys.version_info.major < 3:
                    thread = threading.Thread(target=self.executor, args=(buf.encode('gbk'), ))
                else:
                    thread = threading.Thread(target=self.executor, args=(buf, ))
                thread.setDaemon(True)
                thread.start()

    def __del__(self):
        if self._socket:
            print('delete')
            self._socket.close()


if __name__ == '__main__':
    Cmd2WinServer()

