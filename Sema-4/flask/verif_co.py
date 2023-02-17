# Import de Flask
from flask import Flask

# Import de requests pour vérifier la connexion internet
import requests

# Initialisation de l'application Flask
app = Flask(__name__)

@app.route('/get_connection_status')
# Fonction pour vérifier la connexion internet
def get_connection_status():
    try:
        # Envoie une requête GET à Google avec un timeout de 5 secondes
        response = requests.get("http://google.com", timeout=5)
        if response.status_code == 200:
            # Si la réponse est 200 (OK), on renvoie "vous êtes bien connecté"
            return "vous êtes bien connecté"
        else:
            # Sinon, on renvoie "déconnecté"
            return "déconnecté"
    except requests.exceptions.RequestException:
        # Si une exception RequestException est levée, on renvoie "déconnecté"
        return "déconnecté"

# Route pour la page d'accueil
@app.route('/')
def index():
    # On appelle la fonction get_connection_status() et on renvoie le résultat
    return get_connection_status()

# Condition pour exécuter l'application Flask si le fichier est exécuté en tant que programme principal
if __name__ == '__main__':
    app.run()

# L'URL de la page est http://127.0.0.1:5000/get_connection_status
