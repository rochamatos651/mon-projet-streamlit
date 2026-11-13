# Application Web Interactive avec Streamlit

Application de visualisation de données sécurisée par authentification, développée en Python avec Streamlit, Pandas et Plotly, et déployée sur Streamlit Community Cloud.

## Fonctionnalités

- **Authentification utilisateur** via `accounts.csv` avec gestion des rôles (`utilisateur`, `administrateur`).
- **Sécurité** : verrouillage automatique du compte après 3 tentatives de connexion échouées.
- **Dashboard interactif** : filtrage dynamique, indicateurs clés (KPI) et graphiques interactifs Plotly.

## Structure du projet

- `app.py` : point d'entrée principal de l'application Streamlit.
- `accounts.csv` : base des comptes utilisateurs de démonstration.
- `requirements.txt` : liste des dépendances Python nécessaires au déploiement.
- `.gitignore` : exclusion de l'environnement virtuel (`venv/`) et des fichiers temporaires.

## Exécution en local

```bash
# 1. Activer l'environnement virtuel
venv\Scripts\activate

# 2. Installer les dépendances
pip install -r requirements.txt

# 3. Lancer l'application
streamlit run app.py