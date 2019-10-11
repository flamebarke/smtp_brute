#!/usr/bin/python

import os
import socket
import sys
import datetime

# check for required args / print usage info
if len(sys.argv) != 3:
    print("[*] Usage: smtp_vrfy.py <wordlist> <ip>")
    sys.exit(0)

# Execution start time
start=datetime.datetime.now()
print("[*] Initiating smtp brute force @{}".format(start))
os.system("echo ' '")

# open the wordlist file and readlines
w_open=open(sys.argv[1], "r") #
wordlist=w_open.readlines()

# create a socket and connect to the server
s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connect=s.connect((sys.argv[2],25))                 

# clean the lines / iterate over the wordlist / receive and print the result
for line in wordlist:
    line=line.rstrip() # clean lines
    s.send('VRFY ' + line + '\r\n') # VRFY a user
    result=s.recv(1024) # receive the result
    with open(".tmp", "w") as outfile: # open .tmp file in write mode
        print >>outfile, result # write result to .tmp
    os.system("echo '[*] User found! ';cat .tmp | grep 250; echo ' '") # print successful responses to stdout

# Execution end time
t_elapsed=datetime.datetime.now() - start
print('[*] Script completed (hh:mm:ss:ms) {}'.format(t_elapsed))

# exit cleanly
os.system("rm .tmp")
s.close()
sys.exit(0)