#!/usr/bin/env python
# -*- coding: utf-8 -*-
from zio import *

def chan_buf(num, i):
    if ( i & 1 ):
        v3 = 4 * (i + 1) + 2 + num
    else:
        v3 = num * (((i + 2) >> 1) + 2)
    return v3

def get_ip(tmp, i):
     return i + 4 * tmp % 10000;

ip = '10.211.55.56'
# ip = '192.168.8.103'
port_list = [1234,5678,9087,6543,2190]

for i in range(5):
    if i == 0:
        port = port_list[i]
    else:
        port = get_ip(port_list[i], i)
    print port
    io = zio((ip, port), timeout=10000, print_read=COLORED(REPR,'yellow'),\
        print_write=COLORED(REPR,'blue'))
    buf = l32(io.read(4))
    v13 = chan_buf(buf, i)
    io.write(l32(v13))
    io.readline()
    io.close()
