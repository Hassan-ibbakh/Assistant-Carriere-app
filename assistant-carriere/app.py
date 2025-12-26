import streamlit as st
import json
from core.pdf_extractor import extract_text_from_pdf
from core.n8n_client import send_to_n8n, ask_career_coach, search_jobs_n8n

# --- CONFIGURATION ---
st.set_page_config(
    page_title="Assistant Carrière",
    layout="wide",
    page_icon="",
    initial_sidebar_state="expanded"
)

# --- STYLES CSS OPTIMISÉS ---
st.markdown("""
<style>
    /* Variables CSS pour faciliter la maintenance */
    :root {
        --primary: #3b82f6;
        --primary-dark: #2563eb;
        --secondary: #8b5cf6;
        --accent: #ec4899;
        --success: #10b981;
        --warning: #f59e0b;
        --info: #3b82f6;
        
        /* Couleurs adaptatives */
        --bg-card: rgba(255, 255, 255, 0.95);
        --bg-card-hover: rgba(255, 255, 255, 1);
        --text-primary: #1e293b;
        --text-secondary: #475569;
        --text-muted: #64748b;
        --border-color: rgba(203, 213, 225, 0.5);
        --shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.08);
        --shadow-md: 0 4px 16px rgba(0, 0, 0, 0.1);
        --shadow-lg: 0 8px 32px rgba(0, 0, 0, 0.15);
    }
    
    /* Adaptation automatique au mode sombre */
    @media (prefers-color-scheme: dark) {
        :root {
            --bg-card: rgba(30, 41, 59, 0.7);
            --bg-card-hover: rgba(30, 41, 59, 0.9);
            --text-primary: #f1f5f9;
            --text-secondary: #cbd5e1;
            --text-muted: #94a3b8;
            --border-color: rgba(255, 255, 255, 0.1);
            --shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.3);
            --shadow-md: 0 4px 16px rgba(0, 0, 0, 0.4);
            --shadow-lg: 0 8px 32px rgba(0, 0, 0, 0.5);
        }
    }
    
    /* Forcer le mode sombre pour Streamlit dark theme */
    [data-theme="dark"] {
        --bg-card: rgba(30, 41, 59, 0.7);
        --bg-card-hover: rgba(30, 41, 59, 0.9);
        --text-primary: #f1f5f9;
        --text-secondary: #cbd5e1;
        --text-muted: #94a3b8;
        --border-color: rgba(255, 255, 255, 0.1);
        --shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.3);
        --shadow-md: 0 4px 16px rgba(0, 0, 0, 0.4);
        --shadow-lg: 0 8px 32px rgba(0, 0, 0, 0.5);
    }
    
    /* En-tête principal */
    .header-container {
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 50%, #ec4899 100%);
        padding: 2.5rem;
        border-radius: 20px;
        margin-bottom: 2.5rem;
        box-shadow: 0 10px 40px rgba(79, 70, 229, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.15);
        position: relative;
        overflow: hidden;
    }
    
    .header-container::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: pulse 4s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); opacity: 0.5; }
        50% { transform: scale(1.1); opacity: 0.8; }
    }
    
    .header-title {
        color: white;
        font-size: 2.8rem;
        font-weight: 800;
        margin: 0;
        text-align: center;
        text-shadow: 0 4px 20px rgba(0,0,0,0.3);
        position: relative;
        z-index: 1;
    }
    
    .header-subtitle {
        color: rgba(255,255,255,0.95);
        font-size: 1.15rem;
        text-align: center;
        margin-top: 0.8rem;
        position: relative;
        z-index: 1;
        font-weight: 500;
    }
    
    /* Cards utilisant les variables CSS */
    .metric-card {
        background: var(--bg-card);
        backdrop-filter: blur(12px);
        padding: 1.8rem;
        border-radius: 16px;
        box-shadow: var(--shadow-md);
        border-left: 5px solid var(--primary);
        border: 1px solid var(--border-color);
        margin-bottom: 1.2rem;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .metric-card:hover {
        transform: translateY(-8px);
        box-shadow: var(--shadow-lg);
        border-color: var(--primary);
        background: var(--bg-card-hover);
    }
    
    .metric-card h3 {
        color: var(--text-primary);
        font-size: 1.3rem;
        margin-bottom: 0.5rem;
        font-weight: 700;
    }
    
    .metric-card p {
        color: var(--text-secondary);
        line-height: 1.6;
        font-size: 0.95rem;
    }
    
    /* Status badges */
    .status-badge {
        display: inline-block;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.9rem;
        margin: 0.5rem 0;
    }
    
    .status-success {
        background: rgba(16, 185, 129, 0.15);
        color: var(--success);
        border: 1px solid rgba(16, 185, 129, 0.3);
    }
    
    .status-warning {
        background: rgba(245, 158, 11, 0.15);
        color: var(--warning);
        border: 1px solid rgba(245, 158, 11, 0.3);
    }
    
    .status-info {
        background: rgba(59, 130, 246, 0.15);
        color: var(--info);
        border: 1px solid rgba(59, 130, 246, 0.3);
    }
    
    /* Job cards */
    .job-card {
        background: var(--bg-card);
        backdrop-filter: blur(12px);
        padding: 1.8rem;
        border-radius: 16px;
        box-shadow: var(--shadow-md);
        margin-bottom: 1.2rem;
        border: 1px solid var(--border-color);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .job-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.05) 0%, transparent 50%);
        opacity: 0;
        transition: opacity 0.4s;
    }
    
    .job-card:hover::before {
        opacity: 1;
    }
    
    .job-card:hover {
        box-shadow: var(--shadow-lg);
        border-color: var(--primary);
        transform: translateY(-4px);
    }
    
    .job-title {
        color: var(--text-primary);
        font-size: 1.4rem;
        font-weight: 700;
        margin-bottom: 0.8rem;
        position: relative;
        z-index: 1;
    }
    
    .job-meta {
        color: var(--text-secondary);
        font-size: 0.95rem;
        margin: 0.4rem 0;
        position: relative;
        z-index: 1;
    }
    
    /* Sidebar styling */
    .sidebar-section {
        background: var(--bg-card);
        backdrop-filter: blur(12px);
        padding: 1.8rem;
        border-radius: 16px;
        margin-bottom: 1.2rem;
        box-shadow: var(--shadow-sm);
        border: 1px solid var(--border-color);
        transition: all 0.3s;
    }
    
    .sidebar-section:hover {
        border-color: var(--primary);
        box-shadow: var(--shadow-md);
    }
    
    /* Containers avec bordures */
    [data-testid="stVerticalBlock"] > [style*="border"] {
        background: var(--bg-card) !important;
        backdrop-filter: blur(12px);
        border: 1px solid var(--border-color) !important;
        border-radius: 16px;
        box-shadow: var(--shadow-sm);
    }
    
    /* Amélioration des boutons */
    .stButton>button {
        border-radius: 12px;
        font-weight: 600;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        border: 1px solid var(--border-color);
        position: relative;
        overflow: hidden;
    }
    
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: var(--shadow-md);
        border-color: var(--primary);
    }
    
    .stButton>button[kind="primary"] {
        background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
        border: none;
        color: white;
    }
    
    .stButton>button[kind="primary"]:hover {
        background: linear-gradient(135deg, var(--primary-dark) 0%, var(--secondary) 100%);
        box-shadow: 0 12px 32px rgba(59, 130, 246, 0.4);
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        background: var(--bg-card);
        padding: 0.8rem;
        border-radius: 16px;
        backdrop-filter: blur(10px);
        border: 1px solid var(--border-color);
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 12px;
        color: var(--text-muted);
        font-weight: 600;
        padding: 0.8rem 1.5rem;
        transition: all 0.3s;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(59, 130, 246, 0.1);
        color: var(--primary);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.2) 0%, rgba(139, 92, 246, 0.2) 100%);
        color: var(--primary);
        box-shadow: var(--shadow-sm);
    }
    
    /* Métriques */
    [data-testid="stMetricValue"] {
        color: var(--text-primary);
        font-size: 1.8rem;
    }
    
    [data-testid="stMetricLabel"] {
        color: var(--text-muted);
    }
    
    /* Progress bar */
    .stProgress > div > div {
        background: linear-gradient(90deg, var(--primary) 0%, var(--secondary) 100%);
    }
    
    /* Text input */
    .stTextInput > div > div > input {
        background: var(--bg-card);
        border: 1px solid var(--border-color);
        color: var(--text-primary);
        border-radius: 12px;
        padding: 0.8rem 1rem;
        transition: all 0.3s;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: var(--primary);
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
    }
    
    .stTextInput > div > div > input::placeholder {
        color: var(--text-muted);
    }
    
    /* Multiselect */
    .stMultiSelect > div > div {
        background: var(--bg-card);
        border: 1px solid var(--border-color);
        border-radius: 12px;
    }
    
    .stMultiSelect [data-baseweb="tag"] {
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.2) 0%, rgba(139, 92, 246, 0.2) 100%);
        border: 1px solid rgba(59, 130, 246, 0.3);
        color: var(--primary);
    }
    
    /* Dividers */
    hr {
        border-color: var(--border-color);
    }
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--bg-card);
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--primary);
        border-radius: 5px;
        opacity: 0.5;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        opacity: 1;
    }
    
    /* Chat messages */
    .stChatMessage {
        background: var(--bg-card) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 12px;
    }
    
    /* File uploader */
    [data-testid="stFileUploader"] {
        background: var(--bg-card);
        border: 2px dashed var(--border-color);
        border-radius: 12px;
        padding: 1.5rem;
    }
    
    [data-testid="stFileUploader"]:hover {
        border-color: var(--primary);
        background: var(--bg-card-hover);
    }
</style>
""", unsafe_allow_html=True)

# --- EN-TÊTE PROFESSIONNEL ---
st.markdown("""
<div class="header-container">
    <h1 class="header-title">Assistant Carrière</h1>
    <p class="header-subtitle">Analyse intelligente • Coaching personnalisé • Recherche d'emploi optimisée</p>
</div>
""", unsafe_allow_html=True)

# --- INITIALISATION SESSION STATE ---
if "analysis_data" not in st.session_state:
    st.session_state.analysis_data = None
if "messages" not in st.session_state:
    st.session_state.messages = []
if "jobs_results" not in st.session_state:
    st.session_state.jobs_results = []
if "cv_uploaded" not in st.session_state:
    st.session_state.cv_uploaded = False

# --- SIDEBAR PROFESSIONNELLE ---
with st.sidebar:
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown("### 📂 Votre Dossier")
    
    uploaded_file = st.file_uploader(
        "Importez votre CV",
        type="pdf",
        help="Format PDF uniquement, max 10MB"
    )
    
    if uploaded_file:
        st.session_state.cv_uploaded = True
        file_size = len(uploaded_file.getvalue()) / 1024
        st.caption(f"📄 {uploaded_file.name} ({file_size:.1f} KB)")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Indicateur de statut
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown("### 📊 Statut du Profil")
    
    if st.session_state.analysis_data:
        st.markdown('<span class="status-badge status-success">✓ Analyse complète</span>', unsafe_allow_html=True)
        meta = st.session_state.analysis_data.get("meta", {})
        if meta.get("job_title"):
            st.info(f"**Profil :** {meta['job_title']}")
    else:
        st.markdown('<span class="status-badge status-warning">⏳ En attente d\'analyse</span>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.divider()
    
    # Actions rapides
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Réinitialiser", use_container_width=True):
            st.session_state.analysis_data = None
            st.session_state.messages = []
            st.session_state.jobs_results = []
            st.session_state.cv_uploaded = False
            st.rerun()
    with col2:
        if st.button("💾 Exporter", use_container_width=True):
            if st.session_state.analysis_data:
                st.download_button(
                    "📥 Télécharger JSON",
                    json.dumps(st.session_state.analysis_data, indent=2),
                    "analyse_complete.json",
                    use_container_width=True
                )

# --- CONTENU PRINCIPAL ---
if uploaded_file:
    with st.spinner("🔍 Analyse du document en cours..."):
        resume_text = extract_text_from_pdf(uploaded_file)
    
    if resume_text:
        # Indicateur de progression
        if not st.session_state.analysis_data:
            col1, col2, col3, col4, col5 = st.columns(5)
            steps = [
                ("1", "Upload", col1),
                ("2", "Analyse", col2),
                ("3", "Optimisation", col3),
                ("4", "Coaching", col4),
                ("5", "Recherche", col5)
            ]
            
            for num, label, col in steps:
                with col:
                    if num == "1":
                        st.markdown(f"**✓ {label}**")
                    else:
                        st.markdown(f"○ {label}")
        
        # Onglets professionnels
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📊 Analyse Complète",
            "✨ CV Optimisé",
            "🔄 Comparatif",
            "💬 Coach IA",
            "🌍 Opportunités"
        ])

        # --- TAB 1: ANALYSE ---
        with tab1:
            if st.session_state.analysis_data is None:
                st.markdown("""
                <div class="metric-card">
                    <h3>🚀 Lancement de l'Analyse</h3>
                    <p>Notre IA va analyser votre CV pour identifier vos points forts, axes d'amélioration et générer une version optimisée.</p>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button("🎯 Démarrer l'Analyse Complète", type="primary", use_container_width=True):
                    with st.spinner("🧠 Analyse en cours..."):
                        progress_bar = st.progress(0)
                        
                        progress_bar.progress(30)
                        response = send_to_n8n(resume_text)
                        
                        progress_bar.progress(70)
                        
                        if response:
                            try:
                                raw = response.get("content", "")
                                clean = raw.replace("```json", "").replace("```", "").strip()
                                st.session_state.analysis_data = json.loads(clean)
                                progress_bar.progress(100)
                                st.success("✅ Analyse terminée avec succès !")
                                st.rerun()
                            except Exception as e:
                                st.error(f"❌ Erreur de traitement : {e}")
                                with st.expander("Détails de la réponse"):
                                    st.code(response)
            
            if st.session_state.analysis_data:
                data = st.session_state.analysis_data
                
                # Header avec profil identifié
                job_title = data.get("meta", {}).get("job_title", "Non détecté")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("🎯 Profil Identifié", job_title)
                with col2:
                    skills = data.get("key_skills", [])
                    st.metric("🔑 Compétences Clés", len(skills))
                with col3:
                    st.metric("📈 Statut", "Analysé")
                
                st.divider()
                
                # Analyse détaillée
                col_left, col_right = st.columns([1, 1])
                
                with col_left:
                    st.markdown("### 🔍 Analyse de l'Existant")
                    with st.container(border=True):
                        st.markdown(data.get("analyse_actuelle", "Aucune analyse disponible."))
                
                with col_right:
                    st.markdown("### 💡 Recommandations Structurelles")
                    with st.container(border=True):
                        st.markdown(data.get("conseils_structure", "Aucun conseil spécifique."))
                
                # Compétences clés
                if skills:
                    st.markdown("### 🎯 Compétences Identifiées")
                    cols = st.columns(min(len(skills), 4))
                    for idx, skill in enumerate(skills[:8]):
                        with cols[idx % 4]:
                            st.markdown(f'<span class="status-badge status-info">{skill}</span>', unsafe_allow_html=True)

        # --- TAB 2: CV OPTIMISÉ ---
        with tab2:
            if st.session_state.analysis_data:
                data = st.session_state.analysis_data
                
                st.markdown("### ✨ Votre CV Réécrit par l'IA")
                st.caption("Version professionnelle optimisée pour les ATS et recruteurs")
                
                new_cv = data.get("cv_reecrit", "")
                
                with st.container(border=True):
                    st.markdown(new_cv)
                
                col1, col2 = st.columns(2)
                with col1:
                    st.download_button(
                        "📥 Télécharger (Markdown)",
                        new_cv,
                        "cv_optimise.md",
                        use_container_width=True
                    )
                with col2:
                    st.download_button(
                        "📄 Télécharger (TXT)",
                        new_cv,
                        "cv_optimise.txt",
                        use_container_width=True
                    )
            else:
                st.info("⚠️ Veuillez d'abord lancer l'analyse dans l'onglet 'Analyse Complète'")

        # --- TAB 3: COMPARAISON ---
        with tab3:
            if st.session_state.analysis_data:
                st.markdown("### 🔄 Comparatif Avant / Après")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("#### 📄 Version Originale")
                    with st.container(border=True):
                        st.text_area("", resume_text, height=500, label_visibility="collapsed")
                
                with col2:
                    st.markdown("#### ✨ Version Optimisée")
                    with st.container(border=True):
                        st.markdown(st.session_state.analysis_data.get("cv_reecrit", ""))
            else:
                st.info("⚠️ Veuillez d'abord lancer l'analyse")

        # --- TAB 4: CHATBOT COACH ---
        with tab4:
            st.markdown("### 💬 Coach Carrière IA")
            st.caption("Posez vos questions sur votre parcours, vos compétences ou votre stratégie de recherche")
            
            # Affichage de l'historique
            chat_container = st.container(height=400)
            with chat_container:
                for msg in st.session_state.messages:
                    with st.chat_message(msg["role"]):
                        st.markdown(msg["content"])
            
            # Input utilisateur
            if prompt := st.chat_input("Posez votre question..."):
                st.session_state.messages.append({"role": "user", "content": prompt})
                
                with st.spinner("🤔 Le coach réfléchit..."):
                    reply = ask_career_coach(prompt, resume_text)
                
                st.session_state.messages.append({"role": "assistant", "content": reply})
                st.rerun()

        # --- TAB 5: RECHERCHE D'EMPLOI ---
        with tab5:
            st.markdown("### 🌍 Recherche d'Opportunités Personnalisée")
            
            # Préparation de la requête par défaut
            default_query = "Data Scientist"
            if st.session_state.analysis_data:
                meta = st.session_state.analysis_data.get("meta", {})
                skills = st.session_state.analysis_data.get("key_skills", [])
                default_query = meta.get("job_title") or (f"{skills[0]}" if skills else "")
            
            # Formulaire de recherche
            with st.container(border=True):
                st.markdown("#### 🎯 Définissez vos Critères")
                
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    user_query = st.text_input(
                        "Intitulé du poste",
                        value=default_query,
                        placeholder="Ex: Data Scientist, Ingénieur DevOps..."
                    )
                
                with col2:
                    country_options = ["Maroc", "Canada", "USA"]
                    selected_countries = st.multiselect(
                        "Pays cibles",
                        country_options,
                        default=["Maroc", "Canada"]
                    )
                
                search_col1, search_col2 = st.columns([3, 1])
                with search_col1:
                    st.caption("💡 La recherche inclut automatiquement les offres d'emploi et de stage")
                with search_col2:
                    launch_search = st.button("🔍 Lancer la Recherche", type="primary", use_container_width=True)
            
            # Logique de recherche
            if launch_search:
                if not user_query:
                    st.error("❌ Veuillez entrer un intitulé de poste")
                elif not selected_countries:
                    st.error("❌ Veuillez sélectionner au moins un pays")
                else:
                    st.session_state.jobs_results = []
                    all_jobs = []
                    
                    location_map = {
                        "Maroc": "Morocco",
                        "Canada": "Toronto, Canada",
                        "USA": "United States"
                    }
                    
                    progress = st.progress(0)
                    status_text = st.empty()
                    
                    for i, country_name in enumerate(selected_countries):
                        api_loc = location_map.get(country_name, country_name)
                        
                        sub_targets = [
                            {"type": "Emploi", "q": user_query, "icon": "💼"},
                            {"type": "Stage", "q": f"Stage {user_query}", "icon": "🎓"}
                        ]
                        
                        for sub in sub_targets:
                            status_text.text(f"🔍 Recherche {sub['type']} en {country_name}...")
                            
                            found = search_jobs_n8n(sub['q'], api_loc)
                            
                            flag_map = {"Maroc": "🇲🇦", "Canada": "🇨🇦", "USA": "🇺🇸"}
                            flag = flag_map.get(country_name, "🌍")
                            badge = f"{sub['icon']} {sub['type'].upper()}"
                            
                            for j in found:
                                j['display_tag'] = f"{flag} {badge}"
                                j['country'] = country_name
                                all_jobs.append(j)
                        
                        progress.progress((i + 1) / len(selected_countries))
                    
                    unique_jobs = {v['link']: v for v in all_jobs}.values()
                    st.session_state.jobs_results = list(unique_jobs)
                    
                    progress.empty()
                    status_text.empty()
                    
                    st.success(f"✅ Recherche terminée : {len(st.session_state.jobs_results)} opportunités trouvées !")
            
            st.divider()
            
            # Affichage des résultats
            jobs = st.session_state.jobs_results
            
            if jobs:
                # Statistiques
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("📊 Total", len(jobs))
                with col2:
                    stages = sum(1 for j in jobs if "STAGE" in j.get('display_tag', ''))
                    st.metric("🎓 Stages", stages)
                with col3:
                    emplois = len(jobs) - stages
                    st.metric("💼 Emplois", emplois)
                
                st.markdown("### 📋 Opportunités Disponibles")
                
                # Grille de résultats
                for i in range(0, len(jobs), 2):
                    col1, col2 = st.columns(2)
                    
                    for idx, col in enumerate([col1, col2]):
                        job_idx = i + idx
                        if job_idx < len(jobs):
                            job = jobs[job_idx]
                            
                            with col:
                                with st.container(border=True):
                                    st.markdown(f"**{job.get('display_tag', '🌍')}**")
                                    st.markdown(f"<div class='job-title'>{job.get('title', 'Titre inconnu')}</div>", unsafe_allow_html=True)
                                    
                                    company = job.get('company', 'Entreprise non spécifiée')
                                    location = job.get('location', 'Localisation non spécifiée')
                                    
                                    if "Anywhere" in location:
                                        location = "🌍 Remote"
                                    
                                    st.markdown(f"<div class='job-meta'>🏢 {company}</div>", unsafe_allow_html=True)
                                    st.markdown(f"<div class='job-meta'>📍 {location}</div>", unsafe_allow_html=True)
                                    
                                    st.link_button("👉 Consulter l'offre", job.get('link', '#'), use_container_width=True)
            
            elif jobs == []:
                st.info("🔍 Configurez vos critères de recherche ci-dessus et lancez la recherche")

    else:
        st.error("❌ Impossible de lire le fichier PDF. Veuillez vérifier le format.")

else:
    # Page d'accueil vide
    st.markdown("""
    <div style='text-align: center; padding: 4rem 2rem;'>
        <h2 style='color: var(--text-primary);'>👋 Bienvenue sur votre Assistant Carrière</h2>
        <p style='font-size: 1.2rem; color: var(--text-secondary); margin: 2rem 0;'>
            Commencez par importer votre CV dans la barre latérale pour débuter l'analyse
        </p>
        <div style='margin-top: 3rem;'>
            <h3 style='color: var(--text-secondary);'>🎯 Ce que nous faisons pour vous :</h3>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>📊 Analyse Complète</h3>
            <p>Évaluation détaillée de votre CV avec identification des points forts et axes d'amélioration</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3>✨ Optimisation IA</h3>
            <p>Réécriture professionnelle de votre CV optimisée pour les ATS et recruteurs</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3>🌍 Recherche Ciblée</h3>
            <p>Découverte d'opportunités au Maroc, Canada et USA adaptées à votre profil</p>
        </div>
        """, unsafe_allow_html=True)