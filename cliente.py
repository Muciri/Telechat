#!/usr/bin/env python3
import socket
import threading




#cadastro do usuário
cliente = input('qual seu nome completo? ')
while True:
    tipo_verificacao = input('você é Consumidor[C]? ou atendente[A] ')
    if not tipo_verificacao.upper() == 'C' and not tipo_verificacao.upper() == 'A':
        print('destino inválido!')
        continue
    break

tipo = 'consumidor' if tipo_verificacao.upper() == 'C' else 'atendente'



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

sock.sendall((f'CONNECT - {cliente} - {tipo}\n').encode('utf-8')) #envia para o servidor o nome do cliente e seu tipo

print('conectado ao servidor (digite "QUIT" para sair)')

print()
print("Verificar historico: historico <nome_do_cliente>\n\nListar quem ja utilizou o chat: <listar usuarios>" if tipo == 'atendente' else "Bem vindo, em que posso lhe auxiliar?")

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

#loop para o envio de mensagens para o servidor
while True:
    msg = input(" ")
    if msg.upper() == "QUIT":
        sock.sendall(f'QUIT - {cliente}\n'.encode('utf-8'))
        break
    elif msg.upper().startswith("HISTORICO"):
        if len(msg.split(" ", 1)) == 2:
            sock.sendall(f'HISTORICO - {cliente} - {msg.split(" ", 1)[1]}\n'.encode('utf-8'))
        else:
            print("Formato incorreto. O formato esperado é: historico <nome de usuário>")
    elif msg.upper() == "LISTAR USUARIOS":
        sock.sendall(f'LISTAR - {cliente} - {msg.split(" ", 1)[1]}\n'.encode('utf-8'))
        
    else:
        sock.sendall(f'MSG - {cliente} enviou: {msg}\n'.encode('utf-8'))



sock.close()


print("Desconectado do servidor.")