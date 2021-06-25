from datetime import datetime
import requests
import socket 
import json
from icmplib import ping
from nslookup import Nslookup
import time
import sys

#teste de ping
class ConnectionTestPing:

    def __init__(self, ip):
        self.ip = ip
        self.status = ""

    def pingTest(self):
        pingTest = ping(self.ip, count = 1)

        if pingTest.packet_loss == 0.0:
            self.status = f"Connection Status 'OK' to {self.ip}. date: {datetime.now()}"

        else:
            self.status = f"Connection Status 'Loss' to {self.ip}. date: {datetime.now()}"
        
        return self

#teste web
class ConnectionTestWeb:

    def __init__(self, httpAddress):
        self.httpAddress = httpAddress
        self.status = ""

    def webTest(self):
        request = requests.get(self.httpAddress)
        self.status = f"Request Status Code: '{request.status_code}'. date: {datetime.now()}"
        return self

# teste dns
class DnsTest:

    def __init__(self, ipDns, domain):
        self.ipDns = ipDns
        self.status = ""
        self.domain = domain
    
    def dnsTest(self):
        dns_query = Nslookup(dns_servers=[self.ipDns])
        ips_record = dns_query.dns_lookup(self.domain)

        if ips_record.response_full != []:
            self.status = f"Dns status 'OK'. {ips_record.response_full[0]}. date: {datetime.now()}"
        
        else:
            self.status = f"Dns status 'Loss'. date: {datetime.now()}"

        return self

def leitura_arq():
	configtxt = open('config/config.txt','r')
	configtxtall= [line.split() for line in configtxt]
	
	return configtxtall

if len(sys.argv) != 3: 
    print("Inform ip and port")
    sys.exit()
try:
    port = int(sys.argv[1])
    ip = sys.argv[2]

except:
    print("server port must be interer")
    sys.exit()

configtxtall = leitura_arq()
"""ipHost= ''
ipAp = ''
ipWeb = ''
ipDns = ''
httpAdress = ''
domain = ''"""

for teste_elemento in configtxtall: 
	
	if teste_elemento[0] == 'ipHost':
		ipHost = teste_elemento[1]

	elif teste_elemento[0] == 'ipAp':
		ipAp = teste_elemento[1]

	elif teste_elemento[0] == 'ipWeb':
		ipWeb = teste_elemento[1]

	elif teste_elemento[0] == 'ipDns':
		ipDns = teste_elemento[1]

	elif teste_elemento[0] == 'httpAdress':
		httpAdress = teste_elemento[1]

	if teste_elemento[0] == 'domain':
		domain = teste_elemento[1]

while True:
    tempo = 5
    #def status para encaminhar via servidor

    objectPinglist = [ConnectionTestPing(ipHost).pingTest().status,
                    ConnectionTestPing(ipAp).pingTest().status,
                    ConnectionTestPing(ipWeb).pingTest().status,
                    ConnectionTestPing(ipDns).pingTest().status
                    ]

    objectWebTest = ConnectionTestWeb(httpAdress).webTest().status

    obejectDnsTest = DnsTest(ipDns = ipDns, domain = domain).dnsTest().status

    statusMonitor = {"Ping Status": objectPinglist,
                    "Server web Status": objectWebTest,
                    "Dns status": obejectDnsTest
                }
    #print(statusMonitor)
    print(statusMonitor)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as send:
        try:
            send.connect((ip, port))
            b = json.dumps(statusMonitor).encode('utf-8')
            send.sendall(b)
            print("sucesso")


        except ConnectionRefusedError:
            print("nao enviado")


    time.sleep(tempo) 

