from flask import Flask, request
from flask import render_template
import subprocess

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/run_script", methods=["POST"])
def run_script():
    script = request.form["script_name"]
    output = subprocess.run([script], capture_output=True, text=True)
    return output.stdout

if __name__ == "__main__":
    app.run(debug=True)
