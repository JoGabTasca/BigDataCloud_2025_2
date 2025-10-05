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

        prompt = MessageFactory.text(
            "🎉 **Que bom te conhecer!**\n\n"
            "Vou fazer um cadastro super rápido para você. São apenas alguns dados "
            "básicos para que eu possa te oferecer o melhor atendimento!\n\n"
            "👤 **Vamos começar! Qual é seu nome completo?**"
        )
        return await step_context.prompt(TextPrompt.__name__, PromptOptions(prompt=prompt))

    async def solicitar_email_step(self, step_context: WaterfallStepContext):
        step_context.values["nome"] = step_context.result

        prompt = MessageFactory.text(
            f"� **Prazer em conhecer você, {step_context.values['nome'].split()[0]}!**\n\n"
            "Agora preciso do seu e-mail para enviar as confirmações de reserva "
            "e manter você sempre informado sobre suas viagens.\n\n"
            "📧 **Qual é seu melhor e-mail?**"
        )
        return await step_context.prompt(TextPrompt.__name__, PromptOptions(prompt=prompt))

    async def solicitar_telefone_step(self, step_context: WaterfallStepContext):
        step_context.values["email"] = step_context.result

        prompt = MessageFactory.text(
            "📱 **Última informação!**\n\n"
            "Para finalizar, preciso do seu telefone. Assim posso te avisar sobre "
            "atualizações importantes das suas viagens, se necessário.\n\n"
            "📝 **Digite seu telefone:**\n"
            "*Formato: (11) 99999-9999*"
        )
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
                f"🎉 **Bem-vindo(a) à família RESEVIA, {nome.split()[0]}!**\n\n"
                f"✨ Seu cadastro foi concluído com sucesso! Agora você faz parte "
                f"do nosso time de viajantes.\n\n"
                f"📎 **Seus dados estão seguros conosco:**\n"
                f"👤 **Nome:** {nome}\n"
                f"🏷️ **CPF:** {cpf}\n"
                f"📧 **Email:** {email}\n"
                f"📱 **Telefone:** {telefone}\n\n"
                f"🎆 **Tudo pronto! Agora você pode:**\n"
                f"✈️ Reservar voos incríveis\n"
                f"🏨 Encontrar hotéis perfeitos\n"
                f"📋 Gerenciar todas suas viagens\n\n"
                f"🚀 **Vamos começar sua jornada?**"
            )

            await step_context.context.send_activity(MessageFactory.text(mensagem_sucesso))

            # Retorna os dados do cliente criado na API
            return await step_context.end_dialog(result)
        else:
            await step_context.context.send_activity(
                MessageFactory.text(
                    "😔 **Ops! Tivemos um probleminha técnico...**\n\n"
                    "Não consegui finalizar seu cadastro agora, mas não desista! "
                    "É algo temporário.\n\n"
                    "🔄 **Pode tentar novamente em alguns minutos?**\n"
                    "Ou se preferir, nossa equipe de suporte está pronta para te ajudar!"
                )
            )
            return await step_context.cancel_all_dialogs()