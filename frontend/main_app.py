import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io
import os

# Gestion des imports optionnels pour Plotly
try:
    import plotly.express as px
    import plotly.graph_objects as go
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False

# --- Configuration de la page ---
st.set_page_config(
    page_title="HevitraVizor+",
    layout="wide", 
    page_icon="📊",
    initial_sidebar_state="expanded"
)

# --- Personnalisation du style avec couleurs douces ---
st.markdown("""
<style>
    .stApp {
        background: #f8f9fa;
        color: #2c3e50;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Header professionnel */
    .main-header {
        background: white;
        padding: 2rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        box-shadow: 0 2px 12px rgba(0,0,0,0.08);
        border-left: 4px solid #3498db;
    }
    
    .title-text {
        font-size: 2.8rem;
        font-weight: 700;
        color: #2c3e50;
        margin: 0;
        background: linear-gradient(135deg, #2c3e50 0%, #3498db 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .subtitle-text {
        font-size: 1.1rem;
        color: #7f8c8d;
        font-weight: 400;
        margin-top: 0.5rem;
    }
    
    /* Cartes modernes et douces */
    .modern-card {
        background: white;
        border-radius: 12px;
        padding: 1.8rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06);
        border: 1px solid #e9ecef;
    }
    
    .card-title {
        font-size: 1.4rem;
        font-weight: 600;
        color: #2c3e50;
        margin-bottom: 1.2rem;
        display: flex;
        align-items: center;
        gap: 10px;
        padding-bottom: 0.8rem;
        border-bottom: 2px solid #f1f3f4;
    }
    
    /* Métriques douces */
    .metric-card {
        background: linear-gradient(135deg, #3498db 0%, #2c3e50 100%);
        color: white;
        padding: 1.2rem;
        border-radius: 10px;
        text-align: center;
        margin: 0.3rem;
        box-shadow: 0 2px 8px rgba(52, 152, 219, 0.2);
    }
    
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        margin: 0;
    }
    
    .metric-label {
        font-size: 0.85rem;
        opacity: 0.9;
        margin: 0;
        font-weight: 400;
    }
    
    /* Boutons élégants */
    .stButton button {
        background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 1.5rem;
        font-weight: 500;
        transition: all 0.3s ease;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

# --- Header professionnel ---
col1, col2 = st.columns([1, 10])
with col1:
    # Logo simplifié avec emoji pour éviter les erreurs de fichier
    st.markdown("""
    <div style="text-align: center; padding: 10px;">
        <div style="font-size: 3rem;">📊</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="main-header">
        <h1 class="title-text">HevitraVizor+</h1>
        <p class="subtitle-text">Plateforme d'analyse de données • Transformez vos données en insights actionnables</p>
    </div>
    """, unsafe_allow_html=True)

# --- Sidebar épuré ---
with st.sidebar:
    st.markdown("""
    <div style='text-align: center; margin-bottom: 2rem; padding: 1rem; background: #2c3e50; border-radius: 10px;'>
        <h3 style='color: white; margin: 0;'>📊</h3>
        <h4 style='color: white; margin: 0.5rem 0;'>Navigation</h4>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    uploaded_file = st.file_uploader(
        "**📁 Charger vos données**", 
        type=["csv", "xlsx", "xls"],
        help="Importez votre fichier CSV ou Excel pour commencer l'analyse"
    )

# --- Contenu principal ---
if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith(".csv"):
            data = pd.read_csv(uploaded_file)
        else:
            data = pd.read_excel(uploaded_file)
        
        # --- Métriques principales ---
        st.markdown('<div class="modern-card">', unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{data.shape[0]:,}</div>
                <div class="metric-label">Lignes</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{data.shape[1]}</div>
                <div class="metric-label">Colonnes</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            missing_values = data.isnull().sum().sum()
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{missing_values:,}</div>
                <div class="metric-label">Valeurs manquantes</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            numeric_cols = len(data.select_dtypes(include='number').columns)
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{numeric_cols}</div>
                <div class="metric-label">Variables numériques</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

        # --- Aperçu des données ---
        st.markdown('<div class="modern-card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">📋 Aperçu des données</div>', unsafe_allow_html=True)
        
        tab1, tab2, tab3 = st.tabs(["🔍 Données brutes", "📊 Structure", "📈 Statistiques"])
        
        with tab1:
            st.dataframe(data.head(10), use_container_width=True)
        
        with tab2:
            col1, col2 = st.columns(2)
            with col1:
                st.write("**Types de données :**")
                st.write(data.dtypes.astype(str))
            with col2:
                st.write("**Valeurs manquantes :**")
                missing_df = pd.DataFrame(data.isnull().sum(), columns=['Valeurs manquantes'])
                st.dataframe(missing_df)
        
        with tab3:
            st.write("**Statistiques descriptives :**")
            st.dataframe(data.describe(), use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

        # --- Filtrage interactif ---
        st.markdown('<div class="modern-card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">🔎 Filtrage avancé</div>', unsafe_allow_html=True)
        
        filter_cols = st.multiselect("Sélectionnez les colonnes à filtrer :", data.columns)
        filtered_data = data.copy()
        
        for col in filter_cols:
            if data[col].dtype == 'object' or str(data[col].dtype).startswith('category'):
                options = filtered_data[col].dropna().unique().tolist()
                selected = st.multiselect(f"Valeurs pour **{col}**", options, key=f"cat_{col}")
                if selected:
                    filtered_data = filtered_data[filtered_data[col].isin(selected)]
            else:
                min_val, max_val = float(filtered_data[col].min()), float(filtered_data[col].max())
                val_range = st.slider(f"Plage pour **{col}**", min_val, max_val, (min_val, max_val), key=f"num_{col}")
                filtered_data = filtered_data[(filtered_data[col] >= val_range[0]) & (filtered_data[col] <= val_range[1])]
        
        st.success(f"**📊 Données filtrées :** {filtered_data.shape[0]} lignes × {filtered_data.shape[1]} colonnes")
        st.dataframe(filtered_data.head(10), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # --- Visualisations interactives ---
        if PLOTLY_AVAILABLE:
            st.markdown('<div class="modern-card">', unsafe_allow_html=True)
            st.markdown('<div class="card-title">📈 Visualisations interactives</div>', unsafe_allow_html=True)
            
            viz_col1, viz_col2 = st.columns([1, 2])
            
            with viz_col1:
                plot_type = st.selectbox("Type de visualisation :", 
                                       ["Histogramme", "Boxplot", "Scatter Plot", "Line Chart", "Bar Chart", "Pie Chart"])
                
                numeric_cols = filtered_data.select_dtypes(include='number').columns.tolist()
                cat_cols = filtered_data.select_dtypes(include=['object', 'category']).columns.tolist()
                
                if plot_type in ["Histogramme", "Boxplot"] and numeric_cols:
                    selected_col = st.selectbox("Colonne numérique :", numeric_cols)
                elif plot_type == "Scatter Plot" and len(numeric_cols) >= 2:
                    x_col = st.selectbox("Axe X :", numeric_cols)
                    y_col = st.selectbox("Axe Y :", [c for c in numeric_cols if c != x_col])
                elif plot_type == "Pie Chart" and cat_cols:
                    selected_col = st.selectbox("Colonne catégorielle :", cat_cols)
            
            with viz_col2:
                try:
                    # Couleurs douces pour les graphiques
                    soft_colors = ['#3498db', '#2ecc71', '#e74c3c', '#f39c12', '#9b59b6', '#1abc9c']
                    
                    if plot_type == "Histogramme" and numeric_cols:
                        fig = px.histogram(filtered_data, x=selected_col, 
                                         title=f"Distribution de {selected_col}",
                                         color_discrete_sequence=['#3498db'])
                        fig.update_layout(plot_bgcolor='white', paper_bgcolor='white')
                        st.plotly_chart(fig, use_container_width=True)
                    
                    elif plot_type == "Boxplot" and numeric_cols:
                        fig = px.box(filtered_data, y=selected_col, 
                                   title=f"Boxplot de {selected_col}",
                                   color_discrete_sequence=['#2ecc71'])
                        fig.update_layout(plot_bgcolor='white', paper_bgcolor='white')
                        st.plotly_chart(fig, use_container_width=True)
                    
                    elif plot_type == "Scatter Plot" and len(numeric_cols) >= 2:
                        fig = px.scatter(filtered_data, x=x_col, y=y_col,
                                       title=f"{x_col} vs {y_col}",
                                       color_discrete_sequence=['#e74c3c'])
                        fig.update_layout(plot_bgcolor='white', paper_bgcolor='white')
                        st.plotly_chart(fig, use_container_width=True)
                    
                    elif plot_type == "Pie Chart" and cat_cols:
                        pie_data = filtered_data[selected_col].value_counts().head(10)
                        fig = px.pie(values=pie_data.values, names=pie_data.index,
                                   title=f"Répartition de {selected_col}",
                                   color_discrete_sequence=soft_colors)
                        fig.update_layout(plot_bgcolor='white', paper_bgcolor='white')
                        st.plotly_chart(fig, use_container_width=True)
                    
                except Exception as e:
                    st.warning("Impossible de générer la visualisation avec les paramètres sélectionnés.")
            
            st.markdown('</div>', unsafe_allow_html=True)

        # --- Analyse des corrélations ---
        numeric_cols = filtered_data.select_dtypes(include='number').columns.tolist()
        if len(numeric_cols) >= 2:
            st.markdown('<div class="modern-card">', unsafe_allow_html=True)
            st.markdown('<div class="card-title">🔗 Matrice de corrélation</div>', unsafe_allow_html=True)
            
            corr_matrix = filtered_data[numeric_cols].corr()
            
            if PLOTLY_AVAILABLE:
                fig = px.imshow(corr_matrix, 
                              title="Matrice de corrélation",
                              color_continuous_scale='Blues',
                              aspect='auto')
                fig.update_layout(plot_bgcolor='white', paper_bgcolor='white')
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.dataframe(corr_matrix, use_container_width=True)
                # Visualisation simple avec matplotlib
                fig, ax = plt.subplots(figsize=(10, 8))
                im = ax.imshow(corr_matrix, cmap='Blues', interpolation='none')
                ax.set_xticks(range(len(numeric_cols)))
                ax.set_yticks(range(len(numeric_cols)))
                ax.set_xticklabels(numeric_cols, rotation=45, ha='right')
                ax.set_yticklabels(numeric_cols)
                plt.colorbar(im)
                st.pyplot(fig)
            
            st.markdown('</div>', unsafe_allow_html=True)

        # --- Téléchargement ---
        st.markdown('<div class="modern-card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">💾 Export des données</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            csv = filtered_data.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Télécharger CSV", 
                             data=csv, 
                             file_name="donnees_analysees.csv",
                             mime="text/csv")
        
        with col2:
            excel_buffer = io.BytesIO()
            with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
                filtered_data.to_excel(writer, index=False, sheet_name='Données')
            st.download_button("📥 Télécharger Excel",
                             data=excel_buffer.getvalue(),
                             file_name="donnees_analysees.xlsx",
                             mime="application/vnd.ms-excel")
        
        st.markdown('</div>', unsafe_allow_html=True)

    except Exception as e:
        st.error(f"❌ Erreur lors du traitement des données : {str(e)}")

else:
    # --- Page d'accueil épurée et sécurisée ---
    
    # Container principal
    with st.container():
        st.markdown(
            "<h1 style='text-align: center; color: #2c3e50; margin-bottom: 1rem;'>📊 HevitraVizor+</h1>",
            unsafe_allow_html=True
        )
        st.markdown(
            "<p style='text-align: center; color: #7f8c8d; font-size: 1.2rem; margin-bottom: 3rem;'>Votre plateforme d'analyse de données professionnelle</p>",
            unsafe_allow_html=True
        )
        
        # Features en colonnes
        col1, col2, col3 = st.columns(3)
        
        features = [
            {"icon": "📁", "title": "Import simple", "desc": "Support CSV et Excel"},
            {"icon": "📊", "title": "Visualisations", "desc": "Graphiques interactifs et clairs"},
            {"icon": "🔍", "title": "Analyse intelligente", "desc": "Insights automatiques"}
        ]
        
        for i, feature in enumerate(features):
            with [col1, col2, col3][i]:
                st.markdown(f"### {feature['icon']} {feature['title']}")
                st.write(feature['desc'])
        
        st.markdown("---")
        
        # Call to action
        st.success("💡 **Comment commencer ?** Utilisez le panneau de gauche pour importer votre premier fichier de données !")
        
        # Informations supplémentaires
        with st.expander("📋 Formats de fichiers supportés"):
            st.write("""
            - **CSV** (.csv) - Fichiers texte séparés par des virgules
            - **Excel** (.xlsx, .xls) - Feuilles de calcul Microsoft Excel
            - **Taille maximale** : 200MB
            """)
        
        with st.expander("🔧 Fonctionnalités disponibles"):
            st.write("""
            - 📈 **Analyse exploratoire** : Statistiques descriptives et métriques
            - 🔍 **Filtrage avancé** : Filtrage interactif par colonnes et valeurs
            - 📊 **Visualisations** : Graphiques interactifs et matrices de corrélation
            - 💾 **Export** : Téléchargement des données analysées
            """)

# --- Footer ---
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: #7f8c8d;'>HevitraVizor+ • Plateforme d'analyse de données</p>",
    unsafe_allow_html=True
)