from botbuilder.dialogs import ComponentDialog
from botbuilder.core import UserState, MessageFactory
from botbuilder.dialogs.prompts import TextPrompt, PromptOptions
from botbuilder.dialogs import WaterfallDialog, WaterfallStepContext
from config import DefaultConfig
from azure.ai.language.conversations import ConversationAnalysisClient
from azure.core.credentials import AzureKeyCredential

CONFIG = DefaultConfig()

class AjudaDialog(ComponentDialog):
    def __init__(self, user_state: UserState):
        super(AjudaDialog, self).__init__("AjudaDialog")

        self.user_state = user_state

        self.add_dialog(TextPrompt(TextPrompt.__name__))

        from .nova_reserva_hotel import NovaReservaHotelDialog
        self.add_dialog(NovaReservaHotelDialog(self.user_state))

        from .nova_reserva_voo import NovaReservaVooDialog
        self.add_dialog(NovaReservaVooDialog(self.user_state))

        from .cancelar_reserva import CancelarReservaDialog
        self.add_dialog(CancelarReservaDialog(self.user_state))

        from .consultar_voo import ConsultarVooDialog
        self.add_dialog(ConsultarVooDialog(self.user_state))

        from .consultar_hoteis import ConsultarHoteisDialog
        self.add_dialog(ConsultarHoteisDialog(self.user_state))

        self.add_dialog(
            WaterfallDialog(
                "AjudaDialog",
                [
                    self.prompt_ajuda_step,
                    self.final_step
                ]
            )
        )
        self.initial_dialog_id = "AjudaDialog"

        self.client = ConversationAnalysisClient(
            endpoint=DefaultConfig.CLU_ENDPOINT,
            credential=AzureKeyCredential(DefaultConfig.CLU_KEY)
        )

    async def prompt_ajuda_step(self, step_context: WaterfallStepContext):
        prompt = MessageFactory.text("🤖 **Ajuda do Bot de Reservas**\n\nPor favor, descreva sua dúvida ou problema:")
        return await step_context.prompt(TextPrompt.__name__, PromptOptions(prompt=prompt))

    async def final_step(self, step_context: WaterfallStepContext):
        escolha = step_context.result

        request_payload = {
            "kind": "Conversation",
            "analysisInput": {
                "conversationItem": {
                    "text": escolha,
                    "id": "1",
                    "participantId": "user1",
                    "modality": "text",
                    "language": "pt-BR",
                }
            },
            "parameters": {
                "projectName": DefaultConfig.CLU_PROJECT,
                "deploymentName": DefaultConfig.CLU_DEPLOYMENT_NAME,
                "verbose": True
            }
        }
        # Chama o serviço de análise de conversação
        response = self.client.analyze_conversation(request_payload)
        top_intent = response["result"]["prediction"]["topIntent"]

        if top_intent == "ReservarHotel":
            #Comeca o dialog de reserva de hotel
            return await step_context.begin_dialog("NovaReservaHotelDialog")
        elif top_intent == "ReservarVoo":
            #Comeca o dialog de reserva de voo
            return await step_context.begin_dialog("NovaReservaVooDialog")
        elif top_intent == "CancelarVoo":
            #Comeca o dialog de cancelamento de voo
            return await step_context.begin_dialog("CancelarVooDialog")
        elif top_intent == "CancelarHotel":
            #Comeca o dialog de cancelamento de hotel
            return await step_context.begin_dialog("CancelarReservaDialog")
        elif top_intent == "ConsultarVoo":
            #Comeca o dialog de consulta de voo
            return await step_context.begin_dialog("ConsultarVooDialog")
        elif top_intent == "ConsultarHotel":
            #Comeca o dialog de consulta de hotel
            return await step_context.begin_dialog("ConsultarHoteisDialog")
        else:
            await step_context.context.send_activity(
                MessageFactory.text(
                    "Desculpe, não consegui entender sua dúvida. Por favor, tente reformular sua pergunta ou entre em contato com o suporte."
                )
            )

        await step_context.context.end_dialog()
        