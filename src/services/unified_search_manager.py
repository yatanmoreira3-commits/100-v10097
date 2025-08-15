#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQV30 Enhanced v2.0 - Unified Search Manager
Gerenciador unificado de busca com múltiplos provedores
"""

import logging
import time
from typing import Dict, List, Any, Optional
from services.production_search_manager import production_search_manager
from services.exa_client import exa_client

logger = logging.getLogger(__name__)

class UnifiedSearchManager:
    """Gerenciador unificado de busca"""
    
    def __init__(self):
        """Inicializa o gerenciador unificado"""
        self.providers = {
            'production_search': production_search_manager,
            'exa': exa_client
        }
        
        logger.info("Unified Search Manager inicializado")
    
    def unified_search(self, query: str, max_results: int = 20) -> Dict[str, Any]:
        """Executa busca unificada em todos os provedores"""
        
        logger.info(f"🔍 Executando busca unificada: {query}")
        
        all_results = []
        provider_stats = {}
        
        # Busca com production search manager
        try:
            prod_results = production_search_manager.search_with_fallback(query, max_results // 2)
            if isinstance(prod_results, list):
                all_results.extend(prod_results)
                provider_stats['production_search'] = {
                    'results': len(prod_results),
                    'success': True
                }
            else:
                provider_stats['production_search'] = {
                    'results': 0,
                    'success': False,
                    'error': 'Resultado inválido'
                }
        except Exception as e:
            logger.error(f"❌ Erro no production search: {e}")
            provider_stats['production_search'] = {
                'results': 0,
                'success': False,
                'error': str(e)
            }
        
        # Busca com Exa se disponível
        if exa_client.is_available():
            try:
                exa_results = exa_client.search(query, max_results // 2)
                if exa_results and 'results' in exa_results:
                    exa_formatted = []
                    for item in exa_results['results']:
                        exa_formatted.append({
                            'title': item.get('title', ''),
                            'url': item.get('url', ''),
                            'snippet': item.get('text', '')[:300],
                            'source': 'exa'
                        })
                    all_results.extend(exa_formatted)
                    provider_stats['exa'] = {
                        'results': len(exa_formatted),
                        'success': True
                    }
                else:
                    provider_stats['exa'] = {
                        'results': 0,
                        'success': False,
                        'error': 'Sem resultados'
                    }
            except Exception as e:
                logger.error(f"❌ Erro no Exa: {e}")
                provider_stats['exa'] = {
                    'results': 0,
                    'success': False,
                    'error': str(e)
                }
        
        # Remove duplicatas
        unique_results = self._remove_duplicates(all_results)
        
        return {
            'query': query,
            'results': unique_results,
            'total_results': len(unique_results),
            'provider_stats': provider_stats,
            'success': len(unique_results) > 0
        }
    
    def _remove_duplicates(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Remove resultados duplicados baseado na URL"""
        
        seen_urls = set()
        unique_results = []
        
        for result in results:
            url = result.get('url', '')
            if url and url not in seen_urls:
                seen_urls.add(url)
                unique_results.append(result)
        
        return unique_results
    
    def get_provider_status(self) -> Dict[str, Any]:
        """Retorna status dos provedores"""
        
        return {
            'production_search': {
                'available': True,
                'providers': production_search_manager.get_provider_status()
            },
            'exa': {
                'available': exa_client.is_available()
            }
        }

# Instância global
unified_search_manager = UnifiedSearchManager()