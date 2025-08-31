import requests

# === Configuration ===
OLLAMA_ENDPOINT = "http://localhost:11434/api/generate"
MODEL_NAME = "codellama:7b"  # Change selon ton modèle local
FICHIER_DESCRIPTION = "resultat_synthese.txt"  # Fichier d'entrée
FICHIER_SORTIE = "nom.txt"  # Fichier de sortie

# === Lecture de la description du projet ===
with open(FICHIER_DESCRIPTION, 'r', encoding='utf-8') as f:
    description = f.read().strip()

# === Prompt injecté ===
prompt_template = f"""
Tu es un assistant expert chargé de nommer des prompts de génération d'interfaces utilisateur (UI) à partir de descriptions fonctionnelles.

Je vais te fournir un paragraphe décrivant un système ou un module logiciel (par exemple : un workflow XML, une fonctionnalité métier, ou un composant d'interface).

Ta tâche est de générer un **titre clair, professionnel et concis** pour ce prompt, qui servira à guider un modèle LLM dans la génération de maquettes UI. Ce titre doit décrire l’objectif principal du système, le type d’interface, et le contexte fonctionnel.

Le format attendu est :
**Prompt pour génération d'interface utilisateur – [Nom du système ou de la fonctionnalité]**

Voici la description à analyser :
{description}

Donne uniquement le nom du prompt final, sans explication.
"""

# === Requête à Ollama ===
response = requests.post(OLLAMA_ENDPOINT, json={
    "model": MODEL_NAME,
    "prompt": prompt_template,
    "stream": False
})

# === Traitement du résultat ===
if response.status_code == 200:
    resultat = response.json()["response"].strip()

    # Affichage
    print("\n🟩 Nom du prompt généré :\n", resultat)

    # Sauvegarde dans un fichier
    with open(FICHIER_SORTIE, 'w', encoding='utf-8') as f:
        f.write(resultat)
        print(f"\n📝 Résultat sauvegardé dans : {FICHIER_SORTIE}")
else:
    print("❌ Erreur lors de la génération :", response.status_code)
    print(response.text)
