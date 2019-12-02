import pandas as pd
#Essa biblioteca vai ajudar a gente a manter uma certa ordem na análise dos dados disponíveis
#Se for usar o PC do CIn, recomendo usar o Ubuntu pois ele não tem frescura com instalar biblioteca
#ou, caso você realmente prefira usar Windows10, O Spyder é a IDE que já vem com esses packs.
#Eu suponho que para usar com o PyCharm basta que o Enviroment seja baseado no Anaconda.
#Em caso de dúvidas no funcionamento da biblioteca, só perguntar.
#Enviei no e-mail (espero) alguns materiais de estudo acerca dela.

import datetime
#Essa biblioteca nos vai fornecer a hora atual no computador

import socket
#Biblioteca necessária para o trabalho

"""
---Last Change: 27/11/2019 17:30---

@author1: André

Desc:
    O programa aqui apresentado visa fazer a função de servidor para o trabalho
    A ideia é basicamente a seguinte:
        - Dois arquivos em formato .csv serão utilizados para guardar os dados dos peers
        - Um arquivo (is_on), vai analizar se o peer está disponível.
        - O outro (who_has), vai analizar se o peer está capaz.
"""

def read_docs():
    """
    Função:
        - Ler os documentos.csv
        - Construir uma estrutura de dados em Pandas com eles
    
    Retornos:
        - Lista contendo ambas estruturas em Pandas dos dois arquivos
    """
    who_has = pd.read_csv("who_has.csv")
    is_on = pd.read_csv("is_on.csv")
    return [who_has, is_on]

class Server:
    """
        Classe usada para representar o servidor em si.
        
        Atributos:
            is_on - Estrutura de dados em Pandas representando quem está ON e quem não está
            who_has - Estrutura de dados em Pandas representando quais arquivos estão disponíveis
                    e quem pode distribuí-los
    """
    def __init__(self, who=[], on=[]):
        self.who_has = who
        self.is_on = on

    def looking_for(self, archive):
        #We gotta improve this so it can also check by timeframe
        #Only useful once we start using sockets
        ok = []
        who = self.who_has["WHO_HAS"].where(self.who_has["ARCHIVE_NAME"]==archive)
        for on in self.is_on["WHO"].where(self.is_on["STATUS"] =="ON"):
            if(on in who):
                ok.append(on)
        return ok

    def peer_got_something(self,new_arc, peer):
        doc1 = open("who_has.csv","a")
        doc1.write(new_arc, peer, datetime.datetime.now())
        doc1.close()
        self.restart()

    def peer_lost_something(self,old_arc, peer):
        doc = open("who_has.csv","r")
        lines = doc.readlines()
        new_lines = []
        for line in lines:
            new_line = line.split(",")
            if((new_line[0] == old_arc)and(new_line[1] == peer)):
                pass
            else:
                new_lines.append(line)
                doc.close()
                doc = open("who_has.csv","w")
        for line in new_lines:
            doc.write(line+"\n")
        self.restart()

    def peer_is_on(self,peer):
        alpha = read_docs()
        is_on = alpha[1]
        if(peer in is_on):
            is_on["STATUS"].where(is_on["WHO"] == peer) = "ON"
        else:
            doc1 = open("is_on.csv","a")
            doc1.write(peer, "OFF", datetime.datetime.now())
            doc1.close()
            self.restart()
            is_on["STATUS"].where(is_on["WHO"] == peer) = "ON"

    def peer_is_off(self,peer):
        alpha = read_docs()
        is_on = alpha[1]
        if(peer in is_on):
           is_on["STATUS"].where(is_on["WHO"] == peer) = "OFF"
           
    def restart(self):
        docs = read_docs()
        self.who_has = docs[0]
        self.is_on = docs[1]
    
    
    def listen(self):
        #UNTESTED METHOD
        #MAY CONTAIN ERRORS!
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ('localhost',777)
        sick.bind(server_address)
        sock.listen(1)
        while(True):
            connection, client_address = sock.accept()
            try:
                while True:
                    data = connection.recv(18)
                    #Tamanho máximo de um IP address + 3 caracteres
                    self.peer_is_on(client_address)
                    #We first gotta define how the client
                    #will send his requests to the tracker
                    #and how the tracker will behave
                    #under these coments, we have just an idea of what we can do:
                    datatype = data[0:3]
                    if(datatype == "REQ"):
                        who = self.looking_for(data[3:])
                        if(len(who[0] < 15)):
                            dif = 15 - len(who[0])
                        for i in range(dif):
                            who[0] = who[0] + ""
                        connection.sendall(who[0])
                    elif(datatype == "SOM"):
                        self.peer_is_off(data[3:])
                        #Same as above
                        connection.sendall("OK")
                    elif(datatype == "LOS"):
                        self.peer_lost_something(data[3:], client_address)
                        #needs improvement in order to keep accepting more stuff in the same message
                        connection.sendall("OK")
                    elif(datatype == "NEW"):
                        self.peer_got_something(data[3:], client_address)
                        #Same as above
                        connection.sendall("OK")
                    elif(datatype == "LOG"):
                        connection.sendall("OK")
                    else:
                        connection.sendall("Sorry, I can't understand you")
            finally:
                connection.close()
