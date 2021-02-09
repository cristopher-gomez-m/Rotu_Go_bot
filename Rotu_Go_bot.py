import psycopg2
import logging
import os
import telegram
from telegram.ext import Updater,CommandHandler

#Configurar el loggin
logging.basicConfig(
    level = logging.INFO, format= "%(asctime)s - %(name)s - %(levelname)s - %(message)s,"
)

logger = logging.getLogger()

#Solicitar el TOKEN
TOKEN= os.getenv("TOKEN")

def start(update, context):
    logger.info(f"El usuario {update.effective_user['fist_name']},ha iniciado una conversación")
    name= update.effective_user['first_name']
    update.message.reply_text(f"Hola {name}, soy tu asistente de vuelo UwU")

if __name__ == "__main__":
    #Obtenemos la informacion del bot
    bot= telegram.Bot(token= TOKEN)
    print(bot.getMe())

#Enlazamos el updater con el bot
updater= Updater(bot.token, use_context=True)

#Despachador
despachador = updater.dispatcher

#Creamos las funciones del bot
despachador.add_handler(CommandHandler("start", start))
updater.start_polling()
updater.idle() #Permite finaliza el bot con Ctrl + C
despachador.add_handler(CommandHandler)


 

 #Global constant
 PSQL_HOST="localhost"
 PSQL_PORT="5432"
 PSQL_USER="postgres"
 PSQL_PASS="748596alex"
 PSQL_DB="Rotu_Go_bot"

 #Connection
 connection_address="""
 

     

