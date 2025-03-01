#!/usr/bin/env python3
import socket
import threading

#cadastro do consumidor
cliente = input('qual seu nome completo? ')
while True:
    tipo = input('você é normal[N]? ou preferencial[P] ') #bom adicionar uma verificação robusta depois
    if not tipo.upper() == 'N' and not tipo.upper() == 'P':
        print('destino inválido!')
        continue
    break

#verificação da máquina de destino (IP onde o servidor está rodando)
while True:
    destino = input('qual o IP da máquina de Destino? (digite 0 caso seja a própria máquina) ')
    if not destino == '0' and not destino.count('.') == 3:
        print('destino inválido!')
        continue
    break

TAM_MSG = 1024                                     # Tamanho do bloco de mensagem
HOST = '127.0.0.1' if destino == '0' else destino  # IP do Servidor
PORT = 40000                                       # Porta que o Servidor escuta

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