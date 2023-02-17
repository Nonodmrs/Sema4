import time #Ce module sert à manipuler le temps dans un code en python, dans notre cas il nous sert à calculer les vitesses de DL et UL
import threading #Ce module sert à lancer divers processus léger, dans notre cas il nous sert à lancer divers scan dans la fonction scan réseau.
import requests #Ce module sert à envoyer des requêtes HTTP en utilisant Python, nous nous en servons dans la partie connection.
import ipaddress #Ce module sert à inspecter et manipuler des adresses IP, nous nous en servons un peu partout dans nos fonctions, c'est un module très utile.
import socket #Ce module est utilisé dans plusieurs fonction et permet de gérer les connexions par socket
import psutil #Ce module permet de récupérer des informations sur l'utilisation du système et sur la gestion des processus en cours d'exécution
import os     #Ce module fournit des fonctionnalités pour communiquer avec les systèmes d'exploitation. #La bibliothèque time de Python fournit des fonctions pour travailler avec l'heure et la date.
import tkinter as tk
from tkinter import simpledialog #Tkinter permet d'afficher une interface graphique

#----------------------------------------------------------------------------------------------------------------------------------------------------------
#FONCTION 1 Ce code récupère le nom d'hôte ainsi que le domaine et son adresse ip

#ok
def get_ip_and_domain_name():
    hostname = socket.gethostname()
    domain_name = socket.getfqdn(hostname)
    ip = socket.gethostbyname(hostname)
    return hostname, domain_name, ip

hostname, domain_name, ip = get_ip_and_domain_name()
print("Nom d'hôte : ", hostname)
print("Nom de domaine : ", domain_name)
print("Adresse IP : ", ip)

#----------------------------------------------------------------------------------------------------------------------------------------------------------
#FONCTION 2 Ce code récupère l'adresse ip publique

#ok
def get_public_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    public_ip = s.getsockname()[0]
    s.close()
    return public_ip

print("votre ip publique est : ", get_public_ip())


#----------------------------------------------------------------------------------------------------------------------------------------------------------
#FONCTION 3 Ce code permet de voir si la connection à google est établie ou non

#ok
def get_connection_status():
    try:
        response = requests.get("http://google.com", timeout=5)
        if response.status_code == 200:
            return "vous êtes bien connecté"
        else:
            return "déconnecté"
    except requests.exceptions.RequestException:
        return "déconnecté"

print(get_connection_status())


#----------------------------------------------------------------------------------------------------------------------------------------------------------
#FONCTION 4 Ce code permet d'effectuer un SCAN RESEAU et retourne les ip qui sont trouver sur un port

#ok
# Liste pour stocker les adresses IP actives
active_ips = []

# Affichage d'une boîte de dialogue pour demander le port à scanner
root = tk.Tk()
root.withdraw()
port = simpledialog.askinteger("Port à scanner", "Entrez le port à scanner:", minvalue=1, maxvalue=65535)

# Affichage d'une boîte de dialogue pour demander le sous-réseau à scanner
root = tk.Tk()
root.withdraw()
subnet = simpledialog.askstring("Sous-réseau à scanner", "Entrez le sous-réseau à scanner (ex. 192.168.1.0/24):")

def scan_ip(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.5)
    try:
        # Tentative de connexion au port spécifié
        result = sock.connect_ex((str(ip), port))
        if result == 0:
            # Ajout de l'adresse IP active à la liste
            active_ips.append(str(ip))
    except:
        pass
    sock.close()

# Boucle de scan des adresses IP
threads = []
for ip in ipaddress.ip_network(subnet).hosts():
    t = threading.Thread(target=scan_ip, args=(ip, port))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

# Affichage des adresses IP actives avec le nom de l'hôte
if active_ips:
    print("Adresses IP actives avec le port " + str(port) + " ouvert :")
    for ip in active_ips:
        hostname = socket.gethostbyaddr(ip)[0]
        print(ip + " - " + hostname)
else:
    print("Aucune adresse IP active avec le port " + str(port) + " ouvert.")


#----------------------------------------------------------------------------------------------------------------------------------------------------------
#FONCTION 5 Ce code permet de faire un speedtest en download et en upload et retourne les valeurs de ceci en Mbps

#ok
def download_speed(file_size, url):
    start = time.time()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((url, 80))
    s.sendall(b'GET /large-file HTTP/1.1\r\nHost: example.com\r\n\r\n')
    s.recv(file_size)
    end = time.time()
    s.close()
    return file_size / (end - start)

def upload_speed(file_size, url):
    start = time.time()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((url, 80))
    s.sendall(b'POST /large-file HTTP/1.1\r\nHost: example.com\r\nContent-Length: file_size\r\n\r\n')
    s.sendall(b'0'*file_size)
    end = time.time()
    s.close()
    return file_size / (end - start)

file_size = 1 # 100MB
url = "example.com"
print("Download speed: {:.2f} Mbps".format(download_speed(file_size, url)))
print("Upload speed: {:.2f} Mbps".format(upload_speed(file_size, url)))


#----------------------------------------------------------------------------------------------------------------------------------------------------------
#FONCTION 6 ce code permet de faire un ping à google et montre à l'écran si la connection est ok ou non
    
 #ok   

def ping_test():
    hostname = "google.com"
    response = os.system("ping -n 1 " + hostname + " > nul && echo votre connection est bien établie || echo vous n'êtes pas connecté à internet")
    return response

print(ping_test())



