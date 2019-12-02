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
        #Still needs improvements
        flag=True
        while flag == True:
            command=int(input("Deseja requisitar algum arquivo(1) ou sair do sistema(2)?"))
            #We shouldn't use inputs in classes
            if command == 1:
                self.send_request(connect)
            if command == 2:
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
    
    def getarchive(self,connect, address):
        #Incomplete
        connect.sendall("getsize")
