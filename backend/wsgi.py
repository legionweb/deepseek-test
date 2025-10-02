#!/usr/bin/env python
"""
🚀 WSGI Configuration pour DeepSeek Coder Web Generator
Configuration optimisée pour déploiement serveur en production
"""

import sys
import os
import logging

# 🔹 Configuration du logging pour la production
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# 🔹 Définir le chemin du projet de manière absolue
PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))
PARENT_PATH = os.path.dirname(PROJECT_PATH)

# 🔹 Ajouter les chemins nécessaires dans sys.path
sys.path.insert(0, PROJECT_PATH)
sys.path.insert(0, PARENT_PATH)

# 🔹 Variables d'environnement pour la configuration
os.environ.setdefault('FLASK_ENV', 'production')
os.environ.setdefault('FLASK_DEBUG', 'False')

# 🔹 Configuration du modèle selon les ressources serveur
# Ajustez MODEL_SIZE selon votre serveur : 1.3b, 6.7b
os.environ.setdefault('MODEL_SIZE', '6.7b')  # Par défaut : modèle léger

try:
    # 🔹 Import de l'application Flask
    from app import app as application
    
    # 🔹 Configuration supplémentaire pour la production
    application.config.update(
        SECRET_KEY=os.environ.get('SECRET_KEY', os.urandom(24)),
        MAX_CONTENT_LENGTH=16 * 1024 * 1024,  # 16MB max
        JSON_SORT_KEYS=False,
        JSONIFY_PRETTYPRINT_REGULAR=False
    )
    
    logging.info("✅ Application WSGI chargée avec succès")
    logging.info(f"📁 Chemin du projet: {PROJECT_PATH}")
    logging.info(f"🤖 Taille du modèle: {os.environ.get('MODEL_SIZE', '1.3b')}")
    
except ImportError as e:
    logging.error(f"❌ Erreur d'import de l'application: {e}")
    raise
except Exception as e:
    logging.error(f"❌ Erreur de configuration: {e}")
    raise

# 🔹 Point d'entrée pour tests locaux
if __name__ == "__main__":
    # Mode développement local uniquement
    port = int(os.environ.get('PORT', 5000))
    application.run(
        host='0.0.0.0',
        port=port,
        debug=os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    )