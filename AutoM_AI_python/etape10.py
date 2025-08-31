# -*- coding: utf-8 -*-
"""
Created on Fri Jul 18 11:17:23 2025

@author: elmou
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Jul 18 10:40:00 2025
@author: elmou
"""

import requests
import os
import json

# === CONFIGURATION ===
MODEL_NAME = "prompt/hermes-2-pro:latest"
OLLAMA_URL = "http://localhost:11434/api/generate"
INPUT_JSON = "resume_processus.json"
OUTPUT_DESCRIPTION = "interfaces.txt"

# === PROMPT TEMPLATE ===
PROMPT_TEMPLATE = """
Tu es un expert en conception d’interfaces utilisateur. À partir du JSON suivant décrivant les étapes d’un processus métier, génère une description textuelle de chaque interface requise pour l’application.

Pour chaque interface, donne :
- Le nom de l'écran
- Le rôle utilisateur impliqué
- Les actions possibles (transitions)
- Le but de l'écran (ex: saisie des détails du patient)
- Les éléments de formulaire probables

Voici le JSON :
{resume_json}
"""

def run():
    if not os.path.exists(INPUT_JSON):
        print(f"❌ Fichier introuvable : {INPUT_JSON}")
        return

    with open(INPUT_JSON, "r", encoding="utf-8") as f:
        resume_json = f.read()

    prompt = PROMPT_TEMPLATE.format(resume_json=resume_json)

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()
        result_text = response.json().get("response", "")

        with open(OUTPUT_DESCRIPTION, "w", encoding="utf-8") as f:
            f.write(result_text)

        print(f"✅ Description des interfaces sauvegardée dans : {OUTPUT_DESCRIPTION}")

    except Exception as e:
        print(f"❌ Erreur lors de l'appel à Ollama : {e}")

if __name__ == "__main__":
    run()
