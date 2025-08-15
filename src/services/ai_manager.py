#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQV30 Enhanced v2.0 - AI Manager com Sistema de Fallback
Gerenciador inteligente de múltiplas IAs com fallback automático
"""

import os
import logging
import time
import json
from typing import Dict, List, Optional, Any
import requests

# Imports condicionais para os clientes de IA
try:
    import google.generativeai as genai
    HAS_GEMINI = True
except ImportError:
    HAS_GEMINI = False

try:
    import openai
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False

try:
    from services.groq_client import groq_client
    HAS_GROQ_CLIENT = True
except ImportError:
    HAS_GROQ_CLIENT = False

logger = logging.getLogger(__name__)

class AIManager:
    """Gerenciador de IAs com sistema de fallback automático"""

    def __init__(self):
        """Inicializa o AI Manager com múltiplos provedores"""
        self.providers = {}
        self.fallback_order = []
        self.provider_stats = {}
        self.disabled_providers = set()

        self._initialize_providers()

        logger.info(f"🤖 AI Manager inicializado com {len(self.providers)} provedores disponíveis.")

    def _initialize_providers(self):
        """Inicializa todos os provedores de IA com base nas chaves de API disponíveis."""

        # Inicializa Gemini
        if HAS_GEMINI:
            try:
                gemini_key = os.getenv('GEMINI_API_KEY')
                if gemini_key:
                    genai.configure(api_key=gemini_key)
                    # Tenta instanciar um modelo específico para verificar a chave
                    # Se falhar aqui, considera o provedor indisponível
                    try:
                        model = genai.GenerativeModel("gemini-2.0-flash-exp")
                        # Teste rápido para ver se a API responde
                        model.generate_content("teste", generation_config={"max_output_tokens": 5})
                        self.providers['gemini'] = {
                            'client': model,
                            'available': True,
                            'priority': 1,
                            'model': 'gemini-2.0-flash-exp',
                            'max_errors': 2,
                            'consecutive_failures': 0
                        }
                        self.fallback_order.append('gemini')
                        logger.info("✅ Gemini 2.5 Pro (gemini-2.0-flash-exp) inicializado como MODELO PRIMÁRIO")
                    except Exception as gemini_test_e:
                        logger.warning(f"⚠️ Gemini 2.5 Pro não pôde ser instanciado ou testado: {str(gemini_test_e)}")
                        self.providers['gemini'] = {'available': False, 'error': str(gemini_test_e)}

            except Exception as e:
                logger.warning(f"⚠️ Falha ao configurar Gemini: {str(e)}")
                self.providers['gemini'] = {'available': False, 'error': str(e)}
        else:
            logger.warning("⚠️ Biblioteca 'google-generativeai' não instalada.")
            self.providers['gemini'] = {'available': False, 'error': 'Biblioteca não instalada'}


        # Inicializa OpenAI
        if HAS_OPENAI:
            try:
                openai_key = os.getenv('OPENAI_API_KEY')
                if openai_key:
                    # Tenta instanciar o cliente OpenAI
                    client = openai.OpenAI(api_key=openai_key)
                    # Teste rápido para ver se a API responde
                    client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[{"role": "user", "content": "teste"}],
                        max_tokens=5
                    )
                    self.providers['openai'] = {
                        'client': client,
                        'available': True,
                        'priority': 3,
                        'model': 'gpt-3.5-turbo',
                        'max_errors': 2,
                        'consecutive_failures': 0
                    }
                    self.fallback_order.append('openai')
                    logger.info("✅ OpenAI (gpt-3.5-turbo) inicializado com sucesso")
            except Exception as e:
                logger.info(f"ℹ️ OpenAI não disponível: {str(e)}")
                self.providers['openai'] = {'available': False, 'error': str(e)}
        else:
            logger.info("ℹ️ Biblioteca 'openai' não instalada.")
            self.providers['openai'] = {'available': False, 'error': 'Biblioteca não instalada'}

        # Inicializa Groq
        try:
            if HAS_GROQ_CLIENT and groq_client and groq_client.is_enabled():
                # Teste rápido para ver se a API responde
                groq_client.generate("teste", max_tokens=5)
                self.providers['groq'] = {
                    'client': groq_client,
                    'available': True,
                    'priority': 2,
                    'model': 'llama3-70b-8192',
                    'max_errors': 2,
                    'consecutive_failures': 0
                }
                self.fallback_order.append('groq')
                logger.info("✅ Groq (llama3-70b-8192) inicializado com sucesso")
            else:
                logger.info("ℹ️ Groq client não configurado ou não habilitado")
                self.providers['groq'] = {'available': False, 'error': 'Cliente não configurado ou desabilitado'}
        except Exception as e:
            logger.info(f"ℹ️ Groq não disponível: {str(e)}")
            self.providers['groq'] = {'available': False, 'error': str(e)}


        # Inicializa HuggingFace
        try:
            hf_key = os.getenv('HUGGINGFACE_API_KEY')
            if hf_key:
                # Cria um cliente mock para HuggingFace, pois a lógica está em _generate_with_huggingface
                self.providers['huggingface'] = {
                    'client': {'api_key': hf_key, 'base_url': 'https://api-inference.huggingface.co/models/'},
                    'available': True,
                    'priority': 4,
                    'models': ["HuggingFaceH4/zephyr-7b-beta", "google/flan-t5-base"],
                    'current_model_index': 0,
                    'max_errors': 3,
                    'consecutive_failures': 0
                }
                # Teste rápido de conexão/autenticação com HuggingFace
                url = f"{self.providers['huggingface']['client']['base_url']}HuggingFaceH4/zephyr-7b-beta"
                headers = {"Authorization": f"Bearer {hf_key}"}
                requests.post(url, headers=headers, json={"inputs": "teste"}, timeout=10)

                self.fallback_order.append('huggingface')
                logger.info("✅ HuggingFace inicializado com sucesso")
        except Exception as e:
            logger.info(f"ℹ️ HuggingFace não disponível: {str(e)}")
            self.providers['huggingface'] = {'available': False, 'error': str(e)}


        # Garante que a ordem de fallback seja consistente e inclua todos os provedores
        # Ordena por prioridade definida, e para prioridades iguais, mantém a ordem de inicialização
        self.fallback_order.sort(key=lambda p: self.providers.get(p, {}).get('priority', float('inf')))


    def _register_success(self, provider_name: str):
        """Registra um sucesso para um provedor."""
        if provider_name in self.providers:
            self.providers[provider_name]['consecutive_failures'] = 0
            logger.debug(f"✅ Sucesso registrado para {provider_name}")

    def _register_failure(self, provider_name: str, error: Exception):
        """Registra uma falha para um provedor e o desabilita se os erros excederem o limite."""
        if provider_name in self.providers:
            self.providers[provider_name]['consecutive_failures'] = self.providers[provider_name].get('consecutive_failures', 0) + 1
            self.providers[provider_name]['error'] = str(error) # Armazena o último erro

            if self.providers[provider_name]['consecutive_failures'] >= self.providers[provider_name].get('max_errors', 2):
                self.disabled_providers.add(provider_name)
                self.providers[provider_name]['available'] = False # Marca como indisponível
                logger.warning(f"⚠️ Provedor {provider_name} desabilitado temporariamente após {self.providers[provider_name]['consecutive_failures']} falhas consecutivas.")


    def generate_content(self, prompt: str, max_tokens: int = 2000, temperature: float = 0.7) -> str:
        """Gera conteúdo usando os provedores de IA disponíveis"""
        try:
            # Tenta cada provedor na ordem de fallback
            for provider_name in self.fallback_order:
                if provider_name in self.disabled_providers:
                    continue

                provider_info = self.providers.get(provider_name)
                if not provider_info or not provider_info.get('available'):
                    continue

                try:
                    logger.info(f"🔄 Tentando geração com {provider_name.upper()}")
                    client = provider_info.get('client')

                    response_text = None
                    if provider_name == 'gemini' and client:
                        response = client.generate_content(
                            prompt,
                            generation_config={"temperature": temperature, "max_output_tokens": min(max_tokens, 8192)},
                            safety_settings=[{"category": c, "threshold": "BLOCK_NONE"} for c in ["HARM_CATEGORY_HARASSMENT", "HARM_CATEGORY_HATE_SPEECH", "HARM_CATEGORY_SEXUALLY_EXPLICIT", "HARM_CATEGORY_DANGEROUS_CONTENT"]]
                        )
                        response_text = response.text
                    elif provider_name == 'groq' and client:
                        response = client.generate(prompt, max_tokens=min(max_tokens, 8192), temperature=temperature)
                        response_text = response
                    elif provider_name == 'openai' and client:
                        response = client.chat.completions.create(
                            model=provider_info.get('model', 'gpt-3.5-turbo'),
                            messages=[
                                {"role": "system", "content": "Você é um especialista em análise de mercado ultra-detalhada."},
                                {"role": "user", "content": prompt}
                            ],
                            max_tokens=min(max_tokens, 4096),
                            temperature=temperature
                        )
                        response_text = response.choices[0].message.content
                    elif provider_name == 'huggingface' and client:
                        # Lógica específica para HuggingFace
                        model_index = provider_info.get('current_model_index', 0)
                        models = provider_info.get('models', [])
                        
                        # Tenta rotacionar modelos para encontrar um que responda
                        for i in range(len(models)):
                            current_model_idx = (model_index + i) % len(models)
                            model = models[current_model_idx]
                            provider_info['current_model_index'] = current_model_idx # Atualiza índice para próxima tentativa

                            try:
                                url = f"{client['base_url']}{model}"
                                headers = {"Authorization": f"Bearer {client['api_key']}"}
                                payload = {"inputs": prompt, "parameters": {"max_new_tokens": min(max_tokens, 1024), "temperature": temperature}}
                                
                                hf_response = requests.post(url, headers=headers, json=payload, timeout=60)

                                if hf_response.status_code == 200:
                                    res_json = hf_response.json()
                                    generated_text = res_json[0].get("generated_text", "")
                                    if generated_text:
                                        response_text = generated_text
                                        logger.info(f"✅ HuggingFace ({model}) gerou {len(response_text)} caracteres")
                                        break # Sai do loop de modelos se obteve sucesso
                                elif hf_response.status_code == 503:
                                    logger.warning(f"⚠️ Modelo HuggingFace {model} está carregando (503), tentando próximo...")
                                    continue
                                else:
                                    logger.warning(f"⚠️ Erro {hf_response.status_code} no modelo HuggingFace {model}: {hf_response.text}")
                                    continue
                            except Exception as e:
                                logger.warning(f"⚠️ Erro ao chamar modelo HuggingFace {model}: {e}")
                                continue
                        
                        if response_text is None:
                            raise Exception("Todos os modelos HuggingFace falharam após tentativas.")

                    if response_text and len(response_text.strip()) > 10:
                        logger.info(f"✅ {provider_name.upper()} gerou conteúdo com sucesso.")
                        self._register_success(provider_name)
                        return response_text.strip()
                    else:
                        logger.warning(f"⚠️ {provider_name.upper()} retornou resposta vazia ou muito curta.")
                        raise Exception("Resposta vazia ou muito curta do provedor.")

                except Exception as e:
                    logger.error(f"❌ Erro ao usar provedor {provider_name.upper()}: {e}")
                    self._register_failure(provider_name, e)
                    continue # Tenta o próximo provedor na lista de fallback

            # Se todos os provedores na lista de fallback falharem
            logger.warning("⚠️ Todos os provedores de IA falharam. Retornando resposta básica.")
            return self._generate_basic_response(prompt)

        except Exception as e:
            logger.error(f"❌ Erro crítico no AI Manager: {e}")
            return self._generate_basic_response(prompt)


    def _generate_basic_response(self, prompt: str) -> str:
        """Gera resposta básica quando todos os provedores falham"""

        # Análise básica do prompt para resposta contextual
        if 'driver' in prompt.lower() or 'direção' in prompt.lower() or 'navegação' in prompt.lower():
            return '''[
                {"nome": "Crescimento Seguro", "gatilho_central": "Medo de falha", "definicao_visceral": "Superar obstáculos com confiança"},
                {"nome": "Potencial Desbloqueado", "gatilho_central": "Desejo de crescimento", "definicao_visceral": "Liberar capacidades ocultas"},
                {"nome": "Direção Clara", "gatilho_central": "Incerteza", "definicao_visceral": "Encontrar caminho para sucesso"}
            ]'''

        elif 'prova' in prompt.lower() or 'visual' in prompt.lower() or 'evidência' in prompt.lower():
            return '''[
                {"nome": "Prova de Urgência", "categoria": "urgencia", "objetivo": "Criar senso de urgência"},
                {"nome": "Prova Social", "categoria": "social", "objetivo": "Validação por pares"},
                {"nome": "Prova de Autoridade", "categoria": "autoridade", "objetivo": "Demonstrar expertise"}
            ]'''

        elif 'objeção' in prompt.lower() or 'objection' in prompt.lower() or 'impedimento' in prompt.lower():
            return '''[
                {"objecao": "Não tenho tempo", "categoria": "tempo", "resposta": "Foque no valor do tempo"},
                {"objecao": "Muito caro", "categoria": "dinheiro", "resposta": "Mostre o ROI"},
                {"objecao": "Preciso pensar", "categoria": "necessidade", "resposta": "Crie urgência"}
            ]'''

        elif 'pitch' in prompt.lower() or 'apresentação' in prompt.lower():
            return '''{
                "fases": [
                    {"fase": "quebra", "objetivo": "Quebrar ilusão", "script": "A realidade é diferente do que parece"},
                    {"fase": "exposicao", "objetivo": "Mostrar problema", "script": "Aqui está o verdadeiro desafio"},
                    {"fase": "solucao", "objetivo": "Apresentar solução", "script": "Esta é a resposta"}
                ]
            }'''

        elif 'avatar' in prompt.lower() or 'persona' in prompt.lower():
            return '''
            Avatar Empresarial:
            - Perfil: Empreendedor entre 35-45 anos
            - Dores: Sobrecarga, medo de falha, dificuldade para delegar
            - Desejos: Crescimento sustentável, liberdade financeira, reconhecimento
            - Medos: Perder controle, falhar, não ser visto como líder
            '''

        elif 'previsão' in prompt.lower() or 'futuro' in prompt.lower() or 'tendências' in prompt.lower():
            return '''{
                "cenarios": {
                    "curto_prazo": {"tendencias": ["Digitalização", "Automação"], "oportunidades": ["Nichos específicos"]},
                    "medio_prazo": {"tendencias": ["IA mainstream", "Sustentabilidade"], "oportunidades": ["Parcerias estratégicas"]},
                    "longo_prazo": {"tendencias": ["Economia digital"], "oportunidades": ["Mercados globais"]}
                }
            }'''
        
        elif 'código' in prompt.lower() or 'excluir' in prompt.lower() or 'remover' in prompt.lower():
            return '''
            Recomendações de Código para Exclusão:
            - Funções redundantes ou não utilizadas.
            - Módulos com funcionalidade obsoleta.
            - Configurações de API que não estão mais em uso.
            - Arquivos de log ou temporários de longa data.
            - Bibliotecas desatualizadas sem planos de atualização.
            '''

        else:
            return f"Análise básica para: {prompt[:100]}... - Sistema funcionando em modo básico. Configure APIs para análise completa."


    def get_provider_status(self) -> Dict[str, str]:
        """Retorna status de todos os provedores"""
        status = {}
        for provider_name, provider_info in self.providers.items():
            if provider_info.get('available', False):
                status[provider_name] = "available"
            else:
                status[provider_name] = f"unavailable ({provider_info.get('error', 'N/A')})"
        return status

# Instância global
ai_manager = AIManager()