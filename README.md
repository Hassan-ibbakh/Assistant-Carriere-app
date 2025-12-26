# Assistant Carrière

Application intelligente d'analyse de CV, de coaching carrière et de recherche d'emploi automatisée.

## 🛠 Structure du projet
- **streamlit-app/** : Interface utilisateur développée avec Streamlit (Python).
- **n8n-backend/** : Workflows d'orchestration pour l'analyse IA et la recherche d'offres.

## 🚀 Fonctionnalités
- **Analyse de CV** : Extraction de données structurées et audit de profil (GPT-4o).
- **Coach IA** : Chatbot contextuel pour préparer des entretiens (RAG).
- **Chasseur de Têtes** : Recherche d'offres d'emploi multi-pays via SerpApi (Google Jobs).

## 🔧 Installation
1. Clonez le dépôt.
2. Configurez vos clés API (OpenAI et SerpApi) dans un fichier `.env`.
3. Lancez l'application Streamlit et les conteneurs Docker pour n8n.
