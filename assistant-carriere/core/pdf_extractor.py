import pdfplumber
import streamlit as st

def extract_text_from_pdf(uploaded_file):
    """
    Lit un fichier PDF en essayant de préserver la disposition visuelle (colonnes).
    Utilise 'layout=True' pour garder les espaces horizontaux.
    """
    try:
        # On ouvre le fichier PDF
        with pdfplumber.open(uploaded_file) as pdf:
            full_text = ""
            
            for page in pdf.pages:
                # L'argument layout=True est magique ici :
                # Il essaie de reproduire la mise en page physique avec des espaces.
                # Cela permet à GPT-4 de "voir" les colonnes grâce aux espaces.
                text = page.extract_text(layout=True)
                
                if text:
                    full_text += text + "\n\n"
                    
        return full_text

    except Exception as e:
        st.error(f"Erreur d'extraction PDF : {e}")
        return None