#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQV30 Enhanced v2.0 - URL Resolver
Resolvedor de URLs com redirecionamentos
"""

import logging
import requests
from typing import Optional
from urllib.parse import urlparse

logger = logging.getLogger(__name__)

class URLResolver:
    """Resolvedor de URLs com suporte a redirecionamentos"""
    
    def __init__(self):
        """Inicializa o resolvedor de URLs"""
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        logger.info("URL Resolver inicializado")
    
    def resolve_redirect_url(self, url: str) -> str:
        """Resolve redirecionamentos de URL"""
        
        if not url or not url.startswith('http'):
            return url
        
        try:
            # Faz HEAD request para seguir redirecionamentos
            response = self.session.head(
                url, 
                allow_redirects=True, 
                timeout=10
            )
            
            # Retorna URL final após redirecionamentos
            final_url = response.url
            
            if final_url != url:
                logger.info(f"🔄 URL resolvida: {url} -> {final_url}")
            
            return final_url
            
        except Exception as e:
            logger.warning(f"⚠️ Erro ao resolver URL {url}: {e}")
            return url
    
    def is_valid_url(self, url: str) -> bool:
        """Verifica se URL é válida"""
        
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except:
            return False

# Instância global
url_resolver = URLResolver()