import os
import random
from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from dotenv import load_dotenv
from auth.auth import gerar_token

load_dotenv()

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
bot = TeleBot(TOKEN)

# Lista de mensagens românticas
romantic_messages = [
    "O universo se alinha para que nossos caminhos se cruzem... E aqui estamos, compartilhando um momento juntos.",
    "Quando o coração fala, as palavras são poucas. E o meu coração está falando: você é especial.",
    "Entre o céu e a terra, encontrei você. E agora, o mundo parece mais bonito.",
    "Se eu pudesse te dar uma coisa na vida, eu te daria a habilidade de se ver através dos meus olhos. Só então você perceberia o quanto é especial.",
    "Nosso encontro não é mera coincidência. O destino sabe o que faz.",
    "Não é um adeus, é só um até logo. Até nos encontrarmos novamente, no espaço e no tempo.",
    "O silêncio entre nós também é poesia. Cada palavra não dita, um abraço invisível.",
    "A felicidade é uma escolha, e eu escolho estar ao seu lado.",
    "Às vezes, as palavras não são necessárias. Apenas estar perto de você já é tudo o que preciso.",
    "O amor é uma linguagem silenciosa. Quando nossos olhares se cruzam, entendemos tudo."
]

# Mensagens de boas-vindas românticas
welcome_messages = [
    "O primeiro passo para nossa história acaba de ser dado. Você está pronto para embarcar nessa jornada de encantos comigo?",
    "Aqui estamos, o destino nos uniu e agora, cada palavra trocada se torna poesia no nosso encontro.",
    "Ao seu lado, o tempo parece fluir de maneira suave e doce. Bem-vindo ao meu pequeno mundo encantado.",
    "Entre as estrelas, nossos caminhos se cruzaram. Agora, nossos corações batem no mesmo ritmo. Bem-vindo!"
]

# Comando /start com botão do WebApp
@bot.message_handler(commands=['start'])
def send_welcome(message):
    keyboard = InlineKeyboardMarkup()
    
    # Enviar o ID do usuário como parte da URL do WebApp
    token = gerar_token(message.from_user.id)
    webapp_url = f"https://ve-scores-vacuum-mall.trycloudflare.com?token={token}"  # Incluindo o user_id na URL
    
    # Botão que abre o WebApp "Instante Infinito"
    webapp_button = InlineKeyboardButton(
        text="🌐 Abrir Instante Infinito",
        web_app=WebAppInfo(url=webapp_url)  # Passando a URL com o user_id
    )
    
    # Botão que abre o WebApp "Nosso Diário"
    diario_button = InlineKeyboardButton(
        text="📖 Nosso Diário",
        web_app=WebAppInfo(url=f"https://ve-scores-vacuum-mall.trycloudflare.com/diario?token={token}")  # Passando a URL com o user_id
    )
    
    # Adiciona os dois botões no teclado
    keyboard.add(webapp_button)
    keyboard.add(diario_button)

    # Enviar uma mensagem de boas-vindas romântica
    welcome_message = random.choice(welcome_messages)
    bot.send_message(
        message.chat.id,
        f"{welcome_message}\n\nEscolha uma das opções abaixo para abrir o WebApp desejado, e continuarmos nossa história.",
        reply_markup=keyboard
    )

# Comando /romance para enviar uma mensagem romântica específica
@bot.message_handler(commands=['romance'])
def send_romantic_message(message):
    # Envia uma mensagem romântica aleatória
    romantic_message = random.choice(romantic_messages)
    bot.send_message(message.chat.id, f"💌 {romantic_message}")

# Comando /explicacao para uma descrição romântica sobre o bot
@bot.message_handler(commands=['explicacao'])
def send_explanation(message):
    # Mensagem romântica explicando o funcionamento do bot
    explanation_message = (
        "Ah, você quer saber um pouco mais sobre essa nossa troca de palavras? Cada mensagem que trocamos é como um verso de poesia, "
        "onde cada palavra tem o poder de encantar e envolver. Esse bot foi feito para compartilhar momentos com você, como um conto romântico, "
        "onde os botões são apenas pequenos pontos de partida para o que chamamos de destino... Agora, dê o próximo passo e abra o WebApp, "
        "onde nossos corações podem conversar de outra maneira."
    )
    bot.send_message(message.chat.id, explanation_message)

# Comando /despedida para uma mensagem romântica de despedida
@bot.message_handler(commands=['despedida'])
def send_farewell(message):
    # Mensagem romântica de despedida
    farewell_message = (
        "Por enquanto, é só um até logo... O amor nunca diz adeus, apenas guarda na memória os momentos especiais que compartilhamos. "
        "Enquanto nos afastamos, saiba que você estará sempre em meus pensamentos. Até breve, querido(a)."
    )
    bot.send_message(message.chat.id, farewell_message)

# Captura dados retornados do WebApp (caso você envie algo de volta)
@bot.message_handler(content_types=["web_app_data"])
def receive_webapp_data(message):
    data = message.web_app_data
    bot.send_message(message.chat.id, f"Você enviou: {data.data}")

if __name__ == "__main__":
    bot.infinity_polling()
