import socket
from  threading import Thread
import os
import ftplib
from ftplib import FTP
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
IP_ADDRESS = '127.0.0.1'
PORT = 8080
SERVER = None
BUFFER_SIZE = 4096
clients = {}

is_dir_exists = os.path.isdir('shared_files')
if(not is_dir_exists):
    os.makedirs('shared_files')


def acceptConnections():
    global SERVER
    global clients

    while True:
        client, addr = SERVER.accept()
        print(client, addr)
        client_name = client.recv(4096).decode().lower()
        clients[client_name] = {
                "client"            : client,
                "address"           : addr,
                "connected_with"    : "",
                "file_name"         : "",
                "file_size"         : 409600
        }
def setup():
    print("\n\t\t\t\t\t\tMusic Sharing App\n")
    global PORT
    global IP_ADDRESS
    global SERVER

    SERVER  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER.bind((IP_ADDRESS, PORT))
    SERVER.listen(100)

    print("\t\t\t\tWaiting for Users to Join")
    print("\n")

    acceptConnections()

def ftp():
    global IP_ADDRESS
    authorizer = DummyAuthorizer()
    authorizer.add_user("root", "toor", ".", perm = "elradfmw")
    handler = FTPHandler
    handler.authorizer = authorizer

    ftp_server = FTPServer((IP_ADDRESS, 21), handler)
    ftp_server.serve_forever()

setup_thread = Thread(target=setup)      
setup_thread.start()

ftp_thread = Thread(target = ftp)
ftp_thread.start()
