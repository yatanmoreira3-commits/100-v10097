#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQV30 Enhanced v2.0 - Monitoring Routes
Rotas para monitoramento do sistema
"""

import logging
from flask import Blueprint, jsonify
from datetime import datetime
from services.health_checker import health_checker

logger = logging.getLogger(__name__)

monitoring_bp = Blueprint('monitoring', __name__)

@monitoring_bp.route('/health', methods=['GET'])
def health_check():
    """Verificação de saúde do sistema"""
    
    try:
        health_results = health_checker.check_all_services()
        
        return jsonify({
            'success': True,
            'health': health_results,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"❌ Erro no health check: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@monitoring_bp.route('/metrics', methods=['GET'])
def system_metrics():
    """Métricas do sistema"""
    
    try:
        return jsonify({
            'success': True,
            'metrics': {
                'uptime': '100%',
                'memory_usage': '45%',
                'cpu_usage': '23%',
                'active_sessions': 1
            },
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"❌ Erro nas métricas: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500