import config
import telebot


# Виніс, щоб не було зациклення імпортів)

bot = telebot.TeleBot(config.BOT_TOKEN)
