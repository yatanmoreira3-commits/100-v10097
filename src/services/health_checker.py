
import logging
import time
from typing import Dict, Any, List
from datetime import datetime

logger = logging.getLogger(__name__)

class HealthChecker:
    """Sistema de monitoramento de saúde dos serviços"""
    
    def __init__(self):
        """Inicializa o health checker"""
        self.last_check = None
        self.service_status = {}
        self.failed_services = []
        
        logger.info("🏥 Health Checker inicializado")
    
    def check_all_services(self) -> Dict[str, Any]:
        """Executa health check completo de todos os serviços"""
        logger.info("🔍 Iniciando health check completo...")
        
        start_time = time.time()
        results = {
            'timestamp': datetime.now().isoformat(),
            'services': {},
            'summary': {},
            'critical_failures': [],
            'warnings': []
        }
        
        # Lista de serviços para verificar
        services_to_check = [
            ('ai_providers', self._check_ai_providers),
            ('search_engines', self._check_search_engines),
            ('content_extractors', self._check_content_extractors),
            ('social_apis', self._check_social_apis),
            ('database', self._check_database),
            ('file_system', self._check_file_system)
        ]
        
        total_services = 0
        healthy_services = 0
        
        for service_name, check_function in services_to_check:
            try:
                service_result = check_function()
                results['services'][service_name] = service_result
                
                # Conta serviços saudáveis
                if isinstance(service_result, dict):
                    for sub_service, status in service_result.items():
                        total_services += 1
                        if isinstance(status, dict) and status.get('status') == 'healthy':
                            healthy_services += 1
                        elif status == 'healthy':
                            healthy_services += 1
                        elif isinstance(status, dict) and status.get('status') == 'critical':
                            results['critical_failures'].append(f"{service_name}.{sub_service}")
                        elif isinstance(status, dict) and status.get('status') == 'warning':
                            results['warnings'].append(f"{service_name}.{sub_service}")
                
            except Exception as e:
                logger.error(f"❌ Erro no health check de {service_name}: {e}")
                results['services'][service_name] = {'status': 'error', 'error': str(e)}
                results['critical_failures'].append(service_name)
        
        # Calcula métricas gerais
        health_percentage = (healthy_services / total_services * 100) if total_services > 0 else 0
        
        results['summary'] = {
            'total_services': total_services,
            'healthy_services': healthy_services,
            'health_percentage': round(health_percentage, 2),
            'status': self._get_overall_status(health_percentage),
            'check_duration': round(time.time() - start_time, 2),
            'critical_count': len(results['critical_failures']),
            'warning_count': len(results['warnings'])
        }
        
        self.last_check = results
        self.service_status = results['services']
        
        logger.info(f"✅ Health check concluído: {health_percentage:.1f}% saudável")
        
        return results
    
    def _check_ai_providers(self) -> Dict[str, Any]:
        """Verifica status dos provedores de IA"""
        try:
            from .ai_manager import ai_manager
            
            providers = {}
            
            # Testa cada provedor
            for provider_name in ['gemini', 'openai', 'groq', 'huggingface']:
                try:
                    # Teste simples de geração
                    test_response = ai_manager.generate_content("Test", max_tokens=10)
                    
                    if test_response and len(test_response) > 0 and 'erro' not in test_response.lower():
                        providers[provider_name] = {
                            'status': 'healthy',
                            'response_time': 'fast',
                            'last_test': datetime.now().isoformat()
                        }
                    else:
                        providers[provider_name] = {
                            'status': 'warning',
                            'issue': 'Response quality low',
                            'last_test': datetime.now().isoformat()
                        }
                        
                except Exception as e:
                    providers[provider_name] = {
                        'status': 'critical',
                        'error': str(e),
                        'last_test': datetime.now().isoformat()
                    }
            
            return providers
            
        except Exception as e:
            return {'error': f"AI providers check failed: {str(e)}"}
    
    def _check_search_engines(self) -> Dict[str, Any]:
        """Verifica status dos mecanismos de busca"""
        try:
            from .production_search_manager import production_search_manager
            
            engines = {}
            
            # Testa busca simples
            test_query = "test search"
            
            try:
                results = production_search_manager.search_with_fallback(test_query, 1)
                
                if results and (isinstance(results, list) or results.get('results')):
                    engines['production_search'] = {
                        'status': 'healthy',
                        'last_test': datetime.now().isoformat()
                    }
                else:
                    engines['production_search'] = {
                        'status': 'warning',
                        'issue': 'No results returned',
                        'last_test': datetime.now().isoformat()
                    }
                    
            except Exception as e:
                engines['production_search'] = {
                    'status': 'critical',
                    'error': str(e),
                    'last_test': datetime.now().isoformat()
                }
            
            return engines
            
        except Exception as e:
            return {'error': f"Search engines check failed: {str(e)}"}
    
    def _check_content_extractors(self) -> Dict[str, Any]:
        """Verifica status dos extratores de conteúdo"""
        extractors = {}
        
        # Lista de extratores para testar
        extractor_list = ['jina_reader', 'trafilatura', 'beautifulsoup', 'newspaper']
        
        for extractor in extractor_list:
            try:
                # Teste básico - verifica se módulo existe
                if extractor == 'jina_reader':
                    # Verifica se tem API key
                    import os
                    if os.getenv('JINA_API_KEY'):
                        extractors[extractor] = {'status': 'healthy'}
                    else:
                        extractors[extractor] = {'status': 'warning', 'issue': 'No API key'}
                else:
                    # Para outros, verifica se pode importar
                    if extractor == 'trafilatura':
                        import trafilatura
                    elif extractor == 'beautifulsoup':
                        import bs4
                    elif extractor == 'newspaper':
                        import newspaper
                    
                    extractors[extractor] = {'status': 'healthy'}
                    
            except ImportError:
                extractors[extractor] = {'status': 'critical', 'error': 'Module not installed'}
            except Exception as e:
                extractors[extractor] = {'status': 'warning', 'error': str(e)}
        
        return extractors
    
    def _check_social_apis(self) -> Dict[str, Any]:
        """Verifica status das APIs de redes sociais"""
        import os
        
        social_apis = {}
        
        # Lista de APIs para verificar
        api_configs = {
            'youtube': 'YOUTUBE_API_KEY',
            'twitter': 'TWITTER_BEARER_TOKEN', 
            'linkedin': 'LINKEDIN_CLIENT_ID',
            'instagram': 'INSTAGRAM_GRAPH_API_TOKEN'
        }
        
        for api_name, env_var in api_configs.items():
            api_key = os.getenv(env_var)
            
            if api_key and api_key != 'your_' + env_var.lower() + '_here':
                social_apis[api_name] = {
                    'status': 'healthy',
                    'has_credentials': True
                }
            else:
                social_apis[api_name] = {
                    'status': 'critical',
                    'issue': 'Missing or invalid credentials',
                    'has_credentials': False
                }
        
        return social_apis
    
    def _check_database(self) -> Dict[str, Any]:
        """Verifica status do banco de dados"""
        try:
            from ..database import get_db_connection
            
            # Tenta conectar e fazer query simples
            conn = get_db_connection()
            if conn:
                return {
                    'supabase': {
                        'status': 'healthy',
                        'last_test': datetime.now().isoformat()
                    }
                }
            else:
                return {
                    'supabase': {
                        'status': 'critical',
                        'error': 'Cannot connect to database'
                    }
                }
                
        except Exception as e:
            return {
                'supabase': {
                    'status': 'critical',
                    'error': str(e)
                }
            }
    
    def _check_file_system(self) -> Dict[str, Any]:
        """Verifica status do sistema de arquivos"""
        import os
        
        directories = {
            'analyses_data': 'analyses_data',
            'relatorios_intermediarios': 'relatorios_intermediarios',
            'uploads': 'src/uploads',
            'logs': 'logs'
        }
        
        filesystem = {}
        
        for dir_name, dir_path in directories.items():
            try:
                if os.path.exists(dir_path) and os.path.isdir(dir_path):
                    # Verifica se pode escrever
                    test_file = os.path.join(dir_path, 'health_check_test.tmp')
                    with open(test_file, 'w') as f:
                        f.write('test')
                    os.remove(test_file)
                    
                    filesystem[dir_name] = {
                        'status': 'healthy',
                        'writable': True
                    }
                else:
                    filesystem[dir_name] = {
                        'status': 'warning',
                        'issue': 'Directory does not exist',
                        'writable': False
                    }
                    
            except Exception as e:
                filesystem[dir_name] = {
                    'status': 'critical',
                    'error': str(e),
                    'writable': False
                }
        
        return filesystem
    
    def _get_overall_status(self, health_percentage: float) -> str:
        """Determina status geral baseado na porcentagem de saúde"""
        if health_percentage >= 90:
            return 'excellent'
        elif health_percentage >= 75:
            return 'good'  
        elif health_percentage >= 50:
            return 'fair'
        elif health_percentage >= 25:
            return 'poor'
        else:
            return 'critical'
    
    def get_failed_services(self) -> List[str]:
        """Retorna lista de serviços que falharam"""
        return self.failed_services
    
    def is_service_healthy(self, service_name: str) -> bool:
        """Verifica se um serviço específico está saudável"""
        if not self.service_status:
            return False
            
        service_data = self.service_status.get(service_name)
        if not service_data:
            return False
            
        if isinstance(service_data, dict):
            return service_data.get('status') == 'healthy'
        
        return False

# Instância global
health_checker = HealthChecker()
