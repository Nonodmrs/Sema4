from flask import Flask

import os

app = Flask(__name__)

def ping_test():
    hostname = "google.com"
    response = os.system("ping -n 1 " + hostname + " > nul")
    if response == 0:
        return "vous êtes bien connecté"
    else:
        return "vous n'êtes pas connecté à internet"

@app.route('/ping_test')
def index():
    return ping_test()

if __name__ == '__main__':
    app.run()

#Lien : http://127.0.0.1:5000/ping_test