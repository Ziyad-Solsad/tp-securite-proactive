import ipaddress
import sqlite3
import subprocess
from flask import Flask, request

app = Flask(__name__)

# Correction 1 : Sécurisation du ping (validation stricte de l'IP + pas de shell)
@app.route("/ping")
def ping():
    ip = request.args.get("ip", "127.0.0.1")
    try:
        # Validation d'un format IP strict pour bloquer toute commande arbitraire
        ipaddress.ip_address(ip)
        result = subprocess.run(
            ["ping", "-c", "1", ip],
            capture_output=True,
            text=True,
            timeout=5
        )
        return f"<pre>{result.stdout}</pre>"
    except ValueError:
        return "Format d'adresse IP invalide", 400
    except Exception as e:
        return f"Erreur : {str(e)}", 500

# Correction 2 : Sécurisation de la requête SQL (requête préparée paramétrée)
@app.route("/user")
def get_user():
    username = request.args.get("username", "")
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    # Utilisation d'un paramètre '?' pour neutraliser l'injection
    query = "SELECT * FROM users WHERE name = ?"
    cursor.execute(query, (username,))
    user = cursor.fetchall()
    conn.close()
    return str(user)

@app.route("/")
def index():
    return "Application sécurisée DevSecOps"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
