import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df_iris = pd.read_csv("https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv")

st.subheader("Distribution par espèce (Seaborn)")

# 1. Création explicite de la figure
fig, ax = plt.subplots(figsize=(8, 4))
sns.barplot(data=df_iris, x="species", y="sepal_length", ax=ax,
palette="viridis")
ax.set_title("Longueur moyenne des sépales par espèce")

# 2. Rendu dans Streamlit
st.pyplot(fig)




# autre aproche ----------------------------------------------



import streamlit as st
import pandas as pd
import plotly.express as px
df_iris = pd.read_csv("https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv")
st.subheader("Nuage de points interactif (Plotly)")
# Création de la figure Plotly
fig_plotly = px.scatter(
 df_iris,
 x="sepal_width",
 y="sepal_length",
 color="species",
 size="petal_length",
 hover_data=["petal_width"],
 title="Relation Sépale vs Pétale"
)
# Rendu dans Streamlit
st.plotly_chart(fig_plotly, use_container_width=True)
