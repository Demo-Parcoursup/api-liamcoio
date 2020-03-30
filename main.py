# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 23:52:50 2020

@author: Liam Cornu
"""

# Import de l'app flask et de la clé API
from app import app, zone_secret, api_secret, email

# Import librairies tiers
from flask import jsonify
from flask import request
import requests

# Code en cas de réponse 404 (Page non trouvée)
@app.errorhandler(404)
def not_found():
    # Message a affiché
    message = {
        "status": 404,
        "message": "Cette url n'a pas été trouvée (eh oui cette API prends en compte les erreurs 404): "
        + request.url,
    }
    # Encodage en JSON du message
    message_json = jsonify(message)
    # Code de Status HTTP à renvoyer
    message_json.status_code = 404
    return message_json

# Code du root de l'api
@app.route("/", methods=["GET", "POST", "PUT", "PATCH", "OPTIONS", "HEAD"]) # Méthodes acceptées
def homepage():
    # Fonction qui envoie une requête à l'API cloudflare
    try:
        r = requests.get(
            f"https://api.cloudflare.com/client/v4/zones/{zone_secret}/analytics/dashboard?since=-43800&until=0&continuous=false",
            headers={
                "X-AUTH-EMAIL": email,
                "X-AUTH-KEY": api_secret,
            },
        )
        # Filtrage des résultats en JSON
        since = r.json()["result"]["totals"]["since"]
        until = r.json()["result"]["totals"]["until"]
        request_all = r.json()["result"]["totals"]["requests"]["all"]
        request_cached = r.json()["result"]["totals"]["requests"]["cached"]
        request_uncached = r.json()["result"]["totals"]["requests"]["uncached"]
        ssl = r.json()["result"]["totals"]["requests"]["ssl"]
        http_status = r.json()["result"]["totals"]["requests"]["http_status"]
        content_type = r.json()["result"]["totals"]["requests"]["content_type"]
        country = r.json()["result"]["totals"]["requests"]["country"]
        # Mise en place de la réponse
        code = {
            "domaine": "liamco.io",
            "depuis": since,
            "jusqu_a": until,
            "nombre_de_requetes": {
                "totales": request_all,
                "mise_en_cache": request_cached,
                "pas_mise_en_cache": request_uncached,
                "ssl": ssl,
            },
            "status_http": http_status,
            "type_de_contenue": content_type,
            "pays": country,
        }
    except Exception as e:
        return crash(str(e))
    try:
        # Code pour acquérir l'addresse IP du visiteur
        if request.environ.get("HTTP_X_FORWARDED_FOR") is None:
            ip_address = request.environ["REMOTE_ADDR"]
        else:
            ip_address = request.environ["HTTP_X_FORWARDED_FOR"]
        # Données du User-Agent du visiteur (naviguateur)
        request_data = request.headers.get("User-Agent")
        # Message à renvoyer
        message = {
            "message": "Bienvenue à ce petit exemple d'API codé en guise de démonstration pour Parcoursup. Cet API RESTFUL est programmé en Python avec flask et gunicorn",
            "methode_HTTP": request.method,
            "statistiques_du_site": code,
            "info_visiteur": {
                "ip": ip_address,
                "agent_naviguateur": request_data,
            },
        }
        # Encodage JSON de la réponse et mise en place d'un code de status 200 (OK)
        message_json = jsonify(message)
        message_json.status_code = 200
        return message_json
    except Exception as e:
        return crash(str(e))

# En cas d'erreur systéme
@app.errorhandler(500)
def crash(error=None):
    # Renvoyer l'erreur déclaré par le traceback Python
    message = {
        "status": 500,
        "message": "Quelque chose c'est mal passé: " + error,
    }
    message_json = jsonify(message)
    message_json.status_code = 500
    return message_json


if __name__ == "__main__":
    app.run()
