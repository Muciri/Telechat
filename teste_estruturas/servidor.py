#!/usr/bin/env python3
import socket
import threading
from structures.PilhaEncadeada import Pilha
from structures.FilaEncadeadaHeadAndTail import Fila

TAM_MSG = 1024
HOST = '0.0.0.0'
PORT = 40000

# clientes_conectados = []
clientes_conectados = Fila()
lock = threading.Lock()

def tratar_cliente(con, cliente):
    """ Função para tratar a comunicação com um cliente específico """
    global clientes_conectados

    # print(f"Conexão com o cliente {cliente} estabelecida.")    //////VERIFICAR DEPOIS

    with lock:
        #clientes_conectados.append(con)
        clientes_conectados.enfileirar(con)
    
    try:
        while True:
            # Receber dados do cliente
            msg = con.recv(TAM_MSG)
            if not msg:
                # print(f"Cliente {cliente} desconectou.")
                break

            msg_processada = msg.decode('utf-8')

            if msg_processada.startswith('CONNECT') or msg_processada.startswith('atendente'):  # Reconhecimento do cliente no servidor
                print(f"{msg_processada} - {cliente}") 
            
            elif msg_processada.startswith('MSG'):
                resposta = '+OK Mensagem recebida!\n'
                # print(f"{cliente} {msg_processada}")
                print(f"{msg_processada}")
                con.sendall(resposta.encode('utf-8'))  # Confirmação ao cliente
            
            elif msg_processada.startswith('QUIT'):
                resposta = '+OK ate mais!\n'
                print(f"{msg_processada} - {cliente}")
                con.sendall(resposta.encode('utf-8'))  # Confirmação ao cliente
            
            # Encaminhar mensagem para os outros clientes conectados
            with lock:
                for c in clientes_conectados:
                    if c != con:  # Evitar eco para o próprio remetente
                        # c.sendall(f"{cliente}: {msg_processada}".encode('utf-8'))
                        c.sendall(f"{msg_processada}".encode('utf-8'))
    
    except Exception as e:
        # print(f"Ocorreu um erro com o cliente {cliente}: {e}") ////verificar possíveis excessões depois (o cliente se desconectando gera uma excessão por exemplo)
        pass

    finally:
        with lock:
            if con in clientes_conectados:  # Verifica antes de remover
                #clientes_conectados.remove(con)
                clientes_conectados.desenfileirar()
        con.close()
        print(f"Conexão com {cliente} encerrada.")

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))
sock.listen(50)

print("Servidor aguardando conexões...")

while True:
    try:
        con, cliente = sock.accept()
        thread = threading.Thread(target=tratar_cliente, args=(con, cliente), daemon=True)
        thread.start()
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        break