# Image Python légère
FROM python:3.9-slim

# Répertoire de travail dans le conteneur
WORKDIR /app

# Installation des outils système de base (nécessaire pour certaines libs PDF)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copie des dépendances et installation
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie de tout le code du projet (app.py, core/, etc.)
COPY . .

# Exposition du port
EXPOSE 8501

# Lancement de Streamlit
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]