import streamlit as st
import pandas as pd
# Fonction pour charger les données
@st.cache_data
def load_data(uploaded_file):
    try:
        if uploaded_file.name.endswith('.csv'):
            return pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith('.xlsx'):
            return pd.read_excel(uploaded_file)
        else:
            st.warning("Type de fichier non supporté. Veuillez uploader un fichier .csv ou .xlsx")
            return None
    except Exception as e:
        st.error(f"Erreur lors du chargement : {e}")
        return None