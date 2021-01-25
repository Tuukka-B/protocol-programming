#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 30 17:44:20 2019

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
#server program
import socket
import argparse

def main():
    
    parser = argparse.ArgumentParser(description='Process some arguments.')
    parser.add_argument('ip',help='a string argument for establishing a socket name or address')
    parser.add_argument('port',type= int,help='a string argument for establishing a port number')
    args = parser.parse_args()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((args.ip, args.port))
    sock.listen(5)
    try:
        while True:
            print('Waiting for connections...')
            (client, addr) = sock.accept()
            print("Received a connection from ", addr[0])
            data = ""
            check = 0
            while True:
                
                data = data + str(client.recv(1024), "utf-8")
                
                for x in range(0, len(data)):
                    if data[x] == "!":
                        check = int(data[0:x])
                        print(f'found checksum of {check}')
                print(f'the actual length of the received message ({len(data)}) is compared to proclaimed length of message')
                if len(data) == check:
                    print(f'length of message matches the proclaimed length: ({len(data)} and {check} match), sending confirmation')
                    client.send(bytes(str(check), "utf-8"))
                    break
                else:
                    print(f'length of message does not match the proclaimed length: ({len(data)} and {check} are unequal), continuing receiving')
                    #client.send(bytes(str(check), "utf-8"))
                    
            received = "".join(data.split("!")[1:])
            print(f'received data from address {addr[0]}: {received}')
    finally:
        #this makes sure keyboard interrupts close the connection
        if sock:
            print("\nClosing connection...")
            sock.close()

if __name__ == "__main__":
    main()
#    toSend = "asdfbvbfdxbdv cv nfcvxsdxvgn vccfbfgnbvcxsdfgbnjhgbvcxsafgbnhb vcxsdfghnjm cswertghnbvcdsw4r5tyhnbvfdcewrtghnbvcdertghnbvcderthn bvcdertghn bvcdtgyhujnhbvcderthjnhbvcdwerthnb vxswertghn bvcdwertghbvcdewrthnbvcderthnb vcdewrthnb vcdertyhnb vcderthynbvdertyhnb vcderthb vcdtyhnb vdethnb vcdertyhnb vcdghnb vcdck"
#    check = len(toSend)
#    lenC= len("%i" % check)
#    check = check + lenC
#    #print(lenC)
#    toSend = toSend + "!" + str(check)
#    print(toSend)