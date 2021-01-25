#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 10 18:52:43 2019

@author: tuukka

Write a client and a server program that can be used to send files to the server. 
You have to come up with a simple protocol (you don’t have to document the 
protocol, but you can) which allows the transfer of files. The protocol should 
be able to transmit name, size and contents of the file being sent. It is up 
to you to implmement this. The client HAS to send this information:

    name of the file
    size of the file (in bytes!)
    contents of the file (actual bytes of the file from disk)

When the server receives the connection, it uses this information to:

    create a new file with the same name
    receive the total size of the file to receive (in bytes)
    Receive the contents of the file and write them to a file on disk.
        under the received files directory.
        name of the file has to be same as the one that the client sent

Start early so you can ask questions from the lecturer!
Server

The server takes three command line arguments:

    path to a folder where to store the received files
    server address
    server port

Once started, the server will listen for clients and receive files from the 
clients one by one. Each time a file is received the name of that file should 
be printed.

The server will print an error message and exits if any of the following 
conditions are met:

    The target folder doesn’t exist
    Receiving a file failed
    Any other that you can think of

"""
import socket
import argparse
import os

parser = argparse.ArgumentParser(description='Process some arguments.')
parser.add_argument('path',help='the filepath of the transferred file to be saved')
parser.add_argument('hostname',help='a string argument for establishing a host name or ip address to which tcp clients can communicate to')
parser.add_argument('port',type= int,help='a string argument for establishing a port number from which the connection is routed')
args = parser.parse_args()
localhost = args.hostname
port = args.port
filepath = args.path
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((localhost, port))
s.listen(5)
try:
    while True:
        print('Waiting for connections...')
        (client, addr) = s.accept()
        print("Received a connection from ", addr[0])
        data = ""
        check = 0

        print("Waiting for client to send a filename...")
        filename = str(client.recv(1024))
        if filename:
            print(f"Received a filename: {filename}, sending confirmation...")
            #raise ValueError(filename)
            client.send(bytes("ok", "utf-8"))
            if "'" in filename:
                print("Cleaning filename...", end=" ")
                filename = filename.split("'")[1]
                filename.strip(" ")
                if filename == "":
                    raise ValueError("filename not found, aborting process")
                print(f"filename cleaned to {filename}")
        else:
            client.send(bytes(str(0), "utf-8"))
        #TO-DO: merge filename to filepath
        if "/" in filepath:
            if not filepath.endswith("/"):
                filepath += "/" + filename
                print(f"Saving to filepath: '{filepath}'")
            else:
                filepath += filename
                print(f"Saving to filepath: '{filepath}'")

                #raise ValueError(filepath)
        elif "\x5c" in filepath:
            #x5c is the ascii code for backwards slash
            if not filepath.endswith("\x5c"):
                    #print(f"filename : {filename}")
                    #filepath += '\x5c' + filename
                    filepath += "\x5c" + filename
                    print(f"Saving to filepath: '{filepath}'")
            else:
                filepath += filename
                print(f"Saving to filepath: '{filepath}'")
        else:
            raise ValueError("Please input a correct directory marked with forward slash with Linux ('/') or backwards slash ('\\') with Windows.")
            
        try:
            file = open(filepath, 'wb')
            #file.write(received)
            print("Waiting for client to send a length of file...")
            length = str(client.recv(1024))
            if length :
                print(f"Received length of file: {length}, sending confirmation...")
                if "'" in length:
                    print("Cleaning length...", end = " ")
                    length = length.split("'")[1]
                    length.strip(" ")
                    if length == "":
                        raise ValueError("length not found, aborting process")
                    length = int(length)
                    print(f"length cleaned to {length}")

                client.send(bytes("ok", "utf-8"))
            else:
                client.send(bytes(str(0), "utf-8"))
                raise ValueError('Failed to receive length of file, aborting...')
            l = client.recv(1024)
            print(f"Receiving data and writing to file in {filepath}...")
            closingBytes = bytes(str(int(0)), "utf-8")
            #   raise ValueError(closingBytes)
            while (l != closingBytes):
                #print(l, "\n")
        #        if closingBytes != l:
                file.write(l)
                l = client.recv(1024)
            print("Writing complete.")
            if file :
                file.close()
            received = os.path.getsize(filepath)
            print(f'Wrote a file of {received} length', end = "")
            if received == length:
                print(f' and it is equal to the length of the file stated by client\nSending confirmation...')
                client.send(bytes("ok", "utf-8"))
            else:
                print(f" and it is not equal than the proclaimed length of file: {length}")
                print(f"Data found missing from the file. Corruption detected in the sending process, deleting file.\nConfirming failure to client.")

                client.send(bytes(str(0), "utf-8"))
                os.remove(filepath)
        finally:
            pass
            #raise ValueError(type(length), type(received))
            

finally:
    print(f"\nClosing all connections... \nGoodbye!")
    s.close()