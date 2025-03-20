#!/usr/bin/env python3
import socket
import threading
from multiprocessing import Manager
from structures.LinearProbingLoadFactor import HashTable

TAM_MSG = 1024
HOST = '0.0.0.0'
PORT = 40000

clientes_conectados = []
lock = threading.Lock()
rodando = True


def salvar_conversa(conversa):
    """Salva a conversa completa do cliente no arquivo ao desconectar"""# Garante que a escrita no arquivo seja segura
    with open("conversas.txt", "w", encoding="utf-8") as f:
            f.write("".join(conversa))

def tratar_cliente(con, cliente):
    """ Função para tratar a comunicação com um cliente específico """
    global clientes_conectados
    conversa_cliente = []  # Armazena mensagens da sessão desse cliente
    
    # print(f"Conexão com o cliente {cliente} estabelecida.")    //////VERIFICAR DEPOIS
    with lock:
        clientes_conectados.append(con)
        
    try:
        while True:
            # Receber dados do cliente
            msg = con.recv(TAM_MSG)
            if not msg:
                # print(f"Cliente {cliente} desconectou.")
                break

            msg_processada = msg.decode('utf-8')

            # Armazena na conversa do cliente
            conversa_cliente.append(msg_processada)
            
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
    except KeyboardInterrupt:
        print("\n[!] Servidor encerrado pelo usuário.")

    finally:
        with lock:
            print(conversa_cliente)
            if conversa_cliente:
                salvar_conversa(conversa_cliente)
            if con in clientes_conectados:  # Verifica antes de remover
                clientes_conectados.remove(con)
        con.close()
        print(f"Conexão com {cliente} encerrada.")


def servidor_input():
    """Thread separada para capturar comandos no terminal"""
    global rodando
    while rodando:
        comando = input().strip().lower()
        if comando.lower() == "quit":
            print("[!] Encerrando servidor...")
            rodando = False
            break




#funçao principal para rodar o servidor
def run_servidor():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST, PORT))
    sock.listen(50)

    print("Servidor aguardando conexões... Digite 'QUIT' para encerrar.")

    # Inicia a thread para capturar entrada do servidor
    thread_input = threading.Thread(target=servidor_input, daemon=True)
    thread_input.start()


    try:
        while rodando:
            sock.settimeout(1)  # Evita travar esperando conexões
            try:
                con, cliente = sock.accept()
                thread = threading.Thread(target=tratar_cliente, args=(con, cliente), daemon=True)
                thread.start()
            except socket.timeout:
                continue
            except Exception as e:
                print(f"Ocorreu um erro: {e}")
                break
    except KeyboardInterrupt:
        print("\n[!] Servidor encerrado pelo usuário.")
    finally:
        sock.close()
        print("[!] Socket fechado. Servidor desligado com sucesso.")

if __name__ == "__main__":
    run_servidor()