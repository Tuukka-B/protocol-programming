This program is my final assignment in Protocol Programming course at JAMK. The purpose of this protocol is to transfer files between client and a host -instance of the protocol. Current features are implemented:
* Encryption of all traffic with TLS
* Certificate handling to used with TLS (localhost/loopback-ONLY)
* File integrity checks / fragmentation preventation made possible by checksums
* Rudimentary error condition handling (TO-DO: make this better, right now it's not good)
* Both Windows and Linux support
* Uniform packet size for ease of use

The protocol supports these operations:
* List all available files (LIST operation)
* Download a file from server (DOWNLOAD operation)
* Upload a file to server (UPLOAD operation)

Getting started 101:
* start server with "python M2296_assignment05.py server localhost 8888"
* connect to server with client by "python M2296_assignment05.py client localhost 8888 \<command>"

Because the certificate is only valid for localhost, the client and the server must operate on the same computer and connect through loopback address-space.

Below is an old readme for reference.
--------------------------------------------------------------------------------------------------------------------------------------------

First of all, read SPEC_UPGRADE.txt for explanation of changed specifications.

Second, start the program M2296_assignment05.py and type "server" or "client" after the python command, for example "python3 M2296_assignment05.py server". This will give you argparse's help-page of the server arguments. 

Typing "python3 M2296_assignment05.py client" will give you client help.

Typing "python3 M2296_assignment05.py client download" will give you download help for the client.

Typing "python3 M2296_assignment05.py client upload" will give you upload help for the client.

Typing "python3 M2296_assignment05.py client list" does not have a separate help, instead the command will execute as is (it does need server's address and port though, but the error message will tell you that)

Do NOT change the location of any of the Python files. GFTP.py, M2296_assignment05.py and sha_struct.py need to be in the same folder.

Provided with the assignment are also "server-files" and "test-files" folder. "server-files" is the default folder the server uses for its operations (you can change that though - see server help page). It is provided for the ease of use.

"test-files" folder contains files to test the functionality of the server or the client. It has no other purpose.

Happy testing!
