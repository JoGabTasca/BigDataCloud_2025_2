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

        #Registro do Dialogo de Ajuda
        from .ajuda_dialog import AjudaDialog
        self.add_dialog(AjudaDialog(self.user_state))

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

        choices = [
            Choice("Voos e Passagens"),
            Choice("Hotéis e Hospedagem"),
            Choice("Cancelar Reservas"),
            Choice("Preciso de Ajuda")
        ]

        if not user_profile.get("welcomed", False):
            # Primeira vez - mostrar boas-vindas
            welcome_message = MessageFactory.text(
                "✨ **Perfeito! Agora vamos começar!**\n\n"
                "Estou aqui para tornar sua experiência de viagem incrível. Posso te ajudar com:\n\n"
                "✈️ **Voos** - Consultar, reservar ou gerenciar suas viagens aéreas\n"
                "🏨 **Hotéis** - Encontrar e reservar hospedagens incríveis\n"
                "❌ **Cancelar Reservas** - Visualizar e cancelar reservas existentes\n\n"
                "🎯 **O que você gostaria de fazer hoje?**"
            )
            user_profile["welcomed"] = True
            await user_profile_accessor.set(step_context.context, user_profile)
        else:
            # Retorno ao menu - mensagem simples
            welcome_message = MessageFactory.text(
                "🏠 **Estou aqui novamente para te ajudar!**\n\n🎯 O que você precisa fazer hoje?"
            )

        return await step_context.prompt(
            ChoicePrompt.__name__,
            PromptOptions(prompt=welcome_message, choices=choices)
        )
    async def process_option_step(self, step_context: WaterfallStepContext):
        option = step_context.result.value

        if option == "Voos e Passagens":
            # Inicia o dialogo de consulta de voos
            return await step_context.begin_dialog("ConsultarVooDialog")
        elif option == "Hotéis e Hospedagem":
            # Inicia o dialogo de consulta de hoteis
            return await step_context.begin_dialog("ConsultarHoteisDialog")
        elif option == "Cancelar Reservas":
            return await step_context.begin_dialog("CancelarReservaDialog")
        elif option == "Preciso de Ajuda":
            return await step_context.begin_dialog("AjudaDialog")

        # Retorna ao menu principal após qualquer ação
        return await step_context.replace_dialog("MainDialog")

    async def return_to_menu_step(self, step_context: WaterfallStepContext):
        # Este step sempre retorna ao menu principal após qualquer diálogo
        return await step_context.replace_dialog("MainDialog")



