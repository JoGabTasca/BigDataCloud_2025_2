from botbuilder.dialogs import ComponentDialog
from botbuilder.core import UserState, MessageFactory
from botbuilder.dialogs.prompts import ChoicePrompt, PromptOptions, TextPrompt
from botbuilder.dialogs import WaterfallDialog, WaterfallStepContext
from botbuilder.dialogs.choices import Choice
from helpers.ApiClient import ApiClient

class ConsultarVooDialog(ComponentDialog):
    def __init__(self, user_state: UserState):

        super(ConsultarVooDialog, self).__init__("ConsultarVooDialog")

        #Grava na memoria aonde o usuário está no fluxo de conversa
        self.user_state = user_state
        self.api_client = ApiClient()

        # Adiciona prompt de texto
        self.add_dialog(TextPrompt(TextPrompt.__name__))
        # Adiciona prompt de escolha
        self.add_dialog(ChoicePrompt(ChoicePrompt.__name__))

        # Registro dos sub-diálogos
        from .cadastro_cliente import CadastroClienteDialog
        from .nova_reserva_voo import NovaReservaVooDialog
        self.add_dialog(CadastroClienteDialog(self.user_state))
        self.add_dialog(NovaReservaVooDialog(self.user_state))

        # Funcoes de Conversação Sequencial
        self.add_dialog(
            WaterfallDialog(
                "ConsultarVooDialog",
                [
                    self.pedir_cpf_step,
                    self.verificar_cliente_step,
                    self.escolher_acao_step,
                    self.processar_step
                ]
            )
        )

        self.initial_dialog_id = "ConsultarVooDialog"

    async def pedir_cpf_step(self, step_context: WaterfallStepContext):
        prompt = MessageFactory.text(
            "✈️ **Vamos decolar juntos!**\n\n"
            "Para acessar suas informações e oferecer o melhor atendimento, "
            "preciso que você me informe seu CPF:\n\n"
            "📝 *Digite apenas os números (sem pontos ou traços)*"
        )
        return await step_context.prompt(TextPrompt.__name__, PromptOptions(prompt=prompt))

    async def verificar_cliente_step(self, step_context: WaterfallStepContext):
        cpf = step_context.result
        step_context.values["cpf"] = cpf

        # Verificar se o cliente existe
        cliente = await self.api_client.get_cliente_by_cpf(cpf)

        if not cliente:
            # Cliente não existe, iniciar cadastro
            await step_context.context.send_activity(
                MessageFactory.text(
                    "🎉 **Que ótimo! Você é novo por aqui!**\n\n"
                    "Não encontrei seu CPF no nosso sistema, mas não se preocupe. "
                    "Vou fazer um cadastro rapidinho para você e em poucos minutos "
                    "teremos tudo pronto!\n\n"
                    "📝 **Vamos começar seu cadastro:**"
                )
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
            Choice("Ver minhas viagens"),
            Choice("Reservar nova viagem"),
            Choice("Explorar destinos")
        ]

        prompt = MessageFactory.text(
            f"👋 **Olá, {cliente['nome']}! É um prazer te atender!**\n\n"
            f"Estou aqui para tornar sua experiência de viagem incrível. "
            f"O que podemos fazer juntos hoje?"
        )
        return await step_context.prompt(
            ChoicePrompt.__name__,
            PromptOptions(prompt=prompt, choices=choices)
        )

    async def processar_step(self, step_context: WaterfallStepContext):
        escolha = step_context.result.value
        cliente = step_context.values["cliente"]

        if escolha == "Ver minhas viagens":
            reservas = await self.api_client.get_reservas_voo_by_cliente(cliente["id"])

            if not reservas:
                await step_context.context.send_activity(
                    MessageFactory.text("📭 Você não possui reservas de voo no momento.\n\nQue tal fazer uma nova reserva?")
                )
            else:
                mensagem = f"**✈️ Suas reservas de voo, {cliente['nome']}:**\n\n"
                for i, reserva in enumerate(reservas, 1):
                    status_emoji = "✅" if reserva["status"] == "CONFIRMADA" else "⏳"
                    mensagem += f"{status_emoji} **Reserva {i}:**\n"
                    mensagem += f"• **Rota:** {reserva['origem']} → {reserva['destino']}\n"
                    mensagem += f"• **Data Partida:** {reserva['dataHoraPartida']}\n"
                    mensagem += f"• **Data Volta:** {reserva['dataHoraVolta']}\n"
                    mensagem += f"• **Classe:** {reserva['classe']}\n"
                    mensagem += f"• **Status:** {reserva['status']}\n\n"

                await step_context.context.send_activity(MessageFactory.text(mensagem))

        elif escolha == "Reservar nova viagem":
            return await step_context.begin_dialog("NovaReservaVooDialog", {"cliente": cliente})

        elif escolha == "Explorar destinos":
            todas_reservas = await self.api_client.get_all_reservas_voo()

            if not todas_reservas:
                await step_context.context.send_activity(
                    MessageFactory.text("📭 Não há voos disponíveis no momento.")
                )
            else:
                mensagem = "**✈️ Voos disponíveis:**\n\n"
                for i, voo in enumerate(todas_reservas, 1):
                    mensagem += f"✈️ **Voo {i}:**\n"
                    mensagem += f"• **Rota:** {voo['origem']} → {voo['destino']}\n"
                    mensagem += f"• **Data Partida:** {voo['dataHoraPartida']}\n"
                    mensagem += f"• **Data Volta:** {voo['dataHoraVolta']}\n"
                    mensagem += f"• **Classe:** {voo['classe']}\n"
                    mensagem += f"• **Status:** {voo['status']}\n\n"

                await step_context.context.send_activity(MessageFactory.text(mensagem))

        return await step_context.end_dialog()
