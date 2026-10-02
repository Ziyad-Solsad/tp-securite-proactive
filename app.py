import os
import sqlite3
from flask import Flask, request, render_template_string

app = Flask(__name__)

# Vulnérabilité 1 : Injection de commande système (CWE-78)
@app.route("/ping")
def ping():
    ip = request.args.get("ip", "127.0.0.1")
    # Exécution directe non assainie
    command = f"ping -c 1 {ip}"
    output = os.popen(command).read()
    return f"<pre>{output}</pre>"

# Vulnérabilité 2 : Injection SQL (CWE-89)
@app.route("/user")
def get_user():
    username = request.args.get("username", "")
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    # Concaténation de chaîne vulnérable
    query = f"SELECT * FROM users WHERE name = '{username}'"
    cursor.execute(query)
    user = cursor.fetchall()
    return str(user)

@app.route("/")
def index():
    return "Application vulnérable pour test SAST"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
