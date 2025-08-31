# -*- coding: utf-8 -*-
"""
Created on Wed Jul 16 16:11:05 2025

@author: elmou
"""

# === Fichiers sources ===
fichier_nom = "nom.txt"
fichier_contexte = "resultat_synthese.txt"
fichier_structure = "structure_des_donnees.txt"
fichier_sortie = "prompt_final.txt"

# === Lecture des fichiers ===
def lire_fichier(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read().strip()
    except FileNotFoundError:
        return f"[Fichier introuvable : {path}]"

titre = lire_fichier(fichier_nom)
contexte = lire_fichier(fichier_contexte)
structure = lire_fichier(fichier_structure)

# === Construction du prompt structuré ===
texte_final = f"""{titre}

Context métier :
{contexte}

Structure des données :
{structure}
"""

# === Sauvegarde dans le fichier final ===
with open(fichier_sortie, 'w', encoding='utf-8') as f:
    f.write(texte_final)

print(f"✅ Prompt structuré sauvegardé dans : {fichier_sortie}")
