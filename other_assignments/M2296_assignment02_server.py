#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 30 17:44:20 2019

@author: tuukka

Instructions:
    Modify the client and server example (from the slides) to work 
    correctly for arbitrarily sized messages. This means two things:

    Make sure everything gets sent and received
    Figure out a way to specify the length of the message to 
    the receiver

Feel free to use any of the methods covered in the slides!

Again, just copy pasting from the slides is not enough. 
If you have trouble understanding what this assignment is all about, 
then please ask!
"""
#server program
import socket

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("127.0.0.5", 8888))
    sock.listen(5)
    print('Waiting for connections...')
    (client, addr) = sock.accept()
    print("Received a connection from ", addr[0])
    data = ""
    check = 0
    while True:
        
        data = data + str(client.recv(1024), "utf-8")
        
        for x in range(0, len(data)):
            length = data.split("\n")[0]
            if data[x] == "!":
                check = int(data[0:x])
                print(f'found checksum of {check}')
        print(f'the length of the received message ({len(data)}) is compared to checksum')
        if len(data) == check:
            print(f'checksum matches the length of message ({len(data)} and {check} match), sending confirmation')
            client.send(bytes(str(check), "utf-8"))
            break
        else:
            print(f'checksums do not match ({len(data)} and {check} are unequal), sending confirmation')
            #client.send(bytes(str(check), "utf-8"))
            
    data = "".join(data.split("!")[1:])
    print(f'received data from address {addr[0]}: {data}')
    sock.close()
    #print(data)
    # plan: send data + len of whole message (including the "checksum")
    # so --> data + ! + (check + lenC)
    
    #check = check + lenC + 1 #lisätään +1 (huutomerkki)
    #print(lenC)
    #toSend = toSend + "!" + str(check)
    #client.send(bytes(toSend, "utf-8"))

if __name__ == "__main__":
    main()
#    toSend = "asdfbvbfdxbdv cv nfcvxsdxvgn vccfbfgnbvcxsdfgbnjhgbvcxsafgbnhb vcxsdfghnjm cswertghnbvcdsw4r5tyhnbvfdcewrtghnbvcdertghnbvcderthn bvcdertghn bvcdtgyhujnhbvcderthjnhbvcdwerthnb vxswertghn bvcdwertghbvcdewrthnbvcderthnb vcdewrthnb vcdertyhnb vcderthynbvdertyhnb vcderthb vcdtyhnb vdethnb vcdertyhnb vcdghnb vcdck"
#    check = len(toSend)
#    lenC= len("%i" % check)
#    check = check + lenC
#    #print(lenC)
#    toSend = toSend + "!" + str(check)
#    print(toSend)