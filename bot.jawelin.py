import os
import datetime
import re
import random
import pytz
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# ==========================================
# === CONFIGURACIÓN Y VARIABLES DE ENTORNO ===
# ==========================================
BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_USERNAME = os.getenv('ADMIN_USERNAME', 'kirschteiinz')

if not BOT_TOKEN:
    raise ValueError("Error: La variable de entorno BOT_TOKEN no está configurada.")

# ID numéricos de los grupos de Telegram desde variables de entorno
GROUPS = {
    'cherrys': int(os.getenv('GROUP_CHERRYS', '-1002327728583')),
    'testing': int(os.getenv('GROUP_TESTING', '-1004332628770'))
}

# Base de datos en memoria
db = {
    'users': {},
    'activeHunt': {
        'active': False,
        'targetGroup': None
    },
    'activeWitch': None,
    'graves_today': [0, 0, 0, 0, 0],
    'pumpkin': {
        'active': False,
        'courtesy': 0,
        'total': 0,
        'participants': []
    }
}

bot = telebot.TeleBot(BOT_TOKEN)

# ==========================================
# === DICCIONARIO DE TIPOS DE BRUJAS ===
# ==========================================
WITCH_TYPES = {
    'comun': {
        'name': 'común',
        'reward': 20,
        'photo': 'https://pin.it/5cBvTP7zt',
        'caption': '¡Una bruja común ha aparecido!'
    }
}

# ==========================================
# === MANEJADORES DE COMANDOS ===
# ==========================================
@bot.message_handler(commands=['start'])
def cmd_start(message):
    text = (
        "⠀⠀⠀⠀⠀⢀⣴⣿⣿⣿⣦⠀\n"
        "⠀⠀⠀⠀⣰⣿⡟⢻⣿⡟⢻⣧    𝗈𝖿𝗂𝖼𝗂𝖺𝗅𝗆𝖾𝗇𝗍𝖾 𝖿𝗈𝗋𝗆𝖺𝗌 𝗉𝖺𝗋𝗍𝖾 𝖽𝖾 𝗅𝖺 𝖼𝖺𝗌𝖺\n"
        "⠀⠀⠀⣰⣿⣿⣇⣸⣿⣇⣸⣿     𝖽𝖾𝗅 𝗍𝖾𝗋𝗋𝗈𝗋 𝖽𝖾 𝖼𝗁𝖾𝗋𝗋𝗒'𝗌. \n"
        "⠀⠀⣴⣿⣿⣿⣿⠟⢻⣿⣿⣿    𝗍𝖾 𝖽𝖾𝗌𝖾𝗈 𝗆𝗎𝖼𝗁𝖺 𝗌𝗎𝖾𝗋𝗍𝖾 𝗒... \n"
        "⣠⣾⣿⣿⣿⣿⣿⣤⣼⣿⣿⠇   𝗉𝖺𝖼𝗂𝖾𝗇𝖼𝗂𝖺, 𝗍𝖺𝗆𝖻𝗂é𝗇. \n"
        "⢿⡿⢿⣿⣿⣿⣿⣿⣿⣿⡿⠀𝗌𝗈𝗒 𝗊𝗎𝗂é𝗇 𝗍𝖾 𝖺𝗒𝗎𝖽𝖺𝗋á 𝖺\n"
        "⠀⠀⠈⠿⠿⠋⠙⢿⣿⡿⠁⠀ 𝗅𝗅𝖾𝗀𝖺𝗋 𝖺𝗅 𝗍𝗈𝗉 1 𝖽𝖾𝗅 𝖾𝗏𝖾𝗇𝗍𝗈,\n"
        "ㅤㅤㅤㅤㅤㅤㅤㅤ𝗉𝖾𝗋𝗈 𝗇𝗈 𝗅𝖾𝗌 𝖽𝗂𝗀𝖺𝗌 𝖺 𝗅𝗈𝗌 𝖽𝖾𝗆á𝗌.\n\n"
        "ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ 𝗌𝗂𝗇 𝗆á𝗌 𝗊𝗎𝖾 𝖽𝖾𝖼𝗂𝗋,\n"
        "ㅤㅤ ¡𝗉𝗎𝖾𝖽𝖾𝗌 𝖾𝗆𝗉𝖾𝗓𝖺𝗋 𝖺 𝗃𝗎𝗀𝖺𝗋 𝗅𝗈𝗌 𝗃𝗎𝖾𝗀𝗈𝗌 𝖽𝖾 𝗆𝗂 𝗂𝗇𝗏𝖾𝗇𝗍𝖺𝗋𝗂𝗈! ㅤㅤㅤㅤㅤ ㅤㅤㅤㅤ𝖼𝗈𝗇𝗌ú𝗅𝗍𝖺𝗅𝗈𝗌 𝗎𝗌𝖺𝗇𝖽𝗈  /games."
    )
    bot.send_message(message.chat.id, text)

# ==========================================
# === INICIALIZACIÓN ===
# ==========================================
if __name__ == '__main__':
    print("Bot en marcha en Railway...")
    bot.infinity_polling()