import requests
from flask import Flask

app = Flask(__name__)

@app.route('/get_public_ip')
def get_public_ip():
    response = requests.get('https://api.ipify.org')
    public_ip = response.text
    return f"Votre adresse IP publique est : {public_ip}"

if __name__ == '__main__':
    app.run()

#Lien : http://127.0.0.1:5000/get_public_ip