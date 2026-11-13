import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/flights.csv"
    return pd.read_csv(url)

df_flights = load_data()

annees = st.slider(
    "Sélectionner la plage d'années :", min_value=int(df_flights["year"].min()), max_value=int(df_flights["year"].max()), value=(int(df_flights["year"].min()), int(df_flights["year"].max())))

options_mois = ["Tous"] + list(df_flights["month"].unique().dropna())
mois_selectionne = st.selectbox("Sélectionner un mois :", options_mois)

df_filtre = df_flights[(df_flights["year"] >= annees[0]) & (df_flights["year"] <= annees[1])]

if mois_selectionne != "Tous": df_filtre = df_filtre[df_filtre["month"] == mois_selectionne]

total_passagers = df_filtre["passengers"].sum()

st.metric(label="Total de passagers", value=f"{total_passagers:,}")

st.line_chart(df_filtre, x="year", y="passengers")

if st.checkbox("Afficher la Heatmap"):

    df_pivot = df_flights.pivot(
        index="month", columns="year", values="passengers"
    )
    fig, ax = plt.subplots()
    sns.heatmap(df_pivot, ax=ax)
    st.pyplot(fig)