# -*- coding: utf-8 -*-
"""
Created on Fri Jul 18 10:33:19 2025
@author: elmou
"""

import requests
import os

# === CONFIGURATION ===
MODEL_NAME = "hermes-2-pro"  # CORRIGÉ pour fonctionner avec l'API Ollama
OLLAMA_URL = "http://localhost:11434/api/generate"
XML_PATH = "workflow.txt"  # Ton fichier texte contenant le XML JBPM

# === PROMPT FIXE ===
PROMPT_TEMPLATE = """
Tu es un expert en modélisation d'application métier. Analyse le XML JBPM suivant et génère un résumé JSON de l'application.

Pour chaque écran (state ou task-node), donne les informations suivantes :
- nom
- type (state ou task)
- transitions sortantes (nom, destination)
- utilisateur ou groupe affecté (si présent)
- description (si présente)
- rôle fonctionnel (ex: saisie, validation, etc.)

N’ajoute pas de commentaire, retourne uniquement le JSON.

Voici le XML :
{xml_content}
"""

def run():
    if not os.path.exists(XML_PATH):
        print(f"❌ Fichier XML introuvable : {XML_PATH}")
        return

    with open(XML_PATH, "r", encoding="utf-8") as f:
        xml_content = f.read()

    prompt = PROMPT_TEMPLATE.format(xml_content=xml_content)

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()
        result = response.json().get("response", "")
        print("🟢 Résultat JSON :\n")
        print(result)
    except Exception as e:
        print(f"❌ Erreur lors de l'appel au modèle : {e}")

if __name__ == "__main__":
    run()
