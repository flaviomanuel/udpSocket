import socket
import threading
 
# Endereço IP e porta para o servidor
host = 'ip'  # Endereço IP do servidor
porta = 5005  # Porta do servidor
 
# Cria um objeto socket UDP
socket_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
 
# Liga o socket ao endereço e porta especificados
socket_server.bind((host, porta))

friend_ip = "" 
friend_name = ""
friendsList = []

print(f"Servidor UDP aguardando mensagens em {host}:{porta}")


def modify_friend_ip(ip):
    global friend_ip 
    friend_ip = ip

def sendSocketMessage(message,cliente_socket, friendIp = "ip from friend"):
    cliente_socket.sendto(message.encode('utf-8'), (friendIp, 5000))

def verifyIfFriendExists(friendName):
    ip = ""
    for user in friendsList:
        nameUser = user.split(",")
        if(nameUser[0] == friendName):
            global friend_ip 
            friend_ip = nameUser[1]
            return True
        

    return False

# Função para receber mensagens
def receber_mensagens():
    while True:
        try:
            # Recebe os dados e o endereço do remetente
            dados, endereco = socket_server.recvfrom(1024)  # Tamanho do buffer é 1024 bytes

            mensagem = dados.decode('utf-8')
            friendsList.extend(mensagem.split("\n"))
            
            print(f"Recebido de {endereco[0]}:{endereco[1]}: {mensagem}")

        except UnicodeDecodeError:
            print(f"Recebido de {endereco[0]}:{endereco[1]}: Erro de decodificação (não UTF-8)")

# Inicializa uma thread para receber mensagens
thread_recebimento = threading.Thread(target=receber_mensagens)
thread_recebimento.daemon = True
thread_recebimento.start()

# Função para enviar mensagens
def enviar_mensagens():
    cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    while True:
        mensagem = input("Digite a mensagem a ser enviada: ")

        commandSplit = mensagem.split(' ')
        isCommand = commandSplit[0].find(".") != -1

        if isCommand:
            prefix = commandSplit[0]
            commandParamenter =  ""

           

            if(prefix == '.entrar'):
                commandParamenter = commandSplit[1]
                sendSocketMessage(prefix + " " + commandParamenter ,cliente_socket)
                print("comando /entrar print")


            elif(prefix == ".sair"):
                commandParamenter = commandSplit[1]
                print("comando /sair print")
                sendSocketMessage(prefix + " " + commandParamenter ,cliente_socket)

            elif(prefix == ".contatos"):
                print("comando /contatos print")
                sendSocketMessage(prefix + commandParamenter ,cliente_socket)

            else:
                commandParamenter = commandSplit[1]
                friendName = prefix.replace('.', '')
                if(verifyIfFriendExists(friendName)):
                    sendSocketMessage(prefix + commandParamenter ,cliente_socket, friend_ip)
                    print("comando /entrar print")
        
        if mensagem == "/encerrar":
            print("Encerrando o programa...")
            print("Fechando portas de escuta:")
            thread_recebimento.join()
            break
        else:
            cliente_socket.sendto(mensagem.encode('utf-8'), ("10.113.60.230", porta))

# Inicializa uma thread para enviar mensagens
thread_envio = threading.Thread(target=enviar_mensagens)
thread_envio.start()

# Aguarda as threads finalizarem
thread_envio.join()
print("Threads encerradas.")
# Feche o socket (isso nunca será executado no loop acima)
socket_server.close()
print("Socket encerrado. Bye Bye")

