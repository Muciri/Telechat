#!/usr/bin/env python3
import socket
import threading
import time

cliente = input('qual seu nome completo? ')
tipo = input('você é preferencial[P] ou normal[N]? ') #bom adicionar uma verificação robusta depois

TAM_MSG = 1024      # Tamanho do bloco de mensagem
HOST = '127.0.0.1'  # IP do Servidor
PORT = 40000        # Porta que o Servidor escuta

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

sock.sendall((f'cliente: {cliente} - {tipo}').encode('utf-8')) #envia para o servidor o nome do cliente e seu tipo

print('conectado ao servidor (digite "QUIT" para sair)')

def receber_mensagens():
    """ Thread para receber mensagens do servidor continuamente """
    while True:
        try:
            msg = sock.recv(TAM_MSG)
            if not msg:
                break
            print(f"\n{msg.decode('utf-8')}\n--> ", end="")
        except:
            print("\n[Conexão perdida com o servidor]")
            break

# Iniciar thread para receber mensagens do servidor
thread_receber = threading.Thread(target=receber_mensagens, daemon=True)
thread_receber.start()

while True:
    msg = input(" ")
    if msg.upper() == "QUIT":
        break
    sock.sendall(f'({cliente}) enviou: {msg}'.encode('utf-8'))

sock.close()
print("Desconectado do servidor.")


# while True:
#     # Enviar uma mensagem para o servidor
#     msg = input('--> ')
#     if msg.upper() == 'QUIT':
#         break
#     else:
#         sock.sendall(f'({cliente}) enviou: {msg}'.encode('utf-8')) #envia para o servidor o nome do cliente, e sua mensagem
        
#         # Receber a resposta do servidor
#         resposta = sock.recv(TAM_MSG)
#         print(f"Resposta do servidor: {resposta.decode('utf-8')}")
        
#         time.sleep(1)  # Aguardar um segundo antes de enviar a próxima mensagem