import os
from flask import Flask
from routes.endpoints import endpoints_blueprint
from routes.plots import plots_blueprint

app = Flask(__name__)

# Datenbank-Konfiguration zentral definieren
app.config['DB_CONFIG'] = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_API_USER"),
    "password": os.getenv("DB_API_USER_PW"),
    "database": os.getenv("DB_NAME")
}

# Blueprint für View-Routen registrieren
app.register_blueprint(endpoints_blueprint)
app.register_blueprint(plots_blueprint)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)