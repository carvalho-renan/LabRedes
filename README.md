# LabRedes

Sistema para Monitoramento de Redes

## Docker Basics
Construindo aplicação com 3 serviços: Monitor, ServerTcp e Apache Server.

Monitor: Gera Ping-Tests, DNS-Test e GetRequest.

ServerTcp: Salva os testes em um arquivo .html

Servidor Apache: Cria um servidor http para mostrar os testes.

Cada serviço deve ser executado em um container diferente.

## Instalação
Em primeiro lugar, você precisa instalar o docker. Vá para a página oficial para mais detalhes sobre a instalação.

## Containers
### Execute o container "monitor".

sudo docker run --rm --network=host --name=monitor labredes2021 python3 monitor.py "PortServer" "HostServer"

### Exemplo

sudo docker run --rm -it --network=host stephanybino/labredesmonitor python3 monitor.py 9091 192.168.1.99 (IpServer)

Obs: O comando acima deve estar na mesma pasta do seu config.txt (por exemplo, este arquivo está na pasta config deste mesmo repositório).

### Agora, na mesma pasta execute os containers "tcpserver" e "my-apache-app".

sudo docker run --rm -it -p 9091:9091 -v "$(pwd):/app/www" stephanybino/labredesserver python3 server.py 9091

sudo docker run -it --rm -d --name my-apache-app -p 8080:80 -v "$PWD":/usr/local/apache2/htdocs/ httpd:2.4
