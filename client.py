"""
Last Modified: 02/12/2019

@author: vrs2

@author2: acasf
"""
import socket
#Classe obrigatória para o trabalho
import os
#Essa classe nos vai auxiliar a identificar o tamanho dos arquivos
#Bem como criará a pasta do compartilhamento se necessário 
import sys
#Não sei pra que serve SYS
from urllib.request import urlopen
#Essa biblioteca nos ajudará a recuperar meu IP.
class Client:
    def __init__(self):
        self.appear_on = True

    def new_stuff(self):
        #Incomplete
        #I also don't knwo how to get our own IP address
        if(os.path.exists("share")):
            os.mkdir("share")
        else:
            pass
        #Same questions as "im_off()", might ask ehammo
        
    
    def send_request(self,moi, what):
        server_address = ('localhost', 777)
        moi.connect(server_address)
        try:
            data = "REQ" + what
            moi.sendall(data)
            who = moi.recv(16)
        except:
            moi.close()
        return who
                
    def im_off(self, moi):
        #IDK how to procceed here. Might ask ehammo
        server_address = ('localhost', 777)
        moi.connect(server_address)
        try:
            msg = "SOM"
            moi.sendall(msg)
            #IDK how to get our own IP
            data = moi.recv(2)
        finally:
            moi.close()
        self.appear_on = False
        return data
    
    def its_off(self ,moi, peer):
        server_address = ('localhost', 777)
        moi.connect(server_address)
        try:
            msg = "SOM" + peer
            moi.sendall(msg)
            data = moi.recv(2)
            item=data.decode("utf-8")
            if item  == "OK":
                print("Peer is off")
            
            else:
                print("Failed")
                
            #The length of the response will be only 2 chars
        finally:
            moi.close()
        return data
    
    def peer_lost(self, who, what):
        pass
        #This will tell the tracker when a peer lost some data
        #The datatype code is "LOS"
    
    def main(self):
        connect = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # forma correta = my_address = urlopen('https://ident.me').read().decode('utf8')
        my_address = "127.0.0.1" # forma temporária
        print(my_address)
        flag = True
        while flag == True:

            command=int(input("Deseja requisitar algum arquivo(1), seedar(2) ou sair do sistema(3)?"))
            #We shouldn't use inputs in classes
            if command == 1:
                arquivo = input("Digite o nome do arquivo:")
                ip = self.send_request(connect, arquivo)
                self.getarchive(ip)

            if command == 2:

                seed = self.im_seed(my_address)
    
            if command == 3:
                #Change it to an elif
                flag = False
                #There are more than 3 options in this scenario

        command=int(input("Deseja fechar a conexão? Se sim digite (1). Caso não,para abrir novamente o painel de controle (2)"))
        #We shouldn't use inputs in classes
        if command == 1:
            connect.close()
        else:
            self.main()
            #I'm skeptical about the functionability of this
    
    def i_have(self, path):
        data = open(path, "r")
        if data:
            return True
        else:
            return False
        
    def im_seed(self, my_address):
        socket_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_tcp.bind((my_address,777))
        socket_tcp.listen(5)
        while True:
            print ('Waiting connection...')
            connection, addr = socket_tcp.accept()
            print ("Peer connected - IP:", addr)
            while True:
                request = connection.recv(150)
                print(request)
                file_name = request.decode("utf-8")
                print(file_name)
                have = self.i_have(file_name)
                if have:
                    file = open(file_name, 'r')
                    kar = file.read(150)
                    connection.send(kar.encode())
            print ("Upload complete")
            file.close()
            connection.close()
        socket_tcp.close()

    def getarchive(self, address):
        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connection.connect((address,777))
        while True:
            name = input("Enter file name: ")
            connection.sendall(name.encode())
            print("Wainting for file...")
            data = connection.recv(150)
            print("Download completed :)")
            if data:
                print(str(data))
            else:
                connection.close()

if __name__ == "__main__":
    a = Client()
    a.main()
