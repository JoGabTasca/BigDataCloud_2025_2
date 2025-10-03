import aiohttp
import json
from typing import List, Dict, Optional
import logging

class ApiClient:
    def __init__(self, base_url: str = "http://localhost:8080"):
        self.base_url = base_url
        self.logger = logging.getLogger(__name__)
    
    async def get_clientes(self) -> List[Dict]:
        """Busca todos os clientes"""
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(f"{self.base_url}/clientes") as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        self.logger.error(f"Erro ao buscar clientes: {response.status}")
                        return []
            except Exception as e:
                self.logger.error(f"Erro na requisição para clientes: {e}")
                return []
    
    async def get_cliente_by_cpf(self, cpf: str) -> Optional[Dict]:
        """Busca cliente por CPF"""
        clientes = await self.get_clientes()
        for cliente in clientes:
            if cliente.get('cpf') == cpf:
                return cliente
        return None
    
    async def get_reservas_voo_by_cliente(self, cliente_id: int) -> List[Dict]:
        """Busca reservas de voo por ID do cliente"""
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(f"{self.base_url}/api/reservas-voo/cliente/{cliente_id}") as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        self.logger.error(f"Erro ao buscar reservas de voo: {response.status}")
                        return []
            except Exception as e:
                self.logger.error(f"Erro na requisição para reservas de voo: {e}")
                return []
    
    async def get_reservas_hospedagem_by_cliente(self, cliente_id: int) -> List[Dict]:
        """Busca reservas de hospedagem por ID do cliente"""
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(f"{self.base_url}/api/reservas-hospedagem/cliente/{cliente_id}") as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        self.logger.error(f"Erro ao buscar reservas de hospedagem: {response.status}")
                        return []
            except Exception as e:
                self.logger.error(f"Erro na requisição para reservas de hospedagem: {e}")
                return []
    
    async def get_all_reservas_voo(self) -> List[Dict]:
        """Busca todas as reservas de voo"""
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(f"{self.base_url}/api/reservas-voo") as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        self.logger.error(f"Erro ao buscar todas as reservas de voo: {response.status}")
                        return []
            except Exception as e:
                self.logger.error(f"Erro na requisição para todas as reservas de voo: {e}")
                return []
    
    async def get_all_reservas_hospedagem(self) -> List[Dict]:
        """Busca todas as reservas de hospedagem"""
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(f"{self.base_url}/api/reservas-hospedagem") as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        self.logger.error(f"Erro ao buscar todas as reservas de hospedagem: {response.status}")
                        return []
            except Exception as e:
                self.logger.error(f"Erro na requisição para todas as reservas de hospedagem: {e}")
                return []
    
    async def criar_cliente(self, cliente_data: Dict) -> Optional[Dict]:
        """Cria um novo cliente na API"""
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(f"{self.base_url}/clientes", json=cliente_data) as response:
                    if response.status == 201 or response.status == 200:
                        return await response.json()
                    else:
                        error_text = await response.text()
                        self.logger.error(f"Erro ao criar cliente: {response.status} - {error_text}")
                        print(f"ERRO API CLIENTE - Status: {response.status}, Resposta: {error_text}")
                        return None
            except Exception as e:
                self.logger.error(f"Erro na requisição para criar cliente: {e}")
                print(f"ERRO EXCEÇÃO CLIENTE: {e}")
                return None
    
    async def criar_reserva_voo(self, reserva_data: Dict) -> Optional[Dict]:
        """Cria uma nova reserva de voo na API"""
        async with aiohttp.ClientSession() as session:
            try:
                print(f"ENVIANDO DADOS PARA API: {reserva_data}")
                async with session.post(f"{self.base_url}/api/reservas-voo", json=reserva_data) as response:
                    if response.status == 201 or response.status == 200:
                        result = await response.json()
                        print(f"RESERVA CRIADA COM SUCESSO: {result}")
                        return result
                    else:
                        error_text = await response.text()
                        self.logger.error(f"Erro ao criar reserva de voo: {response.status} - {error_text}")
                        print(f"ERRO API - Status: {response.status}, Resposta: {error_text}")
                        return None
            except Exception as e:
                self.logger.error(f"Erro na requisição para criar reserva de voo: {e}")
                print(f"ERRO EXCEÇÃO: {e}")
                return None
    
    async def criar_reserva_hospedagem(self, reserva_data: Dict) -> Optional[Dict]:
        """Cria uma nova reserva de hospedagem na API"""
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(f"{self.base_url}/api/reservas-hospedagem", json=reserva_data) as response:
                    if response.status == 201 or response.status == 200:
                        return await response.json()
                    else:
                        self.logger.error(f"Erro ao criar reserva de hospedagem: {response.status}")
                        return None
            except Exception as e:
                self.logger.error(f"Erro na requisição para criar reserva de hospedagem: {e}")
                return None
    
    async def cancelar_reserva_voo(self, reserva_id: int) -> Optional[Dict]:
        """Cancela uma reserva de voo (muda status para CANCELADA)"""
        async with aiohttp.ClientSession() as session:
            try:
                async with session.patch(f"{self.base_url}/api/reservas-voo/{reserva_id}/cancelar") as response:
                    if response.status == 200:
                        result = await response.json()
                        print(f"RESERVA DE VOO CANCELADA COM SUCESSO: {result}")
                        return result
                    else:
                        error_text = await response.text()
                        self.logger.error(f"Erro ao cancelar reserva de voo: {response.status} - {error_text}")
                        print(f"ERRO API CANCELAMENTO VOO - Status: {response.status}, Resposta: {error_text}")
                        return None
            except Exception as e:
                self.logger.error(f"Erro na requisição para cancelar reserva de voo: {e}")
                print(f"ERRO EXCEÇÃO CANCELAMENTO VOO: {e}")
                return None
    
    async def cancelar_reserva_hospedagem(self, reserva_id: int) -> Optional[Dict]:
        """Cancela uma reserva de hospedagem (muda status para CANCELADA)"""
        async with aiohttp.ClientSession() as session:
            try:
                async with session.patch(f"{self.base_url}/api/reservas-hospedagem/{reserva_id}/cancelar") as response:
                    if response.status == 200:
                        result = await response.json()
                        print(f"RESERVA DE HOSPEDAGEM CANCELADA COM SUCESSO: {result}")
                        return result
                    else:
                        error_text = await response.text()
                        self.logger.error(f"Erro ao cancelar reserva de hospedagem: {response.status} - {error_text}")
                        print(f"ERRO API CANCELAMENTO HOSPEDAGEM - Status: {response.status}, Resposta: {error_text}")
                        return None
            except Exception as e:
                self.logger.error(f"Erro na requisição para cancelar reserva de hospedagem: {e}")
                print(f"ERRO EXCEÇÃO CANCELAMENTO HOSPEDAGEM: {e}")
                return None