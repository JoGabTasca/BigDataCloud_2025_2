from botbuilder.dialogs import ComponentDialog
from botbuilder.core import UserState, MessageFactory
from botbuilder.dialogs.prompts import TextPrompt, PromptOptions
from botbuilder.dialogs import WaterfallDialog, WaterfallStepContext
from helpers.ApiClient import ApiClient

class CadastroClienteDialog(ComponentDialog):
    def __init__(self, user_state: UserState):
        super(CadastroClienteDialog, self).__init__("CadastroClienteDialog")
        
        self.user_state = user_state
        self.api_client = ApiClient()
        
        # Adiciona prompt de texto
        self.add_dialog(TextPrompt(TextPrompt.__name__))
        
        # Fluxo de cadastro
        self.add_dialog(
            WaterfallDialog(
                "CadastroClienteDialog",
                [
                    self.solicitar_nome_step,
                    self.solicitar_email_step,
                    self.solicitar_telefone_step,
                    self.confirmar_cadastro_step
                ]
            )
        )
        
        self.initial_dialog_id = "CadastroClienteDialog"
    
    async def solicitar_nome_step(self, step_context: WaterfallStepContext):
        # O CPF já foi informado anteriormente e está salvo no user state
        cpf = step_context.options.get("cpf", "")
        step_context.values["cpf"] = cpf
        
        prompt = MessageFactory.text("📝 **Vamos fazer seu cadastro!**\n\nPor favor, informe seu nome completo:")
        return await step_context.prompt(TextPrompt.__name__, PromptOptions(prompt=prompt))
    
    async def solicitar_email_step(self, step_context: WaterfallStepContext):
        step_context.values["nome"] = step_context.result
        
        prompt = MessageFactory.text("📧 Agora informe seu e-mail:")
        return await step_context.prompt(TextPrompt.__name__, PromptOptions(prompt=prompt))
    
    async def solicitar_telefone_step(self, step_context: WaterfallStepContext):
        step_context.values["email"] = step_context.result
        
        prompt = MessageFactory.text("📱 Por último, informe seu telefone (formato: (11) 99999-9999):")
        return await step_context.prompt(TextPrompt.__name__, PromptOptions(prompt=prompt))
    
    async def confirmar_cadastro_step(self, step_context: WaterfallStepContext):
        step_context.values["telefone"] = step_context.result
        
        # Criar cliente na API
        nome = step_context.values["nome"]
        email = step_context.values["email"] 
        telefone = step_context.values["telefone"]
        cpf = step_context.values["cpf"]
        
        new_cliente = {
            "nome": nome,
            "email": email,
            "telefone": telefone,
            "cpf": cpf
        }
        
        # Fazer o cadastro real na API
        api_client = self.api_client
        result = await api_client.criar_cliente(new_cliente)
        
        if result:
            mensagem_sucesso = (
                f"✅ **Cadastro realizado com sucesso!**\n\n"
                f"**Seus dados:**\n"
                f"• **Nome:** {nome}\n"
                f"• **CPF:** {cpf}\n"
                f"• **Email:** {email}\n"
                f"• **Telefone:** {telefone}\n\n"
                f"Agora você pode acessar todas as funcionalidades do sistema!"
            )
            
            await step_context.context.send_activity(MessageFactory.text(mensagem_sucesso))
            
            # Retorna os dados do cliente criado na API
            return await step_context.end_dialog(result)
        else:
            await step_context.context.send_activity(
                MessageFactory.text("❌ Erro ao realizar cadastro. Tente novamente mais tarde.")
            )
            return await step_context.cancel_all_dialogs()