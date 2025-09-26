import re
from typing import Optional

class CodeProcessor:
    
    @staticmethod
    def extract_html_code(text: str) -> Optional[str]:
        """Extrait le code HTML de la réponse"""
        # Pattern pour bloc HTML
        patterns = [
            r'```html\n(.*?)\n```',
            r'```\n(<!DOCTYPE html.*?)\n```',
            r'(<!DOCTYPE html.*?</html>)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        return None
    
    @staticmethod
    def validate_html(html_code: str) -> dict:
        """Validation basique du HTML"""
        if not html_code:
            return {"valid": False, "error": "Code vide"}
        
        required_tags = ['<!DOCTYPE html>', '<html', '</html>', '<head>', '</head>', '<body>', '</body>']
        missing_tags = []
        
        html_lower = html_code.lower()
        for tag in required_tags:
            if tag.lower() not in html_lower:
                missing_tags.append(tag)
        
        return {
            "valid": len(missing_tags) == 0,
            "missing_tags": missing_tags,
            "length": len(html_code)
        }
    
    @staticmethod
    def sanitize_html(html_code: str) -> str:
        """Nettoyage basique du HTML"""
        # Suppression de balises potentiellement dangereuses (pour cette version on garde tout)
        return html_code.strip()