# -*- coding: utf-8 -*-
"""
Created on Wed Jul  2 11:39:37 2025

@author: elmou
"""

import os
import json

# === Fichiers d'entrée/sortie ===
FICHIER_SOURCE = "resume_composants.json"
DOSSIER_SORTIE = "entites_split"

# === Chargement des entités ===
with open(FICHIER_SOURCE, "r", encoding="utf-8") as f:
    data = json.load(f)

entites = data.get("entites", [])

# === Création du dossier s'il n'existe pas ===
os.makedirs(DOSSIER_SORTIE, exist_ok=True)

# === Sauvegarde de chaque entité dans un fichier séparé ===
for entite in entites:
    code = entite.get("code", "inconnu")
    nom_fichier = f"{code}.json"
    chemin_fichier = os.path.join(DOSSIER_SORTIE, nom_fichier)

    with open(chemin_fichier, "w", encoding="utf-8") as f_out:
        json.dump(entite, f_out, indent=2, ensure_ascii=False)

    print(f"✅ Fichier créé : {chemin_fichier}")

print(f"\n📁 {len(entites)} entités exportées dans le dossier : {DOSSIER_SORTIE}")
