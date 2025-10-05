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
        # Salva a data de partida e pede diretamente a data de volta (ida e volta por padrão)
        step_context.values["data_partida"] = step_context.result

        prompt = MessageFactory.text("🔄 Consideramos ida e volta por padrão. Qual a data de volta? (formato: DD/MM/AAAA)")
        return await step_context.prompt(TextPrompt.__name__, PromptOptions(prompt=prompt))

    async def solicitar_classe_step(self, step_context: WaterfallStepContext):
        # Neste fluxo, o step anterior forneceu a data de volta como texto.
        posible_data_volta = step_context.result
        # Salva a data de volta (se for string)
        if posible_data_volta and isinstance(posible_data_volta, str):
            step_context.values["data_volta"] = posible_data_volta

        # Em seguida, dispara o prompt para escolher a classe
        return await self._escolher_classe(step_context)

    async def solicitar_passageiros_step(self, step_context: WaterfallStepContext):
        # Aqui sempre chegamos após a escolha da classe (ChoicePrompt)
        # step_context.result será um objeto Choice quando vindo do ChoicePrompt
        chosen = step_context.result
        if chosen:
            # Se veio do ChoicePrompt, extrai o valor; caso venha diferente, tenta usar como string
            step_context.values["classe"] = getattr(chosen, "value", str(chosen))

        prompt = MessageFactory.text("👥 Quantos passageiros? (digite o número)")
        return await step_context.prompt(TextPrompt.__name__, PromptOptions(prompt=prompt))

    async def confirmar_reserva_step(self, step_context: WaterfallStepContext):
        # Temos o número de passageiros no resultado deste passo
        step_context.values["passageiros"] = step_context.result

        # Temos todos os dados, criar reserva na API
        cliente = step_context.values.get("cliente", {})
        origem = step_context.values.get("origem")
        destino = step_context.values.get("destino")
        data_partida = step_context.values.get("data_partida")
        data_volta = step_context.values.get("data_volta", "Não informada")
        classe = step_context.values.get("classe", "Econômica")
        passageiros = step_context.values.get("passageiros")

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
            "clienteId": cliente.get("id")
        }

        api_client = self.api_client
        result = await api_client.criar_reserva_voo(reserva_data)

        if result:
            mensagem_confirmacao = (
                f"✅ **Reserva de Voo Confirmada!**\n\n"
                f"**Detalhes da Reserva:**\n"
                f"• **Passageiro:** {cliente.get('nome', '')}\n"
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