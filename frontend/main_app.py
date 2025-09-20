import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt



# --- Streamlit App ---

st.set_page_config(page_title="HevitraVizor+", layout="wide", page_icon="📊")

# --- Personnalisation du style ---
st.markdown("""
<style>
.stApp {
    background: linear-gradient(90deg, #2e2e2e 60%, #3c3c3c 100%);
    color: white;
}
.big-title {
    font-size: 2.5em;
    font-weight: bold;
    color: #00b4d8;
    text-align: center;
    margin-bottom: 0.2em;
}
.banner {
    background: #00b4d8;
    color: white;
    padding: 1em;
    border-radius: 10px;
    text-align: center;
    font-size: 1.2em;
    margin-bottom: 1em;
}
.section-box {
    background: #222;
    border-radius: 10px;
    padding: 1em;
    margin-bottom: 1em;
    box-shadow: 0 2px 8px #0002;
}
</style>
""", unsafe_allow_html=True)

# --- Logo et bannière ---
col1, col2 = st.columns([1, 8])
with col1:
    st.image("frontend/assets/logo.png", width=80)
with col2:
    st.markdown('<div class="big-title">HevitraVizor+</div>', unsafe_allow_html=True)

st.markdown('<div class="banner">Bienvenue dans l\'application d\'analyse de données d\'entreprise ! 🚀</div>', unsafe_allow_html=True)

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
    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.markdown("### 🗂️ Aperçu des données")
    st.dataframe(data.head(20))
    st.markdown('</div>', unsafe_allow_html=True)

    # --- Filtrage interactif ---
    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.markdown("### 🔎 Filtrer les données")
    filter_cols = st.multiselect("Colonnes à filtrer :", data.columns)
    filtered_data = data.copy()
    for col in filter_cols:
        if data[col].dtype == 'object' or str(data[col].dtype).startswith('category'):
            options = filtered_data[col].dropna().unique().tolist()
            selected = st.multiselect(f"Valeurs pour {col}", options)
            if selected:
                filtered_data = filtered_data[filtered_data[col].isin(selected)]
        else:
            min_val, max_val = float(filtered_data[col].min()), float(filtered_data[col].max())
            val_range = st.slider(f"Plage pour {col}", min_val, max_val, (min_val, max_val))
            filtered_data = filtered_data[(filtered_data[col] >= val_range[0]) & (filtered_data[col] <= val_range[1])]
    st.write(f"**Lignes après filtre :** {filtered_data.shape[0]}")
    st.dataframe(filtered_data.head(20))
    st.markdown('</div>', unsafe_allow_html=True)

    # --- Téléchargement des données filtrées ---
    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.markdown("### ⬇️ Télécharger les données filtrées")
    csv = filtered_data.to_csv(index=False).encode('utf-8')
    st.download_button("Télécharger en CSV", data=csv, file_name="donnees_filtrees.csv", mime="text/csv")
    st.markdown('</div>', unsafe_allow_html=True)

    # --- Analyse rapide ---
    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.markdown("### 📊 Analyse rapide")
    st.write(f"**Dimensions :** {filtered_data.shape}")
    st.write(f"**Colonnes :** {list(filtered_data.columns)}")
    st.write("**Types de données :**")
    st.write(filtered_data.dtypes)
    st.write("**Valeurs manquantes :**")
    st.write(filtered_data.isnull().sum())
    st.write("**Statistiques descriptives :**")
    st.write(filtered_data.describe())
    st.markdown('</div>', unsafe_allow_html=True)

    # --- Corrélations ---
    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.markdown("### 🔗 Corrélations entre variables numériques")
    numeric_cols = filtered_data.select_dtypes(include='number').columns.tolist()
    if len(numeric_cols) >= 2:
        corr = filtered_data[numeric_cols].corr()
        st.dataframe(corr)
        fig, ax = plt.subplots()
        im = ax.imshow(corr, cmap='coolwarm', interpolation='none')
        ax.set_xticks(range(len(numeric_cols)))
        ax.set_yticks(range(len(numeric_cols)))
        ax.set_xticklabels(numeric_cols, rotation=45, ha='right')
        ax.set_yticklabels(numeric_cols)
        fig.colorbar(im)
        st.pyplot(fig)
    st.markdown('</div>', unsafe_allow_html=True)

    # --- Visualisation interactive ---
    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.markdown("### 📈 Visualisation interactive")
    plot_type = st.selectbox("Type de graphique :", ["Histogramme", "Boîte à moustaches", "Nuage de points", "Camembert"])
    cat_cols = filtered_data.select_dtypes(include=['object', 'category']).columns.tolist()

    if plot_type == "Histogramme" and numeric_cols:
        col = st.selectbox("Colonne numérique :", numeric_cols)
        fig, ax = plt.subplots()
        ax.hist(filtered_data[col].dropna(), bins=20, color='#00b4d8', edgecolor='black')
        ax.set_title(f"Histogramme de {col}")
        ax.set_xlabel(col)
        ax.set_ylabel("Fréquence")
        st.pyplot(fig)
    elif plot_type == "Boîte à moustaches" and numeric_cols:
        col = st.selectbox("Colonne numérique :", numeric_cols)
        fig, ax = plt.subplots()
        ax.boxplot(filtered_data[col].dropna(), patch_artist=True, boxprops=dict(facecolor='#00b4d8'))
        ax.set_title(f"Boîte à moustaches de {col}")
        ax.set_xlabel(col)
        st.pyplot(fig)
    elif plot_type == "Nuage de points" and len(numeric_cols) >= 2:
        x_col = st.selectbox("Axe X :", numeric_cols, key="x_scatter")
        y_col = st.selectbox("Axe Y :", [c for c in numeric_cols if c != x_col], key="y_scatter")
        fig, ax = plt.subplots()
        ax.scatter(filtered_data[x_col], filtered_data[y_col], alpha=0.7, color='#00b4d8')
        ax.set_title(f"Nuage de points : {x_col} vs {y_col}")
        ax.set_xlabel(x_col)
        ax.set_ylabel(y_col)
        st.pyplot(fig)
    elif plot_type == "Camembert" and cat_cols:
        col = st.selectbox("Colonne catégorielle :", cat_cols)
        pie_data = filtered_data[col].value_counts()
        fig, ax = plt.subplots()
        ax.pie(pie_data, labels=pie_data.index, autopct='%1.1f%%', startangle=90, colors=['#00b4d8', '#90e0ef', '#caf0f8', '#0077b6', '#03045e'])
        ax.set_title(f"Répartition de {col}")
        st.pyplot(fig)
    else:
        st.info("Aucune colonne adaptée à ce type de graphique.")
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.info("Veuillez charger un fichier pour commencer l'analyse.")
