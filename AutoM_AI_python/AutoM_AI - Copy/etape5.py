import os
import json
import requests

# === CONFIGURATION ===
REPERTOIRE_ENTITES = "entites_split"
REPERTOIRE_SORTIE = "resultats_docs"
MODELE = "prompt/hermes-2-pro:latest"
OLLAMA_URL = "http://localhost:11434/api/generate"


os.makedirs(REPERTOIRE_SORTIE, exist_ok=True)


PROMPT_TEMPLATE = """
Tu es un assistant expert en modélisation métier.

Tu vas recevoir un composant d'entité métier au format JSON. Il contient une liste d'attributs techniques sans description ni regroupement logique.

Ta mission est de :
1. Lire tous les attributs du JSON.
2. Repérer le nom du composant à partir du champ "code".
3. Regrouper les attributs par blocs fonctionnels logiques, comme :
   - Informations de base (identifiant, numéro de dossier…)
   - Données patient
   - Données médicales
   - Données financières
   - Suivi et statut
   - Documents associés
4. Pour chaque attribut, écris :
   - son nom (type métier entre parenthèses : string, date, double, DP, PP…)
   - une description claire et concise de son rôle

Présente le résultat avec ce format :

Composant : <Nom du composant> (<description synthétique déduite si possible)

[Bloc fonctionnel] :

nomAttribut (type) : description
...

Ne donne que le résultat final. N'explique pas tes choix.

=== DONNÉES JSON ===
{json_data}
"""


for nom_fichier in os.listdir(REPERTOIRE_ENTITES):
    if nom_fichier.endswith(".json"):
        chemin_fichier = os.path.join(REPERTOIRE_ENTITES, nom_fichier)

        try:
            with open(chemin_fichier, "r", encoding="utf-8") as f:
                contenu_json = json.load(f)
        except json.JSONDecodeError as e:
            print(f"❌ Erreur de décodage JSON dans {nom_fichier} : {e}")
            continue  # passe au fichier suivant

        prompt = PROMPT_TEMPLATE.replace(
            "{json_data}", json.dumps(contenu_json, indent=2, ensure_ascii=False)
        )

        print(f"🔄 Traitement de : {nom_fichier}")
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODELE,
                "prompt": prompt,
                "stream": False
            }
        )

        reponse_llm = response.json().get("response", "").strip()

        nom_fichier_sortie = os.path.splitext(nom_fichier)[0] + "_doc.txt"
        chemin_sortie = os.path.join(REPERTOIRE_SORTIE, nom_fichier_sortie)

        with open(chemin_sortie, "w", encoding="utf-8") as out:
            out.write(reponse_llm)

        print(f"✅ Sauvegardé : {chemin_sortie}")
