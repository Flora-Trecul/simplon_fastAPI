# 🎓 Simplon API

## Objectif du projet

Projet dans le cadre de la formation Développeur en intelligence artificielle de Simplon.

Nous avons développé une API de gestion de formation pour l'organisme Simplon.

- L'API elle-même avec FastAPI
- La validation de données avec Pydantic
- La base de données avec SQLAlchemy et SQLite3

L'objectif est de gérer les différentes formations et sessions de formations, ainsi que les apprenants, formateurs et personnel de l'organisme.


---


## Structure du projet

L'organisation des fichiers suit une séparation stricte des responsabilités :

```text
alembic/
app/
├── main.py          # Lancement de l'API
├── api/
│   └── routers/     # Routes et contrôleurs (FastAPI)
├── core/            # Configuration de la base de données
├── crud/            # Interactions avec la base de donnés
├── data/            # Bases de données SQLite
├── models/          # Modèles de la base de données (SQLAlchemy)
├── schemas/         # Validation des données (Pydantic)
└── tests/           # Tests unitaires et d'intégration
main.py              # Lancement du projet
documents/           # Slides de présentation du projet
```


---

## Lancement du projet

Attention, ce projet a été élaboré sur **Linux / Ubuntu**

### 1. Créer un environnement virtuel

```bash
python -m venv venv
```

### 2. Activer l'environnement virtuel

```bash
source venv/bin/activate
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. Créer la base de données

```bash
python -m app.core.database --create-db
```

### 5a. Créer des données factices (optionnel)

```bash
python -m  main --seed-data
```

### 5b. Lancer l'API sans créer de données factices

```bash
python -m  main
```

### 6. Ouvrir l'API dans le navigateur

Si l'API ne s'est pas ouverte automatiquement dans votre navigateur, vous pouvez y accéder via l'URL **http://127.0.0.1:8000/**


### 7. Accéder à la documentation Swagger (optionnel)

La documentation de l'API est accessible à l'endpoint /docs : **http://127.0.0.1:8000/docs**


### 8. Lancer les tests (optionnel)

```bash
pytest            # Pour exécuter les tests
```
```bash
pytest --cov=app  # Pour vérifier la couverture des tests
```

---

## Collaboration

Le projet a été réalisé en équipe de 3. L'architecture et les modèles SQLAlchemy ont été décidés en commun, puis le travail a été réparti comme suit.

|   | Lien GitHub | Contribution |
| :--- | :--- | :--- |
| **Fatima** | [Voir le profil](https://github.com/FatimaUY) | Gestion des **Users** (apprenants, formateurs, personnel) |
| **Edilene** | [Voir le profil](https://github.com/EdileneSilva) | Gestion des **Courses** (formations) |
| **Flora** | [Voir le profil](https://github.com/Flora-Trecul) | Gestion des **Learning Sessions** (sessions de formation) |

---