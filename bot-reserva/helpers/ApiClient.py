import aiohttp
import json
from typing import List, Dict, Optional
import logging

class ApiClient:
    def __init__(self, base_url: str = "https://chatbot-api-jgk-grbhazazdygrfsec.canadacentral-01.azurewebsites.net"):
        self.base_url = base_url
        self.logger = logging.getLogger(__name__)

    async def get_clientes(self) -> List[Dict]:
        """Busca todos os clientes"""
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(f"{self.base_url}/clientes") as response:
                    if response.status == 200:
                        result = await response.json()
                        print(f"DEBUG - get_clientes retornou tipo: {type(result)}")
                        if isinstance(result, list):
                            print(f"DEBUG - Número de clientes: {len(result)}")
                        return result if isinstance(result, list) else []
                    else:
                        self.logger.error(f"Erro ao buscar clientes: {response.status}")
                        error_text = await response.text()
                        print(f"DEBUG - Erro {response.status}: {error_text}")
                        return []
            except Exception as e:
                self.logger.error(f"Erro na requisição para clientes: {e}")
                print(f"DEBUG - Exceção: {e}")
                return []

    async def get_cliente_by_cpf(self, cpf: str) -> Optional[Dict]:
        """Busca cliente por CPF"""
        print(f"DEBUG - Buscando cliente com CPF: '{cpf}' (tipo: {type(cpf)})")

        clientes = await self.get_clientes()

        # Verifica se clientes é uma lista válida
        if not isinstance(clientes, list):
            self.logger.error(f"get_clientes retornou tipo inválido: {type(clientes)}")
            print(f"DEBUG - ERRO: get_clientes retornou {type(clientes)} em vez de lista")
            return None

        print(f"DEBUG - Total de clientes encontrados: {len(clientes)}")

        for i, cliente in enumerate(clientes):
            if isinstance(cliente, dict):
                cpf_banco = cliente.get('cpf', '')
                print(f"DEBUG - Cliente {i+1}: CPF='{cpf_banco}' (tipo: {type(cpf_banco)}), Nome={cliente.get('nome', 'N/A')}")

                # Comparação com conversão para string e remoção de espaços
                if str(cpf_banco).strip() == str(cpf).strip():
                    print(f"DEBUG - ✅ CLIENTE ENCONTRADO! {cliente.get('nome')}")
                    return cliente
            else:
                print(f"DEBUG - Cliente {i+1} não é um dicionário: {type(cliente)}")

        print(f"DEBUG - ❌ CPF '{cpf}' NÃO ENCONTRADO na lista de clientes")
        return None

    async def get_reservas_voo_by_cliente(self, cliente_cpf: str) -> List[Dict]:
        """Busca reservas de voo por CPF do cliente (do documento no Cosmos DB)"""
        async with aiohttp.ClientSession() as session:
            try:
                # Busca todos os clientes e filtra pelo CPF
                async with session.get(f"{self.base_url}/clientes") as response:
                    if response.status == 200:
                        clientes = await response.json()
                        for cliente in clientes:
                            if cliente.get('cpf') == cliente_cpf:
                                # Retorna as reservas de voo do documento do cliente
                                return cliente.get('reservasVoo', []) or []
                        return []
                    else:
                        self.logger.error(f"Erro ao buscar reservas de voo: {response.status}")
                        return []
            except Exception as e:
                self.logger.error(f"Erro na requisição para reservas de voo: {e}")
                return []

    async def get_reservas_voo_by_cliente_id(self, cliente_id: str) -> List[Dict]:
        """Busca reservas de voo por ID do cliente (do documento no Cosmos DB)"""
        try:
            cliente = await self.get_cliente_by_id(cliente_id)
            if cliente:
                reservas = cliente.get('reservasVoo', []) or []
                print(f"DEBUG - Cliente {cliente.get('nome')} tem {len(reservas)} reservas de voo")
                return reservas
            else:
                print(f"DEBUG - Cliente com ID {cliente_id} não encontrado")
                return []
        except Exception as e:
            self.logger.error(f"Erro ao buscar reservas de voo por ID: {e}")
            print(f"DEBUG - Erro ao buscar reservas: {e}")
            return []

    async def get_reservas_hospedagem_by_cliente(self, cliente_cpf: str) -> List[Dict]:
        """Busca reservas de hospedagem por CPF do cliente (do documento no Cosmos DB)"""
        async with aiohttp.ClientSession() as session:
            try:
                # Busca todos os clientes e filtra pelo CPF
                async with session.get(f"{self.base_url}/clientes") as response:
                    if response.status == 200:
                        clientes = await response.json()
                        for cliente in clientes:
                            if cliente.get('cpf') == cliente_cpf:
                                # Retorna as reservas de hospedagem do documento do cliente
                                return cliente.get('reservasHospedagem', []) or []
                        return []
                    else:
                        self.logger.error(f"Erro ao buscar reservas de hospedagem: {response.status}")
                        return []
            except Exception as e:
                self.logger.error(f"Erro na requisição para reservas de hospedagem: {e}")
                return []

    async def get_reservas_hospedagem_by_cliente_id(self, cliente_id: str) -> List[Dict]:
        """Busca reservas de hospedagem por ID do cliente (do documento no Cosmos DB)"""
        try:
            cliente = await self.get_cliente_by_id(cliente_id)
            if cliente:
                reservas = cliente.get('reservasHospedagem', []) or []
                print(f"DEBUG - Cliente {cliente.get('nome')} tem {len(reservas)} reservas de hospedagem")
                return reservas
            else:
                print(f"DEBUG - Cliente com ID {cliente_id} não encontrado")
                return []
        except Exception as e:
            self.logger.error(f"Erro ao buscar reservas de hospedagem por ID: {e}")
            print(f"DEBUG - Erro ao buscar reservas hospedagem: {e}")
            return []

    async def get_all_reservas_voo(self) -> List[Dict]:
        """Busca todas as reservas de voo de todos os clientes"""
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(f"{self.base_url}/clientes") as response:
                    if response.status == 200:
                        clientes = await response.json()
                        todas_reservas = []
                        for cliente in clientes:
                            reservas = cliente.get('reservasVoo', []) or []
                            # Adiciona informações do cliente em cada reserva
                            for reserva in reservas:
                                reserva['clienteNome'] = cliente.get('nome')
                                reserva['clienteCpf'] = cliente.get('cpf')
                                reserva['clienteId'] = cliente.get('id')
                            todas_reservas.extend(reservas)
                        return todas_reservas
                    else:
                        self.logger.error(f"Erro ao buscar todas as reservas de voo: {response.status}")
                        return []
            except Exception as e:
                self.logger.error(f"Erro na requisição para todas as reservas de voo: {e}")
                return []

    async def get_all_reservas_hospedagem(self) -> List[Dict]:
        """Busca todas as reservas de hospedagem de todos os clientes"""
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(f"{self.base_url}/clientes") as response:
                    if response.status == 200:
                        clientes = await response.json()
                        todas_reservas = []
                        for cliente in clientes:
                            reservas = cliente.get('reservasHospedagem', []) or []
                            # Adiciona informações do cliente em cada reserva
                            for reserva in reservas:
                                reserva['clienteNome'] = cliente.get('nome')
                                reserva['clienteCpf'] = cliente.get('cpf')
                                reserva['clienteId'] = cliente.get('id')
                            todas_reservas.extend(reservas)
                        return todas_reservas
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
        """Cria uma nova reserva de voo adicionando ao array reservasVoo do cliente"""
        async with aiohttp.ClientSession() as session:
            try:
                print(f"ENVIANDO DADOS PARA API: {reserva_data}")
                cliente_id = reserva_data.get('clienteId')

                if not cliente_id:
                    self.logger.error("clienteId não fornecido na reserva")
                    return None

                # Buscar o cliente pelo ID usando o endpoint específico
                cliente = await self.get_cliente_by_id(cliente_id)
                if not cliente:
                    self.logger.error(f"Cliente com ID {cliente_id} não encontrado")
                    return None

                # Preparar os dados da reserva (remove clienteId)
                nova_reserva = {k: v for k, v in reserva_data.items() if k != 'clienteId'}

                # Adicionar a nova reserva ao array reservasVoo do cliente
                if not cliente.get('reservasVoo'):
                    cliente['reservasVoo'] = []
                
                cliente['reservasVoo'].append(nova_reserva)

                # Atualizar o cliente completo no Cosmos DB via PUT
                async with session.put(f"{self.base_url}/clientes/{cliente_id}", json=cliente) as response:
                    if response.status == 200 or response.status == 201:
                        return nova_reserva
                    else:
                        error_text = await response.text()
                        self.logger.error(f"Erro ao atualizar cliente: {response.status} - {error_text}")
                        print(f"ERRO PUT CLIENTE: {response.status} - {error_text}")
                        return None

            except Exception as e:
                self.logger.error(f"Erro na criação de reserva de voo: {e}")
                print(f"ERRO EXCEÇÃO RESERVA VOO: {e}")
                return None

    async def get_cliente_by_id(self, cliente_id: str) -> Optional[Dict]:
        """Busca cliente por ID"""
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(f"{self.base_url}/clientes") as response:
                    if response.status == 200:
                        clientes = await response.json()
                        for cliente in clientes:
                            if cliente.get('id') == cliente_id:
                                return cliente
                        return None
                    else:
                        self.logger.error(f"Erro ao buscar clientes: {response.status}")
                        return None
            except Exception as e:
                self.logger.error(f"Erro na busca de cliente por ID: {e}")
                return None

    async def criar_reserva_hospedagem(self, reserva_data: Dict) -> Optional[Dict]:
        """Cria uma nova reserva de hospedagem adicionando ao array reservasHospedagem do cliente"""
        async with aiohttp.ClientSession() as session:
            try:
                print(f"ENVIANDO DADOS DE HOSPEDAGEM PARA API: {reserva_data}")
                cliente_id = reserva_data.get('clienteId')

                if not cliente_id:
                    self.logger.error("clienteId não fornecido na reserva")
                    return None

                # Buscar o cliente pelo ID
                cliente = await self.get_cliente_by_id(cliente_id)
                if not cliente:
                    self.logger.error(f"Cliente com ID {cliente_id} não encontrado")
                    return None

                # Preparar os dados da reserva (remove clienteId)
                nova_reserva = {k: v for k, v in reserva_data.items() if k != 'clienteId'}

                # Adicionar a nova reserva ao array reservasHospedagem do cliente
                if not cliente.get('reservasHospedagem'):
                    cliente['reservasHospedagem'] = []
                
                cliente['reservasHospedagem'].append(nova_reserva)

                # Atualizar o cliente completo no Cosmos DB via PUT
                async with session.put(f"{self.base_url}/clientes/{cliente_id}", json=cliente) as response:
                    if response.status == 200 or response.status == 201:
                        return nova_reserva
                    else:
                        error_text = await response.text()
                        self.logger.error(f"Erro ao atualizar cliente: {response.status} - {error_text}")
                        print(f"ERRO PUT CLIENTE HOSPEDAGEM: {response.status} - {error_text}")
                        return None

            except Exception as e:
                self.logger.error(f"Erro na criação de reserva de hospedagem: {e}")
                print(f"ERRO EXCEÇÃO RESERVA HOSPEDAGEM: {e}")
                return None

    async def cancelar_reserva_voo(self, cliente_cpf: str, reserva_index: int) -> Optional[Dict]:
        """Cancela uma reserva de voo (muda status para CANCELADA) no array do cliente"""
        async with aiohttp.ClientSession() as session:
            try:
                # Busca o cliente atual pelo CPF
                async with session.get(f"{self.base_url}/clientes") as get_response:
                    if get_response.status == 200:
                        clientes = await get_response.json()
                        cliente = None
                        for c in clientes:
                            if c.get('cpf') == cliente_cpf:
                                cliente = c
                                break

                        if not cliente:
                            self.logger.error(f"Cliente com CPF {cliente_cpf} não encontrado")
                            return None

                        reservas = cliente.get('reservasVoo', [])
                        if not reservas or reserva_index >= len(reservas):
                            self.logger.error(f"Reserva de índice {reserva_index} não encontrada")
                            return None

                        # Atualiza o status da reserva
                        reservas[reserva_index]['status'] = 'CANCELADA'
                        cliente['reservasVoo'] = reservas

                        # Atualiza o cliente usando o ID
                        cliente_id = cliente.get('id')
                        async with session.put(f"{self.base_url}/clientes/{cliente_id}", json=cliente) as put_response:
                            if put_response.status == 200:
                                result = await put_response.json()
                                print(f"RESERVA DE VOO CANCELADA COM SUCESSO: {result}")
                                return result
                            else:
                                error_text = await put_response.text()
                                self.logger.error(f"Erro ao cancelar reserva: {put_response.status} - {error_text}")
                                return None
                    else:
                        self.logger.error(f"Erro ao buscar cliente: {get_response.status}")
                        return None
            except Exception as e:
                self.logger.error(f"Erro na requisição para cancelar reserva de voo: {e}")
                print(f"ERRO EXCEÇÃO CANCELAMENTO VOO: {e}")
                return None

    async def cancelar_reserva_hospedagem(self, cliente_cpf: str, reserva_index: int) -> Optional[Dict]:
        """Cancela uma reserva de hospedagem (muda status para CANCELADA) no array do cliente"""
        async with aiohttp.ClientSession() as session:
            try:
                # Busca o cliente atual pelo CPF
                async with session.get(f"{self.base_url}/clientes") as get_response:
                    if get_response.status == 200:
                        clientes = await get_response.json()
                        cliente = None
                        for c in clientes:
                            if c.get('cpf') == cliente_cpf:
                                cliente = c
                                break

                        if not cliente:
                            self.logger.error(f"Cliente com CPF {cliente_cpf} não encontrado")
                            return None

                        reservas = cliente.get('reservasHospedagem', [])
                        if not reservas or reserva_index >= len(reservas):
                            self.logger.error(f"Reserva de índice {reserva_index} não encontrada")
                            return None

                        # Atualiza o status da reserva
                        reservas[reserva_index]['status'] = 'CANCELADA'
                        cliente['reservasHospedagem'] = reservas

                        # Atualiza o cliente usando o ID
                        cliente_id = cliente.get('id')
                        async with session.put(f"{self.base_url}/clientes/{cliente_id}", json=cliente) as put_response:
                            if put_response.status == 200:
                                result = await put_response.json()
                                print(f"RESERVA DE HOSPEDAGEM CANCELADA COM SUCESSO: {result}")
                                return result
                            else:
                                error_text = await put_response.text()
                                self.logger.error(f"Erro ao cancelar reserva: {put_response.status} - {error_text}")
                                return None
                    else:
                        self.logger.error(f"Erro ao buscar cliente: {get_response.status}")
                        return None
            except Exception as e:
                self.logger.error(f"Erro na requisição para cancelar reserva de hospedagem: {e}")
                print(f"ERRO EXCEÇÃO CANCELAMENTO HOSPEDAGEM: {e}")
                return None