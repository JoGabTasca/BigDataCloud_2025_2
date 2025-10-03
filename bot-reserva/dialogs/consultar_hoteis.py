from botbuilder.dialogs import ComponentDialog
from botbuilder.core import UserState, MessageFactory
from botbuilder.dialogs.prompts import TextPrompt, PromptOptions, ChoicePrompt
from botbuilder.dialogs import WaterfallDialog, WaterfallStepContext
from botbuilder.dialogs.choices import Choice
from helpers.ApiClient import ApiClient

class ConsultarHoteisDialog(ComponentDialog):
    def __init__(self, user_state: UserState):
        super(ConsultarHoteisDialog, self).__init__("ConsultarHoteisDialog")
        self.user_state = user_state
        self.api_client = ApiClient()
        
        self.add_dialog(TextPrompt(TextPrompt.__name__))
        self.add_dialog(ChoicePrompt(ChoicePrompt.__name__))
        
        # Registro dos sub-diálogos
        from .cadastro_cliente import CadastroClienteDialog
        from .nova_reserva_hotel import NovaReservaHotelDialog
        self.add_dialog(CadastroClienteDialog(self.user_state))
        self.add_dialog(NovaReservaHotelDialog(self.user_state))
        
        self.add_dialog(
            WaterfallDialog(
                "ConsultarHoteisDialog",
                [
                    self.pedir_cpf_step,
                    self.verificar_cliente_step,
                    self.escolher_acao_step,
                    self.processar_step
                ]
            )
        )
        self.initial_dialog_id = "ConsultarHoteisDialog"

    async def pedir_cpf_step(self, step_context: WaterfallStepContext):
        prompt = MessageFactory.text("🏨 **Consulta de Hotéis**\n\nPor favor, informe seu CPF para acessar o sistema:")
        return await step_context.prompt(TextPrompt.__name__, PromptOptions(prompt=prompt))

    async def verificar_cliente_step(self, step_context: WaterfallStepContext):
        cpf = step_context.result
        step_context.values["cpf"] = cpf
        
        # Verificar se o cliente existe
        cliente = await self.api_client.get_cliente_by_cpf(cpf)
        
        if not cliente:
            # Cliente não existe, iniciar cadastro
            await step_context.context.send_activity(
                MessageFactory.text("🔍 CPF não encontrado no sistema.\n\nVamos fazer seu cadastro para continuar!")
            )
            
            return await step_context.begin_dialog("CadastroClienteDialog", {"cpf": cpf})
        else:
            # Cliente existe, salvar dados e prosseguir
            step_context.values["cliente"] = cliente
            return await step_context.next(cliente)

    async def escolher_acao_step(self, step_context: WaterfallStepContext):
        # Se retornamos do cadastro, usar o cliente cadastrado
        if step_context.result and isinstance(step_context.result, dict):
            step_context.values["cliente"] = step_context.result
        
        cliente = step_context.values["cliente"]
        
        choices = [
            Choice("📋 Minhas reservas"),
            Choice("➕ Fazer nova reserva"),
            Choice("🔍 Buscar hotéis disponíveis")
        ]
        
        prompt = MessageFactory.text(f"👋 **Olá, {cliente['nome']}!**\n\nO que você gostaria de fazer?")
        return await step_context.prompt(
            ChoicePrompt.__name__, 
            PromptOptions(prompt=prompt, choices=choices)
        )

    async def processar_step(self, step_context: WaterfallStepContext):
        escolha = step_context.result.value
        cliente = step_context.values["cliente"]
        
        if escolha == "📋 Minhas reservas":
            reservas = await self.api_client.get_reservas_hospedagem_by_cliente(cliente["id"])
            
            if not reservas:
                await step_context.context.send_activity(
                    MessageFactory.text("📭 Você não possui reservas de hospedagem no momento.\n\nQue tal fazer uma nova reserva?")
                )
            else:
                mensagem = f"**🏨 Suas reservas de hospedagem, {cliente['nome']}:**\n\n"
                for i, reserva in enumerate(reservas, 1):
                    status_emoji = "✅" if reserva["status"] == "CONFIRMADA" else "⏳"
                    mensagem += f"{status_emoji} **Reserva {i}:**\n"
                    mensagem += f"• **Hotel:** {reserva['nomeHotel']}\n"
                    mensagem += f"• **Cidade:** {reserva['cidade']}\n"
                    mensagem += f"• **Check-in:** {reserva['dataCheckIn']}\n"
                    mensagem += f"• **Check-out:** {reserva['dataCheckOut']}\n"
                    mensagem += f"• **Tipo de quarto:** {reserva['tipoQuarto']}\n"
                    mensagem += f"• **Preço:** R$ {reserva['precoTotal']}\n"
                    mensagem += f"• **Status:** {reserva['status']}\n\n"
                
                await step_context.context.send_activity(MessageFactory.text(mensagem))
        
        elif escolha == "➕ Fazer nova reserva":
            return await step_context.begin_dialog("NovaReservaHotelDialog", {"cliente": cliente})
        
        elif escolha == "🔍 Buscar hotéis disponíveis":
            todas_reservas = await self.api_client.get_all_reservas_hospedagem()
            
            if not todas_reservas:
                await step_context.context.send_activity(
                    MessageFactory.text("📭 Não há hotéis disponíveis no momento.")
                )
            else:
                mensagem = "**🏨 Hotéis disponíveis:**\n\n"
                for i, hotel in enumerate(todas_reservas, 1):
                    mensagem += f"🏨 **Hotel {i}:**\n"
                    mensagem += f"• **Nome:** {hotel['nomeHotel']}\n"
                    mensagem += f"• **Cidade:** {hotel['cidade']}\n"
                    mensagem += f"• **Endereço:** {hotel['endereco']}\n"
                    mensagem += f"• **Check-in:** {hotel['dataCheckIn']}\n"
                    mensagem += f"• **Check-out:** {hotel['dataCheckOut']}\n"
                    mensagem += f"• **Tipo de quarto:** {hotel['tipoQuarto']}\n"
                    mensagem += f"• **Preço total:** R$ {hotel['precoTotal']}\n"
                    mensagem += f"• **Status:** {hotel['status']}\n"
                    if hotel.get('telefoneHotel'):
                        mensagem += f"• **Telefone:** {hotel['telefoneHotel']}\n"
                    mensagem += "\n"
                
                await step_context.context.send_activity(MessageFactory.text(mensagem))
        
        return await step_context.end_dialog()