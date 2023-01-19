# SoftDesk API

Ce projet a été réalisé dans le cadre de la formation OpenClassrooms *Développeur d'application - Python*.

→ Développement d'une API REST sécurisée avec **Django REST framework**.

## Présentation de l'API

L'API est destinée à être utilisée par une application de gestion de projets.

Les utilisateurs peuvent créer des projets et y ajouter des contributeurs. Chaque contributeur est alors en mesure d'associer au projet des problèmes comprenant un titre, une description, un statut, un indice de priorité, etc. Par ailleurs, les problèmes peuvent faire l'objet de commentaires.

Notes :

- L'utilisation de l'API nécessite la création d'un compte et l'authentification via JWT (JSON Web Token).

- Les problèmes et commentaires sont accessibles uniquement aux contributeurs du projet. L'auteur du projet fait nécessairement partie des contributeurs.

- Seul l'auteur d'un projet, problème ou commentaire peut modifier ou supprimer ce dernier.

## Lancement de l'application
- créer un environnement virtuel : python -m venv [nom]
- activer l'environnement virtuel : [nom]\Scripts\activate
- installer les packages : pip install -r requirements.txt
- lancer le serveur de développement : python manage.py runserver
- se rendre à l'adresse : http://127.0.0.1:8000/

## Points de terminaison

### Inscription
→ POST **signup/**
- Données à renseigner (Body) :
    - first_name : *prénom*
    - last_name : *nom*
    - email : *adresse e-mail*
    - password : *mot de passe*

### Récupération d'un couple token d'accès / token de rafraichissement
→ POST **token/**
- Données à renseigner (Body) :
    - email : *adresse e-mail*
    - password : *mot de passe*

### Récupération d'un token d'accès à partir d'un token de rafraichissement
→ POST **token/refresh/**
- Données à renseigner (Body) :
    - refresh : *token de rafraichissement*