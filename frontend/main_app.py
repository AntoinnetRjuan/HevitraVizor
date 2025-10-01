import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io
import os
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Gestion des imports optionnels pour Plotly
try:
    import plotly.express as px
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
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
    
    /* Badges */
    .badge {
        display: inline-block;
        padding: 0.25rem 0.5rem;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 600;
        margin: 0.1rem;
    }
    
    .badge-success { background: #d4edda; color: #155724; }
    .badge-warning { background: #fff3cd; color: #856404; }
    .badge-danger { background: #f8d7da; color: #721c24; }
    .badge-info { background: #d1ecf1; color: #0c5460; }
</style>
""", unsafe_allow_html=True)

# --- Header professionnel ---
col1, col2 = st.columns([1, 10])
with col1:
    st.markdown("""
    <div style="text-align: center; padding: 10px;">
        <div style="font-size: 3rem;">📊</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="main-header">
        <h1 class="title-text">HevitraVizor+</h1>
        <p class="subtitle-text">Plateforme d'analyse de données avancée • IA • Machine Learning • Reporting</p>
    </div>
    """, unsafe_allow_html=True)

# --- Sidebar étendu ---
with st.sidebar:
    st.markdown("""
    <div style='text-align: center; margin-bottom: 2rem; padding: 1rem; background: #2c3e50; border-radius: 10px;'>
        <h3 style='color: white; margin: 0;'>🚀</h3>
        <h4 style='color: white; margin: 0.5rem 0;'>Navigation Avancée</h4>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    uploaded_file = st.file_uploader(
        "**📁 Charger vos données**", 
        type=["csv", "xlsx", "xls"],
        help="Importez votre fichier CSV ou Excel pour commencer l'analyse"
    )
    
    # Nouveaux paramètres dans la sidebar
    st.markdown("### ⚙️ Paramètres d'analyse")
    
    analysis_mode = st.selectbox(
        "Mode d'analyse :",
        ["Standard", "Avancé", "Expert"]
    )
    
    auto_clean = st.checkbox("Nettoyage automatique des données", value=True)
    detect_outliers = st.checkbox("Détection automatique des valeurs aberrantes", value=True)
    
    st.markdown("---")
    st.markdown("### 🎯 Modules activés")
    
    ml_enabled = st.checkbox("Machine Learning", value=True)
    forecasting_enabled = st.checkbox("Prévisions temporelles", value=True)
    clustering_enabled = st.checkbox("Clustering", value=True)

# --- Fonctions des nouvelles fonctionnalités ---
def detect_anomalies(df, numerical_columns):
    """Détection des valeurs aberrantes"""
    anomalies = {}
    for col in numerical_columns:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
        anomalies[col] = {
            'count': len(outliers),
            'percentage': (len(outliers) / len(df)) * 100,
            'outliers': outliers[col].tolist()
        }
    return anomalies

def generate_insights(df):
    """Génération automatique d'insights"""
    insights = []
    
    # Insight sur les données manquantes
    missing_percentage = (df.isnull().sum().sum() / (df.shape[0] * df.shape[1])) * 100
    if missing_percentage > 10:
        insights.append(f"⚠️ **Données manquantes** : {missing_percentage:.1f}% des valeurs sont manquantes")
    
    # Insight sur les doublons
    duplicates = df.duplicated().sum()
    if duplicates > 0:
        insights.append(f"🔍 **Doublons** : {duplicates} lignes dupliquées détectées")
    
    # Insight sur les colonnes numériques
    numeric_cols = df.select_dtypes(include=np.number).columns
    if len(numeric_cols) > 0:
        high_variance_cols = []
        for col in numeric_cols:
            if df[col].std() / df[col].mean() > 2:  # Coefficient de variation élevé
                high_variance_cols.append(col)
        if high_variance_cols:
            insights.append(f"📊 **Variance élevée** : {', '.join(high_variance_cols[:3])}")
    
    return insights

def perform_clustering(df, numerical_columns, n_clusters=3):
    """Clustering K-means simple"""
    from sklearn.cluster import KMeans
    from sklearn.preprocessing import StandardScaler
    
    # Préparation des données
    X = df[numerical_columns].dropna()
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Clustering
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    clusters = kmeans.fit_predict(X_scaled)
    
    return clusters, kmeans

def time_series_forecast(df, date_column, value_column):
    """Prévisions temporelles simples"""
    try:
        # Vérifier si c'est une série temporelle
        if date_column in df.columns and value_column in df.columns:
            ts_data = df[[date_column, value_column]].copy()
            ts_data[date_column] = pd.to_datetime(ts_data[date_column], errors='coerce')
            ts_data = ts_data.dropna()
            ts_data = ts_data.set_index(date_column).sort_index()
            
            # Statistiques de base
            stats = {
                'trend': 'positive' if ts_data[value_column].diff().mean() > 0 else 'negative',
                'volatility': ts_data[value_column].std(),
                'last_value': ts_data[value_column].iloc[-1],
                'growth_rate': ((ts_data[value_column].iloc[-1] - ts_data[value_column].iloc[0]) / ts_data[value_column].iloc[0]) * 100
            }
            return stats, ts_data
    except:
        return None, None

# --- Contenu principal ---
if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith(".csv"):
            data = pd.read_csv(uploaded_file)
        else:
            data = pd.read_excel(uploaded_file)
        
        # Nettoyage automatique si activé
        if auto_clean:
            original_shape = data.shape
            # Supprimer les colonnes vides
            data = data.dropna(axis=1, how='all')
            # Supprimer les doublons
            data = data.drop_duplicates()
            if original_shape != data.shape:
                st.success(f"🧹 **Nettoyage automatique** : {original_shape[0]-data.shape[0]} doublons supprimés, {original_shape[1]-data.shape[1]} colonnes vides supprimées")
        
        # --- Métriques principales étendues ---
        st.markdown('<div class="modern-card">', unsafe_allow_html=True)
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        
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
            missing_percentage = (missing_values / (data.shape[0] * data.shape[1])) * 100
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{missing_percentage:.1f}%</div>
                <div class="metric-label">Valeurs manquantes</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            numeric_cols = len(data.select_dtypes(include='number').columns)
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{numeric_cols}</div>
                <div class="metric-label">Numériques</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col5:
            categorical_cols = len(data.select_dtypes(include=['object', 'category']).columns)
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{categorical_cols}</div>
                <div class="metric-label">Catégorielles</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col6:
            duplicates = data.duplicated().sum()
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{duplicates}</div>
                <div class="metric-label">Doublons</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

        # --- Insights automatiques ---
        insights = generate_insights(data)
        if insights:
            st.markdown('<div class="modern-card">', unsafe_allow_html=True)
            st.markdown('<div class="card-title">🤖 Insights Automatiques</div>', unsafe_allow_html=True)
            for insight in insights:
                st.write(insight)
            st.markdown('</div>', unsafe_allow_html=True)

        # --- Aperçu des données ---
        st.markdown('<div class="modern-card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">📋 Exploration des Données</div>', unsafe_allow_html=True)
        
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["🔍 Données brutes", "📊 Structure", "📈 Statistiques", "🎯 Qualité", "🔍 Types de données"])
        
        with tab1:
            st.dataframe(data.head(10), use_container_width=True)
            st.write(f"**Dimensions** : {data.shape[0]} lignes × {data.shape[1]} colonnes")
        
        with tab2:
            col1, col2 = st.columns(2)
            with col1:
                st.write("**Types de données :**")
                type_counts = data.dtypes.value_counts()
                for dtype, count in type_counts.items():
                    st.write(f"- {dtype} : {count} colonnes")
            with col2:
                st.write("**Valeurs manquantes :**")
                missing_df = pd.DataFrame({
                    'Colonne': data.columns,
                    'Valeurs manquantes': data.isnull().sum().values,
                    'Pourcentage': (data.isnull().sum() / len(data) * 100).round(2)
                })
                st.dataframe(missing_df, use_container_width=True)
        
        with tab3:
            st.write("**Statistiques descriptives :**")
            st.dataframe(data.describe(include='all'), use_container_width=True)
        
        with tab4:
            col1, col2 = st.columns(2)
            with col1:
                # Qualité des données
                st.write("**Indicateurs de qualité :**")
                total_cells = data.shape[0] * data.shape[1]
                quality_metrics = {
                    'Complétude': f"{((total_cells - data.isnull().sum().sum()) / total_cells * 100):.1f}%",
                    'Unicité': f"{((data.shape[0] - data.duplicated().sum()) / data.shape[0] * 100):.1f}%",
                    'Consistance': "À analyser",
                    'Précision': "À valider"
                }
                for metric, value in quality_metrics.items():
                    st.write(f"- **{metric}** : {value}")
            
            with col2:
                st.write("**Alertes de qualité :**")
                if data.isnull().sum().sum() > 0:
                    st.error("❌ Données manquantes détectées")
                if data.duplicated().sum() > 0:
                    st.warning("⚠️ Doublons détectés")
                if data.select_dtypes(include='number').empty:
                    st.info("ℹ️ Aucune colonne numérique détectée")
        
        with tab5:
            # Analyse par type de données
            numeric_cols = data.select_dtypes(include='number').columns
            categorical_cols = data.select_dtypes(include=['object', 'category']).columns
            date_cols = [col for col in data.columns if 'date' in col.lower() or 'time' in col.lower()]
            
            st.write(f"**{len(numeric_cols)} colonnes numériques** : {list(numeric_cols)}")
            st.write(f"**{len(categorical_cols)} colonnes catégorielles** : {list(categorical_cols)}")
            if date_cols:
                st.write(f"**{len(date_cols)} colonnes temporelles** : {date_cols}")
        
        st.markdown('</div>', unsafe_allow_html=True)

        # --- Détection des valeurs aberrantes ---
        if detect_outliers and len(data.select_dtypes(include='number').columns) > 0:
            st.markdown('<div class="modern-card">', unsafe_allow_html=True)
            st.markdown('<div class="card-title">🚨 Détection des Valeurs Aberrantes</div>', unsafe_allow_html=True)
            
            numerical_columns = data.select_dtypes(include='number').columns.tolist()
            anomalies = detect_anomalies(data, numerical_columns)
            
            col1, col2 = st.columns(2)
            with col1:
                st.write("**Résumé des anomalies :**")
                for col, info in anomalies.items():
                    if info['count'] > 0:
                        st.write(f"- **{col}** : {info['count']} anomalies ({info['percentage']:.1f}%)")
            
            with col2:
                # Options de traitement
                st.write("**Traitement des anomalies :**")
                handle_outliers = st.selectbox(
                    "Action sur les anomalies :",
                    ["Aucune", "Marquer", "Supprimer", "Remplacer par médiane"]
                )
                
                if st.button("Appliquer le traitement"):
                    if handle_outliers == "Supprimer":
                        for col in numerical_columns:
                            Q1 = data[col].quantile(0.25)
                            Q3 = data[col].quantile(0.75)
                            IQR = Q3 - Q1
                            lower_bound = Q1 - 1.5 * IQR
                            upper_bound = Q3 + 1.5 * IQR
                            data = data[(data[col] >= lower_bound) & (data[col] <= upper_bound)]
                        st.success("Anomalies supprimées avec succès")
            
            st.markdown('</div>', unsafe_allow_html=True)

        # --- Filtrage interactif avancé ---
        st.markdown('<div class="modern-card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">🔎 Filtrage Avancé & Segmentation</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            filter_cols = st.multiselect("Colonnes à filtrer :", data.columns)
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
        
        with col2:
            st.write("**Résultats du filtrage :**")
            st.metric("Lignes filtrées", filtered_data.shape[0])
            st.metric("Colonnes", filtered_data.shape[1])
            reduction = ((data.shape[0] - filtered_data.shape[0]) / data.shape[0]) * 100
            st.metric("Réduction", f"{reduction:.1f}%")
            
            # Sauvegarde du jeu de données filtré
            if st.button("💾 Sauvegarder cette vue"):
                st.session_state['filtered_data'] = filtered_data
                st.success("Vue sauvegardée !")
        
        st.success(f"**📊 Données filtrées :** {filtered_data.shape[0]} lignes × {filtered_data.shape[1]} colonnes")
        st.dataframe(filtered_data.head(10), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # --- Machine Learning & Clustering ---
        if ml_enabled and clustering_enabled and len(data.select_dtypes(include='number').columns) >= 2:
            st.markdown('<div class="modern-card">', unsafe_allow_html=True)
            st.markdown('<div class="card-title">🤖 Machine Learning - Clustering</div>', unsafe_allow_html=True)
            
            numerical_columns = st.multiselect(
                "Sélectionnez les colonnes pour le clustering :",
                data.select_dtypes(include='number').columns.tolist(),
                default=data.select_dtypes(include='number').columns.tolist()[:2]
            )
            
            if len(numerical_columns) >= 2:
                n_clusters = st.slider("Nombre de clusters :", 2, 10, 3)
                
                if st.button("🔍 Exécuter le Clustering"):
                    try:
                        clusters, kmeans = perform_clustering(data, numerical_columns, n_clusters)
                        data['Cluster'] = clusters
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write("**Répartition des clusters :**")
                            cluster_counts = pd.Series(clusters).value_counts().sort_index()
                            for cluster, count in cluster_counts.items():
                                st.write(f"Cluster {cluster} : {count} éléments ({count/len(data)*100:.1f}%)")
                        
                        with col2:
                            if PLOTLY_AVAILABLE:
                                fig = px.scatter(
                                    data, x=numerical_columns[0], y=numerical_columns[1],
                                    color=clusters, title="Visualisation des Clusters",
                                    color_continuous_scale='viridis'
                                )
                                st.plotly_chart(fig, use_container_width=True)
                        
                        st.success("Clustering terminé avec succès !")
                    except Exception as e:
                        st.error(f"Erreur lors du clustering : {e}")
            
            st.markdown('</div>', unsafe_allow_html=True)

        # --- Analyse temporelle ---
        date_columns = [col for col in data.columns if 'date' in col.lower() or 'time' in col.lower()]
        if forecasting_enabled and date_columns:
            st.markdown('<div class="modern-card">', unsafe_allow_html=True)
            st.markdown('<div class="card-title">📈 Analyse Temporelle</div>', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                date_col = st.selectbox("Colonne de date :", date_columns)
            with col2:
                value_col = st.selectbox("Colonne de valeurs :", data.select_dtypes(include='number').columns)
            
            if date_col and value_col:
                stats, ts_data = time_series_forecast(data, date_col, value_col)
                if stats:
                    st.write("**Analyse de la série temporelle :**")
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Tendance", stats['trend'])
                    with col2:
                        st.metric("Volatilité", f"{stats['volatility']:.2f}")
                    with col3:
                        st.metric("Dernière valeur", f"{stats['last_value']:.2f}")
                    with col4:
                        st.metric("Taux croissance", f"{stats['growth_rate']:.1f}%")
                    
                    if PLOTLY_AVAILABLE and ts_data is not None:
                        fig = px.line(ts_data, x=ts_data.index, y=value_col, title=f"Évolution de {value_col}")
                        st.plotly_chart(fig, use_container_width=True)
            
            st.markdown('</div>', unsafe_allow_html=True)

        # --- Visualisations interactives avancées ---
        if PLOTLY_AVAILABLE:
            st.markdown('<div class="modern-card">', unsafe_allow_html=True)
            st.markdown('<div class="card-title">📊 Visualisations Avancées</div>', unsafe_allow_html=True)
            
            viz_tab1, viz_tab2, viz_tab3 = st.tabs(["📈 Graphiques standards", "🔄 Graphiques avancés", "📋 Tableaux croisés"])
            
            with viz_tab1:
                viz_col1, viz_col2 = st.columns([1, 2])
                
                with viz_col1:
                    plot_type = st.selectbox("Type de visualisation :", 
                                           ["Histogramme", "Boxplot", "Scatter Plot", "Line Chart", "Bar Chart", "Pie Chart", "Heatmap"])
                    
                    numeric_cols = filtered_data.select_dtypes(include='number').columns.tolist()
                    cat_cols = filtered_data.select_dtypes(include=['object', 'category']).columns.tolist()
                    
                    if plot_type in ["Histogramme", "Boxplot"] and numeric_cols:
                        selected_col = st.selectbox("Colonne numérique :", numeric_cols)
                    elif plot_type == "Scatter Plot" and len(numeric_cols) >= 2:
                        x_col = st.selectbox("Axe X :", numeric_cols)
                        y_col = st.selectbox("Axe Y :", [c for c in numeric_cols if c != x_col])
                    elif plot_type == "Pie Chart" and cat_cols:
                        selected_col = st.selectbox("Colonne catégorielle :", cat_cols)
                    elif plot_type == "Heatmap" and len(numeric_cols) >= 2:
                        st.write("Heatmap des corrélations")
                
                with viz_col2:
                    try:
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
                        
                        elif plot_type == "Heatmap" and len(numeric_cols) >= 2:
                            corr_matrix = filtered_data[numeric_cols].corr()
                            fig = px.imshow(corr_matrix, 
                                          title="Matrice de corrélations",
                                          color_continuous_scale='RdBu_r',
                                          aspect='auto')
                            st.plotly_chart(fig, use_container_width=True)
                        
                    except Exception as e:
                        st.warning(f"Impossible de générer la visualisation : {e}")
            
            with viz_tab2:
                st.write("**Graphiques avancés**")
                # Ici vous pouvez ajouter des graphiques plus complexes
                # comme les graphiques en violon, les treemaps, etc.
                st.info("Fonctionnalités avancées en développement...")
            
            with viz_tab3:
                st.write("**Tableaux croisés dynamiques**")
                if len(cat_cols) >= 2:
                    row_col = st.selectbox("Lignes :", cat_cols)
                    col_col = st.selectbox("Colonnes :", cat_cols)
                    value_col = st.selectbox("Valeurs :", numeric_cols) if numeric_cols else None
                    
                    if row_col and col_col:
                        pivot_table = pd.pivot_table(
                            filtered_data, 
                            values=value_col if value_col else None,
                            index=row_col, 
                            columns=col_col,
                            aggfunc='count' if not value_col else 'mean'
                        )
                        st.dataframe(pivot_table, use_container_width=True)
            
            st.markdown('</div>', unsafe_allow_html=True)

        # --- Export et reporting avancé ---
        st.markdown('<div class="modern-card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">💾 Export & Reporting Avancé</div>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.write("**Export des données :**")
            csv = filtered_data.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Télécharger CSV", 
                             data=csv, 
                             file_name="donnees_analysees.csv",
                             mime="text/csv")
        
        with col2:
            excel_buffer = io.BytesIO()
            with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
                filtered_data.to_excel(writer, index=False, sheet_name='Données')
                if 'Cluster' in data.columns:
                    data.to_excel(writer, index=False, sheet_name='Avec_Clusters')
            st.download_button("📥 Télécharger Excel",
                             data=excel_buffer.getvalue(),
                             file_name="analyse_complete.xlsx",
                             mime="application/vnd.ms-excel")
        
        with col3:
            st.write("**Rapport d'analyse :**")
            if st.button("📄 Générer le rapport"):
                # Génération d'un rapport sommaire
                report = f"""
                RAPPORT D'ANALYSE - HevitraVizor+
                =================================
                
                Date de génération : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                Fichier source : {uploaded_file.name}
                
                MÉTRIQUES PRINCIPALES :
                - Lignes : {data.shape[0]}
                - Colonnes : {data.shape[1]}
                - Données manquantes : {data.isnull().sum().sum()} ({missing_percentage:.1f}%)
                - Colonnes numériques : {len(data.select_dtypes(include='number').columns)}
                - Colonnes catégorielles : {len(data.select_dtypes(include=['object', 'category']).columns)}
                
                INSIGHTS :
                {chr(10).join(insights)}
                
                Ce rapport a été généré automatiquement par HevitraVizor+.
                """
                
                st.text_area("Rapport généré :", report, height=300)
                st.download_button("📥 Télécharger le rapport",
                                 data=report,
                                 file_name="rapport_analyse.txt",
                                 mime="text/plain")
        
        st.markdown('</div>', unsafe_allow_html=True)

    except Exception as e:
        st.error(f"❌ Erreur lors du traitement des données : {str(e)}")
        st.info("💡 Conseil : Vérifiez le format de votre fichier et réessayez.")

else:
    # --- Page d'accueil étendue ---
    
    with st.container():
        st.markdown(
            "<h1 style='text-align: center; color: #2c3e50; margin-bottom: 1rem;'>🚀 HevitraVizor+</h1>",
            unsafe_allow_html=True
        )
        st.markdown(
            "<p style='text-align: center; color: #7f8c8d; font-size: 1.2rem; margin-bottom: 3rem;'>Plateforme d'analyse de données avancée avec IA et Machine Learning</p>",
            unsafe_allow_html=True
        )
        
        # Nouveaux modules
        col1, col2, col3, col4 = st.columns(4)
        
        features = [
            {"icon": "🤖", "title": "IA & ML", "desc": "Clustering et prédictions automatiques"},
            {"icon": "📈", "title": "Analytique Avancée", "desc": "Time series et analyses multivariées"},
            {"icon": "🔍", "title": "Détection Intelligente", "desc": "Anomalies et patterns cachés"},
            {"icon": "📊", "title": "Reporting Automatisé", "desc": "Rapports et exports intelligents"}
        ]
        
        for i, feature in enumerate(features):
            with [col1, col2, col3, col4][i]:
                st.markdown(f"### {feature['icon']} {feature['title']}")
                st.write(feature['desc'])
        
        st.markdown("---")
        
        # Démonstration avec des données d'exemple
        st.markdown("### 🎯 Démarrage Rapide")
        if st.button("🚀 Charger des données d'exemple"):
            # Créer des données d'exemple
            np.random.seed(42)
            example_data = pd.DataFrame({
                'Date': pd.date_range('2023-01-01', periods=100),
                'Ventes': np.random.normal(1000, 200, 100).cumsum(),
                'Clients': np.random.randint(50, 150, 100),
                'Region': np.random.choice(['Nord', 'Sud', 'Est', 'Ouest'], 100),
                'Produit': np.random.choice(['A', 'B', 'C', 'D'], 100),
                'Satisfaction': np.random.randint(1, 6, 100)
            })
            
            # Sauvegarder en CSV virtuel
            csv = example_data.to_csv(index=False)
            st.download_button(
                label="📥 Télécharger les données d'exemple",
                data=csv,
                file_name="donnees_exemple.csv",
                mime="text/csv"
            )
            st.info("Téléchargez ces données d'exemple pour tester toutes les fonctionnalités !")
        
        st.markdown("---")
        
        # Call to action amélioré
        st.success("""
        💡 **Comment commencer ?**
        1. Utilisez le panneau de gauche pour importer votre fichier
        2. Configurez les paramètres d'analyse avancée
        3. Explorez les nouvelles fonctionnalités IA et ML
        4. Générez des rapports automatisés
        """)
        
        # Informations étendues
        with st.expander("🎯 Fonctionnalités Avancées"):
            st.write("""
            **🤖 Intelligence Artificielle :**
            - Clustering automatique (K-means)
            - Détection des valeurs aberrantes
            - Analyse de séries temporelles
            
            **📊 Analytique Avancée :**
            - Matrices de corrélation interactives
            - Analyses multivariées
            - Segments et profils clients
            
            **🔍 Qualité des Données :**
            - Nettoyage automatique
            - Détection des doublons
            - Métriques de qualité
            
            **📈 Reporting :**
            - Rapports automatisés
            - Exports multiples formats
            - Tableaux de bord interactifs
            """)
        
        with st.expander("📋 Formats Supportés"):
            st.write("""
            - **CSV** (.csv) - Fichiers texte séparés par des virgules
            - **Excel** (.xlsx, .xls) - Feuilles de calcul
            - **Taille maximale** : 200MB
            - **Encodages** : UTF-8, Latin-1, etc.
            """)

# --- Footer étendu ---
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: #7f8c8d;'>HevitraVizor+ v2.0 • IA • Machine Learning • Analytics Avancé</p>",
    unsafe_allow_html=True
)