import requests
import os
import streamlit as st
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

def send_to_n8n(text_content):
    """
    Envoie le texte du CV au Webhook n8n pour l'analyse IA.
    """
    webhook_url = os.getenv("N8N_WEBHOOK_URL")
    
    if not webhook_url:
        st.error("⚠️ ERREUR CONFIG : L'URL du webhook est manquante dans le fichier .env")
        return None

    payload = {"resume_text": text_content}

    try:
        response = requests.post(webhook_url, json=payload)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Erreur n8n ({response.status_code}): {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Erreur de connexion avec le serveur n8n : {e}")
        return None

def ask_career_coach(question, cv_text):
    """
    Envoie une question et le contexte du CV au chatbot n8n.
    """
    webhook_url = os.getenv("N8N_CHAT_WEBHOOK")
    
    if not webhook_url:
        st.error("⚠️ URL Chat Webhook manquante.")
        return None

    payload = {
        "question": question,
        "cv_context": cv_text
    }

    try:
        response = requests.post(webhook_url, json=payload)
        if response.status_code == 200:
            return response.json().get("reply", "Pas de réponse.")
        else:
            return f"Erreur n8n: {response.status_code}"
    except Exception as e:
        return f"Erreur connexion: {e}"

def search_jobs_n8n(query, location):
    """
    Envoie des critères de recherche à n8n.
    Version simple et robuste (sans domain ni gl pour éviter les conflits).
    """
    webhook_url = os.getenv("N8N_SEARCH_WEBHOOK")
    
    if not webhook_url:
        st.error("⚠️ URL Webhook Search manquante (.env)")
        return []

    # Payload simple : juste la requête et la localisation
    payload = {
        "query": query,
        "location": location
    }

    try:
        response = requests.post(webhook_url, json=payload)
        
        if response.status_code == 200:
            data = response.json()
            jobs = data.get("jobs", [])
            
            # --- BLINDAGE ANTI-CRASH ---
            if isinstance(jobs, str):
                # Si c'est une erreur texte, on renvoie une liste vide
                return []
            
            if not isinstance(jobs, list):
                return []
                
            return jobs
        else:
            # En cas d'erreur API (404, 500), liste vide
            return []
            
    except Exception as e:
        return []