#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 30 17:41:00 2019

@author: tuukka

Instructions:
Make the following modifications to the server example:

    Add two command line parameters to the program
    If these two values are not given from the command line the server 
    should print an error message and exit immediately
    These two values should be used for binding the server socket 
    with bind()
    Keep the server running after a single connection has been handled
        You don’t have to be able to handle multiple connections at 
        the same time
        Once a connection has been handled, the server should go back 
        to waiting on accept()

Make the following modifications to the client program:

    Add two command line parameters to the program:
        address
        port
    If these two values are not given from the command line the client 
    should print an error message and exit immediately
    Handle the exceptions from connect() and send() and print a human 
    readable error message if an error occurs.
        e.g. cannot connecto to server or sending data to server 
        failed

Hint: argparse module from the standard library makes handling 
command line parameters easier. In a simple example like this, 
it is a bit of an overkill, but it is extremely useful to be 
familiar with it. You can also use sys.argv if you want.
"""
#client program
import socket
import argparse

parser = argparse.ArgumentParser(description='Process some arguments.')
parser.add_argument('ip',help='a string argument for establishing a socket name or address')
parser.add_argument('port',type= int,help='a string argument for establishing a port number')
args = parser.parse_args()
localhost = args.ip
port = args.port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print(f'Connecting to {localhost}')
try:
    s.connect((localhost, port))
    toSend = str("A" * 10000)
    #raise ValueError(toSend)
    check = len(toSend)
    lenC= len("%i" % check)
    check = check + lenC + 1 #lisätään +1 (huutomerkki)
    #print(lenC)
    toSend =  str(check) + "!" + toSend
    #raise ValueError(toSend)
    print(f"Sending message of {check} characters to server")
    s.sendall(bytes(toSend, "utf-8"))
    ack = int(str(s.recv(1024), "utf-8"))
    #raise ValueError(ack)
    #str(client.recv(1024), "utf-8")
    print(f"Received acknowledgment message '{ack}' from server,", end=" ")
    status = 0
    if ack == check:
        status = 1
        print(f'message was received succesfully')
except ConnectionRefusedError:
    print("server not available!")
except OSError as e:
    print("You are already connected to that endpoint!")

finally:
    if s:
        s.close()