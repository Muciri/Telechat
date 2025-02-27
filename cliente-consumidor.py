import socket
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
while True:
    # Enviar uma mensagem para o servidor
    msg = input('--> ')
    if msg.upper() == 'QUIT':
        break
    else:
        sock.sendall(f'({cliente}) enviou: {msg}'.encode('utf-8')) #envia para o servidor o nome do cliente, e sua mensagem
        
        # Receber a resposta do servidor
        resposta = sock.recv(TAM_MSG)
        print(f"Resposta do servidor: {resposta.decode('utf-8')}")
        
        time.sleep(1)  # Aguardar um segundo antes de enviar a próxima mensagem