#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQV30 Enhanced v2.0 - Groq Client CORRIGIDO
Cliente para integração com Groq API
"""

import os
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class GroqClient:
    """Cliente para integração com Groq API"""
    
    def __init__(self):
        """Inicializa cliente Groq"""
        self.api_key = os.getenv("GROQ_API_KEY")
        self.base_url = "https://api.groq.com/openai/v1"
        self.model = "llama3-70b-8192"
        
        self.available = bool(self.api_key)
        
        if self.available:
            # Testa conexão
            try:
                test_response = self._make_request("Test", max_tokens=5)
                if test_response:
                    logger.info("✅ Cliente Groq (llama3-70b-8192) inicializado com sucesso.")
                else:
                    self.available = False
                    logger.warning("⚠️ Groq API não respondeu ao teste inicial")
            except Exception as e:
                self.available = False
                logger.warning(f"⚠️ Erro ao testar Groq: {e}")
        else:
            logger.warning("⚠️ Groq API key não encontrada")
    
    def is_enabled(self) -> bool:
        """Verifica se o cliente está habilitado"""
        return self.available
    
    def generate(self, prompt: str, max_tokens: int = 1000) -> Optional[str]:
        """Gera texto usando Groq - MÉTODO CORRIGIDO"""
        
        if not self.available:
            logger.warning("Groq não está disponível")
            return None
        
        return self._make_request(prompt, max_tokens)
    
    def _make_request(self, prompt: str, max_tokens: int, temperature: float = 0.7) -> Optional[str]:
        """Faz requisição para Groq API"""
        
        try:
            import requests
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": self.model,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "max_tokens": max_tokens,
                "temperature": temperature,
                "stream": False
            }
            
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                data = response.json()
                content = data["choices"][0]["message"]["content"]
                logger.info(f"✅ Groq gerou {len(content)} caracteres em {response.elapsed.total_seconds():.2f}s")
                return content
            else:
                logger.error(f"Erro Groq: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"Erro na requisição Groq: {str(e)}")
            return None

# Instância global
groq_client = GroqClient()