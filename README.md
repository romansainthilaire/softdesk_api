# SoftDesk API

Ce projet a été réalisé dans le cadre de la formation OpenClassrooms *Développeur d'application - Python*.

→ Développement d'une API REST sécurisée avec **Django REST framework**.

## Présentation de l'API

L'API est destinée à être utilisée par une application de gestion de projets.

Les utilisateurs peuvent créer des projets et y ajouter des contributeurs. Chaque contributeur est alors en mesure d'associer au projet des problèmes comprenant un titre, une description, un statut, un indice de priorité, etc. Par ailleurs, les problèmes peuvent faire l'objet de commentaires.

<ins>Notes :</ins>

- L'utilisation de l'API nécessite la création d'un compte et l'authentification via JWT (JSON Web Token).

- L'utilisateur peut accéder uniquement aux projets auxquels il contribue. De même, les problèmes et commentaires sont accessibles uniquement aux contributeurs du projet. Par ailleurs, l'auteur du projet fait obligatoirement partie des contributeurs.

- Seul l'auteur d'un projet, problème ou commentaire peut modifier ou supprimer ce dernier.

## Lancement de l'application
- créer un environnement virtuel : python -m venv [nom]
- activer l'environnement virtuel : [nom]\Scripts\activate
- installer les packages : pip install -r requirements.txt
- lancer le serveur de développement : python manage.py runserver
- se rendre à l'adresse : http://127.0.0.1:8000/

## Points de terminaison

La documentation **Postman** de l'API est disponible à l'adresse suivante : https://documenter.getpostman.com/view/22554176/2s8ZDX3hZh

### Inscription
→ POST **signup/**
- Body :
    - first_name : *prénom*
    - last_name : *nom*
    - email : *adresse e-mail*
    - password : *mot de passe*

### Récupération d'une paire de tokens : token d'accès et token de rafraichissement
→ POST **token/**
- Body :
    - email : *adresse e-mail*
    - password : *mot de passe*

### Récupération d'un token d'accès à partir d'un token de rafraichissement
→ POST **token/refresh/**
- Body :
    - refresh : *token de rafraichissement*

### Récupération des projets
→ GET **projects/**
- Headers :
    - Authorization : Bearer *token d'accès*

### Création d'un projet
→ POST **projects/**
- Headers :
    - Authorization : Bearer *token d'accès*
- Body :
    - title : *titre du projet*
    - description : *description du projet*
    - type : *nature du projet (ex : BACK-END)*

### Récupération d'un projet
→ GET **projects/<project_id>/**
- Headers :
    - Authorization : Bearer *token d'accès*

### Modification d'un projet
→ PUT **projects/<project_id>/**
- Headers :
    - Authorization : Bearer *token d'accès*
- Body :
    - title : *titre du projet*
    - description : *description du projet*
    - type : *nature du projet (ex : BACK-END)*

### Suppression d'un projet
→ DELETE **projects/<project_id>/**
- Headers :
    - Authorization : Bearer *token d'accès*

### Récupération des contributeurs d'un projet
→ GET **projects/<project_id>/users/**
- Headers :
    - Authorization : Bearer *token d'accès*

### Ajout d'un contributeur à un projet
→ POST **projects/<project_id>/users/<user_id>/**
- Headers :
    - Authorization : Bearer *token d'accès*

### Suppression d'un contributeur d'un projet
→ DELETE **projects/<project_id>/users/<user_id>/**
- Headers :
    - Authorization : Bearer *token d'accès*

### Récupération des problèmes d'un projet
→ GET **projects/<project_id>/issues/**
- Headers :
    - Authorization : Bearer *token d'accès*

### Ajout d'un problème à un projet
→ POST **projects/<project_id>/issues/**
- Headers :
    - Authorization : Bearer *token d'accès*
- Body :
    - title : *titre du problème*
    - description : *description du problème*
    - tag : *balise (ex : BUG)*
    - priority : *priorité (ex : ÉLEVÉE)*
    - status : *statut (ex : EN COURS)*

### Récupération d'un problème
→ GET **projects/<project_id>/issues/<issue_id>/**
- Headers :
    - Authorization : Bearer *token d'accès*

### Modification d'un problème
→ PUT **projects/<project_id>/issues/<issue_id>/**
- Headers :
    - Authorization : Bearer *token d'accès*
- Body :
    - user_in_charge_id : *identifiant du responsable du problème*
    - title : *titre du problème*
    - description : *description du problème*
    - tag : *balise (ex : BUG)*
    - priority : *priorité (ex : ÉLEVÉE)*
    - status : *statut (ex : EN COURS)*

### Suppression d'un problème
→ DELETE **projects/<project_id>/issues/<issue_id>/**
- Headers :
    - Authorization : Bearer *token d'accès*

### Récupération des commentaires d'un problème
→ GET **projects/<project_id>/issues/<issue_id>/comments/**
- Headers :
    - Authorization : Bearer *token d'accès*

### Ajout d'un commentaire à un problème
→ POST **projects/<project_id>/issues/<issue_id>/comments/**
- Headers :
    - Authorization : Bearer *token d'accès*
- Body :
    - description : *commentaire*

### Récupération d'un commentaire
→ GET **projects/<project_id>/issues/<issue_id>/comments/<comment_id>/**
- Headers :
    - Authorization : Bearer *token d'accès*

### Modification d'un commentaire
→ PUT **projects/<project_id>/issues/<issue_id>/comments/<comment_id>/**
- Headers :
    - Authorization : Bearer *token d'accès*
- Body :
    - description : *commentaire*

### Suppression d'un commentaire
→ DELETE **projects/<project_id>/issues/<issue_id>/comments/<comment_id>/**
- Headers :
    - Authorization : Bearer *token d'accès*
