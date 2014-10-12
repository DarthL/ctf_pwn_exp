#!/usr/bin/env python
# -*- coding: utf-8 -*-
from zio import *
import sys

dic = {}

def get_money():
    io.read_until('Your money: $')
    # return int(io.readline().strip())
    money = int(io.readline().strip())
    print money
    return money

def guess():
    io.read_until('Round verification: ')
    cipher = io.readline().strip().decode('hex')
    io.read_until('3. Quit\n')
    if cipher in dic:
        log('test', 'red')
        io.writeline('1')
        #io.read_until('Your guess (0-1000): ')
        io.writeline(dic[cipher])
    else:
        io.writeline('2')
        io.read_until('The lucky number was: ')
        dic[cipher] = io.readline().strip()
    io.read_until("Press 'c' to continue...\n")
    io.writeline('c')



target = ('10.10.10.11',8989)
# target = 'python Luckydraw.py'

#io = zio(target, print_read=COLORED(REPR,'yellow'), print_write=COLORED(REPR,'blue'), write_delay=0.)
io = zio(target, print_read=False, print_write=False, write_delay=0.)
while True:
    if len(dic) % 100 == 0:
        print 'dic size: %d' % len(dic)
    if get_money() > 537:
        io.read_until('3. Quit')
        io.writeline('2')
        io.read_until('s your reward:')
        print 'flag:', io.readline()
        sys.exit()
    else:
        guess()
