import socket
import threading
import random

HOST = '26.250.188.39'
PORT = 9999

# Conexão
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST,PORT))

# Nome
nome = input("Informe seu nome: ")
sock.sendall(str.encode(nome))

# Mensagens de entrada
entermsg = [
    'Um %s selvagem apareceu!',
    'O(A) %s spawnou no chat!',
    '%s se juntou à festa!',
    '%s acabou de chegar, segure minha cerveja!',
    'Swooosh, %s acabou de pousar!',
    'Bem vindo, %s. Espero que tenha trago pizza!'
]

print("----- ULTRA MSN 2 -----")
print("COMANDOS:\n/quit -> sair\n/tell @nome para msg privada\n/help para ver os comandos\n-----------------------")

sock.sendall(str.encode(random.choice(entermsg) % (nome)))

def RecebeDados(sock):
    while True:
        mensagemR = sock.recv(1024).decode()
        print(mensagemR)

# Mensagem cliente
try:
    threadRecebeDados = threading.Thread(target = RecebeDados, args = ([sock]))
    threadRecebeDados.start()
    while True:
        mensagem = input(f'{nome} >> ')
        if mensagem == "/quit":
            break
        elif mensagem == '/help':
            print("-----------------------\nCOMANDOS:\n/quit -> sair\n/tell @nome para msg privada\n/help para ver os comandos\n-----------------------")
        sock.sendall(str.encode(mensagem))
finally:
    sock.close()