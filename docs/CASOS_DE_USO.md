# Casos de Uso - Chatbot de Reservas

## Visão Geral do Sistema

O Chatbot de Reservas é uma aplicação conversacional que permite aos usuários gerenciar reservas de voos e hospedagem através de uma interface natural de chat. O sistema integra um bot Python com uma API REST Java para operações completas de CRUD.

---

## UC001 - Inicializar Conversa com Chatbot

### Informações Básicas
- **Ator Principal**: Usuário
- **Objetivo**: Estabelecer primeira comunicação com o chatbot
- **Pré-condições**: Chatbot ativo no Bot Framework Emulator
- **Pós-condições**: Menu principal exibido

### Fluxo Principal
1. Usuário inicia conversa digitando qualquer mensagem
2. Sistema verifica se é primeira interação do usuário
3. **[Primeira vez]** Sistema exibe mensagem de boas-vindas completa com explicação das funcionalidades
4. **[Retorno]** Sistema exibe menu simplificado
5. Sistema apresenta opções principais:
   - 🛩️ Consultar Voos
   - 🏨 Consultar Hotéis  
   - ❌ Cancelar Reserva
   - ℹ️ Ajuda

### Fluxos Alternativos
- **FA01 - Solicitação de Ajuda**: Usuário escolhe "ℹAjuda" → Sistema exibe manual completo → Retorna ao menu

### Exceções
- Não aplicável para este caso de uso

---

## UC002 - Cadastrar Novo Cliente

### Informações Básicas
- **Ator Principal**: Usuário novo
- **Objetivo**: Registrar dados pessoais no sistema para utilizar os serviços
- **Pré-condições**: CPF não cadastrado no sistema
- **Pós-condições**: Cliente criado na base de dados com ID único

### Fluxo Principal
1. Sistema detecta CPF não cadastrado durante verificação
2. Sistema informa: "🔍 CPF não encontrado no sistema. Vamos fazer seu cadastro!"
3. Sistema solicita **Nome completo**
4. Usuário informa nome
5. Sistema solicita **Email**
6. Usuário informa email
7. Sistema solicita **Telefone**
8. Usuário informa telefone
9. Sistema compila dados:
   ```json
   {
     "nome": "string",
     "email": "string",
     "telefone": "string", 
     "cpf": "string (já coletado)"
   }
   ```
10. Sistema envia `POST /clientes` para API
11. **[Sucesso]** API retorna cliente criado com ID
12. Sistema exibe: "Cadastro realizado com sucesso!"
13. Sistema prossegue para menu de operações

### Fluxos Alternativos
- **FA01 - Usuário cancela**: Em qualquer etapa, usuário pode cancelar → Retorna ao menu principal

### Exceções
- **EX01 - Erro na API**: Falha na criação → "Erro ao criar cadastro. Tente novamente" → Retorna ao menu

---

## UC003 - Autenticar Cliente Existente

### Informações Básicas
- **Ator Principal**: Cliente cadastrado
- **Objetivo**: Validar identidade para acessar operações pessoais
- **Pré-condições**: Cliente possui CPF cadastrado
- **Pós-condições**: Cliente autenticado e dados carregados

### Fluxo Principal
1. Sistema solicita: "Por favor, informe seu CPF para acessar o sistema"
2. Usuário informa CPF (formato: XXX.XXX.XXX-XX)
3. Sistema executa `GET /clientes/cpf/{cpf}`
4. **[Cliente encontrado]** API retorna dados do cliente
5. Sistema carrega informações na sessão
6. Sistema exibe: "Olá, {nome}! O que você gostaria de fazer?"
7. Sistema prossegue para menu de operações

### Fluxos Alternativos
- **FA01 - CPF não encontrado**: Cliente não existe → Inicia UC002 (Cadastrar Novo Cliente)

### Exceções
- **EX01 - Erro de conexão**: Falha na API → "❌ Erro de conexão. Tente novamente"
- **EX02 - CPF inválido**: Formato incorreto → Solicita novamente

---

## UC004 - Criar Reserva de Voo

### Informações Básicas
- **Ator Principal**: Cliente autenticado
- **Objetivo**: Reservar passagem aérea com dados específicos
- **Pré-condições**: Cliente autenticado no sistema
- **Pós-condições**: Reserva de voo criada com status CONFIRMADA

### Fluxo Principal
1. Cliente no menu de voos escolhe "➕ Fazer nova reserva"
2. Sistema solicita **Cidade de origem**
3. Cliente informa origem (ex: "São Paulo")
4. Sistema solicita **Cidade de destino** 
5. Cliente informa destino (ex: "Rio de Janeiro")
6. Sistema solicita **Data de partida** (formato DD/MM/AAAA)
7. Cliente informa data (ex: "15/12/2025")
8. Sistema pergunta: "Esta viagem é de ida e volta?"
9. **[Ida e volta]** Cliente confirma → Sistema solicita **Data de volta**
10. **[Somente ida]** Cliente nega → Prossegue para próximo passo
11. Sistema oferece **Classes**: Econômica | Executiva | Primeira Classe
12. Cliente seleciona classe
13. Sistema solicita **Número de passageiros**
14. Cliente informa quantidade (ex: "2")
15. Sistema compila dados da reserva:
    ```json
    {
      "origem": "São Paulo",
      "destino": "Rio de Janeiro",
      "dataHoraPartida": "15/12/2025 08:00",
      "dataHoraChegada": "15/12/2025 09:30",
      "dataHoraVolta": "16/12/2025 18:00", // se ida e volta
      "classe": "Econômica",
      "numeroPassageiros": 2,
      "companhiaAerea": "LATAM Airlines",
      "numeroVoo": "LA1234",
      "preco": 500.0,
      "status": "CONFIRMADA",
      "clienteId": 1
    }
    ```
16. Sistema executa `POST /api/reservas-voo`
17. **[Sucesso]** Sistema exibe confirmação com código da reserva

### Fluxos Alternativos
- **FA01 - Somente ida**: No passo 9, cliente escolhe apenas ida → Pula coleta de data de volta
- **FA02 - Cancelar reserva**: Cliente pode cancelar em qualquer etapa → Retorna ao menu

### Exceções
- **EX01 - Data inválida**: Formato incorreto → Solicita nova data
- **EX02 - Erro na API**: Falha na criação → "❌ Erro ao criar reserva"

---

## UC005 - Criar Reserva de Hospedagem

### Informações Básicas
- **Ator Principal**: Cliente autenticado  
- **Objetivo**: Reservar acomodação hoteleira
- **Pré-condições**: Cliente autenticado no sistema
- **Pós-condições**: Reserva de hotel criada com status CONFIRMADA

### Fluxo Principal
1. Cliente no menu de hotéis escolhe "➕ Fazer nova reserva"
2. Sistema solicita **Cidade de destino**
3. Cliente informa cidade (ex: "Rio de Janeiro")
4. Sistema solicita **Data de check-in** (formato DD/MM/AAAA)
5. Cliente informa data (ex: "20/12/2025")
6. Sistema solicita **Data de check-out** (formato DD/MM/AAAA)
7. Cliente informa data (ex: "22/12/2025")
8. Sistema solicita **Número de hóspedes**
9. Cliente informa quantidade (ex: "2")
10. Sistema oferece **Tipos de quarto**: Standard | Deluxe | Suíte | Suíte Premium
11. Cliente seleciona tipo
12. Sistema compila dados da reserva:
    ```json
    {
      "nomeHotel": "Hotel Rio de Janeiro Plaza",
      "cidade": "Rio de Janeiro",
      "dataCheckIn": "20/12/2025",
      "dataCheckOut": "22/12/2025",
      "numeroHospedes": 2,
      "tipoQuarto": "Deluxe",
      "precoTotal": 400.0,
      "status": "CONFIRMADA", 
      "clienteId": 1
    }
    ```
13. Sistema executa `POST /api/reservas-hospedagem`
14. **[Sucesso]** Sistema exibe confirmação com código da reserva

### Fluxos Alternativos
- **FA01 - Alterar dados**: Cliente pode corrigir informações antes da confirmação

### Exceções
- **EX01 - Datas inválidas**: Check-out anterior ao check-in → Solicita correção
- **EX02 - Erro na API**: Falha na criação → "❌ Erro ao criar reserva"

---

## UC006 - Consultar Minhas Reservas

### Informações Básicas
- **Ator Principal**: Cliente autenticado
- **Objetivo**: Visualizar reservas pessoais (voos e/ou hotéis)
- **Pré-condições**: Cliente autenticado
- **Pós-condições**: Lista de reservas exibida

### Fluxo Principal
1. Cliente no menu de operações escolhe "📋 Minhas reservas"
2. **[Contexto: Voos]** Sistema executa `GET /api/reservas-voo/cliente/{id}`
3. **[Contexto: Hotéis]** Sistema executa `GET /api/reservas-hospedagem/cliente/{id}`
4. **[Reservas encontradas]** Sistema formata e exibe:
   ```
   ✈️ Suas reservas de voo, João Silva:
   
   ✅ Reserva 1:
   • Rota: São Paulo → Rio de Janeiro
   • Data de Partida: 15/12/2025 08:00
   • Classe: Econômica
   • Passageiros: 2
   • Status: CONFIRMADA
   ```
5. Sistema retorna automaticamente ao menu principal

### Fluxos Alternativos
- **FA01 - Nenhuma reserva**: Lista vazia → "📭 Você não possui reservas no momento"

### Exceções
- **EX01 - Erro na API**: Falha na consulta → "❌ Erro ao consultar reservas"

---

## UC007 - Buscar Reservas Disponíveis

### Informações Básicas
- **Ator Principal**: Cliente autenticado
- **Objetivo**: Visualizar todas as reservas do sistema (marketplace)
- **Pré-condições**: Cliente autenticado
- **Pós-condições**: Lista geral de reservas exibida

### Fluxo Principal
1. Cliente escolhe "🔍 Buscar {voos/hotéis} disponíveis"
2. **[Voos]** Sistema executa `GET /api/reservas-voo`
3. **[Hotéis]** Sistema executa `GET /api/reservas-hospedagem`
4. Sistema filtra reservas por status "CONFIRMADA"
5. Sistema exibe lista formatada com informações públicas
6. Sistema retorna ao menu principal

### Fluxos Alternativos
- **FA01 - Lista vazia**: Nenhuma reserva disponível → Informa ausência de opções

### Exceções
- **EX01 - Erro na API**: Falha na consulta → Mensagem de erro

---

## UC008 - Cancelar Reserva

### Informações Básicas
- **Ator Principal**: Cliente autenticado
- **Objetivo**: Cancelar reserva existente alterando status para CANCELADA
- **Pré-condições**: Cliente possui reserva com status CONFIRMADA
- **Pós-condições**: Reserva alterada para status CANCELADA

### Fluxo Principal
1. Cliente no menu principal escolhe "❌ Cancelar Reserva"
2. Sistema solicita CPF para verificação
3. Cliente informa CPF
4. Sistema executa `GET /clientes/cpf/{cpf}` para validar
5. Sistema oferece tipos: "Reservas de Voo" | "Reservas de Hospedagem"
6. Cliente seleciona tipo
7. Sistema busca reservas ativas do cliente
8. **[Reservas encontradas]** Sistema lista opções numeradas:
   ```
   Suas reservas ativas:
   
   Reserva 1: São Paulo → Rio de Janeiro (15/12/2025)
   Reserva 2: Rio de Janeiro → São Paulo (20/12/2025)
   ```
9. Cliente seleciona reserva específica
10. Sistema solicita confirmação: "⚠️ Confirma cancelamento?"
11. **[Confirmado]** Sistema executa `PATCH /api/reservas-{tipo}/{id}/cancelar`
12. API atualiza status para "CANCELADA"
13. Sistema exibe: "✅ Reserva cancelada com sucesso!"

### Fluxos Alternativos
- **FA01 - Cancelar operação**: Cliente pode cancelar em qualquer etapa
- **FA02 - Nenhuma reserva ativa**: Lista vazia → Informa que não há reservas para cancelar

### Exceções
- **EX01 - Reserva não encontrada**: ID inválido → "❌ Reserva não localizada"
- **EX02 - Erro na API**: Falha no cancelamento → "❌ Erro ao cancelar reserva"

---

## UC009 - Solicitar Ajuda

### Informações Básicas
- **Ator Principal**: Usuário
- **Objetivo**: Obter informações sobre como usar o chatbot
- **Pré-condições**: Nenhuma
- **Pós-condições**: Manual de uso exibido

### Fluxo Principal
1. Usuário no menu principal escolhe "ℹ️ Ajuda"
2. Sistema exibe manual completo:
   ```
   ℹ️ Central de Ajuda - Bot de Reservas
   
   Como usar o bot:
   1️⃣ Selecione uma opção no menu principal
   2️⃣ Informe seu CPF quando solicitado
   3️⃣ Siga as instruções para cada operação
   
   Funcionalidades disponíveis:
   • Consultar e criar reservas de voo
   • Consultar e criar reservas de hotel
   • Cancelar reservas existentes
   • Visualizar reservas disponíveis
   
   Formatos aceitos:
   • CPF: XXX.XXX.XXX-XX
   • Data: DD/MM/AAAA
   • Números: Digite apenas números
   ```
3. Sistema retorna automaticamente ao menu principal

### Fluxos Alternativos
- Não aplicável

### Exceções
- Não aplicável

---

## Matriz de Rastreabilidade

| Requisito Funcional | Casos de Uso Relacionados |
|-------------------|---------------------------|
| RF01 - Autenticação por CPF | UC002, UC003 |
| RF02 - Cadastro de cliente | UC002 |
| RF03 - Reserva de voo | UC004 |
| RF04 - Reserva de hotel | UC005 |
| RF05 - Consulta de reservas | UC006 |
| RF06 - Cancelamento | UC008 |
| RF07 - Busca geral | UC007 |
| RF08 - Interface conversacional | UC001, UC009 |

## Regras de Negócio

### RN001 - Identificação Única
- Todo cliente deve possuir CPF único no sistema
- Não é permitido cadastro duplicado de CPF

### RN002 - Status de Reserva
- Reservas são criadas com status "CONFIRMADA"
- Cancelamento altera status para "CANCELADA"
- Reservas canceladas não podem ser reativadas

### RN003 - Dados Obrigatórios
- **Cliente**: Nome, CPF, Email, Telefone
- **Voo**: Origem, Destino, Data partida, Classe, Passageiros
- **Hotel**: Cidade, Check-in, Check-out, Hóspedes, Tipo quarto

### RN004 - Geração Automática
- Códigos de voo: Padrão "LA" + 4 dígitos aleatórios
- Nomes de hotel: "Hotel {cidade} Plaza" 
- Preços: Voo R$ 500,00 | Hotel R$ 200,00 por diária

### RN005 - Validação de Datas
- Check-out deve ser posterior ao check-in
- Datas devem estar no formato DD/MM/AAAA
- Não há validação de datas futuras (permite teste)

## Requisitos Não Funcionais

### Performance
- **RNF001**: Tempo de resposta da API ≤ 2 segundos
- **RNF002**: Suporte a múltiplas conversas simultâneas

### Usabilidade  
- **RNF003**: Interface conversacional intuitiva
- **RNF004**: Mensagens de erro claras e acionáveis
- **RNF005**: Emojis para melhor experiência visual

### Integração
- **RNF006**: Comunicação via HTTP REST
- **RNF007**: Dados persistidos em banco relacional
- **RNF008**: CORS habilitado para integração

### Confiabilidade
- **RNF009**: Tratamento de erros em todas as operações
- **RNF010**: Log de transações para auditoria

---

**Documento criado em**: Outubro 2025  
**Versão**: 1.0  
**Status**: Casos de uso implementados e testados  
**Cobertura**: 100% das funcionalidades principais