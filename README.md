# API RESTful SoftDesk Support

API de suivi de problèmes techniques (Issue Tracker) pour entreprises B2B, sécurisée et conforme aux normes OWASP, RGPD et Green Code.

##  Objectifs du projet

SoftDesk Support permet aux entreprises de :
- Créer et gérer des projets
- Suivre des problèmes techniques (bugs, tâches, fonctionnalités)
- Collaborer via un système de contributeurs
- Commenter et discuter sur les issues

##  Architecture

### Modèles principaux

- **User** : Utilisateurs avec validation RGPD (âge ≥ 15 ans, consentements)
- **Project** : Projets avec types (back-end, front-end, iOS, Android)
- **Contributor** : Liaison many-to-many entre User et Project
- **Issue** : Problèmes/tâches avec priorité, statut, balise
- **Comment** : Commentaires sur les issues avec UUID unique

### Technologies utilisées

- Python 3.13
- Django 6.0
- Django REST Framework
- Django REST Framework SimpleJWT (authentification JWT)
- SQLite (base de données)
- Pipenv (gestion des dépendances)

##  Dépendances

### Gestion des dépendances

Le projet utilise **Pipenv** pour la gestion des dépendances et de l'environnement virtuel.

**Fichiers de dépendances :**
- `Pipfile` : Liste des packages requis
- `Pipfile.lock` : Versions exactes verrouillées (sécurité)
- `requirements.txt` : Export pour compatibilité avec pip

### Principales dépendances

- Django 6.0
- djangorestframework
- djangorestframework-simplejwt

### Ajouter une nouvelle dépendance
```bash
pipenv install <nom_du_package>
```

### Mettre à jour requirements.txt
```bash
pipenv requirements > requirements.txt
```

##  Sécurité

### OWASP - Triple A

1. **Authentification** : JWT avec tokens à durée de vie limitée (5h access, 1 jour refresh)
2. **Autorisation** : Accès limité aux contributeurs des projets
3. **Accès** : Permissions (lecture pour contributeurs, modification pour auteurs)

### RGPD

- ✅ Vérification de l'âge minimum (15 ans)
- ✅ Collecte des consentements (`can_be_contacted`, `can_data_be_shared`)
- ✅ Droit à l'oubli (suppression en cascade)
- ✅ Horodatage de toutes les ressources

### Green Code

- ✅ Pagination (10 résultats/page)
- ✅ Filtrage intelligent des requêtes
- ✅ Gestion optimisée des dépendances

##  Installation

### Prérequis

- Python 3.8 ou supérieur
- Pipenv

### Étapes d'installation

1. **Cloner le repository**
```bash
git clone <url_du_repository>
cd softdesk_api
```

2. **Installer Pipenv**
```bash
pip install pipenv
```

3. **Installer les dépendances et créer l'environnement virtuel**
```bash
pipenv install
```

4. **Activer l'environnement virtuel**
```bash
pipenv shell
```

5. **Effectuer les migrations**
```bash
python manage.py migrate
```

6. **Créer un superutilisateur**
```bash
python manage.py shell
```

Puis dans le shell Python :
```python
from api.models import User
from datetime import date

user = User.objects.create_superuser(
    username='admin',
    email='admin@example.com',
    password='admin123',
    date_of_birth=date(1990, 1, 1),
    can_be_contacted=True,
    can_data_be_shared=False
)
exit()
```

7. **Lancer le serveur**
```bash
python manage.py runserver
```

L'API est accessible à : `http://127.0.0.1:8000/`

##  Endpoints de l'API

### Authentification

| Endpoint              | Méthode | Description                 | Permission |
|----------             |---------|-------------                |------------|
| `/api/signup/`        | POST    | Inscription                 | AllowAny |
| `/api/token/`         | POST    | Connexion (obtenir JWT)     | AllowAny |
| `/api/token/refresh/` | POST    | Renouveler le token         | AllowAny |
| `/api/users/me/`      | GET     | Profil utilisateur connecté | IsAuthenticated |

### Projets

| Endpoint              | Méthode | Description         | Permission |
|----------             |---------|-------------        |------------|
| `/api/projects/`      | GET     | Liste des projets   | IsAuthenticated |
| `/api/projects/`      | POST    | Créer un projet     | IsAuthenticated |
| `/api/projects/{id}/` | GET     | Détail d'un projet  | Contributeur |
| `/api/projects/{id}/` | PATCH   | Modifier un projet  | Auteur |
| `/api/projects/{id}/` | DELETE  | Supprimer un projet | Auteur |

### Contributeurs

| Endpoint                  | Méthode | Description             |Permission |
|----------                 |---------|-------------            |------------|
| `/api/contributors/`      | GET     | Liste des contributeurs | IsAuthenticated |
| `/api/contributors/`      | POST    | Ajouter un contributeur | Auteur du projet |
| `/api/contributors/{id}/` | DELETE  | Retirer un contributeur | Auteur du projet |

### Issues

| Endpoint | Méthode | Description | Permission |
|----------|---------|-------------|------------|
| `/api/issues/` | GET | Liste des issues | IsAuthenticated |
| `/api/issues/` | POST | Créer une issue | Contributeur |
| `/api/issues/{id}/` | GET | Détail d'une issue | Contributeur |
| `/api/issues/{id}/` | PATCH | Modifier une issue | Auteur |
| `/api/issues/{id}/` | DELETE | Supprimer une issue | Auteur |

### Commentaires

| Endpoint | Méthode | Description | Permission |
|----------|---------|-------------|------------|
| `/api/comments/` | GET | Liste des commentaires | IsAuthenticated |
| `/api/comments/` | POST | Créer un commentaire | Contributeur |
| `/api/comments/{id}/` | GET | Détail d'un commentaire | Contributeur |
| `/api/comments/{id}/` | PATCH | Modifier un commentaire | Auteur |
| `/api/comments/{id}/` | DELETE | Supprimer un commentaire | Auteur |

##  Exemples d'utilisation

### 1. Inscription
```bash
POST /api/signup/
Content-Type: application/json

{
    "username": "alice",
    "email": "alice@example.com",
    "password": "SecurePass123!",
    "password_confirm": "SecurePass123!",
    "date_of_birth": "2000-01-01",
    "can_be_contacted": true,
    "can_data_be_shared": false
}
```

### 2. Connexion
```bash
POST /api/token/
Content-Type: application/json

{
    "username": "alice",
    "password": "SecurePass123!"
}
```

**Réponse :**
```json
{
    "refresh": "eyJ0eXAiOiJKV1QiLC...",
    "access": "eyJ0eXAiOiJKV1QiLC..."
}
```

### 3. Créer un projet
```bash
POST /api/projects/
Authorization: Bearer <access_token>
Content-Type: application/json

{
    "name": "Mon Projet",
    "description": "Description du projet",
    "type": "back-end"
}
```

### 4. Ajouter un contributeur
```bash
POST /api/contributors/
Authorization: Bearer <access_token>
Content-Type: application/json

{
    "user": 2,
    "project": 1,
    "role": "contributor"
}
```

### 5. Créer une issue
```bash
POST /api/issues/
Authorization: Bearer <access_token>
Content-Type: application/json

{
    "title": "Bug dans le panier",
    "description": "Les prix ne s'affichent pas",
    "priority": "HIGH",
    "status": "To Do",
    "tag": "BUG",
    "project": 1,
    "assigned_to": 2
}
```

### 6. Commenter une issue
```bash
POST /api/comments/
Authorization: Bearer <access_token>
Content-Type: application/json

{
    "description": "J'ai trouvé la solution dans le fichier cart.js",
    "issue": 1
}
```

## Codes HTTP

- `200 OK` : Requête réussie
- `201 Created` : Ressource créée
- `400 Bad Request` : Données invalides
- `401 Unauthorized` : Authentification requise
- `403 Forbidden` : Permission refusée
- `404 Not Found` : Ressource inexistante

## Tests

Pour tester l'API, utilisez **Postman** ou **curl**.

### Avec Postman

1. Importer la collection (si disponible)
2. Configurer l'authentification Bearer Token
3. Tester les endpoints

##  Structure du projet
```
softdesk_api/
├── api/
│   ├── migrations/
│   ├── serializers/
│   │   ├── user_serializer.py
│   │   ├── project_serializer.py
│   │   ├── contributor_serializer.py
│   │   ├── issue_serializer.py
│   │   └── comment_serializer.py
│   ├── permissions/
│   │   ├── project_permissions.py
│   │   ├── contributor_permissions.py
│   │   ├── issue_permissions.py
│   │   └── comment_permissions.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
├── softdesk/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
├── Pipfile               # Dépendances Pipenv
├── Pipfile.lock          # Versions verrouillées
├── requirements.txt      # Export pour compatibilité pip
├── README.md
└── .gitignore
```

##  Contribution

Ce projet est réalisé dans le cadre de la formation OpenClassrooms - Développeur d'application Python.

## 📝 Licence

Ce projet est à usage éducatif.
