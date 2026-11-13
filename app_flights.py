import streamlit as st
import pandas as pd

# Chargement direct du dataset "flights" depuis GitHub
@st.cache_data
def load_data():
 url = ("https://raw.githubusercontent.com/mwaskom/seaborn-data/master/flights.csv")
 return pd.read_csv(url)
df_flights = load_data()

st.title("Dashboard Flights - Fabio")

st.subheader("Aperçu des données")
st.dataframe(df_flights.head(10))

# Affichage de KPI
total_passengers = df_flights["passengers"].sum()
st.metric(label="Total de passagers historiques",
value=f"{total_passengers:,}")


# Préparation des données : évolution annuelle du total des passagers
annual_passengers = df_flights.groupby("year")["passengers"].sum()
st.subheader("Évolution du trafic aérien (Bar Chart natif)")
st.bar_chart(annual_passengers)