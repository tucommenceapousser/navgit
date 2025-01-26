import streamlit as st
import requests
import openai
import os
from dotenv import load_dotenv

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Configuration des clés API OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

# URL GitHub pour récupérer les repos personnels
GITHUB_API_URL = "https://api.github.com/users/tucommenceapousser/repos"

# Fonction pour récupérer les repos GitHub
def get_github_repos():
    response = requests.get(GITHUB_API_URL)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Erreur de récupération des repos : {response.status_code}")
        return []

# Fonction GPT-4 pour générer des réponses
def chat_gpt(query):
    try:
        response = openai.Completion.create(
            engine="gpt-4", 
            prompt=query, 
            max_tokens=150
        )
        return response.choices[0].text.strip()
    except openai.error.AuthenticationError:
        st.error("Erreur d'authentification avec OpenAI. Vérifiez votre clé API.")
        return ""

# Fonction DALL-E pour générer des images
def generate_image(description):
    try:
        response = openai.Image.create(
            prompt=description,
            n=1,
            size="1024x1024"
        )
        return response['data'][0]['url']
    except Exception as e:
        st.error(f"Erreur lors de la génération de l'image : {e}")
        return ""

# Titre de l'application
st.title("Hacker Tools Repository")

# Design personnalisé
st.markdown("""
    <style>
    body {
        background-color: #121212;
        color: #00FF00;
        font-family: 'Courier New', Courier, monospace;
    }
    .stButton button {
        background-color: #FF0080;
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 10px;
        cursor: pointer;
        font-size: 16px;
    }
    .stButton button:hover {
        background-color: #FF00FF;
    }
    .stTextInput input {
        background-color: #333333;
        color: #00FF00;
        border: 1px solid #FF00FF;
        border-radius: 5px;
    }
    .stTextInput input:focus {
        border: 2px solid #00FF00;
    }
    </style>
""", unsafe_allow_html=True)

# Introduction
st.write("Bienvenue sur l'interface d'outils high-tech pour hackers. Obtenez des repos GitHub et interagissez avec GPT-4 et DALL-E.")

# Recherche des repos
st.subheader("Trouver des repos GitHub")
query = st.text_input("Entrez un mot-clé pour rechercher des repos :", "")

if query:
    repos = get_github_repos()
    filtered_repos = [repo for repo in repos if query.lower() in repo["name"].lower()]
    
    if filtered_repos:
        st.write(f"**Résultats pour '{query}' :**")
        for repo in filtered_repos:
            st.write(f"[{repo['name']}]({repo['html_url']}) - {repo['description']}")
    else:
        st.write(f"Aucun repo trouvé pour '{query}'.")

# Chat GPT-4
st.subheader("Pose une question à GPT-4")
question = st.text_input("Que souhaitez-vous savoir ?", "")

if question:
    response = chat_gpt(question)
    if response:
        st.write("**Réponse de GPT-4 :**", response)

# Génération d'images avec DALL-E
st.subheader("Générer une image avec DALL-E")
image_prompt = st.text_input("Décrivez l'image que vous souhaitez générer :")

if image_prompt:
    image_url = generate_image(image_prompt)
    if image_url:
        st.image(image_url, caption="Image générée par DALL-E", use_column_width=True)

# Footer
st.markdown("<br><hr><p style='text-align: center;'>Créé par trhacknon | <a href='https://www.facebook.com/share/g/SpQ3RD4dqmVHwfFm/'>Facebook</a></p>", unsafe_allow_html=True)
