import psycopg2
import logging
import os
import telegram
from telegram.ext import Updater,CommandHandler
import random

#Configurar el loggin
logging.basicConfig(
    level = logging.INFO, format= "%(asctime)s - %(name)s - %(levelname)s - %(message)s,"
)

logger = logging.getLogger()

#Solicitar el TOKEN
TOKEN= os.getenv("TOKEN")
#Funcion de inicio
def start(update, context):
    logger.info(f"El usuario {update.effective_user['first_name']},ha iniciado una conversación")
    name= update.effective_user['first_name']
    update.message.reply_text(f"Hola {name}-kun, soy tu asistente de vuelo,¿que deseas hacer? UwU ")

def random_number(update, context):
    user_id= update.effective_user['id']
    logger.info(f"El usuario {user_id},ha solicitado un numero aleatorio")
    number=random.randint(0,10)
    context.bot.sendMessage(chat_id=user_id,parse_mode="HTML", text=f"Numero aleatorio:\n{number}")
#Listar todos los vuelos disponibles. 
def listar(update, context):
    user_id= update.effective_user['id']
    logger.info(f"El usuario {user_id},ha solicitado listar los vuelos")
    conn = psycopg2.connect(
        dbname="Rotu_Go_bot",
        user="postgres",
        password="748596alex",
        host="localhost",
        port="5432"
    )
    cursor=conn.cursor()
    query= '''SELECT aeropuerto, codigo_iata,lugar_de_origen,lugar_de_llegada,fecha_de_ida, fecha_de_llegada FROM vuelo'''
    cursor.execute(query)
    row= cursor.fetchall()
    #print(row[0][1]) {}
    for x in row:
        context.bot.sendMessage(chat_id=user_id,parse_mode="HTML", text=f"Vuelo:\n{x[0]},{x[1]},{x[2]},{x[3]},{x[4]},{x[5]}")

    conn.commit()
    conn.close()

#Buscar destino
def SEARCHD(update, context):
    pass

#Buscar origen
def SEARCHO(update, context):
    pass

#Reservar vuelo solo de ida
def BUY_TICKET(update, context):
    pass

def BUYRT_TICKET(update, context):
    pass

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
despachador.add_handler(CommandHandler("listar",listar))
despachador.add_handler(CommandHandler("random",random_number))
despachador.add_handler(CommandHandler("SEARCHD",SEARCHD))
despachador.add_handler(CommandHandler("SEARCHO",SEARCHO))
despachador.add_handler(CommandHandler("BUY_TICKET",BUY_TICKET))
despachador.add_handler(CommandHandler("BUYRT_TICKET",BUYRT_TICKET))
updater.start_polling()
updater.idle() #Permite finaliza el bot con Ctrl + C
updater.start_polling()
despachador.add_handler(CommandHandler("SEARCHD",SEARCHD))
despachador.add_handler(CommandHandler("SEARCHO",SEARCHO))
despachador.add_handler(CommandHandler("BUY_TICKET",BUY_TICKET))
despachador.add_handler(CommandHandler("BUYRT_TICKET",BUYRT_TICKET))



 

 #Global constant
 #PSQL_HOST="localhost"
 #PSQL_PORT="5432"
 #PSQL_USER="postgres"
 #PSQL_PASS="748596alex"
 #PSQL_DB="Rotu_Go_bot"

 #Connection
 #connection_address="""
 

     

