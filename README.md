sshpasswordchanger
==================

Python command tool for changing password remotely over ssh using paramiko module

usage:
======

python sshpasschanger.py -c \<config filename>

config format:
==============

HOST \<host number/name><br />
IP: \<ip address><br />
username: \<username><br />
password: \<current password><br />
newpass: \<new password><br />
<pre>
# Example Config example
HOST 1
IP: 192.168.1.2
username: testuser
password: testpass
newpass: testnewpass
</pre>
