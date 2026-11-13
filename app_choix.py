import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px




st.title(" Explorateur Interactif Seaborn Data - Fabio")
# 1. Sélection du jeu de données
dataset_name = st.selectbox(
 "Choisissez un jeu de données Seaborn :",
 ["flights", "iris", "penguins", "taxis"]
)
# Chargement dynamique
@st.cache_data
def get_dataset(name):
    return pd.read_csv(f"https://raw.githubusercontent.com/mwaskom/seaborn-data/master/{name}.csv")
df = get_dataset(dataset_name)
st.write(f"### Aperçu du dataset `{dataset_name}` ({df.shape[0]}lignes, {df.shape[1]} colonnes)")
st.dataframe(df.head())
# 2. Configuration du graphique interactif
st.subheader("Configuration de la visualisation")
# Séparation des colonnes numériques et catégorielles
num_cols = df.select_dtypes(include=['float64',
'int64']).columns.tolist()
if len(num_cols) >= 2:
 col_x = st.selectbox("Axe X :", num_cols, index=0)
 col_y = st.selectbox("Axe Y :", num_cols, index=min(1,
len(num_cols)-1))
 chart_type = st.radio("Type de graphique :", ["Scatter Chart",
"Line Chart", "Bar Chart"], horizontal=True)
 # Génération du graphique selon le choix
 if chart_type == "Scatter Chart":
    st.scatter_chart(df, x=col_x, y=col_y)
 elif chart_type == "Line Chart":
    st.line_chart(df.set_index(col_x)[col_y])
 elif chart_type == "Bar Chart":
    st.bar_chart(df.set_index(col_x)[col_y])
 # 3. Option pour afficher la matrice de corrélation
 st.divider()
 if st.checkbox("Afficher la matrice de corrélation numérique"):
    st.subheader("Matrice de corrélation")
    corr = df[num_cols].corr()
    fig_corr, ax_corr = plt.subplots(figsize=(6, 4))
    sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", ax=ax_corr)
    st.pyplot(fig_corr)
else:
    st.warning("Ce jeu de données ne contient pas assez de colonnes numériques pour générer ce graphique.")