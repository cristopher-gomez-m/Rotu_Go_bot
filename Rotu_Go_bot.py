import psycopg2
import logging
import os
import telegram
from telegram.ext import Updater,CommandHandler
import random
import time
from datetime import datetime 
import dateutil.parser 
import pytz
import tzlocal
import locale
    

#Configurar el loggin
logging.basicConfig(
    level = logging.INFO, format= "%(asctime)s - %(name)s - %(levelname)s - %(message)s,"
)

logger = logging.getLogger()

#Solicitar el TOKEN
TOKEN= os.getenv("TOKEN")
#Funcion de inicio
def start(update, context):
    user_id= update.effective_user['id']
    logger.info(f"El usuario {update.effective_user['first_name']},ha iniciado una conversación")
    name= update.effective_user['first_name']
    update.message.reply_text(f"Bienvenido {name},Soy Izumi,tu asistente de vuelo")
    update.message.reply_text(f'''/listar - Lista los vuelos disponibles
    /SEARCHD Busca los vuelos de acuerdo al destino seleccionado(ciudad,nombre del aeropuerto o código IATA)
    /SEARCHD Busca los vuelos de acuerdo al origen seleccionado(ciudad,nombre del aeropuerto o código IATA)
    /BUY_TICKET Reserva un vuelo solo de ida(Ejemplo: /BUY_TICKET Cristopher Gómez Guayaquil 19-03-2021 Quito 19-03-2021)
     ''')
    photo="https://www.pinterest.es/pin/621567186048088830/"
    bot.send_photo(user_id, photo)
    

def random_number(update, context):
    user_id= update.effective_user['id']
    logger.info(f"El usuario {user_id},ha solicitado un numero aleatorio")
    number=random.randint(0,10)
    context.bot.sendMessage(chat_id=user_id,parse_mode="HTML", text=f"Numero aleatorio:\n{number}")
#Listar todos los vuelos disponibles. 
def listar(update, context):
    user_id= update.effective_user['id']
    logger.info(f"El usuario {user_id},ha solicitado listar un vuelo")
    #context.bot.sendMessage(chat_id=user_id,parse_mode="HTML", text=f"Ingrese el destino del viaje: ")
    texto=update.message.text.replace("/listar ", "")
    print(texto)
    textito=str(texto)
    print(textito)
    conn = psycopg2.connect(
    dbname="Rotu_Go_bot",
    user="postgres",
    password="748596alex",
    host="localhost",
    port="5432"
    )
    cursor=conn.cursor()
    query= "SELECT (id_vuelo, aeropuerto_origen, codigo_iata_origen, aeropuerto_destino, codigo_iata_destino, lugar_de_origen, lugar_de_llegada, asientos, fecha_de_ida, fecha_de_llegada) FROM public.vuelo WHERE vuelo.lugar_de_llegada LIKE '{}'"  
    cursor.execute("SELECT id_vuelo, aeropuerto_origen, codigo_iata_origen, aeropuerto_destino, codigo_iata_destino, lugar_de_origen, lugar_de_llegada, asientos, fecha_de_ida, fecha_de_llegada FROM public.vuelo WHERE vuelo.lugar_de_llegada LIKE %s ESCAPE '' OR vuelo.codigo_iata_destino LIKE %s ESCAPE '' OR vuelo.aeropuerto_destino LIKE %s ESCAPE '' OR vuelo.lugar_de_origen LIKE %s ESCAPE '' OR vuelo.codigo_iata_origen LIKE %s ESCAPE '' OR vuelo.aeropuerto_origen LIKE %s ESCAPE ''",(textito,textito,textito,textito,textito,textito,))
    row= cursor.fetchall()
    for x in row:
        formato_local = "%x %X"
        locale.setlocale(locale.LC_ALL, "esp")
        print(x[8])
        fecha_sql1=x[8]
        fecha_sql2=x[9]
        fecha_formateada1=fecha_sql1.strftime(formato_local)
        fecha_formateada2=fecha_sql2.strftime(formato_local)
        context.bot.sendMessage(chat_id=user_id,parse_mode="HTML", text=f'''Vuelo:{x[0]},Aeropuerto de salida: {x[1]},Codigo IATA:{x[2]},Fecha de salida:{fecha_formateada1}
        Aeropuerto de destino:{x[4]}, Codigo IATA:{x[5]},Fecha de llegada:{fecha_formateada2}''') 
    conn.commit()
    conn.close()



def SEARCHD(update, context):
    user_id= update.effective_user['id']
    logger.info(f"El usuario {user_id},ha solicitado listar un vuelo")
    #context.bot.sendMessage(chat_id=user_id,parse_mode="HTML", text=f"Ingrese el destino del viaje: ")
    texto=update.message.text.replace("/SEARCHD ", "")
    print(texto)
    textito=str(texto)
    print(textito)
    conn = psycopg2.connect(
    dbname="Rotu_Go_bot",
    user="postgres",
    password="748596alex",
    host="localhost",
    port="5432"
    )
    cursor=conn.cursor()
    query= "SELECT (id_vuelo, aeropuerto_origen, codigo_iata_origen, aeropuerto_destino, codigo_iata_destino, lugar_de_origen, lugar_de_llegada, asientos, fecha_de_ida, fecha_de_llegada) FROM public.vuelo WHERE vuelo.lugar_de_llegada LIKE '{}'"  
    cursor.execute("SELECT id_vuelo, aeropuerto_origen, codigo_iata_origen, aeropuerto_destino, codigo_iata_destino, lugar_de_origen, lugar_de_llegada, asientos, fecha_de_ida, fecha_de_llegada FROM public.vuelo WHERE vuelo.lugar_de_llegada LIKE %s ESCAPE '' OR vuelo.codigo_iata_destino LIKE %s ESCAPE '' OR vuelo.aeropuerto_destino LIKE %s ESCAPE ''",(textito,textito,textito,))
    row= cursor.fetchall()
    print(row)
    for x in row:
        formato_local = "%x %X"
        locale.setlocale(locale.LC_ALL, "esp")
        print(x[8])
        fecha_sql1=x[8]
        fecha_sql2=x[9]
        fecha_formateada1=fecha_sql1.strftime(formato_local)
        fecha_formateada2=fecha_sql2.strftime(formato_local)
        context.bot.sendMessage(chat_id=user_id,parse_mode="HTML", text=f'''Vuelo:{x[0]},Aeropuerto de salida: {x[1]},Codigo IATA:{x[2]},Fecha de salida:{fecha_formateada1}
        Aeropuerto de destino:{x[4]}, Codigo IATA:{x[5]},Fecha de llegada:{fecha_formateada2}''') 
    conn.commit()
    conn.close()

#Buscar origen
def SEARCHO(update, context):
    user_id= update.effective_user['id']
    logger.info(f"El usuario {user_id},ha solicitado listar un vuelo")
    #context.bot.sendMessage(chat_id=user_id,parse_mode="HTML", text=f"Ingrese el destino del viaje: ")
    texto=update.message.text.replace("/SEARCHO ", "")
    print(texto)
    textito=str(texto)
    print(textito)
    conn = psycopg2.connect(
    dbname="Rotu_Go_bot",
    user="postgres",
    password="748596alex",
    host="localhost",
    port="5432"
    )
    cursor=conn.cursor()
    query= "SELECT (id_vuelo, aeropuerto_origen, codigo_iata_origen, aeropuerto_destino, codigo_iata_destino, lugar_de_origen, lugar_de_llegada, asientos, fecha_de_ida, fecha_de_llegada) FROM public.vuelo WHERE vuelo.lugar_de_llegada LIKE '{}'"  
    cursor.execute("SELECT id_vuelo, aeropuerto_origen, codigo_iata_origen, aeropuerto_destino, codigo_iata_destino, lugar_de_origen, lugar_de_llegada, asientos, fecha_de_ida, fecha_de_llegada FROM public.vuelo WHERE vuelo.lugar_de_origen LIKE %s ESCAPE '' OR vuelo.codigo_iata_origen LIKE %s ESCAPE '' OR vuelo.aeropuerto_origen LIKE %s ESCAPE ''",(textito,textito,textito,))
    row= cursor.fetchall()
    print(row)
    for x in row:
        formato_local = "%x %X"
        locale.setlocale(locale.LC_ALL, "esp")
        print(x[8])
        fecha_sql1=x[8]
        fecha_sql2=x[9]
        fecha_formateada1=fecha_sql1.strftime(formato_local)
        fecha_formateada2=fecha_sql2.strftime(formato_local)
        context.bot.sendMessage(chat_id=user_id,parse_mode="HTML", text=f'''Vuelo:{x[0]},Aeropuerto de salida: {x[1]},Codigo IATA:{x[2]},Fecha de salida:{fecha_formateada1}
        Aeropuerto de destino:{x[4]}, Codigo IATA:{x[5]},Fecha de llegada:{fecha_formateada2}''') 
    conn.commit()
    conn.close()
#Reservar vuelo solo de ida
def BUY_TICKET(update, context):
    user_id= update.effective_user['id']
    name= update.effective_user['first_name']
    logger.info(f"El usuario {user_id},ha solicitado comprar un vuelo")
    texto=update.message.text.replace("/BUY_TICKET ", "")
    conn = psycopg2.connect(
        dbname="Rotu_Go_bot",
        user="postgres",
        password="748596alex",
        host="localhost",
        port="5432"
    )
    textito= texto.split()
    cursor=conn.cursor()
    query= '''SELECT id_vuelo FROM public.vuelo WHERE vuelo.lugar_de_origen LIKE %s ESCAPE AND vuelo.fecha_de_ida >= CAST('%s' AS timestamp) AND vuelo.lugar_de_llegada LIKE %s ESCAPE AND vuelo.fecha_de_llegada >= CAST('%s' AS timestamp)''' 
    cursor.execute("SELECT id_vuelo FROM public.vuelo WHERE vuelo.lugar_de_origen LIKE %s ESCAPE '' AND vuelo.fecha_de_ida >= CAST(%s AS timestamp) AND vuelo.lugar_de_llegada LIKE %s ESCAPE '' AND vuelo.fecha_de_llegada >= CAST(%s AS timestamp)",(textito[2],textito[3],textito[4],textito[5],))
    row= cursor.fetchall()
    try:
        for x in row:
            row2=cursor.fetchall()
            cursor.execute("INSERT INTO public.cliente (ip_telegram, fist_name, id_vuelo) VALUES (%s, %s, %s)",(user_id,textito[1] ,x))
            update.message.reply_text(f" {name},Gracias por comprar el vuelo {x} <3")   
            photo="https://www.pinterest.com/pin/653162752196322125/"
            bot.send_photo(user_id, photo)
            conn.commit()
            conn.close()
    except (psycopg2.errors.UniqueViolation):
        update.message.reply_text(f" {name},Ya compraste ese vuelo")  
        photo="https://www.pinterest.es/pin/177470041554056898/"
        bot.send_photo(user_id, photo)

def BUYRT_TICKET(update, context):
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
    for x in row:
        context.bot.sendMessage(chat_id=user_id,parse_mode="HTML", text=f"Vuelo:\naeropueto:{x[0]},codigoIATA:{x[1]},Lugar de partida:{x[2]},Destino:{x[3]},Fecha y hora de partida:{x[4]},Fecha y hora de llegada:{x[5]}")

    conn.commit()
    conn.close()




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





 


 

     

