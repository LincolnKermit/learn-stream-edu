import os
import zipfile
from datetime import datetime

def create_backup_zip(source_dir_or_files, backup_folder='backups'):
    """
    Crée un fichier ZIP à partir des fichiers ou dossiers donnés, et l'enregistre dans le dossier 'backups'.
    
    :param source_dir_or_files: Liste de fichiers ou un dossier à compresser
    :param backup_folder: Répertoire où le fichier ZIP sera exporté (par défaut 'backups')
    :return: Le chemin complet vers le fichier ZIP créé
    """
    # Vérifie si le répertoire backups existe, sinon le crée
    if not os.path.exists(backup_folder):
        os.makedirs(backup_folder)
    
    # Génère un nom pour le fichier ZIP basé sur la date et l'heure
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_filename = os.path.join(backup_folder, f"backup_{timestamp}.zip")
    
    # Création du fichier ZIP
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        if os.path.isdir(source_dir_or_files):  # Si c'est un dossier
            for root, dirs, files in os.walk(source_dir_or_files):
                for file in files:
                    file_path = os.path.join(root, file)
                    # Ajoute les fichiers en conservant l'arborescence relative
                    zipf.write(file_path, os.path.relpath(file_path, source_dir_or_files))
        elif isinstance(source_dir_or_files, list):  # Si c'est une liste de fichiers
            for file in source_dir_or_files:
                if os.path.exists(file):
                    zipf.write(file, os.path.basename(file))
    
    print(f"Backup créé : {zip_filename}")
    return zip_filename
