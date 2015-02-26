#!/usr/bin/env python
# -*- coding: utf-8 -*-
from zio import *

target = ('10.211.55.56', 12345)
io = zio(target, timeout=10000, print_read=COLORED(REPR,'yellow'),\
        print_write=COLORED(REPR,'blue'))
io.read_until('Send block 0\n')
