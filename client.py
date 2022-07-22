import socket
import threading
#creazione di una socket inet di tipo stream
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip = input("Inserisci l'ip a cui vuoi connetterti:\n")
port = int(input("Inserisci la porta a cui connettersi:\n"))
print(f"Connessione al server {ip} ...")
#connessione all'indirizzo del server
s.connect((ip, port))

msg = s.recv(1024)
print(msg.decode("utf-8"))

nickname= input('inserisci il tuo nickname e premi invio due volte: ')

#funzione per la recezione
def receive():
    while True:
        try:
            # ricevi messaggi dal server
            # se il messaggio è NICK invia il nickname
            message = s.recv(1024).decode('utf-8')
            if message == 'NICK':
                s.send(nickname.encode('utf-8'))
            else:
                print(message)
        except:
            # Chiusura connessione per un errore
            print("C'è stato un errore")
            client.close()
            break


# Invio messaggi al server
def write():
    while True:
        message = '{}: {}'.format(nickname, input(''))
        s.send(message.encode('utf-8'))

# inizio comunicazione tra client per ascolto
receive_thread = threading.Thread(target=receive)
receive_thread.start()
#scrittura
write_thread = threading.Thread(target=write)
write_thread.start()