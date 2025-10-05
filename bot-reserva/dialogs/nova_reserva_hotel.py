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

        prompt = MessageFactory.text(
            f"✨ **Vamos planejar sua estadia perfeita, {cliente.get('nome', '')}!**\n\n"
            f"🏨 Que emoção! Vou te ajudar a reservar uma hospedagem incrível.\n\n"
            f"🗺️ **Em qual cidade você gostaria de se hospedar?**\n"
            f"*Ex: São Paulo, Rio de Janeiro, Salvador, Gramado...*"
        )
        return await step_context.prompt(TextPrompt.__name__, PromptOptions(prompt=prompt))

    async def solicitar_checkin_step(self, step_context: WaterfallStepContext):
        step_context.values["cidade"] = step_context.result

        prompt = MessageFactory.text(
            "🏙️ **Perfeito! Excelente escolha de destino!**\n\n"
            "Quando você gostaria de chegar ao seu refúgio?\n"
            "*Digite a data de check-in no formato DD/MM/AAAA*\n\n"
            "📝 Exemplo: 15/12/2025"
        )
        return await step_context.prompt(TextPrompt.__name__, PromptOptions(prompt=prompt))

    async def solicitar_checkout_step(self, step_context: WaterfallStepContext):
        step_context.values["checkin"] = step_context.result

        prompt = MessageFactory.text(
            "�️ **Perfeito! Agora vamos definir sua saída...**\n\n"
            "📅 **Quando você pretende fazer o check-out?**\n"
            "*Digite a data de saída no formato DD/MM/AAAA*\n\n"
            "📝 Exemplo: 22/12/2025"
        )
        return await step_context.prompt(TextPrompt.__name__, PromptOptions(prompt=prompt))

    async def solicitar_hospedes_step(self, step_context: WaterfallStepContext):
        step_context.values["checkout"] = step_context.result

        prompt = MessageFactory.text(
            "👥 **Estamos quase lá!**\n\n"
            "Quantas pessoas vão aproveitar essa estadia incrível?\n"
            "*Digite apenas o número total de hóspedes*\n\n"
            "📝 Exemplo: 1, 2, 3, 4..."
        )
        return await step_context.prompt(TextPrompt.__name__, PromptOptions(prompt=prompt))

    async def solicitar_tipo_quarto_step(self, step_context: WaterfallStepContext):
        step_context.values["hospedes"] = step_context.result

        choices = [
            Choice("Standard"),
            Choice("Deluxe"),
            Choice("Suíte"),
            Choice("Suíte Premium")
        ]

        prompt = MessageFactory.text(
            "🌟 **Última pergunta!**\n\n"
            "Que tipo de experiência você gostaria de ter na sua hospedagem?"
        )
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

        # Converter data do formato DD/MM/AAAA para AAAA-MM-DD
        def converter_data_hotel(data_str):
            try:
                # Converte DD/MM/AAAA para AAAA-MM-DD
                dia, mes, ano = data_str.split('/')
                return f"{ano}-{mes.zfill(2)}-{dia.zfill(2)}"
            except:
                return "2025-12-01"  # Data padrão

        reserva_data = {
            "nomeHotel": nome_hotel,
            "cidade": cidade,
            "dataCheckIn": converter_data_hotel(checkin),
            "dataCheckOut": converter_data_hotel(checkout),
            "numeroHospedes": int(hospedes),
            "tipoQuarto": tipo_quarto,
            "precoTotal": 200.0,
            "precoPorNoite": 100.0,
            "endereco": f"Rua Principal, 123 - {cidade}",
            "status": "CONFIRMADA",
            "clienteId": cliente["id"]
        }

        api_client = self.api_client
        result = await api_client.criar_reserva_hospedagem(reserva_data)

        if result:
            mensagem_confirmacao = (
                f"🎉 **UHUL! Sua hospedagem está reservada!**\n\n"
                f"✨ {cliente.get('nome', '')}, tudo certo para sua estadia incrível!\n\n"
                f"🏨 **Detalhes da sua reserva:**\n"
                f"👤 **Hóspede Principal:** {cliente['nome']}\n"
                f"🏢 **Hotel:** {nome_hotel}\n"
                f"🌍 **Cidade:** {cidade}\n"
                f"📅 **Check-in:** {checkin}\n"
                f"📅 **Check-out:** {checkout}\n"
                f"👥 **Hóspedes:** {hospedes}\n"
                f"🛏️ **Tipo de Quarto:** {tipo_quarto}\n"
                f"✅ **Status:** Confirmada\n"
                f"🏷️ **Código:** HTL{result.get('id', 'N/A')}\n\n"
                f"📧 **Já estou preparando seu e-mail de confirmação!**\n"
                f"Você receberá todos os detalhes em instantes.\n\n"
                f"✨ **Tenha uma estadia maravilhosa!**"
            )

            await step_context.context.send_activity(MessageFactory.text(mensagem_confirmacao))
        else:
            await step_context.context.send_activity(
                MessageFactory.text(
                    "😔 **Ops! Algo não saiu como esperado...**\n\n"
                    "Tivemos uma dificuldade técnica para processar sua reserva. "
                    "Mas não se preocupe!\n\n"
                    "🔄 **Pode tentar novamente em alguns minutos?**\n"
                    "Ou se preferir, nossa equipe de suporte está sempre disponível para te ajudar."
                )
            )

        return await step_context.end_dialog()