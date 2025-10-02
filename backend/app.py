from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
import logging
import sys
import os
from model_handler import deepseek_handler
from code_processor import CodeProcessor

# Configuration logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Configuration
app.config['SECRET_KEY'] = os.urandom(24)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

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


processor = CodeProcessor()

@app.route('/')
def index():
    """Page principale"""
    return render_template('index.html')

@app.route('/api/health')
def health():
    """Health check"""
    return jsonify({"status": "healthy", "model_loaded": deepseek_handler.model is not None})

@app.route('/api/generate', methods=['POST'])
def generate_code():
    """Endpoint de génération de code"""
    try:
        data = request.get_json()
        
        if not data or 'description' not in data:
            return jsonify({"error": "Description requise"}), 400
        
        description = data['description'].strip()
        
        if not description:
            return jsonify({"error": "Description vide"}), 400
        
        # Génération avec DeepSeek
        logger.warning(f"Génération pour: {description[:100]}...")
        result = deepseek_handler.generate_web_component(description)
        
        if "error" in result:
            return jsonify({"error": result["error"]}), 500
        
        # Extraction du code HTML
        html_code = processor.extract_html_code(result["response"])
        
        if not html_code:
            return jsonify({
                "error": "Code HTML non trouvé dans la réponse",
                "raw_response": result["response"][:500]
            }), 500
        
        # Validation
        validation = processor.validate_html(html_code)
        
        # Nettoyage
        clean_code = processor.sanitize_html(html_code)
        
        return jsonify({
            "success": True,
            "code": clean_code,
            "validation": validation,
            "raw_response": result["response"][:2000] + "..." if len(result["response"]) > 200 else result["response"]
        })
        
    except Exception as e:
        logger.error(f"Erreur génération: {e}")
        return jsonify({"error": "Erreur serveur interne"}), 500

@app.route('/api/chat', methods=['POST'])
def chat():
    """Endpoint de chat (alias pour generate)"""
    data = request.get_json()
    if data and 'message' in data:
        data['description'] = data['message']
    return generate_code()

@app.errorhandler(413)
def request_entity_too_large(error):
    return jsonify({"error": "Fichier trop volumineux"}), 413

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Erreur 500: {error}")
    return jsonify({"error": "Erreur serveur interne"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)