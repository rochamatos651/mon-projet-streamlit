from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="Application Sécurisée - DataViz",
    page_icon="🔐",
    layout="wide"
)

CSV_PATH = Path(__file__).parent / "accounts.csv"
MAX_ATTEMPTS = 3


def load_accounts() -> pd.DataFrame:
    df = pd.read_csv(CSV_PATH)
    df.columns = df.columns.str.strip()
    return df


def save_accounts(df: pd.DataFrame) -> None:
    df.to_csv(CSV_PATH, index=False)


if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user_info" not in st.session_state:
    st.session_state.user_info = None

# --- ÉCRAN DE CONNEXION ---
if not st.session_state.authenticated:
    st.title("🔐 Connexion à l'application")

    try:
        accounts_df = load_accounts()
    except FileNotFoundError:
        st.error("Fichier `accounts.csv` introuvable à la racine du projet.")
        st.stop()

    with st.form("login_form"):
        username = st.text_input("Nom d'utilisateur").strip()
        password = st.text_input("Mot de passe", type="password")
        submitted = st.form_submit_button("Se connecter")

    if submitted:
        user_mask = accounts_df["name"] == username

        if not user_mask.any():
            st.error("Identifiant inconnu.")
        else:
            idx = accounts_df.index[user_mask][0]
            attempts = int(accounts_df.loc[idx, "failed_login_attempts"])

            if attempts >= MAX_ATTEMPTS:
                st.error("Compte bloqué suite à trop de tentatives échouées.")
            elif str(accounts_df.loc[idx, "password"]) == password:
                accounts_df.loc[idx, "failed_login_attempts"] = 0
                accounts_df.loc[idx, "logged_in"] = True
                save_accounts(accounts_df)

                st.session_state.authenticated = True
                st.session_state.user_info = {
                    "name": accounts_df.loc[idx, "name"],
                    "email": accounts_df.loc[idx, "email"],
                    "role": accounts_df.loc[idx, "role"],
                }
                st.rerun()
            else:
                new_attempts = attempts + 1
                accounts_df.loc[idx, "failed_login_attempts"] = new_attempts
                save_accounts(accounts_df)
                remaining = MAX_ATTEMPTS - new_attempts
                if remaining > 0:
                    st.warning(f"Mot de passe incorrect. Tentatives restantes : {remaining}")
                else:
                    st.error("Compte bloqué après 3 échecs.")

# --- APPLICATION PRINCIPALE ---
else:
    user = st.session_state.user_info

    with st.sidebar:
        st.success(f"Connecté : **{user['name']}**")
        st.caption(f"Rôle : {user['role']} | {user['email']}")
        if st.button("Se déconnecter"):
            accounts_df = load_accounts()
            accounts_df.loc[accounts_df["name"] == user["name"], "logged_in"] = False
            save_accounts(accounts_df)
            st.session_state.authenticated = False
            st.session_state.user_info = None
            st.rerun()

    st.title("📊 Tableau de Bord Analytique")

    df = px.data.tips()

    day_filter = st.sidebar.multiselect(
        "Filtrer par jour",
        options=df["day"].unique().tolist(),
        default=df["day"].unique().tolist()
    )
    df_filtered = df[df["day"].isin(day_filter)]

    col1, col2, col3 = st.columns(3)
    col1.metric("Transactions", len(df_filtered))
    col2.metric("Chiffre d'affaires ($)", f"{df_filtered['total_bill'].sum():,.2f}")
    col3.metric("Pourboire moyen ($)", f"{df_filtered['tip'].mean():,.2f}")

    st.divider()

    c1, c2 = st.columns(2)
    with c1:
        fig_bar = px.bar(
            df_filtered.groupby("day", as_index=False)["total_bill"].sum(),
            x="day",
            y="total_bill",
            title="Total des ventes par jour"
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    with c2:
        fig_scatter = px.scatter(
            df_filtered,
            x="total_bill",
            y="tip",
            color="sex",
            title="Relation Montant / Pourboire"
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

    if user["role"] == "administrateur":
        with st.expander("Administration des comptes (`accounts.csv`)"):
            st.dataframe(load_accounts().drop(columns=["password"]), use_container_width=True)