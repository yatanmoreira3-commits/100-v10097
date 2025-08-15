#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQV30 Enhanced v2.0 - Forensic Analysis Routes
Rotas para análise forense
"""

import logging
from flask import Blueprint, request, jsonify
from datetime import datetime
from services.forensic_cpl_analyzer import forensic_cpl_analyzer

logger = logging.getLogger(__name__)

forensic_bp = Blueprint('forensic', __name__)

@forensic_bp.route('/analyze_cpl', methods=['POST'])
def analyze_cpl():
    """Executa análise forense de CPL"""
    
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Dados não fornecidos'}), 400
        
        transcription = data.get('transcription', '')
        context_data = data.get('context', {})
        
        if not transcription:
            return jsonify({'error': 'Transcrição é obrigatória'}), 400
        
        # Executa análise forense
        result = forensic_cpl_analyzer.analyze_cpl_forensically(
            transcription, context_data
        )
        
        return jsonify({
            'success': True,
            'result': result,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"❌ Erro na análise forense: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@forensic_bp.route('/metrics/<session_id>', methods=['GET'])
def get_forensic_metrics(session_id):
    """Obtém métricas forenses de uma sessão"""
    
    try:
        # Implementar lógica de métricas forenses
        return jsonify({
            'success': True,
            'session_id': session_id,
            'metrics': {
                'density_score': 85,
                'emotional_intensity': 90,
                'persuasion_level': 88
            },
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"❌ Erro nas métricas forenses: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500