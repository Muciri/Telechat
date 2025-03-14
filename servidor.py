#!/usr/bin/env python3
import socket
import threading

TAM_MSG = 1024
HOST = '0.0.0.0'
PORT = 40000

clientes_conectados = []
lock = threading.Lock()

def tratar_cliente(con, cliente):
    """ Função para tratar a comunicação com um cliente específico """
    global clientes_conectados

    # print(f"Conexão com o cliente {cliente} estabelecida.")    //////VERIFICAR DEPOIS

    with lock:
        clientes_conectados.append(con)
    
    try:
        while True:
            # Receber dados do cliente
            msg = con.recv(TAM_MSG)
            if not msg:
                print(f"Cliente {cliente} desconectou.")
                break

            msg_processada = msg.decode('utf-8')

            if msg_processada.startswith('CONNECT') or msg_processada.startswith('atendente'):  # Reconhecimento do cliente no servidor
                print(f"{msg_processada} - {cliente}") 
            
            elif msg_processada.startswith('MSG'):
                resposta = '+OK Mensagem recebida!'
                # print(f"{cliente} {msg_processada}")
                print(f"{msg_processada}")
                con.sendall(resposta.encode('utf-8'))  # Confirmação ao cliente
            
            elif msg_processada.startswith('QUIT'):
                resposta = '+OK até mais!'
                print(f"{msg_processada} - {cliente}")
                con.sendall(resposta.encode('utf-8'))  # Confirmação ao cliente
            
            # Encaminhar mensagem para os outros clientes conectados
            with lock:
                for c in clientes_conectados:
                    if c != con:  # Evitar eco para o próprio remetente
                        # c.sendall(f"{cliente}: {msg_processada}".encode('utf-8'))
                        c.sendall(f"{msg_processada}".encode('utf-8'))
    
    except Exception as e:
        print(f"Ocorreu um erro com o cliente {cliente}: {e}")

    finally:
        with lock:
            if con in clientes_conectados:  # Verifica antes de remover
                clientes_conectados.remove(con)
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