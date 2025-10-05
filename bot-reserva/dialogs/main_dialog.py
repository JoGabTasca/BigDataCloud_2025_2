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
                "✨ **Perfeito! Agora vamos começar!**\n\n"
                "Estou aqui para tornar sua experiência de viagem incrível. Posso te ajudar com:\n\n"
                "✈️ **Voos** - Consultar, reservar ou gerenciar suas viagens aéreas\n"
                "🏨 **Hotéis** - Encontrar e reservar hospedagens incríveis\n"
                "📋 **Minhas Reservas** - Visualizar ou cancelar reservas existentes\n\n"
                "🎯 **O que você gostaria de fazer hoje?**"
            )
            user_profile["welcomed"] = True
            await user_profile_accessor.set(step_context.context, user_profile)
        else:
            # Retorno ao menu - mensagem simples
            welcome_message = "🏠 **Estou aqui novamente para te ajudar!**\n\n🎯 O que você precisa fazer hoje?"

        choices = [
            Choice("✈️ Voos e Passagens"),
            Choice("🏨 Hotéis e Hospedagem"),
            Choice("📋 Minhas Reservas"),
            Choice("💡 Preciso de Ajuda")
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

        if option == "✈️ Voos e Passagens":
            # Inicia o dialogo de consulta de voos
            return await step_context.begin_dialog("ConsultarVooDialog")
        elif option == "🏨 Hotéis e Hospedagem":
            # Inicia o dialogo de consulta de hoteis
            return await step_context.begin_dialog("ConsultarHoteisDialog")
        elif option == "📋 Minhas Reservas":
            return await step_context.begin_dialog("CancelarReservaDialog")
        elif option == "💡 Preciso de Ajuda":
            help_message = (
                "🤝 **Estou aqui para te ajudar!**\n\n"
                "💼 **Como funciona nosso atendimento:**\n"
                "1️⃣ Escolha o que precisa no menu principal\n"
                "2️⃣ Me informe seu CPF para acessar sua conta\n"
                "3️⃣ Siga minhas orientações - é super fácil!\n\n"
                "🎯 **O que posso fazer por você:**\n"
                "✈️ **Voos**: Consultar, reservar passagens e gerenciar viagens\n"
                "🏨 **Hotéis**: Encontrar e reservar hospedagens\n"
                "📋 **Reservas**: Ver detalhes ou cancelar suas reservas\n\n"
                "📌 **Informações úteis:**\n"
                "• Primeira vez aqui? Criaremos sua conta automaticamente\n"
                "• Todas as informações ficam seguras no nosso sistema\n"
                "• Estou disponível 24h para te atender\n\n"
                "🏠 **Voltando ao menu principal...**"
            )
            await step_context.context.send_activity(MessageFactory.text(help_message))
            return await step_context.replace_dialog("MainDialog")

        # Retorna ao menu principal após qualquer ação
        return await step_context.replace_dialog("MainDialog")

    async def return_to_menu_step(self, step_context: WaterfallStepContext):
        # Este step sempre retorna ao menu principal após qualquer diálogo
        return await step_context.replace_dialog("MainDialog")
