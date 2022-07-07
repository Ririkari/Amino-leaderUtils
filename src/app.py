from . import Core
from .lib.lib_app import modules
from os import path
import telebot as tb
import json


token: str = str()

#init telegram bot config file
if path.isfile("src/lib/init/conf.json") == True:
    is_true_token: str = str()
    while True:
        is_true_token = str(input('Start bot with current token: "Y"/"N": ')).upper()
        if is_true_token == "Y":
            with open("src/lib/init/conf.json", "r", encoding= "utf-8") as File:
                data: dict = json.load(File)
                token = data.get("token")
            break
        elif is_true_token == "N":
            token = input("Telegram bot TOKEN: ")
            with open("src/lib/init/conf.json", "w", encoding= "utf-8") as File:
                json.dump(
                            {"token": token},
                            File
                        )
            break
else:
    token = input("Telegram bot TOKEN: ")
    with open("src/lib/init/conf.json", "w", encoding= "utf-8") as File:
        json.dump(
                    {"token": token},
                    File
                )

#init bot
Core = Core.Core()
bot = tb.TeleBot(token)
MODULES = modules.MODULES

@bot.message_handler(commands= 'start')
def init_bot(message) -> None:
    bot.reply_to(message, "Successfully inited")

@bot.message_handler(commands= modules.MODULES)
def bot_answer(message) -> None:
    answer: str = Core.selector(args= message.text)
    try:
        bot.reply_to(message, answer)
    except:
        pass

bot.infinity_polling()
