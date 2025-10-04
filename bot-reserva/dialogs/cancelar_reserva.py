from botbuilder.dialogs import ComponentDialog
from botbuilder.core import UserState, MessageFactory
from botbuilder.dialogs.prompts import ChoicePrompt, PromptOptions, TextPrompt
from botbuilder.dialogs import WaterfallDialog, WaterfallStepContext
from botbuilder.dialogs.choices import Choice
from helpers.ApiClient import ApiClient

class CancelarReservaDialog(ComponentDialog):
    def __init__(self, user_state: UserState):

        super(CancelarReservaDialog, self).__init__("CancelarReservaDialog")

        #Grava na memoria aonde o usuário está no fluxo de conversa
        self.user_state = user_state
        self.api_client = ApiClient()

        #Adiciona prompt de texto
        self.add_dialog(TextPrompt(TextPrompt.__name__))
        self.add_dialog(ChoicePrompt(ChoicePrompt.__name__))

        # Funcoes de Conversação Sequencial
        self.add_dialog(
            WaterfallDialog(
                "CancelarReservaDialog",
                [
                    self.pedir_cpf_step,
                    self.escolher_tipo_reserva_step,
                    self.listar_reservas_step,
                    self.processar_cancelamento_step
                ]
            )
        )


        self.initial_dialog_id = "CancelarReservaDialog"

    async def pedir_cpf_step(self, step_context: WaterfallStepContext):
        message = MessageFactory.text("Por favor, informe seu CPF para acessar suas reservas:")

        prompt_options = PromptOptions(
            prompt=message,
            retry_prompt=MessageFactory.text("Por favor, informe um CPF válido.")
        )
        return await step_context.prompt(TextPrompt.__name__, prompt_options)

    async def escolher_tipo_reserva_step(self, step_context: WaterfallStepContext):
        cpf = step_context.result
        step_context.values["cpf"] = cpf

        # Verificar se o cliente existe
        cliente = await self.api_client.get_cliente_by_cpf(cpf)
        if not cliente:
            await step_context.context.send_activity(
                MessageFactory.text("CPF não encontrado no sistema. Verifique o número informado.")
            )
            return await step_context.end_dialog()

        step_context.values["cliente"] = cliente

        choices = [
            Choice("Reservas de Voo"),
            Choice("Reservas de Hospedagem")
        ]

        prompt = MessageFactory.text("Que tipo de reserva você gostaria de cancelar?")
        return await step_context.prompt(
            ChoicePrompt.__name__,
            PromptOptions(prompt=prompt, choices=choices)
        )

    async def listar_reservas_step(self, step_context: WaterfallStepContext):
        tipo_reserva = step_context.result.value
        cliente = step_context.values["cliente"]
        step_context.values["tipo_reserva"] = tipo_reserva

        if tipo_reserva == "Reservas de Voo":
            reservas = await self.api_client.get_reservas_voo_by_cliente(cliente["id"])
            reservas_ativas = [r for r in reservas if r["status"] == "CONFIRMADA"]

            if not reservas_ativas:
                await step_context.context.send_activity(
                    MessageFactory.text("Você não possui reservas de voo ativas para cancelar.")
                )
                return await step_context.end_dialog()

            step_context.values["reservas"] = reservas_ativas

            choices = []
            mensagem = "**Suas reservas de voo ativas:**\n\n"
            for i, reserva in enumerate(reservas_ativas):
                data_partida = reserva.get('dataHoraPartida', 'N/A')
                if data_partida and 'T' in data_partida:
                    data_partida = data_partida.split('T')[0]  # Extrai apenas a data
                choice_text = f"Reserva {i+1}: {reserva['origem']} → {reserva['destino']} - {data_partida}"
                choices.append(Choice(choice_text))
                mensagem += f"**{i+1}.** {reserva['origem']} → {reserva['destino']}\n"
                mensagem += f"   Data: {data_partida} | Companhia: {reserva['companhiaAerea']}\n\n"

        else:  # hospedagem
            reservas = await self.api_client.get_reservas_hospedagem_by_cliente(cliente["id"])
            reservas_ativas = [r for r in reservas if r["status"] == "CONFIRMADA"]

            if not reservas_ativas:
                await step_context.context.send_activity(
                    MessageFactory.text("Você não possui reservas de hospedagem ativas para cancelar.")
                )
                return await step_context.end_dialog()

            step_context.values["reservas"] = reservas_ativas

            choices = []
            mensagem = "**Suas reservas de hospedagem ativas:**\n\n"
            for i, reserva in enumerate(reservas_ativas):
                choice_text = f"Reserva {i+1}: {reserva['nomeHotel']} - {reserva['cidade']}"
                choices.append(Choice(choice_text))
                mensagem += f"**{i+1}.** {reserva['nomeHotel']} - {reserva['cidade']}\n"
                mensagem += f"   Check-in: {reserva['dataCheckIn']} | Check-out: {reserva['dataCheckOut']}\n\n"

        await step_context.context.send_activity(MessageFactory.text(mensagem))

        prompt = MessageFactory.text("Qual reserva você gostaria de cancelar?")
        return await step_context.prompt(
            ChoicePrompt.__name__,
            PromptOptions(prompt=prompt, choices=choices)
        )

    async def processar_cancelamento_step(self, step_context: WaterfallStepContext):
        escolha_reserva = step_context.result.value
        tipo_reserva = step_context.values["tipo_reserva"]
        reservas = step_context.values["reservas"]

        # Extrair o número da reserva do texto escolhido
        try:
            numero_reserva = int(escolha_reserva.split(":")[0].split()[-1]) - 1  # "Reserva 1:" -> 0
            reserva_selecionada = reservas[numero_reserva]

            # Cancelar via API
            if tipo_reserva == "Reservas de Voo":
                resultado = await self.api_client.cancelar_reserva_voo(reserva_selecionada['id'])
            else:  # Reservas de Hospedagem
                resultado = await self.api_client.cancelar_reserva_hospedagem(reserva_selecionada['id'])

            if resultado:
                # Cancelamento bem-sucedido
                detalhes = ""
                if tipo_reserva == "Reservas de Voo":
                    data_partida = reserva_selecionada.get('dataHoraPartida', 'N/A')
                    if data_partida and 'T' in data_partida:
                        data_partida = data_partida.split('T')[0]
                    detalhes = f"• **Rota:** {reserva_selecionada['origem']} → {reserva_selecionada['destino']}\n" \
                              f"• **Data:** {data_partida}\n" \
                              f"• **Companhia:** {reserva_selecionada['companhiaAerea']}"
                else:
                    detalhes = f"• **Hotel:** {reserva_selecionada['nomeHotel']}\n" \
                              f"• **Cidade:** {reserva_selecionada['cidade']}\n" \
                              f"• **Check-in:** {reserva_selecionada['dataCheckIn']}\n" \
                              f"• **Check-out:** {reserva_selecionada['dataCheckOut']}"

                await step_context.context.send_activity(
                    MessageFactory.text(f"✅ **Cancelamento processado com sucesso!**\n\n"
                                       f"Sua reserva foi cancelada:\n"
                                       f"• **Tipo:** {tipo_reserva}\n"
                                       f"• **ID da Reserva:** {reserva_selecionada['id']}\n"
                                       f"{detalhes}\n"
                                       f"• **Status:** Cancelada\n\n"
                                       f"Você receberá um email de confirmação em breve.")
                )
            else:
                # Erro no cancelamento
                await step_context.context.send_activity(
                    MessageFactory.text("❌ **Erro no cancelamento**\n\n"
                                       "Não foi possível processar o cancelamento da sua reserva. "
                                       "Tente novamente mais tarde ou entre em contato com nosso suporte.")
                )
        except (ValueError, IndexError):
            await step_context.context.send_activity(
                MessageFactory.text("❌ Erro: Reserva não encontrada.")
            )

        return await step_context.end_dialog()
        