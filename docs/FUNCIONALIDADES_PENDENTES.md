# 📋 FUNCIONALIDADES PENDENTES - CHATBOT RESERVAS

## 🎯 STATUS ATUAL DO PROJETO

### ✅ IMPLEMENTADO E FUNCIONANDO
- **Backend API Java (Spring Boot)**: Rodando na porta 8080
- **Estrutura do Bot Python**: Bot Framework configurado
- **Cadastro de Clientes**: Integração completa com API Java
- **Reservas de Voo**: Criação funcionando com API Java
- **Reservas de Hospedagem**: Criação funcionando com API Java
- **Cancelamento de Reservas**: Código implementado (precisa ser testado)

### 🔍 VERIFICAÇÕES OBRIGATÓRIAS

#### 1. VERIFICAR USO CORRETO DA API JAVA
**⚠️ CRÍTICO**: O bot DEVE usar EXCLUSIVAMENTE a API Java (porta 8080)

**Comandos para verificar:**
```bash
# 1. Verificar se API Java está rodando
curl http://localhost:8080/clientes

# 2. Verificar endpoints de reservas
curl http://localhost:8080/api/reservas-voo
curl http://localhost:8080/api/reservas-hospedagem

# 3. Testar cancelamento
Invoke-WebRequest -Uri "http://localhost:8080/api/reservas-voo/1/cancelar" -Method PATCH
```

**Arquivos para revisar:**
- `bot-reserva/helpers/ApiClient.py` → Verificar se `base_url = "http://localhost:8080"`
- Todos os diálogos devem usar `self.api_client` que aponta para a API Java

---

## 🚧 FUNCIONALIDADES PENDENTES

### 1. **TESTE COMPLETO DO CANCELAMENTO**
**Status**: Código implementado, precisa ser testado
**Prioridade**: 🔴 ALTA

**O que fazer:**
- [ ] Executar o bot Python: `cd bot-reserva && python app.py`
- [ ] Testar fluxo completo de cancelamento
- [ ] Verificar se CPF 123.456.789-00 ou 987.654.321-00 funcionam
- [ ] Confirmar se o status da reserva muda para "CANCELADA" na API

**Arquivos envolvidos:**
- `dialogs/cancelar_reserva.py` → Dialog de cancelamento
- `helpers/ApiClient.py` → Métodos `cancelar_reserva_voo()` e `cancelar_reserva_hospedagem()`

### 2. **VALIDAÇÃO DE DADOS E TRATAMENTO DE ERROS**
**Status**: Parcialmente implementado
**Prioridade**: 🟡 MÉDIA

**Melhorias necessárias:**
- [ ] Validação de CPF no formato correto
- [ ] Tratamento de datas inválidas
- [ ] Validação de emails
- [ ] Mensagens de erro mais amigáveis
- [ ] Timeout para chamadas API

### 3. **FUNCIONALIDADES ADICIONAIS DO CHATBOT**
**Status**: Não implementado
**Prioridade**: 🟢 BAIXA

**Novas funcionalidades:**
- [ ] **Consultar Status de Reserva**: Buscar reserva por ID ou CPF
- [ ] **Alterar Reserva**: Modificar datas, horários, quartos
- [ ] **Histórico de Reservas**: Mostrar todas as reservas do cliente
- [ ] **Suporte/Ajuda**: Menu de ajuda e contato

### 4. **MELHORIAS DE UX/UI**
**Status**: Básico implementado
**Prioridade**: 🟢 BAIXA

**Melhorias:**
- [ ] Cards mais visuais para exibir reservas
- [ ] Botões de ação rápida
- [ ] Confirmações antes de ações críticas (cancelar)
- [ ] Progress indicators para operações longas
- [ ] Emojis e formatação melhorada

### 5. **CONFIGURAÇÃO E DEPLOY**
**Status**: Desenvolvimento local apenas
**Prioridade**: 🟡 MÉDIA

**Necessário para produção:**
- [ ] Configurar variáveis de ambiente
- [ ] Configurar HTTPS para produção
- [ ] Configurar banco de dados persistente (não H2)
- [ ] Configurar logs adequados
- [ ] Documentação de instalação e execução

---

## 🧪 PLANO DE TESTES

### Teste 1: Verificar Integração API Java
```bash
# No terminal PowerShell:
cd "c:\Users\jg\Documents\IBMEC\5p\ibmec-bigdata-20252\bot-reserva"
python app.py
```

**Cenários de teste:**
1. **Cadastro de Cliente**: Criar novo cliente e verificar na API
2. **Reserva de Voo**: Criar reserva e verificar persistência
3. **Reserva de Hospedagem**: Criar reserva e verificar persistência
4. **Cancelamento**: Cancelar reserva e verificar mudança de status

### Teste 2: Validar Dados da API
```bash
# Verificar dados de teste disponíveis:
curl http://localhost:8080/clientes
curl http://localhost:8080/api/reservas-voo/cliente/1
curl http://localhost:8080/api/reservas-hospedagem/cliente/1
```

---

## 🔧 CONFIGURAÇÃO ATUAL

### API Java (Backend)
- **URL**: http://localhost:8080
- **Banco**: H2 (in-memory)
- **Status**: ✅ Funcionando
- **Dados de teste**: Clientes com CPF 123.456.789-00 e 987.654.321-00

### Bot Python (Frontend)
- **Framework**: Microsoft Bot Framework
- **Porta**: 3978 (padrão)
- **Integração**: AIOHTTP → API Java
- **Status**: ⚠️ Precisa ser testado

### Endpoints Principais da API Java
```
GET    /clientes                                    # Listar clientes
GET    /clientes/{id}                              # Buscar cliente por ID
POST   /clientes                                   # Criar cliente

GET    /api/reservas-voo                           # Listar voos
GET    /api/reservas-voo/cliente/{clienteId}       # Voos por cliente
POST   /api/reservas-voo                           # Criar reserva voo
PATCH  /api/reservas-voo/{id}/cancelar             # Cancelar voo

GET    /api/reservas-hospedagem                    # Listar hospedagens
GET    /api/reservas-hospedagem/cliente/{clienteId} # Hospedagens por cliente
POST   /api/reservas-hospedagem                    # Criar reserva hospedagem
PATCH  /api/reservas-hospedagem/{id}/cancelar      # Cancelar hospedagem
```

---

## ⚠️ PONTOS DE ATENÇÃO

1. **SEMPRE usar API Java**: Nunca usar endpoints Python ou outras APIs
2. **Verificar conexão**: Antes de testar bot, confirmar que API Java está rodando
3. **Dados de teste**: Usar CPFs 123.456.789-00 ou 987.654.321-00 para testes
4. **Formato de datas**: API Java espera ISO 8601 (ex: 2025-11-15T08:30:00)
5. **Status das reservas**: "CONFIRMADA", "CANCELADA", etc.

---

## 📞 PRÓXIMOS PASSOS

1. **IMEDIATO**: Testar cancelamento de reservas
2. **CURTO PRAZO**: Implementar validações e tratamento de erros
3. **MÉDIO PRAZO**: Adicionar funcionalidades extras (consulta, alteração)
4. **LONGO PRAZO**: Preparar para produção

---

*Documento atualizado em: 01/10/2025*
*Status do projeto: 70% completo - Core functionality implementada*