class ChatBot {
    constructor() {
        this.messageInput = document.getElementById('messageInput');
        this.sendButton = document.getElementById('sendButton');
        this.chatMessages = document.getElementById('chatMessages');
        this.previewFrame = document.getElementById('previewFrame');
        this.previewPlaceholder = document.getElementById('previewPlaceholder');
        this.loadingIndicator = document.getElementById('loadingIndicator');
        this.fullscreenBtn = document.getElementById('fullscreenBtn');
        this.refreshBtn = document.getElementById('refreshBtn');
        this.codeModal = document.getElementById('codeModal');
        this.codeContent = document.getElementById('codeContent');
        this.downloadBtn = document.getElementById('downloadBtn');
        
        this.currentCode = '';
        this.isGenerating = false;
        
        this.init();
    }
    
    init() {
        this.sendButton.addEventListener('click', () => this.sendMessage());
        this.messageInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });
        
        this.fullscreenBtn.addEventListener('click', () => this.toggleFullscreen());
        this.refreshBtn.addEventListener('click', () => this.refreshPreview());
        
        // Modal events
        document.querySelector('.close').addEventListener('click', () => {
            this.codeModal.style.display = 'none';
        });
        
        document.getElementById('copyCodeBtn').addEventListener('click', () => {
            this.copyCode();
        });
        
        this.downloadBtn.addEventListener('click', () => {
            this.downloadCode();
        });
        
        window.addEventListener('click', (e) => {
            if (e.target === this.codeModal) {
                this.codeModal.style.display = 'none';
            }
        });

        // Gérer les erreurs d'iframe
        this.previewFrame.addEventListener('error', () => {
            console.error('Erreur de chargement de l\'iframe');
            this.showPreviewError();
        });
    }
    
    async sendMessage() {
        if (this.isGenerating) return;
        
        const message = this.messageInput.value.trim();
        if (!message) return;
        
        this.addMessage(message, 'user');
        this.messageInput.value = '';
        this.setLoading(true);
        
        try {
            const response = await fetch('/api/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ description: message })
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.addMessage('Code généré avec succès ! 🎉', 'assistant');
                this.updatePreview(data.code);
                this.currentCode = data.code;
                
                // Bouton pour voir le code
                this.addCodeButton();
                
                if (data.validation && !data.validation.valid) {
                    this.addMessage(`⚠️ Attention: ${data.validation.missing_tags.join(', ')} manquant(s)`, 'assistant');
                }
            } else {
                this.addMessage(`❌ Erreur: ${data.error}`, 'assistant');
                if (data.raw_response) {
                    console.log('Réponse brute:', data.raw_response);
                }
            }
        } catch (error) {
            console.error('Erreur:', error);
            this.addMessage('❌ Erreur de communication avec le serveur', 'assistant');
        } finally {
            this.setLoading(false);
        }
    }
    
    addMessage(content, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}`;
        messageDiv.innerHTML = `<strong>${sender === 'user' ? 'Vous' : 'Assistant'}:</strong> ${content}`;
        
        this.chatMessages.appendChild(messageDiv);
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
    }
    
    addCodeButton() {
        const buttonDiv = document.createElement('div');
        buttonDiv.className = 'message assistant';
        buttonDiv.innerHTML = `
            <button onclick="chatBot.showCode()" style="padding: 8px 16px; background: #4CAF50; color: white; border: none; border-radius: 5px; cursor: pointer;">
                📄 Voir le code source
            </button>
        `;
        
        this.chatMessages.appendChild(buttonDiv);
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
    }
    
    updatePreview(htmlCode) {
        try {
            // Créer un blob avec le code HTML
            const blob = new Blob([htmlCode], { type: 'text/html' });
            const url = URL.createObjectURL(blob);
            
            // Masquer le placeholder et afficher l'iframe
            this.previewPlaceholder.style.display = 'none';
            this.previewFrame.style.display = 'block';
            this.previewFrame.src = url;
            
            // Libérer l'URL après un délai
            setTimeout(() => {
                try {
                    URL.revokeObjectURL(url);
                } catch (e) {
                    console.warn('Erreur lors de la libération de l\'URL:', e);
                }
            }, 5000);
            
        } catch (error) {
            console.error('Erreur lors de la mise à jour du preview:', error);
            this.showPreviewError();
        }
    }
    
    showPreviewError() {
        this.previewFrame.style.display = 'none';
        this.previewPlaceholder.style.display = 'flex';
        this.previewPlaceholder.innerHTML = '<p>❌ Erreur lors du chargement du preview</p>';
    }
    
    refreshPreview() {
        if (this.currentCode) {
            this.updatePreview(this.currentCode);
            this.addMessage('Preview actualisé ! 🔄', 'assistant');
        }
    }
    
    setLoading(loading) {
        this.isGenerating = loading;
        this.sendButton.disabled = loading;
        this.loadingIndicator.style.display = loading ? 'block' : 'none';
        
        if (loading) {
            this.sendButton.textContent = 'Génération...';
        } else {
            this.sendButton.textContent = 'Envoyer';
        }
    }
    
    showCode() {
        this.codeContent.textContent = this.currentCode;
        this.codeModal.style.display = 'block';
    }
    
    async copyCode() {
        try {
            await navigator.clipboard.writeText(this.currentCode);
            const btn = document.getElementById('copyCodeBtn');
            const originalText = btn.textContent;
            btn.textContent = '✅ Copié !';
            setTimeout(() => {
                btn.textContent = originalText;
            }, 2000);
        } catch (error) {
            console.error('Erreur lors de la copie:', error);
            alert('Erreur lors de la copie du code');
        }
    }
    
    downloadCode() {
        try {
            const blob = new Blob([this.currentCode], { type: 'text/html' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `composant-${Date.now()}.html`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
        } catch (error) {
            console.error('Erreur lors du téléchargement:', error);
            alert('Erreur lors du téléchargement');
        }
    }
    
    toggleFullscreen() {
        if (this.previewFrame.requestFullscreen) {
            this.previewFrame.requestFullscreen().catch(err => {
                console.error('Erreur plein écran:', err);
            });
        } else {
            alert('Le plein écran n\'est pas supporté par votre navigateur');
        }
    }
}

// Initialisation
const chatBot = new ChatBot();