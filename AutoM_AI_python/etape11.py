# -*- coding: utf-8 -*-
"""
Created on Fri Jul 18 11:40:50 2025

@author: elmou
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Jul 18 11:00:00 2025
@author: elmou
"""

import requests
import os

# === CONFIGURATION ===
MODEL_NAME = "codellama:latest"
OLLAMA_URL = "http://localhost:11434/api/generate"
INPUT_FILE = "interfaces.txt"
OUTPUT_FILE = "ui_mockups.txt"

# === PROMPT TEMPLATE ===
PROMPT_TEMPLATE = """
Tu es un expert en UX/UI design. À partir de la description fonctionnelle suivante, génère une **description de maquette UI** en texte clair, à l’attention d’un designer.

Sois très structuré :
- Donne le titre de l’écran
- Explique la disposition (par sections : en-tête, formulaire, actions)
- Liste les composants visibles à l’utilisateur (champs, boutons, titres)
- Donne l’objectif fonctionnel de l’écran

Voici la description fonctionnelle de l’écran :
{description}
"""

def run():
    if not os.path.exists(INPUT_FILE):
        print(f"❌ Fichier introuvable : {INPUT_FILE}")
        return

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        full_content = f.read()

    # Tu peux adapter cette séparation si tes écrans sont séparés par autre chose
    descriptions = [desc.strip() for desc in full_content.split("\n\n") if desc.strip()]

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f_out:
        for idx, description in enumerate(descriptions):
            prompt = PROMPT_TEMPLATE.format(description=description)

            payload = {
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": False
            }

            try:
                response = requests.post(OLLAMA_URL, json=payload)
                response.raise_for_status()
                result_text = response.json().get("response", "")
                f_out.write(f"🖼️ UI MAQUETTE POUR ÉCRAN {idx + 1} :\n")
                f_out.write(result_text.strip())
                f_out.write("\n\n" + "="*60 + "\n\n")

            except Exception as e:
                print(f"❌ Erreur pour l'écran {idx+1} : {e}")
                f_out.write(f"Erreur de génération pour écran {idx+1} : {e}\n\n")

    print(f"✅ Maquettes UI générées dans : {OUTPUT_FILE}")

if __name__ == "__main__":
    run()
