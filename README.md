# 🚀 DeepSeek Coder Web Generator

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.3.3-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![AI](https://img.shields.io/badge/AI-DeepSeek--Coder-purple.svg)](https://github.com/deepseek-ai/DeepSeek-Coder)

> Générateur intelligent de composants web utilisant DeepSeek-Coder avec interface de chat et preview en temps réel

## ✨ Fonctionnalités

- 🤖 **IA Avancée** : Génération de code HTML/CSS/JS avec DeepSeek-Coder
- 💬 **Interface Chat** : Interface conversationnelle intuitive
- 👀 **Preview Temps Réel** : Visualisation instantanée des composants générés
- 📱 **Design Responsive** : Compatible mobile et desktop
- 📄 **Gestion du Code** : Visualisation, copie et téléchargement du code source
- ⚡ **Optimisé Serveur** : Configuration pour déploiement en ligne
- 🔒 **Sécurisé** : Sandbox iframe pour l'exécution sécurisée du code

## 🎯 Démo

![Demo Screenshot](https://via.placeholder.com/800x400/667eea/ffffff?text=DeepSeek+Coder+Interface)

### Exemples de génération :

- **Carte de profil** : `"Créer une carte de profil avec photo et boutons sociaux"`
- **Formulaire de contact** : `"Faire un formulaire de contact moderne avec validation"`
- **Slider d'images** : `"Générer un slider d'images responsive"`
- **Menu hamburger** : `"Créer un menu hamburger animé"`

## 🛠️ Installation

### Prérequis

- Python 3.8+
- pip
- 4GB+ RAM (8GB+ recommandé)
- GPU CUDA (optionnel, améliore les performances)

### Installation rapide

```bash
# Cloner le repository
git clone https://github.com/legionweb/deepseek-test.git
cd deepseek-test

# Installer les dépendances
cd backend
pip install -r requirements.txt

# Lancer l'application
python app.py
```

L'application sera accessible sur **http://localhost:5000**

## 🚀 Déploiement en Production

### Serveur WSGI (Recommandé)

```bash
# Production standard
gunicorn --bind 0.0.0.0:8000 --workers 1 --timeout 300 wsgi:application

# Serveur avec ressources limitées
gunicorn --bind 0.0.0.0:8000 --workers 1 --timeout 600 --max-requests 100 wsgi:application

# Avec logs détaillés
gunicorn --bind 0.0.0.0:8000 --workers 1 --timeout 300 --access-logfile - --error-logfile - wsgi:application
```

### Variables d'Environnement

```bash
export FLASK_ENV=production
export FLASK_DEBUG=False
export MODEL_SIZE=1.3b  # Pour moins de 8GB RAM
```

### Déploiement Cloud

#### Heroku
```bash
# Procfile
web: gunicorn --bind 0.0.0.0:$PORT --workers 1 --timeout 600 wsgi:application
```

#### Docker
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY backend/ .
RUN pip install -r requirements.txt
EXPOSE 8000
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "wsgi:application"]
```

## 📁 Structure du Projet

```
deepseek-test/
├── README.md
└── backend/
    ├── app.py                 # 🎯 Application Flask principale
    ├── model_handler.py       # 🤖 Gestion du modèle DeepSeek
    ├── code_processor.py      # 🔧 Traitement et validation du code
    ├── wsgi.py               # 🌐 Point d'entrée WSGI
    ├── requirements.txt      # 📦 Dépendances Python
    ├── templates/
    │   └── index.html        # 🎨 Interface web principale
    └── static/
        ├── style.css         # 💄 Styles et design
        └── script.js         # ⚡ JavaScript frontend
```

## 🔧 Configuration Avancée

### Modèles Disponibles

```python
# Dans model_handler.py, ajustez selon vos ressources :

# Pour serveurs puissants (16GB+ RAM)
deepseek_handler = DeepSeekHandler(model_size="6.7b")

# Pour serveurs moyens (8GB RAM)
deepseek_handler = DeepSeekHandler(model_size="1.3b")

# Configuration GPU optimisée
self.load_config.update({
    "load_in_8bit": True,
    "device_map": "auto",
    "torch_dtype": torch.float16
})
```

### Optimisations Mémoire

```python
# Chargement paresseux du modèle
# Nettoyage automatique après génération
# Quantization 8-bit pour réduire l'usage mémoire
# Gestion des timeouts pour éviter les blocages
```

## 🌐 API Reference

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Interface principale |
| `GET` | `/api/health` | Status de l'application |
| `POST` | `/api/generate` | Génération de code |
| `POST` | `/api/chat` | Alias pour generate |

### Exemple d'Usage API

```javascript
// Génération via API
const response = await fetch('/api/generate', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        description: "Créer une carte de produit e-commerce"
    })
});

const data = await response.json();
console.log(data.code); // Code HTML généré
```

## 🔐 Sécurité

- **Sandbox iframe** : Exécution sécurisée du code généré
- **Validation HTML** : Vérification de la structure du code
- **CORS configuré** : Protection contre les requêtes malveillantes
- **Timeouts** : Protection contre les requêtes infinies

## 📊 Performance

- **Première génération** : 30-60s (téléchargement du modèle)
- **Générations suivantes** : 5-15s selon la complexité
- **RAM utilisée** : 2-8GB selon le modèle
- **GPU** : Accélération optionnelle mais recommandée

## 🐛 Dépannage

### Erreurs Communes

**Erreur de mémoire**
```bash
# Utiliser un modèle plus petit
MODEL_SIZE=1.3b python app.py
```

**Timeout de génération**
```bash
# Augmenter le timeout
gunicorn --timeout 900 wsgi:application
```

**Erreur CUDA**
```bash
# Forcer CPU
export CUDA_VISIBLE_DEVICES=""
```

## 🤝 Contributing

1. Fork le projet
2. Créer une branche feature (`git checkout -b feature/AmazingFeature`)
3. Commit vos changements (`git commit -m 'Add some AmazingFeature'`)
4. Push sur la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## 📄 License

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 🙏 Remerciements

- [DeepSeek-AI](https://github.com/deepseek-ai) pour le modèle DeepSeek-Coder
- [Hugging Face](https://huggingface.co/) pour l'infrastructure Transformers
- [Flask](https://flask.palletsprojects.com/) pour le framework web

## 📞 Support

- 🐛 **Issues** : [GitHub Issues](https://github.com/legionweb/deepseek-test/issues)
- 💬 **Discussions** : [GitHub Discussions](https://github.com/legionweb/deepseek-test/discussions)
- 📧 **Email** : support@legionweb.com

---

⭐ **Star ce projet si il vous a été utile !**