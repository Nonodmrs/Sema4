from flask import Flask, request
import socket
import threading
import ipaddress

# Création de l'application Flask
app = Flask(__name__)

# Page d'accueil avec formulaire de saisie du port et du subnet
@app.route('/')
def index():
    return '''
        <form method="post" action="/scan">
            <label for="port">Port à scanner :</label>
            <input type="number" id="port" name="port" min="1" max="65535" required><br><br>
            <label for="subnet">Sous-réseau à scanner :</label>
            <input type="text" id="subnet" name="subnet" pattern="^\\d+\\.\\d+\\.\\d+\\.\\d+/\\d+$" required>
            <small> (ex. 192.168.1.0/24)</small><br><br>
            <input type="submit" value="Scanner">
        </form>
    '''

# Page de résultat du scan avec affichage des adresses IP actives
@app.route('/scan', methods=['POST'])
def scan():
    # Récupération des valeurs saisies par l'utilisateur
    port = int(request.form['port'])
    subnet = request.form['subnet']

    # Liste pour stocker les adresses IP actives
    active_ips = []

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
        result = "Adresses IP actives avec le port " + str(port) + " ouvert :<br>"
        for ip in active_ips:
            try:
                hostname = socket.gethostbyaddr(ip)[0]
            except:
                hostname = 'Non résolu'
            result += ip + " - " + hostname + "<br>"
    else:
        result = "Aucune adresse IP active avec le port " + str(port) + " ouvert."

    return result

if __name__ == '__main__':
    app.run()

#Lien : http://127.0.0.1:5000