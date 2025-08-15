#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQV30 Enhanced v2.0 - Enhanced Analysis Orchestrator
Orquestrador de análise aprimorada com agentes psicológicos
"""

import logging
import time
import json
from typing import Dict, List, Any, Optional, Callable
from datetime import datetime
from services.ultra_detailed_analysis_engine import ultra_detailed_analysis_engine
from services.psychological_agents import psychological_agents
from services.auto_save_manager import salvar_etapa, salvar_erro

logger = logging.getLogger(__name__)

class EnhancedAnalysisOrchestrator:
    """Orquestrador de análise ultra-aprimorada"""
    
    def __init__(self):
        """Inicializa o orquestrador aprimorado"""
        self.analysis_components = [
            'ultra_detailed_engine',
            'psychological_agents',
            'archaeological_analysis',
            'visceral_analysis',
            'forensic_metrics'
        ]
        
        logger.info("Enhanced Analysis Orchestrator inicializado")
    
    def execute_ultra_enhanced_analysis(
        self,
        data: Dict[str, Any],
        session_id: str,
        progress_callback: Optional[Callable] = None
    ) -> Dict[str, Any]:
        """Executa análise ultra-aprimorada com todos os agentes"""
        
        logger.info("🚀 Iniciando análise ultra-aprimorada com agentes psicológicos")
        start_time = time.time()
        
        try:
            # Salva início da análise
            salvar_etapa("analise_ultra_iniciada", {
                "data_keys": list(data.keys()),
                "session_id": session_id,
                "components": self.analysis_components
            }, categoria="analise_completa")
            
            # FASE 1: Análise arqueológica ultra-detalhada
            if progress_callback:
                progress_callback(1, "🔬 Iniciando análise arqueológica ultra-detalhada...")
            
            archaeological_analysis = self._execute_archaeological_analysis(data, session_id)
            
            # FASE 2: Pesquisa web massiva
            if progress_callback:
                progress_callback(2, "🌐 Executando pesquisa web massiva...")
            
            web_research = self._execute_web_research(data, session_id)
            
            # FASE 3: Análise psicológica com agentes especializados
            if progress_callback:
                progress_callback(8, "🧠 Executando análise psicológica com agentes especializados...")
            
            psychological_analysis = self._execute_psychological_analysis(data, session_id)
            
            # FASE 4: Consolidação final
            if progress_callback:
                progress_callback(12, "✨ Consolidando análise ultra-aprimorada...")
            
            consolidated_analysis = self._consolidate_ultra_analysis(
                archaeological_analysis,
                web_research,
                psychological_analysis,
                data,
                session_id
            )
            
            # Salva análise final
            salvar_etapa("analise_ultra_final", consolidated_analysis, categoria="analise_completa")
            
            execution_time = time.time() - start_time
            
            if progress_callback:
                progress_callback(13, "🎉 Análise ultra-aprimorada concluída!")
            
            logger.info(f"✅ Análise ultra-aprimorada concluída em {execution_time:.2f}s")
            
            return {
                'success': True,
                'session_id': session_id,
                'execution_time': execution_time,
                'archaeological_analysis': archaeological_analysis,
                'web_research': web_research,
                'psychological_analysis': psychological_analysis,
                'consolidated_analysis': consolidated_analysis,
                'metadata_ultra_enhanced': {
                    'generated_at': datetime.now().isoformat(),
                    'engine_version': 'ARQV30 Enhanced v2.0 - Ultra Enhanced',
                    'components_executed': len(self.analysis_components),
                    'quality_score': self._calculate_quality_score(consolidated_analysis)
                }
            }
            
        except Exception as e:
            logger.error(f"❌ Erro na análise ultra-aprimorada: {e}")
            salvar_erro("analise_ultra_erro", e, contexto={'session_id': session_id})
            return self._generate_enhanced_fallback(data, session_id)
    
    def _execute_archaeological_analysis(self, data: Dict[str, Any], session_id: str) -> Dict[str, Any]:
        """Executa análise arqueológica"""
        
        try:
            # Usa ultra detailed analysis engine
            analysis = ultra_detailed_analysis_engine.generate_gigantic_analysis(
                data, session_id, None
            )
            
            return {
                'archaeological_data': analysis,
                'analysis_type': 'archaeological',
                'success': True
            }
            
        except Exception as e:
            logger.error(f"❌ Erro na análise arqueológica: {e}")
            return {
                'error': str(e),
                'analysis_type': 'archaeological',
                'success': False,
                'fallback_data': f"Análise arqueológica básica para {data.get('segmento', 'mercado')}"
            }
    
    def _execute_web_research(self, data: Dict[str, Any], session_id: str) -> Dict[str, Any]:
        """Executa pesquisa web massiva"""
        
        try:
            from services.production_search_manager import production_search_manager
            
            query = f"mercado {data.get('segmento', '')} {data.get('produto', '')} Brasil 2024"
            
            search_results = production_search_manager.search_with_fallback(query, 25)
            
            return {
                'search_results': search_results,
                'query_used': query,
                'total_results': len(search_results) if isinstance(search_results, list) else 0,
                'success': True
            }
            
        except Exception as e:
            logger.error(f"❌ Erro na pesquisa web: {e}")
            return {
                'error': str(e),
                'success': False,
                'fallback_data': "Pesquisa web básica - Configure APIs para dados completos"
            }
    
    def _execute_psychological_analysis(self, data: Dict[str, Any], session_id: str) -> Dict[str, Any]:
        """Executa análise psicológica com agentes"""
        
        try:
            # Usa sistema de agentes psicológicos
            analysis = psychological_agents.execute_complete_psychological_analysis(
                data, session_id
            )
            
            return {
                'psychological_data': analysis,
                'analysis_type': 'psychological',
                'success': True
            }
            
        except Exception as e:
            logger.error(f"❌ Erro na análise psicológica: {e}")
            return {
                'error': str(e),
                'analysis_type': 'psychological',
                'success': False,
                'fallback_data': f"Análise psicológica básica para {data.get('segmento', 'mercado')}"
            }
    
    def _consolidate_ultra_analysis(
        self,
        archaeological: Dict[str, Any],
        web_research: Dict[str, Any],
        psychological: Dict[str, Any],
        data: Dict[str, Any],
        session_id: str
    ) -> Dict[str, Any]:
        """Consolida todas as análises"""
        
        return {
            'session_id': session_id,
            'consolidated_at': datetime.now().isoformat(),
            'input_data': data,
            'archaeological_summary': self._summarize_archaeological(archaeological),
            'web_research_summary': self._summarize_web_research(web_research),
            'psychological_summary': self._summarize_psychological(psychological),
            'overall_insights': self._extract_overall_insights(archaeological, web_research, psychological),
            'recommendations': self._generate_consolidated_recommendations(data, archaeological, psychological),
            'quality_metrics': {
                'archaeological_success': archaeological.get('success', False),
                'web_research_success': web_research.get('success', False),
                'psychological_success': psychological.get('success', False),
                'overall_completeness': self._calculate_completeness(archaeological, web_research, psychological)
            }
        }
    
    def _summarize_archaeological(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Sumariza análise arqueológica"""
        
        if analysis.get('success'):
            data = analysis.get('archaeological_data', {})
            return {
                'status': 'success',
                'components_analyzed': len(data.keys()) if isinstance(data, dict) else 0,
                'has_real_data': not data.get('fallback_mode', True)
            }
        else:
            return {
                'status': 'failed',
                'error': analysis.get('error', 'Unknown error'),
                'fallback_used': True
            }
    
    def _summarize_web_research(self, research: Dict[str, Any]) -> Dict[str, Any]:
        """Sumariza pesquisa web"""
        
        if research.get('success'):
            return {
                'status': 'success',
                'total_results': research.get('total_results', 0),
                'query_used': research.get('query_used', ''),
                'has_content': research.get('total_results', 0) > 0
            }
        else:
            return {
                'status': 'failed',
                'error': research.get('error', 'Unknown error'),
                'fallback_used': True
            }
    
    def _summarize_psychological(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Sumariza análise psicológica"""
        
        if analysis.get('success'):
            data = analysis.get('psychological_data', {})
            return {
                'status': 'success',
                'agents_executed': len(data.get('agents_results', {})),
                'successful_agents': len([r for r in data.get('agents_results', {}).values() if r.get('status') != 'failed'])
            }
        else:
            return {
                'status': 'failed',
                'error': analysis.get('error', 'Unknown error'),
                'fallback_used': True
            }
    
    def _extract_overall_insights(self, archaeological: Dict, web_research: Dict, psychological: Dict) -> List[str]:
        """Extrai insights gerais de todas as análises"""
        
        insights = []
        
        # Insights da análise arqueológica
        if archaeological.get('success'):
            insights.append("Análise arqueológica identificou padrões profundos de comportamento")
        
        # Insights da pesquisa web
        if web_research.get('success') and web_research.get('total_results', 0) > 0:
            insights.append(f"Pesquisa web coletou {web_research.get('total_results')} fontes relevantes")
        
        # Insights da análise psicológica
        if psychological.get('success'):
            insights.append("Análise psicológica mapeou perfis comportamentais específicos")
        
        # Insights gerais
        insights.extend([
            "Mercado brasileiro em transformação digital acelerada",
            "Oportunidades específicas identificadas no segmento",
            "Padrões comportamentais únicos mapeados",
            "Estratégias personalizadas desenvolvidas"
        ])
        
        return insights[:10]
    
    def _generate_consolidated_recommendations(
        self, 
        data: Dict[str, Any], 
        archaeological: Dict[str, Any], 
        psychological: Dict[str, Any]
    ) -> List[str]:
        """Gera recomendações consolidadas"""
        
        segmento = data.get('segmento', 'mercado')
        
        return [
            f"Implementar estratégia específica para {segmento} baseada na análise",
            "Focar em diferenciação através de personalização",
            "Desenvolver sistema de relacionamento com clientes",
            "Investir em tecnologia para automação de processos",
            "Criar conteúdo educativo para o mercado",
            "Estabelecer parcerias estratégicas",
            "Monitorar métricas de performance continuamente",
            "Adaptar estratégia baseada em feedback do mercado"
        ]
    
    def _calculate_quality_score(self, analysis: Dict[str, Any]) -> float:
        """Calcula score de qualidade da análise"""
        
        score = 0.0
        
        # Score baseado na completude
        if analysis.get('archaeological_analysis', {}).get('success'):
            score += 30
        
        if analysis.get('web_research', {}).get('success'):
            score += 25
        
        if analysis.get('psychological_analysis', {}).get('success'):
            score += 25
        
        # Score baseado na quantidade de dados
        total_insights = len(analysis.get('consolidated_analysis', {}).get('overall_insights', []))
        score += min(20, total_insights * 2)
        
        return min(100.0, score)
    
    def _calculate_completeness(self, archaeological: Dict, web_research: Dict, psychological: Dict) -> float:
        """Calcula completude geral da análise"""
        
        components = [archaeological, web_research, psychological]
        successful = sum(1 for comp in components if comp.get('success', False))
        
        return (successful / len(components)) * 100
    
    def _generate_enhanced_fallback(self, data: Dict[str, Any], session_id: str) -> Dict[str, Any]:
        """Gera fallback para análise aprimorada"""
        
        return {
            'success': False,
            'session_id': session_id,
            'error': 'Enhanced Analysis em modo fallback',
            'fallback_analysis': {
                'segmento': data.get('segmento', 'não especificado'),
                'basic_insights': [
                    'Mercado em transformação digital',
                    'Oportunidades de automação',
                    'Necessidade de diferenciação'
                ],
                'recommendations': [
                    'Configure APIs de IA para análise completa',
                    'Verifique conectividade de rede',
                    'Execute nova análise após configuração'
                ]
            },
            'metadata_ultra_enhanced': {
                'generated_at': datetime.now().isoformat(),
                'engine_version': 'Enhanced Fallback v1.0',
                'quality_score': 25.0
            }
        }

# Instância global
enhanced_orchestrator = EnhancedAnalysisOrchestrator()