import requests
import json

# 📥 Lire le XML depuis un fichier
with open("input.txt", "r", encoding="utf-8") as file:
    xml_input = file.read()

# 💬 Prompt pour le modèle
PROMPT_XML = f"""
Tu es un assistant expert en analyse de workflows XML (JBPM).
Voici un fichier XML d’un processus métier de remboursement santé.

Analyse-le et donne un résumé JSON avec :
- Les étapes (type : tâche humaine ou système, nom)
- Les transitions (source → destination)
- Les rôles ou sources d’assignation (startUser, personnePhysique, etc.)
- L’ordre logique des étapes

Voici le XML :
{xml_input}

Réponds uniquement avec un JSON structuré sans aucun text autour ni charachtere comme (```json) .
"""

# ⚙️ Paramètres API Ollama
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "deepseek-coder-v2:latest"  # 🔁 Change le nom selon ton modèle local installé

# 📡 Envoi du prompt à Ollama
response = requests.post(OLLAMA_URL, json={
    "model": MODEL,
    "prompt": PROMPT_XML,
    "stream": False
})

# 📤 Sauvegarder la réponse dans un fichier JSON
if response.status_code == 200:
    result_text = response.json()["response"]

    try:
        # Tentative de validation JSON
        result_json = json.loads(result_text)

        with open("output.json", "w", encoding="utf-8") as out_file:
            json.dump(result_json, out_file, indent=2, ensure_ascii=False)

        print("✅ Résultat JSON enregistré dans output.json")

    except json.JSONDecodeError:
        # Si le modèle a renvoyé un texte non strictement JSON
        with open("output_raw.txt", "w", encoding="utf-8") as raw_file:
            raw_file.write(result_text)

        print("⚠️ Réponse non valide JSON. Résultat brut enregistré dans output_raw.txt")
else:
    print("❌ Erreur lors de l’appel à Ollama :", response.status_code)
    print(response.text)
