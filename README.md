#  Assistant Carrière 

**L'Intelligence Artificielle au service de votre réussite professionnelle.**

[![Python](https://img.shields.io/badge/Python-3.9-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28-FF4B4B.svg)](https://streamlit.io/)
[![n8n](https://img.shields.io/badge/n8n-Workflow-orange.svg)](https://n8n.io/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED.svg)](https://www.docker.com/)

Une application **Full-Stack** conçue pour optimiser le processus de recherche d'emploi. Elle combine une interface utilisateur interactive, une orchestration de workflows via n8n et la puissance des modèles LLM (GPT-4o) pour analyser, conseiller et trouver des opportunités.

---

## 🌟 Fonctionnalités Clés

### 1. 📊 Analyse & Audit de CV (ETL + NLP)
*   **Ingestion :** Extraction intelligente de texte depuis des fichiers PDF complexes (respect des colonnes et de la mise en page via `pdfplumber`).
*   **Diagnostic IA :** Analyse sémantique par GPT-4o pour identifier les points forts/faibles.
*   **Structuration :** Conversion de données non structurées en JSON (détection automatique du poste, compétences clés, niveau d'expérience).

### 2. ✨ Réécriture & Optimisation
*   Génération automatique d'une version "2.0" du CV, optimisée pour les ATS (Applicant Tracking Systems) et les recruteurs.
*   Formatage Markdown professionnel prêt à être téléchargé.

### 3. 💬 Coach Carrière Interactif (RAG Simplifié)
*   **Chatbot Contextuel :** Discutez avec votre propre CV. Le système utilise une architecture RAG (Retrieval-Augmented Generation) en injectant le contenu du CV dans le prompt système à chaque interaction.
*   **Simulation d'entretien :** L'IA peut jouer le rôle du recruteur et poser des questions techniques spécifiques au profil.

### 4. 🌍 Chasseur de Têtes Multi-Pays (Automatisation)
*   **Recherche Ciblée :** Utilisation de l'API Google Jobs (via SerpApi).
*   **Logique Multi-Régions :** Algorithme capable d'interroger simultanément les marchés du **Maroc**, du **Canada** et des **USA**.
*   **Mapping Intelligent :** Adaptation dynamique des paramètres de recherche (`gl`, `google_domain`, `location`) pour garantir des résultats pertinents selon le pays.

---

## 🏗️ Architecture Technique

Le projet repose sur une architecture **Micro-services** conteneurisée :

```mermaid
graph TD
    User((Utilisateur)) -->|Interface| UI[Streamlit (Frontend)]
    UI <-->|API REST| N8N[n8n (Orchestrateur Backend)]
    N8N <-->|Inférence| OpenAI[OpenAI GPT-4o]
    N8N <-->|Scraping| SerpApi[Google Jobs API]
    UI -.->|Persistance Session| RAM[(st.session_state)]
