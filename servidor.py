import socket
import threading
import re

HOST = '26.250.188.39'
PORT = 9999

# Conexão
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST,PORT))
sock.listen()

print(f"O servidor {HOST}:{PORT} está aguardando conexões...")
names = {
    }

def RecebeDados(conn, ender):
    try:
        nome = conn.recv(1024).decode()
        names[conn] = nome
    except:
        print("Ocorreu um erro durante o recebimento do nome de um novo usuário")
        return
    
    print(f"Conectado com {nome}, IP: {ender[0]}, PORTA: {ender[1]}")
    ver = True
    while True:
        try:
            # Bloco pra exibir mensagem de entrada
            if ver:
                mensagem = conn.recv(1024).decode()
                for cliente in names:
                    cliente.sendall(str.encode(mensagem))
                    ver = False
            else:
                mensagem = conn.recv(1024).decode()
                if mensagem == "/quit":
                    break
                
                # Bloco de unicast
                for value in names.values():
                    x = re.search(f"^/tell @{value} .+$", mensagem)
                    if x:
                        tellconn = [k for k, v in names.items() if v == value]
                        mensagemfinal = mensagem.replace(f'/tell @{value}', '')
                        tellconn[0].sendall(str.encode(f"{nome} Sussurou para você: {mensagemfinal}"))
                        break
                    else:
                        continue
                
                # Bloco de condicional para exibir Broadcast
                if x == None:
                    for cliente in names:
                        if cliente != conn:
                            cliente.sendall(str.encode(f"{nome} >> {mensagem}"))
        except:
            print("Ocorreu algum erro na recepção de dados, encerrando conexão")
            break
    conn.close()

# Main loop
while True:
    try:
        conn, ender = sock.accept()
    except:
        print("Ocorreu um erro durante o ACCEPT() de um novo usuário")
        continue
    
    threadRecebeDados = threading.Thread(target = RecebeDados, args = ([conn,ender]))
    threadRecebeDados.start()