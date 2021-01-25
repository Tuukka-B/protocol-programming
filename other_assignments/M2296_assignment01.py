#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 17 17:14:32 2019

@author: tuukka
"""

"""client"""
import socket
import sys
class Error(Exception):
    pass

class SendError(Error):
    pass
#   all below are unnecessary
#    def __init__(self,orig):
#        self.__orig = orig
#    def SendError(self):
#        print(f'could not send data! Original error below\n{self.__orig}')
    
    
def main(s, data):
    import socket
#    test variable to test how lost data is handled (cuts letters off the string)
#    now obsolete (not the goal of the assignment)
#    test = data[0:-6:1]
    try:  
        host = socket.gethostname()
        #okay, better way to do this would be with 2 python files
        #... with one acting as a server code and the other as client
        # but this works, so I'll let this be...
        #s2 = server, s = client
        s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        localhost = "127.0.0.5" #server addr
        with s2:
            s2.bind((localhost, 9999))
            s2.listen(5)
            with s:
                print(f'connecting to {localhost}')
                s.connect((localhost, 9999))
                conn, addr = s2.accept()
                print(f'server accepted connection from {addr[0]} (client address) port {addr[1]}')
                #(client, addr) = s.accept()
                # Send some data over the socket
                s.send(bytes(data, "utf-8"))
                print(f'sending data to {localhost}')
                data2 = str(conn.recv(1024), "utf-8")
                print(f"received from {addr[0]} (client): {data2}")
                """
                if data2 != data:
                    counter = 1
                    while data != data2:
                        if data[0:counter:1] != data2[0:counter:1]:
                            break
                        counter +=1
                    
                    last = -len(data) + counter -1
                    #print(f'-counter :{data[last:]}')
                    missing = data[last:]
                    s2.send(bytes(missing, "utf-8"))
                    new2 = str(conn.recv(1024), "utf-8")
                    data2 = data2[0:counter-1:1] + new2
                    #print(f'reconstructed: \n{data2}')
                    #print(f'original:  \n{data}')
                """
            #print(info)
    except ConnectionRefusedError as e:
        #print(f"Connection refused! Try again later \n({e})")
        raise SendError(e)
    except OSError as e:
        raise SendError(e)
        #print(f"You're already connected to that endpoint  or the address is already in use.\n({e})")
    finally:
        print(f'closing all connections')
        s.close()
        s2.close()
        #s2.close()
    pass
    
if __name__ == '__main__':
#    if sys.argv:
#        print(sys.argv)
    #print(socket.gethostname())
    socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#    print(socket)
    data = "szvdbhtgrfescvbn jhytrDVGF ZXWjmkhm"
    main(socket, data)
    #main()
    