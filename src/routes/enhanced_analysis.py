#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQV30 Enhanced v2.0 - Enhanced Analysis Routes
Rotas para análise aprimorada
"""

import logging
from flask import Blueprint, request, jsonify
from datetime import datetime
from services.enhanced_analysis_orchestrator import enhanced_orchestrator
from services.auto_save_manager import salvar_etapa, salvar_erro

logger = logging.getLogger(__name__)

enhanced_analysis_bp = Blueprint('enhanced_analysis', __name__)

@enhanced_analysis_bp.route('/enhanced_analyze', methods=['POST'])
def enhanced_analyze():
    """Executa análise aprimorada"""
    
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Dados não fornecidos'}), 400
        
        if not data.get('segmento'):
            return jsonify({'error': 'Segmento é obrigatório'}), 400
        
        # Gera session ID
        session_id = f"enhanced_{int(datetime.now().timestamp())}"
        
        # Executa análise aprimorada
        result = enhanced_orchestrator.execute_ultra_enhanced_analysis(
            data, session_id, None
        )
        
        return jsonify({
            'success': True,
            'session_id': session_id,
            'result': result,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"❌ Erro na análise aprimorada: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@enhanced_analysis_bp.route('/enhanced_status/<session_id>', methods=['GET'])
def enhanced_status(session_id):
    """Obtém status da análise aprimorada"""
    
    try:
        # Implementar lógica de status se necessário
        return jsonify({
            'success': True,
            'session_id': session_id,
            'status': 'completed',
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500