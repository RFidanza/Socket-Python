import socket
import threading
import requests

#inizializazzione di due variabili
clients=[]
nicknames=[]

#codice per apertura porta
port = int(input("Inserisci la porta che vuoi aprire:\n"))

print("Adding socket...")
#creazione di una socket inet di tipo stream
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#nome host
hostname = socket.gethostname()
print(f"Nome host: {hostname}")
#indirizzo ip host
ip_address = socket.gethostbyname(hostname)
print(f"Indirizzo host: {ip_address}")
r = requests.get(r'http://jsonip.com')
#indirizzo ip pubblico
public_ip_address = r.json()['ip']
s.bind((ip_address, port))
print("aperta la connessione con l'ip: "+public_ip_address+" e porta: "+str(port))
#server aperto
s.listen(5)
print("Inizializzazione effettuata,in ascolto...")


#Invio messaggio a tutti i clients connessi
def broadcast(message):
    for client in clients:
        client.send(message)


#Manipolazione messaggi clients
def handle(client):
    while True:
        try:
            # trasmissione dei messaggi
            message = client.recv(1024)
            broadcast(message)
        except:
            # Rimozione e chiusura dei clients
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast('{} è uscito!'.format(nickname).encode('utf-8'))
            nicknames.remove(nickname)
            break



# Recezione/ Funzione di ascolto
def receive():
    while True:
        # connessione accettata
        client, address = s.accept()
        print("Connesso con {}".format(str(address)))

        # Richiesta nickname
        client.send('NICK'.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        nicknames.append(nickname)
        clients.append(client)

        # scrittura e trasmissione dei nicknames
        print("Il nickname è {}".format(nickname))
        broadcast("{} è entrato!".format(nickname).encode('utf-8'))
        client.send('Connesso al server!'.encode('utf-8'))

        # inizia a gestire le comunicazione tra i clienti
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()
print('Il server è attivo...')
receive()