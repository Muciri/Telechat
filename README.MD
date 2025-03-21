# TELECHAT: CHAT DE ATENDIMENTO AO CLIENTE

Bem-vindo ao projeto **Chat de Atendimento ao Cliente**. Este sistema visa proporcionar uma comunicação eficiente entre os clientes e o suporte técnico de uma empresa.

---

## Disciplinas

- **Protocolos de Intercomunicação de Redes de Computadores**
- **Estruturas de Dados**

---

## Professores

- **Leônidas Francisco de Lima Junior**
- **Alex Sandro da Cunha Rêgo**

---

## Equipe

- **Murilo Maciel Rodrigues**
- **Melquisedeque Vital de Albuquerque**
- **Mariana Ludmilla de Lima Maroja Limeira**

## Protocolo de Transporte

- Foi usado o protocolo TCP da camada de transporte, sendo utilizado no projeto por meio da API de sockets.

## Protocolo de Aplicação:

- Foi elaborado o protocolo 3MCP (ou MMMCP - Murilo, Melquisedeque, Mariana Ludmilla Comunication Protocol). Suas mensagens são:

  - **CONNECT**: Do cliente ao servidor, indicando uma conexão. Esta mensagem é feita após um breve cadastro do cliente.
  - **MSG**: Do cliente ao servidor, e vice-versa. Envia (no caso do servidor, redireciona) uma mensagem (o servidor retorna um "+ok mensagem recebida").
  - **QUIT**: Mensagem que pode ser executada tanto pelo cliente quanto pelo servidor, indicando o término de uma conexão.
  - **Listar usuarios**: do cliente (somente do tipo atendente) para o servidor, solicitando os usuarios. O servidor retorna estes usuarios
  - **Historico**: do cliente (somente do tipo atendente) para o servidor, solicitando o historico de mensagens do usuário especificado. O servidor retorna estas mensagens

## Estruturas de Dados: Fila, Pilha e Hash table

## Como rodar:

- **Passos**:
  1. Deve-se executar primeiro o servidor, após isso o cliente.
  2. O cliente deve fazer um pequeno cadastro de seu nome e tipo (atendente ou consumidor).
  3. O cliente deve passar o endereço IP da máquina onde o servidor está rodando.

- **Windows**: Pode-se executar normalmente os programas.

- **Linux**: No terminal, deve-se atribuir permissão de execução aos programas utilizando o comando:
  ```bash
  chmod +x *.py

- após isso pode-se rodar os programas com o comando python3, ou então ./ passando como argumento o nome do arquivo

## Bibliotecas: 

- Tanto o servidor quanto o cliente utilizam as bibliotecas socket e threading, sendo estas bibliotecas nativas do python. A biblioteca socket pra uso da API de Sockets, e a biblioteca threading para permitir mais de um acesso de cliente o servidor.

- É utilizada a biblioteca numpy