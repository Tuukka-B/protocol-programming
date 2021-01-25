import socket
import ssl
import sys
from _thread import *
import subprocess
import platform
import os
import sha_struct
import shutil


class GFTP:

    def __init__(self, mode, ip ="localhost", port=8888, *, fileloc="files"):
        import os
        import sys
        fileloc = os.path.join(os.path.dirname(os.path.realpath(sys.argv[0])), fileloc)
        if not os.path.exists(fileloc):
            print(f"Directory {fileloc} not found!\ncreating a directory for files to '{fileloc}'...")
            try:
                os.mkdir(fileloc)
                if mode == "server":
                    print(f"please move files to '{fileloc}' to allow GFTP clients to access them")
                else:
                    print(f"directory created; this will be used as a folder to download files to")

            except Exception:
                print("failed to make a directory, please try another directory name!\nexiting...")
                sys.exit(1)

        if mode == "client":
            # let's not confuse remote and local ip/port... for readability
            self.__remote_ip = ip
            self.__remote_port = port
            self.__port = None
            self.__ip = None
        elif mode == "server":
            self.__port = port
            self.__ip = ip
            self.__remote_ip = None
            self.__remote_port = None
        else:
            print("invalid argument for mode of operation!\nexiting...")
            sys.exit(1)

        # fileloc for server establishes working directory
        # fileloc for client specifies the directory where files are uploaded from or downloaded to
        self.__fileloc = fileloc
        self.__ssl_servername = "localhost" # as defined in the certificate (do NOT change this)
        self.__ssl = None
        self.__mode = mode
        # first run tracker
        self.__first_run = True
        # socket variable
        self.__s = None
        # location for the self-made certificate
        self.__certloc = './essential-files/server2.pem'
        self.__keyloc = './essential-files/server2.key'
        self.__pgpubloc = './essential-files/M2296_public_key.asc'
        self.__pgprivloc = './essential-files/M2296_private_key.asc'
        # self.__len is for determining how much bytes we want to use to send our initial messages with (like
        # authentication and other parameters). It will be used in tandem with my library sha_struct, which can make
        # custom-sized packets with struct-library for sockets to send and receive
        self.__len = 1024
        """ 
        instructions for creating a self-signed cert:
        https://pankajmalhotra.com/Simple-HTTPS-Server-In-Python-Using-Self-Signed-Certs
        as the Canonical Name in the cert is named "localhost", the certificate validation might not work over network...
        """
        self.__file = None

    def __str__(self):
        if self.__ip:
            return f"Hello, I'm a program designed to server General File Transfer Protocol operations! I save files " \
                   f"to {self.__fileloc} and I communicate via host-name or address '{self.__ip}' through port " \
                   f"{self.__port}.\ncurrently I'm running in SERVER -mode!"
        if self.__remote_ip:
            return f"Hello,  I'm a program designed to server General File Transfer Protocol operations! I have been " \
                   f"configured as a CLIENT and I wish to connect to server '{self.__remote_ip}' through port " \
                   f"'{self.__remote_port}'."

    """the methods below are public commands so they are visible if imported as a module """

    @staticmethod
    def check_free_space(filesize):
        usage = shutil.disk_usage(os.getcwd())
        usage = str(usage).strip(")")
        freespace = int(usage.split("=")[3])
        return freespace > filesize

    @staticmethod
    def exit():
        # this is only done by the client, server will not want to exit if it doesn't have to
        sys.exit(0)


    def upload(self, filename, source_folder=None):
        if self.__mode == "server":
            print("Illegal operation for server! Server serves operations automatically with connect() method!")
            return None # should make this an error message (everything server does happens in handle_command)
        elif self.__mode == "client":
            if source_folder:
                if not os.path.exists(os.path.join(source_folder, filename)):
                    self.__error("That file does not exist!", conn=None)
                    self.__exit(conn=self.__ssl)
                    self.exit()
            self.__upload_client(filename, source_folder=source_folder)

    def download(self, filename, destination_folder=None):
        if self.__mode == "server":
            print("Illegal operation for server! Server serves operations automatically with connect() method!")
            return None # should make this an error message (everything server does happens in handle_command)
        elif self.__mode == "client":
            self.__download_client(filename, destination_folder)

    def list(self):
        if self.__mode == "server":
            print("Illegal operation for server! Server serves operations automatically with connect() method!")
            return None # should make this an error message (everything server does happens in handle_command)
        elif self.__mode == "client":
            self.__list_client()

    def connect(self):
        if self.__mode == "client":
            self.__client_connect()
        else:
            self.__server_connect()

    def __server_connect(self):
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        print("the pass phrase is '1234'")
        context.load_cert_chain(self.__certloc, self.__keyloc)
        self.__s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__s.bind((self.__ip, self.__port))
        ssock = context.wrap_socket(self.__s, server_side=True)
        print("Server is online, waiting for requests...")
        ssock.listen(5)

        conn, addr = None, None
        while True:
            try:
                conn, addr = None, None
                (conn, addr) = ssock.accept()
                print(f"Connected to {addr[0]}")
                start_new_thread(self.__handle_command, (conn, ssock))
            except KeyboardInterrupt:
                self.__error("Connection was manually shut down by server", conn=None)
                self.__exit(conn=ssock)
                self.exit()

    def __client_connect(self):
        # creates a socket in the first run, subsequent runs establish connection to server
        try:
            # PROTOCOL_TLS_CLIENT requires valid cert chain and hostname
            context = ssl.SSLContext()
            context.verify_mode = ssl.CERT_REQUIRED
            context.check_hostname = True
            context.load_verify_locations(self.__certloc)
            if self.__first_run: # first run is for if we want to do multiple operations with 1 client (not implemented)
                self.__s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.__ssl = context.wrap_socket(self.__s, server_hostname=self.__ssl_servername)
                self.__first_run = False
            self.__ssl.connect((self.__remote_ip, self.__remote_port))
            # print(self.__ssl.version())
            print("Connected to server!")

        except Exception as e:
            print(e)
            self.__error(e, conn=self.__ssl, local=False)
            if self.__mode == "client":
                self.__exit()
            return None

    def __handle_command(self, conn, ssock, addr=None):
        command = None
        authchecksum = None
        try:
            # initial command and authentication from the server is received below.
            c = conn.recv(self.__len)
            if c == b"":
                print("Connection was closed by client!")
                print("Listening for new connections...")
                exit()
            # all data is sent packed in the beginning, so we unpack it with our own module.
            data = sha_struct.unpackdata(c, int(self.__len / 4))
            data = data.decode("utf-8")
            command = data.split("\r\n")[0]
            authchecksum = data.split("\r\n")[1]
        except Exception:
            self.__error("Invalid command received", conn=conn)
            return None

        pubauth = sha_struct.checkhash(authchecksum, self.__pgpubloc)
        privauth = sha_struct.checkhash(authchecksum, self.__pgprivloc)
        if pubauth or privauth:
            if command == "li":
                print("Serving a list request...")
                self.__list_server(conn=conn)
            elif command == "dl":
                print("Serving a download request...")
                filename = conn.recv(self.__len)
                filename = sha_struct.unpackdata(filename, int(self.__len / 4)).decode("utf-8")
                filename = filename.split("\r\n")[0]
                self.__send_file(filename, conn=conn)
            elif command == "ul":
                if privauth:
                    print("Serving an upload request...")
                    self.__receive_file(conn=conn)
                else:
                    self.__error("You are not authorized for this operation", conn=conn)
            else:
                self.__error("Invalid command, please supply a correct one", conn=conn)
            print("Request completed.")
        else:
            self.__error("Invalid authentication received", conn=conn)

        print("Connection closed, listening for new connections...")
        exit()

    def __authenticate(self, command, *, pgploc):
        # only client uses this method. It can only be called from withing GFTP (private method)

        hash = sha_struct.genhash(pgploc) + "\r\n"
        data = command + hash
        # packed packet is made always to be 1024 bytes, it can be adjusted by changing self.__len
        packed, length = sha_struct.packdata(data, self.__len)
        sent = self.__ssl.sendall(packed)
        # input(sent)

    def __upload_client(self, filename, source_folder=None):
        command = "ul\r\n"
        self.__authenticate(command, pgploc=self.__pgprivloc)
        self.__send_file(filename, source_folder=source_folder)

    def __list_server(self, data=None, *, conn):
        """"
        If GFTP's host is Windows, the list command looks a bit different. But ls is great for Linux, so let's use it!
        """
        formatted = ""
        if "Linux" in platform.system():
            ls = subprocess.run(["ls", "-ogh", self.__fileloc], stdout=subprocess.PIPE).stdout.decode("utf-8")
            data = ls.split("\n")
            for i in data:
                i = i.strip()
                i = i[13:]
                formatted += "\n" + i + "\n"
            formatted = formatted.strip("\n")
            # conn.sendall(bytes(formatted, "utf-8"))
        elif "Windows" in platform.system():
            data = subprocess.run(["dir", self.__fileloc, "/A-D"], shell=True, stdout=subprocess.PIPE).stdout
            data = str(data).split("\\r\\n")
            count = 0
            for line in data:
                if count < 4:
                    #Jätetään huomiotta 4 ensimmäistä riviä
                    count +=1
                    continue
                formatted += line + "\n"
            #Puhdistustoimia....
            formatted = formatted.replace("\\xff", " ")
            formatted = formatted.rstrip("\n")
            formatted = formatted.rstrip("\'")
            formatted = formatted.rstrip("\n")
        # the good thing with the methods above is that you get more data than with os.listdir (coded and formatted
        # below), though os.listdir is platform-neutral
            """try:
                filelist = os.listdir(self.__fileloc)
                # note that too big a file name will break the list formatting
            except Exception as e:
                # list_server is a server function and it does not need an exit call
                self.__error("Couldn't list directory contents, please inform the server maintainer of this error.\nerror:{e}", conn=conn)
                return None
            formatted ='{:>45}'.format('** list of files **\n\n')
            for x in filelist:
                try:
                    size = int(os.path.getsize(os.path.join(self.__fileloc, x)))
                except Exception:
                    # getting the size fails. Even so we want to list the file...
                    size = "unknown"
                    suffix = "bytes"
                    # magic formatting below (defines how much space every variable takes and their type [ s = string ] )
                    formatted += "{:48s} {:6s} {:10s}\n".format(x, size, suffix)
                    continue
                suffix = "bytes"
                if size > 1000:
                    size = size / 1000
                    suffix = "kb"
                    if size > 1024:
                        size = size / 1000
                        suffix = "mb"
                        if size > 1024:
                            size = size / 1000
                            suffix = "gb"
                formatted += ("{:45s} {:10.2f} {:10s}\n").format(x, size, suffix)
            formatted += '\n{:>43}'.format("**  end of list  **")"""
        # final transmissions need not be exactly 1024 bytes as the client is receiving until server closes connection
        # it will be clean exit with or without exact byte-size
        conn.sendall(bytes(formatted, "utf-8"))

    def __list_client(self):
        command = "li\r\n"
        print("sending authentication...")

        self.__authenticate(command, pgploc=self.__pgpubloc)
        output = self.__ssl.recv(self.__len)
        data = self.__ssl.recv(self.__len)
        while data:
            output += data
            data = self.__ssl.recv(self.__len)
        # we get the output here, was it a list or an error. We need to clean it if it was an error
        try:
            output = sha_struct.unpackdata(output, int(len(output)/4)).decode("utf-8")
            output = output.strip("!")
        except Exception as e:
            output = str(output, "utf-8")
            # the error is sent packed, if unpacking fails (raises Exception),
            # we got a true list and just need to decode
        print(output)

    def __download_client(self, filename, destination_folder=None):
        if destination_folder is None:
            destination_folder = self.__fileloc
        command = "dl\r\n"
        print("sending authentication...")
        self.__authenticate(command, pgploc=self.__pgpubloc)
        filename = filename + "\r\n"
        packed, length = sha_struct.packdata(filename, self.__len)
        self.__ssl.sendall(packed)

        # receive the file, destination_folder is an extra feature which can be passed from front-end
        self.__receive_file(destination_folder=destination_folder)

    def __send_file(self, filename, conn=None, source_folder=None):
        client = None
        # if conn was supplied, the sending is done on server mode to the connection established to the server
        # otherwise it's the client that does the sending
        if conn:
            client = conn
        else:
            client = self.__ssl

        if ("/" in filename or "\\" in filename) and self.__mode == "server":
            self.__error("Illegal characters in file name, please do not use \"/\" or \"\\\"", conn=client)
            return None
        filepath = None
        try:
            if source_folder:
                filepath = os.path.join(source_folder, filename)
            else:
                filepath = os.path.join(self.__fileloc, filename)
        except Exception as e:
            self.__error(f"Could not proceed with determining a file path while sending a file\n{e}", conn=client, local=True)
            if self.__mode == "client":
                self.__exit(conn=client)
            return None
        # filesize is not really used anywhere by the client or the server as checksums completely replaced that
        # functionality. It is still passed to the receiver, who can choose what to do with it.
        command = None
        try:
            filesize = os.path.getsize(filepath)
            command = ("{}\r\n{}\r\n{}").format(filename, sha_struct.genhash(filepath), filesize)
        except Exception as e:
            self.__error(e, conn=client)
            return None
        packed, length = sha_struct.packdata(command, self.__len)
        client.sendall(packed)

        file = None
        try:
            with open(filepath, "rb") as file:
                data = file.read(self.__len) # in 1024 byte sized packets, increase self.__len to change this
                while data:
                    client.sendall(data)
                    data = file.read(self.__len)
            # special rules if server is receiving the file
            # the termination of connection must always be done by the server, so the client
            # must allow it to escape the recv-loop, so it sends b"0\r\n" to signal end of file
            if client == self.__ssl:
                client.sendall(b"0\r\n")
                answer = client.recv(self.__len)

                if answer: # this means the connection was not closed by the server, which means an error happened
                    error = sha_struct.unpackdata(answer, int(self.__len / 4)).decode("utf-8").strip("!")
                    self.__error(error, conn="closed", local=True)
                    self.__exit(conn=self.__ssl)
                    return None

                print(f"file '{filename}' has been sent successfully")

        except ConnectionResetError:
            error = "The server suffered an internal error and closed the connection. Inform the server maintainer" \
                    " of this error."
            self.__error(errcode=error, conn=None)
            if self.__mode == "client":
                self.__exit(conn=None)
            return None

        except Exception as e:
            error = f"Could not send file\n{e}"
            self.__error(errcode=error, conn=client)
            if self.__mode == "client":
                self.__exit(conn=client)
            return None

    def __receive_file(self, conn=None, destination_folder=None):

        client = None
        if conn:
            client = conn
        else:
            client = self.__ssl

        data = None
        filename = None
        checksum = None

        try:
            received = client.recv(self.__len)
            # input(received)
            unpacked = sha_struct.unpackdata(received, int(self.__len/4))
            unpacked = unpacked.decode("utf-8")
            filename = unpacked.split("\r\n")[0]
            checksum = unpacked.split("\r\n")[1]
            filesize = int(unpacked.split("\r\n")[2].strip("!"))
        except IndexError as e:
            # we know, that if we don't get everything we need with split, that the server didn't send it
            error = sha_struct.unpackdata(received, int(self.__len/4)).decode("utf-8").strip("!")
            self.__error(error, conn=None)
            if self.__mode == "client":
                self.__exit(conn=client)
            return None
        if "Invalid filename" in filename:
            error = "".join(filename.split("\'")[0:]).strip("!") # horrible frankenstein command, but it does the job
            self.__error(errcode=error, conn="closed", local=True)
            if self.__mode == "client":
                self.__exit(conn=client)
            return None
        filepath = None
        data = "placeholder"
        if ("/" in filename or "\\" in filename) and self.__mode == "server":
            self.__error("Illegal characters in file name, please do not use \"/\" or \"\\\"", conn=client)
            return None
        if destination_folder:
            filepath = os.path.join(destination_folder, filename)
        else:
            filepath = os.path.join(self.__fileloc, filename)
        if os.path.exists(filepath):
            self.__error(("File named {} already exists in current directory.").format(filename), conn=client, local=True)
            if self.__mode == "client":
                self.__exit(conn=client)
            return None

        if not self.check_free_space(filesize):
            self.__error("There's not enough space to save the file!", conn=client)
            if self.__mode == "client":
                self.__exit(conn=client)
            return None
        try:
            with open(filepath, 'wb') as file:
                print(f"Receiving data and writing to file in {filepath}...")
                data = True
                while data:
                    # input(client)
                    data = client.recv(self.__len)

                    # we need a special rule if the server is receiving a file as the server should always be the one to
                    # break the connection, but it cannot be done if it is always waiting to receive, therefore it needs
                    # a closing call to escape the loop
                    if conn:
                        if data == b"0\r\n":
                            break
                        elif data.endswith(b"0\r\n"):
                            data.rstrip(b"0\r\n")
                            file.write(data)
                            break
                    file.write(data)
        except OSError:
            if "The server reports" in filename:
                error = filename.strip("!")
                self.__error(error, conn="closed", local=True)
                return None

        if not sha_struct.checkhash(checksum, filepath): # function returns True or False
            os.remove(filepath)
            self.__error("Error receiving the file, the files are not identical. Removing file...", conn=client)
        else:
            print("The checksum of the file matches the provided checksum.")
            print(f"file '{filename}' has been received and saved successfully to {filepath}")

    def __error(self, errcode, conn, local=False):
        """Explanations for different parameters:
            errcode is the unpacked raw error information. The server will pack and send this to client. The client
            will print this information if other conditions are fulfilled (conn=None or conn="closed", see below)
            conn can be None, "closed" or hold an actual connection
                the difference between "closed" and None is that the client will not wait to receive data if
                conn = "closed", but the server WILL send the error even if conn = "closed".
                With None no sending or receiving is done by the client or the server
                (in a sense maybe naming it "closed" was ambiguous, it means more like that
                it's closed ONLY if the CLIENT stumbles upon the same error)
            parameter local = True means that neither client or server will expect to receive error data from the other
            party: it's a local error, it means the other party has not done anything wrong and is functioning normally
        """
        error = None
        if self.__mode == "server":
            error = f"\rThe server reports that the following error happened and terminated all socket and " \
                    f"file-handling functions:\n{errcode}"
        else:
            error = errcode
        if conn:
            if self.__mode == "server":
                p_error, length = sha_struct.packdata(error, self.__len)
                conn.sendall(p_error)
                print(f"The following error was sent to client:\n\"{error}\"")
            elif not local and conn != "closed":
                # (not local) implies that the error happens on our own side
                recvd_e = conn.recv(self.__len)
                e = sha_struct.unpackdata(recvd_e, int(self.__len/4)).decode("utf-8").strip("!")
                print(e)
            else:
                # if this executes, we have a local error (the mode is client and local=True)
                if conn != "closed":
                    server_sends = True
                    while server_sends:
                        # this closes the connection properly
                        server_sends = conn.recv(self.__len)
                print(error)
        else:
            print(error)

    def __exit(self, conn=None, ssock=None, addr=None):
        if self.__file:
            self.__file.close()
        if conn:
            conn.close()
        if self.__ssl:
            self.__ssl.close()
        elif ssock:
            ssock.close()
            pass
        if self.__s:
            self.__s.close()


if __name__ == "__main__":
    print("This script should be run as a module. A front-end for this module is supplied by M2296_assignment05.py.")
