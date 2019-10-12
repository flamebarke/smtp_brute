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
print("")

# open the wordlist file and readlines
try:
    w_open=open(sys.argv[1], "r") #
    wordlist=w_open.readlines()
except:
    print("[!] Error file not found --> exiting")
    sys.exit(0)

# create a socket
try:
    s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("[*] Socket successfully created")
except socket.error() as err:
    print("[!] Socket creation failed with error code " + err + " --> exiting")
    sys.exit(0)

# connect to socket
try:
    connect=s.connect((sys.argv[2],25))
    print("[*] Socket successfully connected to " + sys.argv[2])
    print("[*] Grabbing banner --->\n")
    banner=s.recv(1024)
    print(banner)
except:
    print("[!] Socket failed to connect --> exiting")
    sys.exit(0)

# clean the lines / iterate over the wordlist / receive and print the result
try:
    for line in wordlist:
        line=line.rstrip()
        print("[*] Trying " + line)
        s.send('VRFY ' + line + '\r\n')
        result=s.recv(1024) # receive the result
        with open("/tmp/.vrfy", "w") as outfile:
            print >>outfile, result
        os.system("cat /tmp/.vrfy | grep 250; echo ' '")
except:
    print("\n[!] Failed sending VRFY request --> exiting")
    sys.exit(0)

# Execution end time
t_elapsed=datetime.datetime.now() - start
print('[*] Script completed (hh:mm:ss:ms) {}'.format(t_elapsed))

# exit cleanly
os.system("rm /tmp/.vrfy")
s.close()
sys.exit(0)
