# Fonction de visualisation
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
def visualize_data(df):
    st.subheader("Visualisation graphique")
    numeric_cols = df.select_dtypes(include=['int', 'float']).columns.tolist()

    if not numeric_cols:
        st.warning("Aucune colonne numérique à afficher.")
        return

    col = st.selectbox("Choisissez une colonne numérique", numeric_cols)
    chart_type = st.selectbox("Type de graphique", ["Histogramme", "Barres"])

    fig, ax = plt.subplots()
    if chart_type == "Histogramme":
        sns.histplot(df[col], kde=True, ax=ax)
    elif chart_type == "Barres":
        df[col].value_counts().plot(kind='bar', ax=ax)

    st.pyplot(fig)