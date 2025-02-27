#!/usr/bin/env python3
import os
import socket
import threading

TAM_MSG = 1024         # Tamanho do bloco de mensagem
HOST = '0.0.0.0'       # IP de alguma interface do Servidor
PORT = 40000           # Porta que o Servidor escuta

def tratar_cliente(con, cliente):
    """ Função para tratar a comunicação com um cliente específico """
    print(f"Conexão com o cliente {cliente} estabelecida.")
    
    while True:
        try:
            # Receber dados do cliente
            msg = con.recv(TAM_MSG)
            if not msg:
                print(f"Cliente {cliente} desconectou.")
                break

            # print(f"{cliente} enviou: {msg.decode('utf-8')}")
            
            msg_processada = msg.decode('utf-8')
            
            if msg_processada.startswith('cliente'): # Reconhecimento do cliente no servidor
                print(f"{msg.decode('utf-8')} - {cliente}") 
            else:
                resposta = 'Mensagem recebida!'
                print(f"{cliente} {msg.decode('utf-8')}")
                
                con.sendall(resposta.encode('utf-8')) # Enviar uma resposta ao cliente confirmando a mensagem
        
        except Exception as e:
            print(f"Ocorreu um erro com o cliente {cliente}: {e}")
            break
    
    # Fechar a conexão com o cliente
    con.close()
    print(f"Conexão com o cliente {cliente} fechada.")

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv = (HOST, PORT)
sock.bind(serv)
sock.listen(50)

print("Servidor aguardando conexões...")

while True:
    try:
        # Aceitar uma conexão de cliente
        con, cliente = sock.accept()
        
        # Criar uma nova thread para tratar o cliente
        thread = threading.Thread(target=tratar_cliente, args=(con, cliente))
        thread.daemon = True  # Tornar a thread como "daemon", ou seja, ela será encerrada quando o programa principal terminar.
        thread.start()
        
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        break