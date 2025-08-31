import os

# === Paramètre ===
DOSSIER_COMPOSANTS = "resultats_docs"  # Remplace par ton dossier réel
EXTENSION = ".txt"
FICHIER_SORTIE = "structure_des_donnees.txt"

# === Fusionner les fichiers texte ===
def fusionner_contenus(dossier, sortie):
    lignes_finales = ["## Structure des données et relations\n"]

    fichiers = sorted([
        f for f in os.listdir(dossier)
        if f.endswith(EXTENSION)
    ])

    for nom_fichier in fichiers:
        chemin = os.path.join(dossier, nom_fichier)
        with open(chemin, encoding="utf-8") as f:
            contenu = f.read().strip()

        titre = f"### {os.path.splitext(nom_fichier)[0]}"
        lignes_finales.append(titre)
        lignes_finales.append(contenu)
        lignes_finales.append("")  # Ligne vide entre les composants

    with open(sortie, "w", encoding="utf-8") as f:
        f.write("\n".join(lignes_finales))

    print(f"✅ Fichier '{sortie}' généré avec succès avec {len(fichiers)} composants.")

# === Exécution principale ===
if __name__ == "__main__":
    fusionner_contenus(DOSSIER_COMPOSANTS, FICHIER_SORTIE)
