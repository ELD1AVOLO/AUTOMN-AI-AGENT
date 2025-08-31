import requests
import json

# 📥 Lire la description de l’interface depuis un fichier JSON
with open("cahier_des_charges.json", "r", encoding="utf-8") as file:
    interface_data = file.read()

# 💬 Prompt structuré pour la génération des composants UI
PROMPT_UI = f"""
Tu es un expert en conception d’interfaces utilisateur métier.

Voici la description d’une interface à créer :
{interface_data}

Génère les éléments suivants :
- composants UI (ex : TextField, Button, Checkbox, Select)
- leur label
- type de champ (texte, nombre, pièce jointe, date, etc.)
- disposition (horizontal / vertical)
- règles de validation associées

Réponds uniquement avec un JSON structuré sans aucun texte autour ni caractères comme (```json).
"""

# ⚙️ Paramètres API Ollama
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3"  # 💡 Change selon le modèle installé

# 📡 Envoi du prompt à Ollama
response = requests.post(OLLAMA_URL, json={
    "model": MODEL,
    "prompt": PROMPT_UI,
    "stream": False
})

# 📤 Sauvegarder la réponse dans un fichier JSON
if response.status_code == 200:
    result_text = response.json()["response"]

    try:
        # Tentative de validation JSON
        result_json = json.loads(result_text)

        with open("etape4_output.json", "w", encoding="utf-8") as out_file:
            json.dump(result_json, out_file, indent=2, ensure_ascii=False)

        print("✅ Résultat JSON enregistré dans etape4_output.json")

    except json.JSONDecodeError:
        # Si le modèle a renvoyé un texte non strictement JSON
        with open("etape4_output_raw.txt", "w", encoding="utf-8") as raw_file:
            raw_file.write(result_text)

        print("⚠️ Réponse non valide JSON. Résultat brut enregistré dans etape4_output_raw.txt")
else:
    print("❌ Erreur lors de l’appel à Ollama :", response.status_code)
    print(response.text)
