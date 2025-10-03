from botbuilder.dialogs import ComponentDialog
from botbuilder.core import UserState, MessageFactory
from botbuilder.dialogs.prompts import ChoicePrompt, PromptOptions
from botbuilder.dialogs import WaterfallDialog, WaterfallStepContext
from botbuilder.dialogs.choices import Choice

class MainDialog(ComponentDialog):
    
    def __init__(self, user_state: UserState):
        super(MainDialog, self).__init__("MainDialog")
        
        #Grava na memoria aonde o usuário está no fluxo de conversa
        self.user_state = user_state
        
        #Registro do Prompt de escolha
        self.add_dialog(ChoicePrompt(ChoicePrompt.__name__))

        #Registro do Dialogo de Consulta de Reserva
        from .consultar_voo import ConsultarVooDialog
        self.add_dialog(ConsultarVooDialog(self.user_state))

        #Registro do Dialogo de Consulta de Hoteis
        from .consultar_hoteis import ConsultarHoteisDialog
        self.add_dialog(ConsultarHoteisDialog(self.user_state))

        #Registro do Dialogo de Cancelamento de Reserva
        from .cancelar_reserva import CancelarReservaDialog
        self.add_dialog(CancelarReservaDialog(self.user_state))

        #Registro de Funções de Conversação Sequencial
        self.add_dialog(
            WaterfallDialog(
                "MainDialog",
                [
                    self.prompt_option_step,
                    self.process_option_step,
                    self.return_to_menu_step
                ]
            )
        )
        self.initial_dialog_id = "MainDialog"
        
    async def prompt_option_step(self, step_context: WaterfallStepContext):
        # Verificar se é a primeira vez (mensagem de boas-vindas) ou retorno
        user_profile_accessor = self.user_state.create_property("user_profile")
        user_profile = await user_profile_accessor.get(step_context.context, lambda: {})
        
        if not user_profile.get("welcomed", False):
            # Primeira vez - mostrar boas-vindas
            welcome_message = (
                "🤖 **Bem-vindo ao Bot de Reservas!**\n\n"
                "Posso te ajudar com:\n"
                "✈️ Consulta de voos e suas reservas\n"
                "🏨 Consulta de hotéis e hospedagens\n" 
                "❌ Cancelamento de reservas\n\n"
                "**Escolha uma opção abaixo:**"
            )
            user_profile["welcomed"] = True
            await user_profile_accessor.set(step_context.context, user_profile)
        else:
            # Retorno ao menu - mensagem simples
            welcome_message = "🔄 **Menu Principal**\n\nEscolha uma opção:"
        
        choices = [
            Choice("🛩️ Consultar Voos"),
            Choice("🏨 Consultar Hotéis"),
            Choice("❌ Cancelar Reserva"),
            Choice("ℹ️ Ajuda")
        ]
        
        return await step_context.prompt(
            ChoicePrompt.__name__,
            PromptOptions(
                prompt=MessageFactory.text(welcome_message),
                choices=choices
            )
        )
    async def process_option_step(self, step_context: WaterfallStepContext):
        option = step_context.result.value
        
        if option == "🛩️ Consultar Voos":
            # Inicia o dialogo de consulta de voos
            return await step_context.begin_dialog("ConsultarVooDialog")
        elif option == "🏨 Consultar Hotéis":
            # Inicia o dialogo de consulta de hoteis
            return await step_context.begin_dialog("ConsultarHoteisDialog")
        elif option == "❌ Cancelar Reserva":
            return await step_context.begin_dialog("CancelarReservaDialog")
        elif option == "ℹ️ Ajuda":
            help_message = (
                "ℹ️ **Central de Ajuda - Bot de Reservas**\n\n"
                "**Como usar o bot:**\n"
                "1️⃣ Selecione uma opção no menu principal\n"
                "2️⃣ Informe seu CPF quando solicitado\n"
                "3️⃣ Siga as instruções do bot\n\n"
                "**Funcionalidades disponíveis:**\n"
                "• **Consultar Voos:** Veja suas reservas ou fazer nova reserva\n"
                "• **Consultar Hotéis:** Veja suas reservas ou fazer nova reserva\n"
                "• **Cancelar Reserva:** Cancele suas reservas ativas\n\n"
                "**Informações importantes:**\n"
                "• Se você não tem cadastro, o sistema fará automaticamente\n"
                "• Use seu CPF para acessar suas informações\n"
                "• Todas as reservas são salvas no sistema\n\n"
                "🔄 **Retornando ao menu principal...**"
            )
            await step_context.context.send_activity(MessageFactory.text(help_message))
            return await step_context.replace_dialog("MainDialog")
        
        # Retorna ao menu principal após qualquer ação
        return await step_context.replace_dialog("MainDialog")
    
    async def return_to_menu_step(self, step_context: WaterfallStepContext):
        # Este step sempre retorna ao menu principal após qualquer diálogo
        return await step_context.replace_dialog("MainDialog")
