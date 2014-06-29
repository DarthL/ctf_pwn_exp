#!/usr/bin/env python2
#-*- coding:utf-8 -*-
from zio import *
import hashlib

ip = '10.211.55.48'
port = 25565

string1 = "quals_leoc#192.168.1.1#asis_ctf#leoc#asis_leoc#nothing#"
string2 = "quals_leoc#192.168.1.1#asis_ctf#leoc#asis_leoc#"

io = zio((ip, port), timeout = 10000, print_write = COLORED(REPR))

io.writeline('hello')
io.readline()
io.writeline('send salt')
salt = io.readline()
log("salt:" + salt, 'red')

log(string2 + salt, 'blue')
#hash_new = hashlib.sha1()
#hash_new.update(string2+salt)
#sha1 = hash_new.hexdigest()
sha1 = hashlib.sha1(string2+salt).hexdigest()

log("sha1: " + sha1, 'yellow')
log("final: " + string1 + sha1, 'red')

io.writeline(string1 + sha1)
io.read()
