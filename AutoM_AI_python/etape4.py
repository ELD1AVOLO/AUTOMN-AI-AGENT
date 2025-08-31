# -*- coding: utf-8 -*-
"""
Created on Mon Jul 14 13:41:37 2025

@author: elmou
"""

# -*- coding: utf-8 -*-
"""
Script pour enrichir automatiquement les entités JSON avec une description générée
par un LLM local (ex: CodeLlama via Ollama), avec une fonction `run()` exécutable indépendamment.
"""

import os
import json
import requests

# === Configuration ===
DOSSIER_ENTREE = "entites_split"
MODEL_NAME = "codellama:7b"
LLM_ENDPOINT = "http://localhost:11434/api/generate"

# === Prompt Template ===
PROMPT_TEMPLATE = """
Tu es un assistant expert en documentation d'entités métier.

Voici une entité métier au format JSON, sans description ou avec une description trop simple :
{json_sans_description}

Ta mission est de rédiger un champ "description" plus riche, en respectant les règles suivantes :
- Une seule phrase complète.
- Expliquer le rôle de cette entité dans un système métier.
- Mentionner brièvement ses attributs et ses éventuelles relations.
- Style professionnel.

Retourne uniquement la description sans aucun commentaire :
{{
  "description": "..."
}}
"""

def appeler_llm_code_llama(prompt):
    data = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(LLM_ENDPOINT, json=data)
        response.raise_for_status()
        return response.json().get("response", None)
    except Exception as e:
        print(f"❌ Erreur lors de l'appel au LLM : {e}")
        return None

def traiter_fichier_json(fichier_path):
    try:
        with open(fichier_path, "r", encoding="utf-8") as f:
            entite = json.load(f)

        json_input = json.dumps(entite, indent=2, ensure_ascii=False)
        prompt = PROMPT_TEMPLATE.format(json_sans_description=json_input)

        response_llm = appeler_llm_code_llama(prompt)

        if not response_llm:
            print(f"❌ Aucune réponse du LLM pour {fichier_path}")
            return

        try:
            # Essai de parsing strict
            result_json = json.loads(response_llm)
        except json.JSONDecodeError:
            # Nettoyage et tentative de parsing doux
            response_llm = response_llm.strip().splitlines()[-1]
            try:
                result_json = json.loads(response_llm)
            except:
                print(f"❌ Réponse non JSON pour {fichier_path} : {response_llm}")
                return

        description = result_json.get("description", "").strip()

        if description:
            entite["description"] = description
            with open(fichier_path, "w", encoding="utf-8") as f:
                json.dump(entite, f, indent=2, ensure_ascii=False)
            print(f"✅ Description ajoutée pour {os.path.basename(fichier_path)}")
        else:
            print(f"⚠️ Description vide pour {fichier_path}")

    except Exception as err:
        print(f"❌ Erreur fichier {fichier_path} : {err}")

def run():
    if not os.path.isdir(DOSSIER_ENTREE):
        print(f"❌ Dossier introuvable : {DOSSIER_ENTREE}")
        return

    fichiers = [f for f in os.listdir(DOSSIER_ENTREE) if f.endswith(".json")]
    print(f"📂 {len(fichiers)} fichiers détectés dans '{DOSSIER_ENTREE}'")

    for fichier in fichiers:
        chemin = os.path.join(DOSSIER_ENTREE, fichier)
        print(f"\n🧠 Traitement de : {fichier}")
        traiter_fichier_json(chemin)

    print("\n✅ Traitement automatique terminé.")

# Si tu veux exécuter le script seul
if __name__ == "__main__":
    run()
