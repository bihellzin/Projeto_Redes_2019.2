#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 27 16:31:12 2019

@author: vrs2
"""
import socket
import sys
#Estabelecendo uma conexão com o Tracker
#O IP do server está representado por "x"
connect = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('x', 777)
#Função usada para controlar envio e recepção de requerimentos pelo Tracker
def controlpanel():
    flag=True
    while flag == True:
        command=int(input("Deseja requisitar algum arquivo(1) ou sair do sistema(2)?"))
        if command == 1:
            connect.sendall("1")
        if command == 2:
            flag = False
    command=int(input("Deseja fechar a conexão? Se sim digite (1). Caso não,para abrir novamente o painel de controle (2)"))
    if command == 1:
        connect.close()
    else:
        controlpanel()
    