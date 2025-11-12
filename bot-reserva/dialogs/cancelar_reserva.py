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
        message = MessageFactory.text(
            "✨ **Vamos cuidar do seu cancelamento!**\n\n"
            "📋 Entendo que às vezes os planos mudam, e estou aqui para te ajudar.\n\n"
            "🔐 **Para acessar suas reservas, informe seu CPF:**\n"
            "*Ex: 123.456.789-00*"
        )

        prompt_options = PromptOptions(
            prompt=message,
            retry_prompt=MessageFactory.text(
                "😅 **Ops! Parece que o CPF não está no formato correto...**\n\n"
                "Por favor, informe um CPF válido no formato: 123.456.789-00"
            )
        )
        return await step_context.prompt(TextPrompt.__name__, prompt_options)

    async def escolher_tipo_reserva_step(self, step_context: WaterfallStepContext):
        cpf = step_context.result
        step_context.values["cpf"] = cpf

        # Verificar se o cliente existe
        cliente = await self.api_client.get_cliente_by_cpf(cpf)
        if not cliente:
            await step_context.context.send_activity(
                MessageFactory.text(
                    "🔍 **Hmm... Não encontrei esse CPF no nosso sistema...**\n\n"
                    "🤔 Pode verificar se digitou corretamente?\n\n"
                    "📞 Se o problema persistir, nossa equipe de suporte está sempre disponível para te ajudar!"
                )
            )
            return await step_context.end_dialog()

        step_context.values["cliente"] = cliente

        choices = [
            Choice("Reservas de Voo"),
            Choice("Reservas de Hospedagem")
        ]

        prompt = MessageFactory.text(
            "🌟 **Perfeito! Encontrei seu perfil!**\n\n"
            "Que tipo de reserva você gostaria de cancelar?"
        )
        return await step_context.prompt(
            ChoicePrompt.__name__,
            PromptOptions(prompt=prompt, choices=choices)
        )

    async def listar_reservas_step(self, step_context: WaterfallStepContext):
        tipo_reserva = step_context.result.value
        
        # Verificar se temos cliente
        if "cliente" not in step_context.values:
            await step_context.context.send_activity(
                MessageFactory.text("❌ Erro: Informações do cliente não encontradas. Retornando ao menu principal.")
            )
            return await step_context.end_dialog()
            
        cliente = step_context.values["cliente"]
        step_context.values["tipo_reserva"] = tipo_reserva

        if tipo_reserva == "Reservas de Voo":
            reservas = await self.api_client.get_reservas_voo_by_cliente(cliente["id"])
            reservas_ativas = [r for r in reservas if r["status"] == "CONFIRMADA"]

            if not reservas_ativas:
                await step_context.context.send_activity(
                    MessageFactory.text(
                        "✈️ **Que interessante!**\n\n"
                        "Você não possui reservas de voo ativas para cancelar no momento.\n\n"
                        "✨ **Isso significa que você está livre para planejar novas aventuras!**"
                    )
                )
                return await step_context.end_dialog()

            step_context.values["reservas"] = reservas_ativas

            choices = []
            mensagem = (
                "✨ **Aqui estão suas reservas de voo ativas:**\n\n"
                "✈️ Escolha qual você gostaria de cancelar:\n\n"
            )
            for i, reserva in enumerate(reservas_ativas):
                data_partida = reserva.get('dataHoraPartida', 'N/A')
                if data_partida and 'T' in data_partida:
                    data_partida = data_partida.split('T')[0]  # Extrai apenas a data
                choice_text = f"Reserva {i+1}: {reserva['origem']} → {reserva['destino']} - {data_partida}"
                choices.append(Choice(choice_text))
                mensagem += f"**{i+1}.** {reserva['origem']} → {reserva['destino']}\n"
                mensagem += f"   Data: {data_partida} | Classe: {reserva.get('classe', 'N/A')}\n\n"

        else:  # hospedagem
            reservas = await self.api_client.get_reservas_hospedagem_by_cliente(cliente["id"])
            reservas_ativas = [r for r in reservas if r["status"] == "CONFIRMADA"]

            if not reservas_ativas:
                await step_context.context.send_activity(
                    MessageFactory.text(
                        "🏨 **Que interessante!**\n\n"
                        "Você não possui reservas de hospedagem ativas para cancelar no momento.\n\n"
                        "✨ **Isso significa que você está livre para planejar novas estadas!**"
                    )
                )
                return await step_context.end_dialog()

            step_context.values["reservas"] = reservas_ativas

            choices = []
            mensagem = (
                "✨ **Aqui estão suas reservas de hospedagem ativas:**\n\n"
                "🏨 Escolha qual você gostaria de cancelar:\n\n"
            )
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
                              f"• **Classe:** {reserva_selecionada.get('classe', 'N/A')}"
                else:
                    detalhes = f"• **Hotel:** {reserva_selecionada['nomeHotel']}\n" \
                              f"• **Cidade:** {reserva_selecionada['cidade']}\n" \
                              f"• **Check-in:** {reserva_selecionada['dataCheckIn']}\n" \
                              f"• **Check-out:** {reserva_selecionada['dataCheckOut']}"

                await step_context.context.send_activity(
                    MessageFactory.text(
                        f"🎉 **Pronto! Cancelamento processado com sucesso!**\n\n"
                        f"✨ Sua reserva foi cancelada conforme solicitado:\n\n"
                        f"📝 **Detalhes do cancelamento:**\n"
                        f"• **Tipo:** {tipo_reserva}\n"
                        f"• **ID da Reserva:** {reserva_selecionada['id']}\n"
                        f"{detalhes}\n"
                        f"• **Status:** Cancelada\n\n"
                        f"📧 **Já estou preparando seu e-mail de confirmação!**\n"
                        f"Você receberá todos os detalhes em instantes."
                    )
                )
            else:
                # Erro no cancelamento
                await step_context.context.send_activity(
                    MessageFactory.text(
                        "😔 **Ops! Algo não saiu como esperado...**\n\n"
                        "Tivemos uma dificuldade técnica para processar o cancelamento da sua reserva. "
                        "Mas não se preocupe!\n\n"
                        "🔄 **Pode tentar novamente em alguns minutos?**\n"
                        "Ou se preferir, nossa equipe de suporte está sempre disponível para te ajudar."
                    )
                )
        except (ValueError, IndexError):
            await step_context.context.send_activity(
                MessageFactory.text(
                    "🤔 **Hmm... Houve um probleminha...**\n\n"
                    "Não consegui localizar essa reserva.\n\n"
                    "🔄 **Pode tentar novamente?**"
                )
            )

        return await step_context.end_dialog()
