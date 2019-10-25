#!/usr/bin/env python

import paramiko
import threading
import re
import argparse
import socket
import thread

arg_parser = argparse.ArgumentParser(description='command line tool for \
                                     changing mutliple passwords over ssh',
                                     usage='%(prog)s -c filename')
arg_parser.add_argument('-c', nargs=1, help='-c followed by filename \
                         containing hosts')
args = arg_parser.parse_args()

ip_re = re.compile("^ip: (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})")
user_re = re.compile("^username: ([\w+\d+]+)")
password_re = re.compile("^password: (.+)")
filename = args.c[0]


# Host class for creating threaded host objects
class Hosts(threading.Thread):
    def __init__(self, host, ip_addr, username, password):
        threading.Thread.__init__(self)
        self.host = host
        self.ip_addr = ip_addr
        self.username = username
        self.password = password

    def HostInfo(self):
        "prints host info"
        print self.host
        print self.ip_addr
        print self.username
        print self.password

    def run(self):
        "use paramiko sshclient to change passwords through ssh"
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(self.ip_addr, username=self.username,
                        password=self.password)
            print "Login succesfull on {}".format(self.ip_addr)
        except socket.error:
            print "Connection refused on %s." % self.ip_addr
            thread.exit()
        except paramiko.AuthenticationException:
            print "wrong username and/or password %s." % self.ip_addr
            thread.exit()
        ssh.close()


def GetHosts(filename):
    "Parse config file to get host information and create host objecs"
    hosts = []
    try:
        hostfd = open(filename, 'r')
    except IOError:
        print "file %s not found" % filename
    hostdata = hostfd.read().split("\n\n")
    hostnum = 0
    for line in hostdata:
        hostarr = line.split("\n")
        print(hostarr)
        for i in hostarr:
            print(i)
            if "ip:" in i:
                ip = i.split(" ")[1]
            if "username:" in i:
                user = i.split(" ")[1]
            if "password:" in i:
                password = i.split(" ")[1]
        host = Hosts(hostnum, ip, user, password)
        hosts.append(host)
        hostnum += 1
    return hosts


def main():
    threads = []
    hosts = GetHosts(filename)
    for host in hosts:
        # host.HostInfo()
        threads.append(host)

    for i in xrange(len(hosts)):
        threads[i].start()

    for i in xrange(len(hosts)):
        threads[i].join()

    print 'all Done'

if __name__ == '__main__':
    main()
