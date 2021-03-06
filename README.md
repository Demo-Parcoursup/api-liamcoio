# A propos
Ceci est un exemple d'API RESTFUL codé en Python avec flask pour Parcoursup.
Cette api est disponible via gunicorn à l'addresse: https://api.liamco.io

Fonctionalités:
---------------
- Renvoyer les statistiques d'un site web via l'API Cloudflare (CDN)
- Renvoyer des infos sur le visiteur (Adresse IP, User Agent)

# Dépendances
- Python (>= 3.2)
- [flask](https://github.com/pallets/flask) (>= 1.0.2)
- [requests](https://github.com/psf/requests) (>= 2.21.0)
- [flask-talisman](https://github.com/GoogleCloudPlatform/flask-talisman) (>= 0.7.0)

Optionnels:
-----------
- [gevent](https://github.com/gevent/gevent) (>= 1.3.7)
- [pyOpenSSL](https://github.com/pyca/pyopenssl) (>= 19.0.0)
- [gunicorn](https://github.com/benoitc/gunicorn) (>= 19.9.0)

# Misc
Je recommande d'utiliser gunicorn avec gevent et pyOpenSSL car le packet requests peut mener à des conflits SSL avec flask-talisman et de plus l'envoie d'une requête HTTP ralentie la réponse de l'api d'où la nécessité d'avoir une gestion "concurrent".

# License
[MIT License](LICENSE)
