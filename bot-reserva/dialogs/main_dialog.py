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
        
        #Registro de Funções de Conversação Sequencial
        self.add_dialog(
            WaterfallDialog(
                "MainDialog",
                [
                    self.prompt_option_step,
                    self.process_option_step
                ]
            )
        )
                
        self.initial_dialog_id = "MainDialog"
        
    async def prompt_option_step(self, step_context: WaterfallStepContext):
        return await step_context.prompt(
            ChoicePrompt.__name__,
            PromptOptions(
                prompt=MessageFactory.text("Escolha a opção desejada:"),
                choices=[
                    Choice("Cadastrar Evento"),
                    Choice("Consultar Evento"),
                    Choice("Ajuda"),
                ]
            )
        )
    async def process_option_step(self, step_context: WaterfallStepContext):
        option = step_context.result.value
        
        if (option == "Cadastrar Evento"):
            return await step_context.context.send_activity(
                MessageFactory.text(f"Voce escolheu a opção Cadastrar Evento")
            )
        elif (option == "Consultar Evento"):
             return await step_context.context.send_activity(
                MessageFactory.text(f"Voce escolheu a opção Consultar Evento")
            )           
        elif (option == "Ajuda"):
            return await step_context.context.send_activity(
                MessageFactory.text(f"Voce escolheu a opção Ajuda")
            )           
