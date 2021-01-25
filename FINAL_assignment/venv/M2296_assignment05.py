import argparse
import GFTP

parser = argparse.ArgumentParser(description='A front-end for establishing and serving connections with GFTP-protocol.')
subparser = parser.add_subparsers()
parser_server = subparser.add_parser('server')
parser_server.add_argument('hostname', type=str, help='an argument for establishing a socket name or ip-address')
parser_server.add_argument('port', type=int, help='an argument for establishing a port number (int)')
parser_server.add_argument('-d', "--working_directory", type=str, help='the directory the server serves its operations on; if argument is unsupplied this command defaults to ./server-files/', default= "server-files")
parser_client = subparser.add_parser('client')
parser_client.add_argument("remote_ip", type=str, help="If you are connecting as a client, input a hostname or ip-address to connect to")
parser_client.add_argument("remote_port", type=int, help="If you are connecting as a client, input a port to connect to. Must be supplied as an integer")
clientsub = parser_client.add_subparsers()
parser.list = clientsub.add_parser("list")
parser.download = clientsub.add_parser("download")
parser.download.add_argument("target_file", type=str, help="The name of the file you want to download from the server")
parser.download.add_argument("-d", "--destination_folder", type=str, help="the folder you want to save the file to; default is current folder", default=".")
parser.upload = clientsub.add_parser("upload")
parser.upload.add_argument("filepath", type=str, help="the name of the file you want to send to the server; searches current directory for match if only name of the file is specified, otherwise tries to send the file with exact file destination")
parser.upload.add_argument("-s", "--source_folder", type=str, help="the folder you want to send the file from; default is current folder", default=".")
args = parser.parse_args()
a = None
# GFTP takes parameters in this order: mode, ip, port, fileloc (=keyword argument)
if args.__contains__("remote_ip") and args.__contains__("remote_port"):
    # client mode
    print("starting GFTP in client mode...")
    a = GFTP.GFTP("client", args.remote_ip, args.remote_port)
    print(a)
    a.connect()
    if args.__contains__("target_file"):
        print("Download operation chosen.")
        a.download(filename=args.target_file, destination_folder=args.destination_folder)
    elif args.__contains__("filepath"):
        print("Upload operation chosen.")
        a.upload(filename=args.filepath, source_folder=args.source_folder)

    else:
        print("List operation chosen.")
        a.list()

elif args.__contains__("hostname") and args.__contains__("port"):
    # server mode
    print("starting GFTP in server mode...")
    a = GFTP.GFTP("server", args.hostname, args.port, fileloc=args.working_directory)
    print(a)
    print("Going to continuous server mode...")
    a.connect()

else:
    parser.error("No mode chosen. Run --help or -h to see options")
