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

host_re = re.compile("(^HOST [\d\w])")
ip_re = re.compile("^IP: (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})")
user_re = re.compile("^username: ([\w+\d+]+)")
password_re = re.compile("^password: ([\w+\d+]+)")
newpass_re = re.compile("^newpass: ([\w+\d+]+)")
filename = args.c[0]


# Host class for creating threaded host objects
class Hosts(threading.Thread):
    def __init__(self, host, ip_addr, username, password, newpass):
        threading.Thread.__init__(self)
        self.host = host
        self.ip_addr = ip_addr
        self.username = username
        self.password = password
        self.newpass = newpass

    def HostInfo():
        "prints host info"
        print self.host
        print self.ip_addr
        print self.username
        print self.password
        print self.newpass

    def run(self):
        "use paramiko sshclient to change passwords through ssh"
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(self.ip_addr, username=self.username,
                        password=self.password)
        except socket.error:
            print "Connection refused on %s." % self.ip_addr
            thread.exit()
        except paramiko.AuthenticationException:
            print "wrong username and/or password %s." % self.ip_addr
            thread.exit()
        stdin, stdout, stderr = ssh.exec_command('passwd')
        if self.username == 'root':
            print 1
            stdin.write('%s\n' % self.newpass)
            stdin.flush()
            print 2
            stdin.write('%s\n' % self.newpass)
            stdin.flush()
            print 3
            print stdout.readlines()
        else:
            print 1
            stdin.write('%s\n' % self.password)
            stdin.flush()
            print 2
            stdin.write('%s\n' % self.newpass)
            stdin.flush()
            print 3
            stdin.write('%s\n' % self.newpass)
            stdin.flush()
            print 4
            print stdout.readlines()
        ssh.close()


def GetHosts(filename):
    "Parse config file to get host information and create host objecs"
    hosts = []
    try:
        hostfile = open(filename)
    except IOError:
        print "file %s not found" % filename
    for line in hostfile:
        line = line.strip("\r\n")
        if host_re.match(line):
            hostnum = host_re.match(line).groups()[0]
        elif ip_re.match(line):
            ip = ip_re.match(line).groups()[0]
        elif user_re.match(line):
            user = user_re.match(line).groups()[0]
        elif password_re.match(line):
            password = password_re.match(line).groups()[0]
        elif newpass_re.match(line):
            newpass = newpass_re.match(line).groups()[0]
            host = Hosts(hostnum, ip, user, password, newpass)
            hosts.append(host)
        else:
            pass
    return hosts


def main():
    threads = []
    hosts = GetHosts(filename)
    for host in hosts:
        threads.append(host)

    for i in xrange(len(hosts)):
        threads[i].start()

    for i in xrange(len(hosts)):
        threads[i].join()

    print 'all Done'

if __name__ == '__main__':
    main()
