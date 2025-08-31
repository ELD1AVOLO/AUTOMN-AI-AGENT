# -*- coding: utf-8 -*-
"""
Created on Wed Aug  6 13:01:51 2025

@author: elmou
"""

import requests
import json

# 📥 Lire le prompt utilisateur depuis un fichier
with open("user_prompt.txt", "r", encoding="utf-8") as f:
    user_prompt = f.read()

# 🧠 Prompt pour l’étape 2
PROMPT_ETAPE_2 = f"""
Tu es un assistant qui analyse un besoin applicatif exprimé par un utilisateur pour générer une interface métier.

Voici le prompt de l’utilisateur :
\"\"\"{user_prompt}\"\"\"

Ta tâche est de résumer ce besoin en JSON enrichi contenant :

- "objectif" : résumé global du besoin
- "utilisateurs" : liste des rôles
- "actions" : dictionnaire des actions par rôle
- "étapes_logiques" : liste ordonnée des étapes du processus
- "interfaces_attendues" : liste des écrans ou interfaces nécessaires
- "données_saisies" : données ou champs mentionnés (ex : montant, justificatif)
- "contraintes" : contraintes techniques ou métier mentionnées

Réponds uniquement avec un JSON structuré, sans texte autour.
"""

# ⚙️ Paramètres API Ollama
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3"  # Remplace par deepseek-coder, hermes-pro, etc. si besoin

# 📡 Envoi du prompt à Ollama
response = requests.post(OLLAMA_URL, json={
    "model": MODEL,
    "prompt": PROMPT_ETAPE_2,
    "stream": False
})

# 📤 Sauvegarde du résultat
if response.status_code == 200:
    result_text = response.json()["response"]

    try:
        result_json = json.loads(result_text)
        with open("etape2_output.json", "w", encoding="utf-8") as f:
            json.dump(result_json, f, indent=2, ensure_ascii=False)
        print("✅ JSON structuré enregistré dans etape2_output.json")

    except json.JSONDecodeError:
        with open("etape2_raw.txt", "w", encoding="utf-8") as f:
            f.write(result_text)
        print("⚠️ Réponse non JSON valide. Résultat brut enregistré dans etape2_raw.txt")

else:
    print("❌ Erreur Ollama :", response.status_code)
    print(response.text)
