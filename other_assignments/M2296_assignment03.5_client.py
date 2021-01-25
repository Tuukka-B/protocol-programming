#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 10 16:29:51 2019

@author: tuukka

Assignment:
    Write a client and a server program that can be used to send files 
    to the server. You have to come up with a simple protocol 
    (you don’t have to document the protocol, but you can) 
    which allows the transfer of files. The protocol should be able to 
    transmit name, size and contents of the file being sent. 
    It is up to you to implement this. The client HAS to send this 
    information:

    name of the file
    size of the file (in bytes!)
    contents of the file (actual bytes of the file from disk)

    When the server receives the connection, it uses this information 
    to:

    create a new file with the same name
    receive the total size of the file to receive (in bytes)
    Receive the contents of the file and write them to a file on disk.
        under the received files directory.
        name of the file has to be same as the one that the client sent

Start early so you can ask questions from the lecturer!

Client

The client takes three command line parameters:

    path of the file to send
    server address
    server port

The client will print an error message and exits if any of the following 
conditions are met:

    The file is missing
    The file cannot be read from
    The client cannot connect to the server
    any others that you can think of

"""
import socket
import argparse
import os
from time import sleep

parser = argparse.ArgumentParser(description='Process some arguments.')
parser.add_argument('path',help='the filepath of the file to be sent')
parser.add_argument('hostname',help='a string argument for establishing a socket name or address')
parser.add_argument('port',type= int,help='a string argument for establishing a port number')
args = parser.parse_args()
localhost = args.hostname
port = args.port
filepath = args.path
#raise ValueError(repr(filepath))
filename = ""
if "/" in filepath:
    filename =filepath.split("/")[-1]
    #raise ValueError(filename)
elif "\\" in filepath:
    #raise ValueError(filepath)
    filename =filepath.split('\\')[-1]
else: 
    #assumes user has written filename and it is in current directory
    filename = filepath
#raise ValueError(filename)

#raise ValueError(args.host, args.port)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((localhost, port))

file = None
try:
    length = str(os.path.getsize(filepath))
    file = open(filepath, 'rb')
    
#    toSend = file.read()
#    length = len(toSend)
#    #print(length)
#    lenC= len("%i" % length)
#    length += lenC +1
#    toSend1 = bytes(str(length),"utf-8") + bytes("!", "utf-8") + bytes(toSend, "utf-8")
#    print(toSend, "\n", toSend1)
#    print(f"sending message of {length} characters to server")
    print(f"Sending filename '{filename}' to server...")
    s.send(bytes(filename, "utf-8"))
    c = str(s.recv(1024))
    if "'" in c:
        c = c.split("'")[1]
    print(f"Confirmation received: '{c}'.", end = " ")
    if c == "0" or not c:
        raise ValueError("transmission failed: server is unresponsive or sending failed")
    else:
        print(f"Filename was received succesfully")
    print(f"Sending length of message to server: {length}")
    s.send(bytes(length, "utf-8"))
    c1= str(s.recv(1024))
    if "'" in c1:
        c1 = c1.split("'")[1]
    if not c1 or c1 == "0":
        raise ValueError("Transmission failed: confirmation was not received or server signalled failure")
    else:
        print(f"Confirmation received: '{c1}'. Length of message was received succesfully.")
        
    l = file.read(1024)
    if not l:
        raise ValueError("File contains no data to send. Try again with another file")
    print("Sending file...")
    count = 0
    while (l):
#        if "'b" in l:
        #l = "".join(l[2:)
        
        print(f"Sending..","."*count, sep ="", end = "\r")
        if count == 20:
            count = 0
            print("Sending..", " "*20, end = "\r")
        else:
            count+=1
        #want some cool graphics on the client side? uncomment below...
        sleep(1/15)
        s.send(l)
        l = file.read(1024)
    print(f'file sent, waiting for confirmation...')
    sleep(2)
    s.send(bytes(str(0), "utf-8"))
    c2 = str(s.recv(1024))
    if "'" in c2:
        c2 = c2.split("'")[1]
    if not c2 or c2 == "0":
        raise ValueError("Transmission failed: confirmation was not received or server signalled failure")
    else:
        print(f"Confirmation received: '{c2}'. Message was received succesfully without corruption of data.")
#    s.sendall(toSend1)
    #ack = int(str(s.recv(1024), "utf-8"))   
finally:
    if file:
        file.close()
        print("Closing program...")
    s.close()
    
            
            
                        

