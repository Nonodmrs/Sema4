import socket
from flask import Flask

# Initialisation de l'application Flask
app = Flask(__name__)

# Définition de la route '/get_ip_and_domain_name' pour laquelle on veut récupérer l'IP et le nom de domaine
@app.route('/get_ip_and_domain_name')
def get_ip_and_domain_name():
    # Obtention du nom d'hôte
    hostname = socket.gethostname()
    # Obtention du nom de domaine à partir du nom d'hôte
    domain_name = socket.getfqdn(hostname)
    # Obtention de l'adresse IP à partir du nom d'hôte
    ip = socket.gethostbyname(hostname)
    # Création d'une chaîne de caractères HTML qui contient les informations de nom d'hôte, de nom de domaine et d'adresse IP
    html = f'<h1>Nom d\'hôte : {hostname}</h1><h1>Nom de domaine : {domain_name}</h1><h1>Adresse IP : {ip}</h1>'
    # Renvoi de la chaîne de caractères HTML au client
    return html

# Exécution de l'application Flask
if __name__ == '__main__':
    app.run()

# Lien : http://localhost:5000/get_ip_and_domain_name
