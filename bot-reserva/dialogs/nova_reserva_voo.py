from botbuilder.dialogs import ComponentDialog
from botbuilder.core import UserState, MessageFactory
from botbuilder.dialogs.prompts import TextPrompt, PromptOptions, ChoicePrompt
from botbuilder.dialogs import WaterfallDialog, WaterfallStepContext
from botbuilder.dialogs.choices import Choice
from helpers.ApiClient import ApiClient

class NovaReservaVooDialog(ComponentDialog):
    def __init__(self, user_state: UserState):
        super(NovaReservaVooDialog, self).__init__("NovaReservaVooDialog")
        
        self.user_state = user_state
        self.api_client = ApiClient()
        
        # Adiciona prompts
        self.add_dialog(TextPrompt(TextPrompt.__name__))
        self.add_dialog(ChoicePrompt(ChoicePrompt.__name__))
        
        # Fluxo de nova reserva
        self.add_dialog(
            WaterfallDialog(
                "NovaReservaVooDialog",
                [
                    self.solicitar_origem_step,
                    self.solicitar_destino_step,
                    self.solicitar_data_partida_step,
                    self.solicitar_data_volta_step,
                    self.solicitar_classe_step,
                    self.solicitar_passageiros_step,
                    self.confirmar_reserva_step
                ]
            )
        )
        
        self.initial_dialog_id = "NovaReservaVooDialog"
    
    async def solicitar_origem_step(self, step_context: WaterfallStepContext):
        # Cliente já foi verificado anteriormente
        cliente = step_context.options.get("cliente", {})
        step_context.values["cliente"] = cliente
        
        prompt = MessageFactory.text(f"✈️ **Nova Reserva de Voo - {cliente.get('nome', '')}**\n\nDe qual cidade você gostaria de partir?")
        return await step_context.prompt(TextPrompt.__name__, PromptOptions(prompt=prompt))
    
    async def solicitar_destino_step(self, step_context: WaterfallStepContext):
        step_context.values["origem"] = step_context.result
        
        prompt = MessageFactory.text("🌍 Para qual cidade você gostaria de viajar?")
        return await step_context.prompt(TextPrompt.__name__, PromptOptions(prompt=prompt))
    
    async def solicitar_data_partida_step(self, step_context: WaterfallStepContext):
        step_context.values["destino"] = step_context.result
        
        prompt = MessageFactory.text("📅 Qual a data de partida? (formato: DD/MM/AAAA)")
        return await step_context.prompt(TextPrompt.__name__, PromptOptions(prompt=prompt))
    
    async def solicitar_data_volta_step(self, step_context: WaterfallStepContext):
        step_context.values["data_partida"] = step_context.result
        
        choices = [
            Choice("Sim, ida e volta"),
            Choice("Não, só ida")
        ]
        
        prompt = MessageFactory.text("🔄 Sua viagem é ida e volta?")
        return await step_context.prompt(
            ChoicePrompt.__name__,
            PromptOptions(prompt=prompt, choices=choices)
        )
    
    async def solicitar_classe_step(self, step_context: WaterfallStepContext):
        escolha_volta = step_context.result.value
        step_context.values["ida_volta"] = escolha_volta
        
        if escolha_volta == "Sim, ida e volta":
            prompt = MessageFactory.text("📅 Qual a data de volta? (formato: DD/MM/AAAA)")
            return await step_context.prompt(TextPrompt.__name__, PromptOptions(prompt=prompt))
        else:
            step_context.values["data_volta"] = None
            return await self._escolher_classe(step_context)
    
    async def solicitar_passageiros_step(self, step_context: WaterfallStepContext):
        # Se a resposta anterior foi uma data (ida e volta), salva a data de volta
        if step_context.values["ida_volta"] == "Sim, ida e volta":
            step_context.values["data_volta"] = step_context.result
            return await self._escolher_classe(step_context)
        else:
            # Se chegou aqui, a classe já foi escolhida
            step_context.values["classe"] = step_context.result.value
            
            prompt = MessageFactory.text("👥 Quantos passageiros? (digite o número)")
            return await step_context.prompt(TextPrompt.__name__, PromptOptions(prompt=prompt))
    
    async def confirmar_reserva_step(self, step_context: WaterfallStepContext):
        # Se ainda não temos a classe, significa que acabamos de escolher
        if "classe" not in step_context.values:
            step_context.values["classe"] = step_context.result.value
            prompt = MessageFactory.text("👥 Quantos passageiros? (digite o número)")
            return await step_context.prompt(TextPrompt.__name__, PromptOptions(prompt=prompt))
        else:
            # Temos todos os dados, criar reserva na API
            step_context.values["passageiros"] = step_context.result
            
            cliente = step_context.values["cliente"]
            origem = step_context.values["origem"]
            destino = step_context.values["destino"]
            data_partida = step_context.values["data_partida"]
            data_volta = step_context.values.get("data_volta", "Não informada")
            classe = step_context.values["classe"]
            passageiros = step_context.values["passageiros"]
            
            # Converter data do formato DD/MM/AAAA para AAAA-MM-DDTHH:mm:ss
            def converter_data(data_str):
                if data_str and data_str != "Não informada":
                    try:
                        # Converte DD/MM/AAAA para AAAA-MM-DDTHH:mm:ss
                        dia, mes, ano = data_str.split('/')
                        return f"{ano}-{mes.zfill(2)}-{dia.zfill(2)}T10:00:00"
                    except:
                        return "2025-12-01T10:00:00"  # Data padrão
                return "2025-12-01T10:00:00"
            
            # Criar reserva na API
            reserva_data = {
                "origem": origem,
                "destino": destino,
                "dataHoraPartida": converter_data(data_partida),
                "dataHoraChegada": converter_data(data_volta) if data_volta != "Não informada" else converter_data(data_partida),
                "companhiaAerea": "LATAM",
                "numeroVoo": "LT1001",
                "assento": "12A",
                "classe": classe.upper(),
                "preco": 500.0,
                "status": "CONFIRMADA",
                "clienteId": cliente["id"]
            }
            
            api_client = self.api_client
            result = await api_client.criar_reserva_voo(reserva_data)
            
            if result:
                mensagem_confirmacao = (
                    f"✅ **Reserva de Voo Confirmada!**\n\n"
                    f"**Detalhes da Reserva:**\n"
                    f"• **Passageiro:** {cliente['nome']}\n"
                    f"• **Rota:** {origem} → {destino}\n"
                    f"• **Data de Partida:** {data_partida}\n"
                    f"• **Data de Volta:** {data_volta}\n"
                    f"• **Classe:** {classe}\n"
                    f"• **Passageiros:** {passageiros}\n"
                    f"• **Status:** Confirmada\n"
                    f"• **Código da Reserva:** VOO{result.get('id', 'N/A')}\n\n"
                    f"🎉 **Parabéns!** Sua reserva foi realizada com sucesso!\n"
                    f"Você receberá um e-mail de confirmação em breve."
                )
                
                await step_context.context.send_activity(MessageFactory.text(mensagem_confirmacao))
            else:
                await step_context.context.send_activity(
                    MessageFactory.text("❌ Erro ao criar reserva. Tente novamente mais tarde.")
                )
            
            return await step_context.end_dialog()
    
    async def _escolher_classe(self, step_context: WaterfallStepContext):
        """Método auxiliar para escolher a classe do voo"""
        choices = [
            Choice("Econômica"),
            Choice("Executiva"),
            Choice("Primeira Classe")
        ]
        
        prompt = MessageFactory.text("💺 Qual classe de voo você prefere?")
        return await step_context.prompt(
            ChoicePrompt.__name__,
            PromptOptions(prompt=prompt, choices=choices)
        )