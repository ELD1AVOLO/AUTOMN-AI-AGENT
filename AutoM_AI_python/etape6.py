import os
import json
import requests

# === CONFIGURATION ===
REPERTOIRE_JSON = "./entites_split"         # dossier contenant les fichiers JSON
FICHIER_PROMPT_INITIAL = "prompt_initial.txt" # fichier contenant le prompt initial (description de l'app)
FICHIER_RESULTAT = "resultat_synthese.txt"    
MODELE_LLM = "prompt/hermes-2-pro:latest"       
OLLAMA_API_URL = "http://localhost:11434/api/generate"

def lire_prompt_initial(fichier):
    with open(fichier, "r", encoding="utf-8") as f:
        return f.read().strip()

def extraire_descriptions_json(repertoire):
    descriptions = []
    for fichier in os.listdir(repertoire):
        if fichier.endswith(".json"):
            chemin = os.path.join(repertoire, fichier)
            try:
                with open(chemin, "r", encoding="utf-8") as jf:
                    data = json.load(jf)
                    desc = data.get("description")
                    if desc:
                        descriptions.append(desc.strip())
            except Exception as e:
                print(f"Erreur lecture JSON {fichier}: {e}")
    return descriptions

def construire_prompt_complet(prompt_initial, descriptions):
    # Met en forme les descriptions pour le prompt
    descriptions_formatees = "\n- ".join(descriptions)
    prompt = f"""
{prompt_initial}

Voici plusieurs descriptions d'entités métier extraites du système :
- {descriptions_formatees}

Ta mission est de rédiger un paragraphe clair et synthétique expliquant comment ces entités fonctionnent ensemble dans cette application métier, en mettant en avant leur rôle dans la gestion des sinistres santé, la traçabilité, la validation et le traitement des remboursements et soins associés.

Réponds uniquement avec le paragraphe de synthèse, sans explications supplémentaires.
"""
    return prompt

def appeler_api_ollama(prompt, modele):
    try:
        print(f"🔄 Envoi du prompt au modèle {modele}...")
        response = requests.post(
            OLLAMA_API_URL,
            json={
                "model": modele,
                "prompt": prompt,
                "stream": False
            }
        )
        response.raise_for_status()
        resultat = response.json().get("response", "").strip()
        return resultat
    except Exception as e:
        print(f"Erreur appel API Ollama : {e}")
        return ""

def sauvegarder_resultat(fichier, contenu):
    with open(fichier, "w", encoding="utf-8") as f:
        f.write(contenu)

def main():
    print("Lecture du prompt initial...")
    prompt_initial = lire_prompt_initial(FICHIER_PROMPT_INITIAL)
    
    print(f"Extraction des descriptions depuis {REPERTOIRE_JSON}...")
    descriptions = extraire_descriptions_json(REPERTOIRE_JSON)
    
    if not descriptions:
        print("Aucune description trouvée, arrêt.")
        return
    
    print(f"Nombre de descriptions trouvées : {len(descriptions)}")
    print("Construction du prompt complet...")
    prompt_complet = construire_prompt_complet(prompt_initial, descriptions)
    
    resultat = appeler_api_ollama(prompt_complet, MODELE_LLM)
    
    if resultat:
        print(f"✅ Sauvegarde du résultat dans {FICHIER_RESULTAT}...")
        sauvegarder_resultat(FICHIER_RESULTAT, resultat)
        print("Terminé avec succès.")
    else:
        print("❌ Aucun résultat généré.")

if __name__ == "__main__":
    main()