import streamlit as st
# Fonction d'analyse
def analyse_data(df):
    st.subheader("Aperçu des données")
    st.dataframe(df.head())

    st.subheader("Informations générales")
    st.write("Dimensions:", df.shape)

    st.write("\nColonnes et types:")
    st.write(df.dtypes)

    st.write("\nValeurs manquantes:")
    st.write(df.isnull().sum())

    st.subheader("Statistiques descriptives")
    st.write(df.describe())