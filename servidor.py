#!/usr/bin/env python3
import socket
import threading
import time
from structures.LinearProbingLoadFactor import HashTable
from structures.PilhaEncadeada import Pilha

TAM_MSG = 1024
HOST = '0.0.0.0'
PORT = 40000

clientes_conectados = []
lock = threading.Lock()
rodando = True
historico_conversas = HashTable() # Armazena sessões por cliente
clientes = {}  # Dicionário para armazenar {nome: tipo}



def iniciar_sessao(usuario):
    """Cria uma nova sessão para o cliente com um identificador único"""
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")  # ID da sessão
    if usuario not in historico_conversas:
        historico_conversas[usuario] = HashTable()
    historico_conversas[usuario][timestamp] = Pilha()
    return timestamp


def salvar_mensagem(usuario, sessao, mensagem):
    """Adiciona a mensagem à sessão ativa do usuário"""
    if usuario in historico_conversas and sessao in historico_conversas[usuario]:
        historico_conversas[usuario][sessao].empilha(mensagem)



def tratar_cliente(con, cliente):
    """ Função para tratar a comunicação com um cliente específico """
    global clientes_conectados
    
    # print(f"Conexão com o cliente {cliente} estabelecida.")    //////VERIFICAR DEPOIS
    with lock:
        clientes_conectados.append(con)
    
    usuario = None
    sessao = None
        
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
                _, nome, tipo = msg_processada.split(" - ")
                clientes[nome.strip()] = tipo.strip() #ARMAZENA O TIPO DO CLIENTE   
 

                """ Formato esperado: CONNECT - Nome_do_Cliente - Tipo """
                partes = msg_processada.split(' - ')
                if len(partes) >= 2:
                    usuario = partes[1]
                    sessao = iniciar_sessao(usuario)
                    print(f"Novo usuário conectado: {usuario} (sessão: {sessao})")
            
            elif msg_processada.startswith('MSG'):
                resposta = '+OK Mensagem recebida!\n'
                # print(f"{cliente} {msg_processada}")

                """ Formato esperado: MSG - Nome_do_Cliente enviou: mensagem """
                partes = msg_processada.split(' enviou: ')
                if len(partes) == 2 and usuario:
                    mensagem = partes[1]
                    salvar_mensagem(usuario, sessao, mensagem)
                    print(f"{usuario} ({sessao}): {mensagem}")

                con.sendall(resposta.encode('utf-8'))  # Confirmação ao cliente
                
            
            elif msg_processada.startswith('QUIT'):
                resposta = '+OK ate mais!\n'
                print(f"{msg_processada} - {cliente}")
                con.sendall(resposta.encode('utf-8'))  # Confirmação ao cliente

            elif msg_processada.startswith('HISTORICO - '):
                _, solicitante, usuario_solicitado = msg_processada.strip().split(" - ")

                 # Verifica se o solicitante é um atendente
                if clientes.get(solicitante) != "atendente":
                    con.sendall("ERRO: Apenas atendentes podem acessar o histórico.\n".encode('utf-8'))
                    continue
                 # Retorna o histórico se existir
                if usuario_solicitado in historico_conversas:
                    resposta = f"Histórico de {usuario_solicitado}:\n"
                    for sessao, pilha in historico_conversas[usuario_solicitado].items():
                        resposta += f"\nSessão {sessao}:\n"
                        for msg in pilha:
                            resposta += f"{msg}\n"
                    con.sendall(resposta.encode('utf-8'))
                else:
                    con.sendall(f"Nenhum histórico encontrado para {usuario_solicitado}.\n".encode('utf-8'))
            
            elif msg_processada.startswith("LISTAR"):

                _, solicitante, _ = msg_processada.strip().split(" - ")

                if clientes.get(solicitante) != "atendente":
                    con.sendall("ERRO: Apenas atendentes podem listar usuários.\n".encode('utf-8'))
                    continue
                if not clientes:
                    con.sendall("ERRO: Não há usuários do chat.\n".encode('utf-8'))
                    continue
                else:
                    resposta = "Lista de usuários que ja usaram o chat\n"
                    for chave in clientes:
                        resposta += f"{chave} : {clientes[chave]}\n"
                    con.sendall(resposta.encode('utf-8'))
                    
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
            if con in clientes_conectados:  # Verifica antes de remover
                clientes_conectados.remove(con)
        con.close()
        print(f"Conexão com {cliente} encerrada.")


def servidor_input():
    """Thread separada para capturar comandos no terminal"""
    global rodando
    while rodando:
        comando = input().strip().lower()
        if comando == "quit":
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