from socket import socket, AF_INET, SOCK_STREAM
import json
import sys
import logging

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

class ServerSocket:
    statusList = []

    def __init__(self, host = '', port = 9090):
        self.host = host
        self.port = port 
    
    def receivePackages(self):
        while True:
            mensage = self.con.recv(1024) 
            if mensage == b'':
                break
            statusMonitor = json.loads(mensage.decode('utf-8'))
            self.statusList.append(statusMonitor)

            with open("www/index.html", "w") as out:
                statusListRev = reversed(self.statusList)
                for monitoramento in statusListRev:
                    out.write(f'<p>  {monitoramento} </p>\n')
                    out.write(f'<br>')

            logging.info(f'save ok: {self.port}')

    def listen(self):
        logging.info(f'Tcp server Listening on: {self.port}')
        self.server = socket(AF_INET, SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen(1)
        while True:
            self.con, self.adr = self.server.accept()
            self.receivePackages()


if len(sys.argv) != 2: 
    print("Inform the server port")
    sys.exit()
try:
    port = int(sys.argv[1])

except:
    print("server port must be interer")
    sys.exit()


TCPserver = ServerSocket(port = port)
TCPserver.listen()