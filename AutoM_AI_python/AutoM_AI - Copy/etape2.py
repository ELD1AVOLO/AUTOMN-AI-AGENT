# -*- coding: utf-8 -*-
"""
Created on Fri Jul  4 15:08:48 2025

@author: elmou
"""

import json
import time
import requests

# === Configuration ===
FICHIER_ENTREE = "combined_result.json"
FICHIER_SORTIE = "resume_composants.json"
FICHIER_INDESIRABLES = "resume_indesirables.json"
DEEPSEEK_API = "http://localhost:11434/api/generate"
MODELE = "prompt/hermes-2-pro:latest"
MAX_RETRY = 3  # Nombre de tentatives en cas d’échec

# === Prompt Template ===
PROMPT_TEMPLATE = """
Tu es un assistant expert en modélisation d'entités métier à partir de composants XML.

Transforme chaque composant XML en un seul objet JSON métier avec la structure suivante :
- "code", "type"
- "attributs" : nom, type, obligatoire
- "relations" : nom, code, type, cardinalité, attributs
- "description"

Règles :
- Pas d’explication.
- Format : objet JSON unique.
- Respecte la structure exacte même si certaines informations sont manquantes.

Exemple 1 :
XML :
<Composant-Definition code="Produit">
  <type>TYPE_BEAN_COMP</type>
  <detailComposants>
    <Attribut code="nom">
      <type>TYPE_ATTR_STR</type>
      <mandatory>true</mandatory>
    </Attribut>
    <Attribut code="prix">
      <type>TYPE_ATTR_DOUBLE</type>
      <mandatory>false</mandatory>
    </Attribut>
  </detailComposants>
</Composant-Definition>

JSON attendu :
{{
  "code": "Produit",
  "type": "TYPE_BEAN_COMP",
  "attributs": [
    {{"nom": "nom", "type": "TYPE_ATTR_STR", "obligatoire": true}},
    {{"nom": "prix", "type": "TYPE_ATTR_DOUBLE", "obligatoire": false}}
  ],
  "relations": [],
  "description": "Entité métier représentant Produit"
}}

Composant à traiter :
{xml_content}
"""

# === Appel du modèle local Hermes ===
def call_hermes(prompt):
    headers = {"Content-Type": "application/json"}
    data = {
        "model": MODELE,
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(DEEPSEEK_API, headers=headers, json=data)
        response.raise_for_status()
        return response.json()["response"]
    except Exception as e:
        print(f"Erreur LLM: {e}")
        return None

# === Correction du JSON brut ===
def corriger_entite(json_data):
    for relation in json_data.get("relations", []):
        if relation.get("cardinalité") == "TYPE_RELATION_SIMPLE":
            relation["cardinalité"] = "1:1"
        elif relation.get("cardinalité") == "TYPE_RELATION_MULTIPLE":
            relation["cardinalité"] = "1:N"
        elif "cardinalité" not in relation:
            relation["cardinalité"] = "1:1"

    if "description" not in json_data or not json_data["description"].strip():
        json_data["description"] = f"Entité métier représentant {json_data['code']}"

    return json_data

# === Traitement principal avec retries ===
def traiter_composants_un_par_un():
    with open(FICHIER_ENTREE, "r", encoding="utf-8") as f:
        data = json.load(f)

    resumes_valides = []
    resumes_invalides = []

    for file in data["files"]:
        nom = file["file_name"]
        content = file["content"]
        prompt = PROMPT_TEMPLATE.format(xml_content=content)

        print(f"🧠 Traitement du composant : {nom}")
        tentative = 0
        succes = False

        while tentative < MAX_RETRY and not succes:
            sortie = call_hermes(prompt)
            tentative += 1

            if sortie:
                try:
                    json_data = json.loads(sortie)
                    json_data = corriger_entite(json_data)
                    resumes_valides.append(json_data)
                    print(f"✅ Résumé généré pour : {nom} (tentative {tentative})")
                    succes = True
                except json.JSONDecodeError:
                    print(f"❌ JSON invalide reçu (tentative {tentative})")
                    if tentative == MAX_RETRY:
                        resumes_invalides.append({
                            "file_name": nom,
                            "error": "JSONDecodeError",
                            "raw_output": sortie
                        })
            else:
                print(f"❌ Aucune réponse reçue (tentative {tentative})")
                if tentative == MAX_RETRY:
                    resumes_invalides.append({
                        "file_name": nom,
                        "error": "NoResponse",
                        "raw_output": None
                    })

            time.sleep(1)

    # Sauvegarde des entités valides
    with open(FICHIER_SORTIE, "w", encoding="utf-8") as f_out:
        json.dump({"entites": resumes_valides}, f_out, indent=2, ensure_ascii=False)

    # Sauvegarde des entités indésirables
    with open(FICHIER_INDESIRABLES, "w", encoding="utf-8") as f_err:
        json.dump({"indesirables": resumes_invalides}, f_err, indent=2, ensure_ascii=False)

    print(f"\n✅ Résumés valides enregistrés dans {FICHIER_SORTIE}")
    print(f"⚠️ Résumés indésirables enregistrés dans {FICHIER_INDESIRABLES}")

if __name__ == "__main__":
    traiter_composants_un_par_un()
