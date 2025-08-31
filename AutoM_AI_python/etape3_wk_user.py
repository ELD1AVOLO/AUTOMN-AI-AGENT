import requests
import json

# Fichier contenant le résumé XML
with open("output.json", "r", encoding="utf-8") as f:
    resume_xml = f.read()

# Fichier contenant le résumé utilisateur
with open("etape2_output.json", "r", encoding="utf-8") as f:
    resume_user = f.read()

PROMPT_CAHIER_DES_CHARGES = f"""
Voici deux sources d’information :

1. Résumé d’un processus XML :
{resume_xml}

2. Résumé d’un besoin utilisateur :
{resume_user}

En te basant sur ces deux sources, génère un cahier des charges des interfaces à implémenter, en listant :
- nom de l’interface
- utilisateur concerné
- champs à remplir
- actions disponibles
- transitions logiques

Réponds en JSON comme ceci :
[
  {{
    "interface": "NomInterface",
    "utilisateur": "assuré",
    "champs": ["..."],
    "actions": ["..."],
    "prochaine_etape": "..."
  }}
]
"""

# Requête à Ollama (serveur local)
response = requests.post(
    "http://localhost:11434/api/generate",
    json={
        "model": "llama3",  # ou hermes-pro, selon ton setup
        "prompt": PROMPT_CAHIER_DES_CHARGES,
        "stream": False
    }
)

# Extraire le résultat
result = response.json()["response"]

# Sauvegarde dans un fichier
with open("cahier_des_charges.json", "w", encoding="utf-8") as f:
    f.write(result)

print("✅ Cahier des charges généré et sauvegardé dans 'cahier_des_charges.json'")
