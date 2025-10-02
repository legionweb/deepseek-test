import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import logging
import gc
import os

class DeepSeekHandler:
    def __init__(self, model_size=None):
        # 🔹 Utiliser la variable d'environnement définie dans wsgi.py
        self.model_size = model_size or os.environ.get('MODEL_SIZE', '1.3b')
        self.model_name = f"deepseek-ai/deepseek-coder-{self.model_size}-instruct"
        self.tokenizer = None
        self.model = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.logger = logging.getLogger(__name__)
        
        # Configuration pour environnement limité
        self.load_config = {
            "torch_dtype": torch.float16 if torch.cuda.is_available() else torch.float32,
            "low_cpu_mem_usage": True,
            "trust_remote_code": True
        }
        
        # Ajout de quantization si GPU limité
        if torch.cuda.is_available():
            try:
                self.load_config["load_in_8bit"] = True
            except:
                pass

        # 🔹 Log de la configuration au démarrage
        self.logger.info(f"🤖 Configuration DeepSeek Handler:")
        self.logger.info(f"   - Modèle: {self.model_name}")
        self.logger.info(f"   - Device: {self.device}")
        self.logger.info(f"   - Quantization 8-bit: {'Activée' if self.load_config.get('load_in_8bit') else 'Désactivée'}")
    
    def load_model(self):
        """Chargement paresseux du modèle"""
        if self.model is None:
            self.logger.info(f"Chargement du modèle {self.model_name}...")
            
            try:
                # Chargement du tokenizer
                self.tokenizer = AutoTokenizer.from_pretrained(
                    self.model_name,
                    trust_remote_code=True
                )
                
                # Chargement du modèle avec optimisations mémoire
                self.model = AutoModelForCausalLM.from_pretrained(
                    self.model_name,
                    **self.load_config
                )
                
                if self.device == "cuda":
                    self.model = self.model.cuda()
                
                self.logger.info("Modèle chargé avec succès")
                return True
                
            except Exception as e:
                self.logger.error(f"Erreur chargement modèle: {e}")
                return False
        
        return True
    
    def generate_web_component(self, description, max_tokens=1024):
        """Génération de composant web"""
        if not self.load_model():
            return {"error": "Impossible de charger le modèle"}
        
        # Template spécialisé pour composants web
        prompt = f"""Tu es un expert développeur web. Crée un composant HTML/CSS/JS complet et fonctionnel pour: {description}

Exigences:
- Code HTML5 autonome et valide
- CSS moderne intégré (Flexbox/Grid)
- JavaScript vanilla si nécessaire
- Design responsive et esthétique
- Pas de dépendances externes

Réponds UNIQUEMENT avec le code HTML complet dans ce format:
```html
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Composant</title>
    <style>
        /* CSS moderne ici */
    </style>
</head>
<body>
    <!-- HTML du composant ici -->
    <script>
        // JavaScript si nécessaire
    </script>
</body>
</html>
```

Description: {description}"""

        try:
            messages = [{"role": "user", "content": prompt}]
            inputs = self.tokenizer.apply_chat_template(
                messages,
                add_generation_prompt=True,
                return_tensors="pt"
            ).to(self.device)
            
            with torch.no_grad():
                outputs = self.model.generate(
                    inputs,
                    max_new_tokens=max_tokens,
                    temperature=0.1,
                    top_p=0.9,
                    do_sample=True,
                    eos_token_id=self.tokenizer.eos_token_id,
                    pad_token_id=self.tokenizer.eos_token_id
                )
            
            response = self.tokenizer.decode(
                outputs[0][len(inputs[0]):],
                skip_special_tokens=True
            )
            
            return {"success": True, "response": response}
            
        except Exception as e:
            self.logger.error(f"Erreur génération: {e}")
            return {"error": str(e)}
        
        finally:
            # Nettoyage mémoire
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
            gc.collect()
    
    def unload_model(self):
        """Libération mémoire"""
        if self.model is not None:
            del self.model
            del self.tokenizer
            self.model = None
            self.tokenizer = None
            
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
            gc.collect()
            
            self.logger.info("Modèle déchargé")

# Instance globale
deepseek_handler = DeepSeekHandler()