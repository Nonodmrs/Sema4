import requests
import socket
import threading
import time
import ipaddress
from tkinter import simpledialog
import tkinter as tk

from flask import Flask

app = Flask(__name__)

@app.route('/speed_test/<int:file_size>/<url>')
def speed_test(file_size, url):
    # Création de deux threads pour exécuter les tests de vitesse de téléchargement et de téléversement en parallèle
    download_thread = threading.Thread(target=download_speed, args=(file_size, url))
    upload_thread = threading.Thread(target=upload_speed, args=(file_size, url))
    download_thread.start()
    upload_thread.start()
    
    # Attente que les deux threads se terminent
    download_thread.join()
    upload_thread.join()
    
    # Retourne les résultats de tests de vitesse de téléchargement et de téléversement
    return "{} - {}".format(download_speed.result, upload_speed.result)


def download_speed(file_size, url):
    # Mesure du temps de téléchargement
    start = time.time()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((url, 80))
    s.sendall(b'GET /large-file HTTP/1.1\r\nHost: example.com\r\n\r\n')
    s.recv(file_size)
    end = time.time()
    s.close()
    
    # Calcul de la vitesse de téléchargement en Mbps
    download_speed.result = "Download speed: {:.2f} Mbps".format(file_size / (end - start) / 10000)

def upload_speed(file_size, url):
    # Mesure du temps de téléversement
    start = time.time()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((url, 80))
    s.sendall(b'POST /large-file HTTP/1.1\r\nHost: example.com\r\nContent-Length: file_size\r\n\r\n')
    s.sendall(b'0'*file_size)
    end = time.time()
    s.close()
    
    # Calcul de la vitesse de téléversement en Mbps
    upload_speed.result = "Upload speed: {:.2f} Mbps".format(file_size / (end - start) / 100000)


if __name__ == '__main__':
    # Initialisation des variables de résultats à None
    download_speed.result = None
    upload_speed.result = None
    
    # Démarrage du serveur Flask pour exposer l'API REST
    app.run(debug=True)

#lien de test local : http://127.0.0.1:5000/speed_test/10000/www.google.com
