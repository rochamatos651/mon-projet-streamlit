import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu

# ---------------------------------------------------------
# 1. INITIALISATION DE LA MÉMOIRE DE SESSION (st.session_state)
# ---------------------------------------------------------
# Garde en mémoire si l'utilisateur est connecté d'un rechargement à l'autre
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if "username" not in st.session_state:
    st.session_state["username"] = ""

# ---------------------------------------------------------
# 2. CHARGEMENT ET VÉRIFICATION DES IDENTIFIANTS
# ---------------------------------------------------------
@st.cache_data
def load_accounts():
    # Charge la liste des utilisateurs autorisés depuis le CSV
    return pd.read_csv("accounts.csv")

def authenticate(username_input, password_input):
    accounts_df = load_accounts()
    # Recherche d'une ligne correspondant au nom et au mot de passe
    user_match = accounts_df[
        (accounts_df["name"] == username_input) & 
        (accounts_df["password"] == password_input)
    ]
    # Renvoie True si au moins un compte correspond, sinon False
    return not user_match.empty

# ---------------------------------------------------------
# 3. AFFICHAGE CONDITIONNEL : CONNEXION OU APPLICATION
# ---------------------------------------------------------
if not st.session_state["logged_in"]:
    # --- FORMULAIRE DE CONNEXION ---
    st.title("🔑 Connexion")
    
    username_input = st.text_input("Nom d'utilisateur")
    password_input = st.text_input("Mot de passe", type="password")
    
    if st.button("Se connecter"):
        if authenticate(username_input, password_input):
            # Enregistrement de l'état de connexion
            st.session_state["logged_in"] = True
            st.session_state["username"] = username_input
            st.rerun()  # Relance le script pour afficher l'interface sécurisée
        else:
            st.error("Nom d'utilisateur ou mot de passe incorrect.")

else:
    # --- INTERFACE SÉCURISÉE (UTILISATEUR CONNECTÉ) ---
    
    # 1. Barre latérale : Message d'accueil et bouton de déconnexion
    with st.sidebar:
        st.write(f"👤 Bienvenue **{st.session_state['username']}** !")
        if st.button("Se déconnecter"):
            st.session_state["logged_in"] = False
            st.session_state["username"] = ""
            st.rerun()  # Relance le script pour revenir au formulaire de connexion
        st.divider()
        
        # 2. Barre latérale : Menu de navigation
        selected_page = option_menu(
            menu_title="Navigation",
            options=["Accueil", "Galerie Photos"],
            icons=["house", "images"],
            default_index=0
        )
    
    # 3. Rendu de la page sélectionnée
    if selected_page == "Accueil":
        st.title("🏠 Espace Réservé")
        st.write("Bienvenue sur la page d'accueil sécurisée.")
        
    elif selected_page == "Galerie Photos":
        st.title("🐾 Galerie d'Animaux")
        
        # Liste des URLs d'images
        # URLs de test sécurisées
        image_urls = [
            "https://static.streamlit.io/examples/cat.jpg",
            "https://static.streamlit.io/examples/dog.jpg",
            "https://static.streamlit.io/examples/owl.jpg"
        ]
        
        # Création des 3 colonnes
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.image(image_urls[0], caption="Chat 🐱", use_container_width=True)
        with col2:
            st.image(image_urls[1], caption="Chien 🐶", use_container_width=True)
        with col3:
            st.image(image_urls[2], caption="Chouette 🦉", use_container_width=True)