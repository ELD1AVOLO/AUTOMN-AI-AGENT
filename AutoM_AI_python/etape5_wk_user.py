# -*- coding: utf-8 -*-
"""
Created on Fri Aug  8 12:19:59 2025

@author: elmou
"""

import requests
import json

# 📥 Charger les données JSON de l'interface
with open("etape4_output.json", "r", encoding="utf-8") as file:
    interface_ui = json.load(file)

# 💬 Prompt pour générer une description fonctionnelle fluide
PROMPT_DESCRIPTION_UI = f"""
Tu es un assistant qui rédige des descriptions fonctionnelles d’interfaces utilisateur.

À partir des données suivantes décrivant une interface :
{json.dumps(interface_ui, indent=2, ensure_ascii=False)}

Écris une description claire de cette interface, incluant :
- Son objectif
- Son utilisateur cible
- Les champs et boutons
- Leur disposition
- Les contraintes éventuelles

Réponds avec un texte fluide et naturel, prêt à être inséré dans un prompt de génération d’image.
"""

# ⚙️ Paramètres de l’API Ollama
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "prompt/hermes-2-pro:latest"  # 🧠 Change selon le modèle que tu veux utiliser

# 📡 Envoi du prompt à Ollama
response = requests.post(OLLAMA_URL, json={
    "model": MODEL,
    "prompt": PROMPT_DESCRIPTION_UI,
    "stream": False
})

# 📤 Sauvegarder la réponse
if response.status_code == 200:
    result_text = response.json()["response"]

    with open("description_ui.txt", "w", encoding="utf-8") as desc_file:
        desc_file.write(result_text)

    print("✅ Description fonctionnelle enregistrée dans description_ui.txt")

else:
    print("❌ Erreur lors de l’appel à Ollama :", response.status_code)
    print(response.text)
