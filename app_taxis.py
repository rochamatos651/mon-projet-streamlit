import streamlit as st
import pandas as pd

df_taxis = pd.read_csv("https://raw.githubusercontent.com/mwaskom/seaborn-data/master/taxis.csv")

st.title("Dashboard Analyse Taxis - Fabio")

dt_pickup_filtre = st.selectbox("Borough de pickup", df_taxis["pickup_borough"].dropna().unique())

df_filtre = df_taxis[df_taxis["pickup_borough"] == dt_pickup_filtre]

st.dataframe(df_filtre.head(5))
st.metric("Total de courses :", len(df_filtre))

