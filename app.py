# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 23:52:53 2020

@author: Liam Cornu
"""

# Imports
from flask import Flask
from flask_talisman import Talisman

# Mise en place de Flask
app = Flask(__name__)
# Utilisation de Talisman pour forcer la sécurité SSL
Talisman(app, content_security_policy=None)
# Données d'API cloudflare
zone_secret = "XXXXXX"
api_secret = "XXXXXX"
email = "example@example.com"
