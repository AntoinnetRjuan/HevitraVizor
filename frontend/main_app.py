import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt



# --- Streamlit App ---
st.set_page_config(page_title="HevitraVizor+", layout="wide", page_icon="📊")

st.markdown("""
<style>
.main {
    background-color: #2e2e2e;
    color: white;
}
.stApp {
    background-color: #2e2e2e;
}
</style>
""", unsafe_allow_html=True)

st.title("📊 HevitraVizor+")
st.markdown("Bienvenue dans l'application d'analyse de données d'entreprise !")

uploaded_file = st.sidebar.file_uploader("Charger un fichier Excel ou CSV", type=["csv", "xlsx", "xls"])
data = None

if uploaded_file:
    try:
        if uploaded_file.name.endswith(".csv"):
            data = pd.read_csv(uploaded_file)
        else:
            data = pd.read_excel(uploaded_file)
    except Exception as e:
        st.error(f"Erreur lors du chargement du fichier : {e}")

if data is not None:
    st.subheader("Aperçu des données")
    st.dataframe(data.head(20))

    st.subheader("Analyse rapide")
    st.write(f"**Dimensions :** {data.shape}")
    st.write(f"**Colonnes :** {list(data.columns)}")
    st.write("**Types de données :**")
    st.write(data.dtypes)
    st.write("**Valeurs manquantes :**")
    st.write(data.isnull().sum())
    st.write("**Statistiques descriptives :**")
    st.write(data.describe())

    st.subheader("Visualisation interactive")
    plot_type = st.selectbox("Type de graphique :", ["Histogramme", "Boîte à moustaches", "Nuage de points", "Camembert"])
    numeric_cols = data.select_dtypes(include='number').columns.tolist()
    cat_cols = data.select_dtypes(include=['object', 'category']).columns.tolist()

    if plot_type == "Histogramme" and numeric_cols:
        col = st.selectbox("Colonne numérique :", numeric_cols)
        fig, ax = plt.subplots()
        ax.hist(data[col].dropna(), bins=20, color='skyblue', edgecolor='black')
        ax.set_title(f"Histogramme de {col}")
        ax.set_xlabel(col)
        ax.set_ylabel("Fréquence")
        st.pyplot(fig)
    elif plot_type == "Boîte à moustaches" and numeric_cols:
        col = st.selectbox("Colonne numérique :", numeric_cols)
        fig, ax = plt.subplots()
        ax.boxplot(data[col].dropna())
        ax.set_title(f"Boîte à moustaches de {col}")
        ax.set_xlabel(col)
        st.pyplot(fig)
    elif plot_type == "Nuage de points" and len(numeric_cols) >= 2:
        x_col = st.selectbox("Axe X :", numeric_cols, key="x_scatter")
        y_col = st.selectbox("Axe Y :", [c for c in numeric_cols if c != x_col], key="y_scatter")
        fig, ax = plt.subplots()
        ax.scatter(data[x_col], data[y_col], alpha=0.7, color='teal')
        ax.set_title(f"Nuage de points : {x_col} vs {y_col}")
        ax.set_xlabel(x_col)
        ax.set_ylabel(y_col)
        st.pyplot(fig)
    elif plot_type == "Camembert" and cat_cols:
        col = st.selectbox("Colonne catégorielle :", cat_cols)
        pie_data = data[col].value_counts()
        fig, ax = plt.subplots()
        ax.pie(pie_data, labels=pie_data.index, autopct='%1.1f%%', startangle=90)
        ax.set_title(f"Répartition de {col}")
        st.pyplot(fig)
    else:
        st.info("Aucune colonne adaptée à ce type de graphique.")
else:
    st.info("Veuillez charger un fichier pour commencer l'analyse.")
