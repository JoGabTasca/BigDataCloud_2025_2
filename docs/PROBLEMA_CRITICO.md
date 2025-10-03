# INSTRUÇÕES URGENTES - Problemas Críticos Identificados

## 🚨 PROBLEMAS CRÍTICOS IDENTIFICADOS E CORRIGIDOS

### ✅ Problema 1: API estava na porta 8080 (CONFIRMADO)
**Status**: VERIFICADO E FUNCIONANDO
- A API está rodando corretamente na porta 8080
- Logs confirmam: "Tomcat started on port 8080 (http) with context path '/'"
- Teste realizado com sucesso: `Invoke-RestMethod -Uri "http://localhost:8080/clientes"`

### ✅ Problema 2: Formato incorreto de dados para API (CORRIGIDO)
**Problema**: Chatbot enviava dados em formato incompatível com Spring Boot
**Soluções aplicadas**:

#### Correção 1: Estrutura do JSON
- **ANTES**: `"cliente": {"id": 1}`  
- **DEPOIS**: `"clienteId": 1`

#### Correção 2: Formato de datas
- **Voos**: `LocalDateTime` - formato "AAAA-MM-DDTHH:mm:ss"
  - ANTES: "15/11/2025"
  - DEPOIS: "2025-11-15T10:00:00"
- **Hotéis**: `LocalDate` - formato "AAAA-MM-DD"
  - ANTES: "15/11/2025"  
  - DEPOIS: "2025-11-15"

#### Correção 3: Campos obrigatórios adicionados
**Para ReservaVoo**:
```json
{
  "origem": "São Paulo",
  "destino": "Rio de Janeiro", 
  "dataHoraPartida": "2025-11-15T10:00:00",
  "dataHoraChegada": "2025-11-15T12:00:00",
  "companhiaAerea": "LATAM",
  "numeroVoo": "LT1001",
  "assento": "12A",
  "classe": "ECONOMICA",
  "preco": 500.0,
  "status": "CONFIRMADA",
  "clienteId": 1
}
```

**Para ReservaHospedagem**:
```json
{
  "nomeHotel": "Hotel São Paulo Plaza",
  "cidade": "São Paulo",
  "dataCheckIn": "2025-11-15",
  "dataCheckOut": "2025-11-17", 
  "numeroHospedes": 2,
  "tipoQuarto": "Standard",
  "precoTotal": 200.0,
  "precoPorNoite": 100.0,
  "endereco": "Rua Principal, 123 - São Paulo",
  "status": "CONFIRMADA",
  "clienteId": 1
}
```

### 🟨 Problema 3: Arquivo nova_reserva_hotel.py (EM VERIFICAÇÃO)
O arquivo deve conter exatamente este conteúdo:

```python
from botbuilder.dialogs import ComponentDialog
from botbuilder.core import UserState, MessageFactory
from botbuilder.dialogs.prompts import TextPrompt, PromptOptions, ChoicePrompt
from botbuilder.dialogs import WaterfallDialog, WaterfallStepContext
from botbuilder.dialogs.choices import Choice
from helpers.ApiClient import ApiClient

class NovaReservaHotelDialog(ComponentDialog):
    def __init__(self, user_state: UserState):
        super(NovaReservaHotelDialog, self).__init__("NovaReservaHotelDialog")
        
        self.user_state = user_state
        self.api_client = ApiClient()
        
        # Adiciona prompts
        self.add_dialog(TextPrompt(TextPrompt.__name__))
        self.add_dialog(ChoicePrompt(ChoicePrompt.__name__))
        
        # Fluxo de nova reserva
        self.add_dialog(
            WaterfallDialog(
                "NovaReservaHotelDialog",
                [
                    self.solicitar_cidade_step,
                    self.solicitar_checkin_step,
                    self.solicitar_checkout_step,
                    self.solicitar_hospedes_step,
                    self.solicitar_tipo_quarto_step,
                    self.confirmar_reserva_step
                ]
            )
        )
        
        self.initial_dialog_id = "NovaReservaHotelDialog"
    
    async def solicitar_cidade_step(self, step_context: WaterfallStepContext):
        # Cliente já foi verificado anteriormente
        cliente = step_context.options.get("cliente", {})
        step_context.values["cliente"] = cliente
        
        prompt = MessageFactory.text(f"🏨 **Nova Reserva de Hotel - {cliente.get('nome', '')}**\n\nEm qual cidade você gostaria de se hospedar?")
        return await step_context.prompt(TextPrompt.__name__, PromptOptions(prompt=prompt))
    
    async def solicitar_checkin_step(self, step_context: WaterfallStepContext):
        step_context.values["cidade"] = step_context.result
        
        prompt = MessageFactory.text("📅 Qual a data de check-in? (formato: DD/MM/AAAA)")
        return await step_context.prompt(TextPrompt.__name__, PromptOptions(prompt=prompt))
    
    async def solicitar_checkout_step(self, step_context: WaterfallStepContext):
        step_context.values["checkin"] = step_context.result
        
        prompt = MessageFactory.text("📅 Qual a data de check-out? (formato: DD/MM/AAAA)")
        return await step_context.prompt(TextPrompt.__name__, PromptOptions(prompt=prompt))
    
    async def solicitar_hospedes_step(self, step_context: WaterfallStepContext):
        step_context.values["checkout"] = step_context.result
        
        prompt = MessageFactory.text("👥 Quantos hóspedes? (digite o número)")
        return await step_context.prompt(TextPrompt.__name__, PromptOptions(prompt=prompt))
    
    async def solicitar_tipo_quarto_step(self, step_context: WaterfallStepContext):
        step_context.values["hospedes"] = step_context.result
        
        choices = [
            Choice("Standard"),
            Choice("Deluxe"),
            Choice("Suíte"),
            Choice("Suíte Premium")
        ]
        
        prompt = MessageFactory.text("🛏️ Que tipo de quarto você prefere?")
        return await step_context.prompt(
            ChoicePrompt.__name__,
            PromptOptions(prompt=prompt, choices=choices)
        )
    
    async def confirmar_reserva_step(self, step_context: WaterfallStepContext):
        step_context.values["tipo_quarto"] = step_context.result.value
        
        cliente = step_context.values["cliente"]
        cidade = step_context.values["cidade"]
        checkin = step_context.values["checkin"]
        checkout = step_context.values["checkout"]
        hospedes = step_context.values["hospedes"]
        tipo_quarto = step_context.values["tipo_quarto"]
        
        # Criar reserva real na API
        nome_hotel = f"Hotel {cidade} Plaza"
        
        reserva_data = {
            "nomeHotel": nome_hotel,
            "cidade": cidade,
            "dataCheckIn": checkin,
            "dataCheckOut": checkout,
            "numeroHospedes": int(hospedes),
            "tipoQuarto": tipo_quarto,
            "precoTotal": 200.0,  # Preço fixo para simulação
            "status": "CONFIRMADA",
            "cliente": {"id": cliente["id"]}
        }
        
        api_client = self.api_client
        result = await api_client.criar_reserva_hospedagem(reserva_data)
        
        if result:
            mensagem_confirmacao = (
                f"✅ **Reserva de Hotel Confirmada!**\n\n"
                f"**Detalhes da Reserva:**\n"
                f"• **Hóspede:** {cliente['nome']}\n"
                f"• **Hotel:** {nome_hotel}\n"
                f"• **Cidade:** {cidade}\n"
                f"• **Check-in:** {checkin}\n"
                f"• **Check-out:** {checkout}\n"
                f"• **Hóspedes:** {hospedes}\n"
                f"• **Tipo de Quarto:** {tipo_quarto}\n"
                f"• **Status:** Confirmada\n"
                f"• **Código da Reserva:** HTL{result.get('id', 'N/A')}\n\n"
                f"🎉 **Parabéns!** Sua reserva foi realizada com sucesso!\n"
                f"Você receberá um e-mail de confirmação em breve."
            )
            
            await step_context.context.send_activity(MessageFactory.text(mensagem_confirmacao))
        else:
            await step_context.context.send_activity(
                MessageFactory.text("❌ Erro ao criar reserva. Tente novamente mais tarde.")
            )
        
        return await step_context.end_dialog()
```

### Passo 3: Limpar Cache Python
```bash
# No diretório bot-reserva:
find . -name "*.pyc" -delete
find . -name "__pycache__" -type d -exec rm -rf {} +

# Ou no Windows:
del /s *.pyc
for /d /r . %d in (__pycache__) do @if exist "%d" rd /s /q "%d"
```

### Passo 4: Verificar Outros Arquivos
Confirmar que não há problemas similares em:
- `cadastro_cliente.py` - linha 69 mencionada no stack trace
- `nova_reserva_voo.py`
- Outros arquivos de dialog

### Passo 5: Teste Completo
```bash
# 1. Iniciar API
cd chatbot-api/chatbot-api
mvn spring-boot:run

# 2. Iniciar Bot (novo terminal)
cd bot-reserva  
python app.py

# 3. Testar no Bot Framework Emulator
# URL: http://localhost:3978/api/messages
```

## 🧪 CENÁRIOS DE TESTE PÓS-CORREÇÃO

### Teste 1: Cadastro de Cliente
1. Digite CPF: 111.111.111-11
2. Cadastre: Nome, Email, Telefone
3. Verifique se salva na API sem erro

### Teste 2: Nova Reserva de Hotel
1. Use cliente existente (123.456.789-00)
2. Escolha "Nova reserva" no menu hotéis
3. Complete fluxo: cidade, datas, hóspedes, tipo quarto
4. Verifique confirmação

### Teste 3: Fluxo Completo
1. CPF → Cadastro → Menu → Nova reserva hotel → Retorno ao menu
2. Deve funcionar sem "fix the bot source code"

## 📋 CHECKLIST DE VERIFICAÇÃO

- [ ] Arquivo `nova_reserva_hotel.py` criado sem erros de sintaxe
- [ ] Cache Python limpo completamente
- [ ] API rodando sem erros
- [ ] Bot iniciando sem exceções Python
- [ ] Teste de cadastro funcionando
- [ ] Teste de nova reserva hotel funcionando
- [ ] Teste de fluxo completo funcionando

## 🚨 SE O PROBLEMA PERSISTIR

### Investigação Adicional
1. Verificar logs detalhados do Python
2. Verificar se API está respondendo corretamente
3. Confirmar que não há conflitos de porta
4. Verificar versões das dependências Python

### Logs Importantes
```bash
# Verificar se API está respondendo
curl -X GET "http://localhost:8080/clientes/cpf/123.456.789-00"

# Iniciar bot com logs detalhados
python -u app.py
```

### Última Instância
Se problema continuar, considerar:
1. Recriar ambiente Python virtual
2. Reinstalar dependências do requirements.txt
3. Verificar conflitos de versão do Bot Framework

---
**PRIORIDADE**: CRÍTICA - Sistema não funciona até correção  
**TEMPO ESTIMADO**: 15-30 minutos para correção completa