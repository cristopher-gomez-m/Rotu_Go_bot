import psycopg2
import logging
import os
import telegram
from telegram.ext import Updater,CommandHandler
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
    update.message.reply_text(f'''/listar - Lista los vuelos disponibles de acuerdo a una ciudad,aeropuerto o codigo IATA,sin importar si es origen o destino en un rango de fechas elejido(ejemplo /listar Quito 21-03-2021)
    /SEARCHD Busca los vuelos de acuerdo al destino seleccionada(ciudad,nombre del aeropuerto o código IATA) (ejemplo /SEARCHD Quito 19-03-2021)
    /SEARCHO Busca los vuelos de acuerdo al origen y fecha seleccionada(ciudad,nombre del aeropuerto o código IATA)(ejemplo /SEARCHO Quito 19-03-2021)
    /ListarIda_Venida Busca los vuelos de acuerdo al origen,destino y fechas de ida y regreso para reservar un viaje de ida-vuelta(Ejemplo: /ListarIda_Venida Guayaquil Quito 19-03-2021 20-03-2021)
    /BUY_TICKET Reserva un vuelo solo de ida(Ejemplo: /BUY_TICKET 1 Cristopher Gómez 35 (el 1 es el numero del vuelo,el 35 es el numero del asiento,puede variar a su gusto)
    /BUYRT_TICKET Reserva un vuelo de ida y vuelta.Especificar primero las fechas del viaje de ida(Ejemplo: /BUY_TICKET 1 2 Cristopher Gómez 35 39 (el 1 es el numero del vuelo de ida.el 2 es vuelo de regresp,el 35 es el numero del asiento,puede variar a su gusto)
     ''')
    photo="https://www.pinterest.es/pin/621567186048088830/"
    bot.send_photo(user_id, photo)
    


def ListarIda_Venida(update, context):
    user_id= update.effective_user['id']
    logger.info(f"El usuario {user_id},ha solicitado listar busca un vuelo de ida-venida")
    #context.bot.sendMessage(chat_id=user_id,parse_mode="HTML", text=f"Ingrese el destino del viaje: ")
    texto=update.message.text.replace("/listarIda_Venida ", "")
    print(texto)
    conn = psycopg2.connect(
    dbname="Rotu_Go_bot",
    user="postgres",
    password="748596alex",
    host="localhost",
    port="5432"
    )
    textito=texto.split()
    cursor=conn.cursor()
    print(textito[0])
    cursor.execute("SELECT id_vuelo, aeropuerto_origen, codigo_iata_origen, aeropuerto_destino, codigo_iata_destino, lugar_de_origen, lugar_de_llegada, asientos, fecha_de_ida, fecha_de_llegada FROM public.vuelo WHERE vuelo.lugar_de_origen LIKE %s ESCAPE '' AND vuelo.lugar_de_llegada LIKE %s ESCAPE '' AND vuelo.fecha_de_ida >= CAST(%s AS timestamp)AND vuelo.fecha_de_ida <= CAST(%s AS timestamp)+CAST('1 day' AS INTERVAL) OR vuelo.codigo_iata_origen LIKE %s ESCAPE '' AND vuelo.codigo_iata_destino LIKE %s ESCAPE '' AND vuelo.fecha_de_ida >= CAST(%s AS timestamp) AND vuelo.fecha_de_ida <= CAST(%s AS timestamp)+CAST('1 day' AS INTERVAL) OR vuelo.aeropuerto_origen LIKE %s ESCAPE '' AND vuelo.aeropuerto_destino LIKE %s ESCAPE '' AND vuelo.fecha_de_ida >= CAST(%s AS timestamp) AND vuelo.fecha_de_ida <= CAST(%s AS timestamp)+CAST('1 day' AS INTERVAL) OR vuelo.lugar_de_origen LIKE %s ESCAPE '' AND vuelo.lugar_de_llegada LIKE %s ESCAPE '' AND vuelo.fecha_de_ida >= CAST(%s AS timestamp)AND vuelo.fecha_de_ida <= CAST(%s AS timestamp)+CAST('1 day' AS INTERVAL) OR vuelo.codigo_iata_origen LIKE %s ESCAPE '' AND vuelo.codigo_iata_destino LIKE %s ESCAPE '' AND vuelo.fecha_de_ida >= CAST(%s AS timestamp)AND vuelo.fecha_de_ida <= CAST(%s AS timestamp)+CAST('1 day' AS INTERVAL) OR vuelo.aeropuerto_origen LIKE %s ESCAPE '' AND vuelo.aeropuerto_destino LIKE %s ESCAPE '' AND vuelo.fecha_de_ida >= CAST(%s AS timestamp)AND vuelo.fecha_de_ida <= CAST(%s AS timestamp)+CAST('1 day' AS INTERVAL)",(textito[0],textito[1],textito[2],textito[2],textito[0],textito[1],textito[2],textito[2],textito[0],textito[1],textito[2],textito[2],textito[1],textito[0],textito[3],textito[3],textito[1],textito[0],textito[3],textito[3],textito[1],textito[0],textito[3],textito[3],))
    row= cursor.fetchall()
    print(row)
    if len(row)== 0:
        context.bot.sendMessage(chat_id=user_id,parse_mode="HTML", text=f"No existe el vuelo buscado")
        photo="https://www.pinterest.es/pin/177470041554056898/"
        bot.send_photo(user_id, photo)
    else:
        for x in row:
            formato_local = "%x %X"
            locale.setlocale(locale.LC_ALL, "esp")
            print(x[8])
            fecha_sql1=x[8]
            fecha_sql2=x[9]
            fecha_formateada1=fecha_sql1.strftime(formato_local)
            fecha_formateada2=fecha_sql2.strftime(formato_local)
            context.bot.sendMessage(chat_id=user_id,parse_mode="HTML", text=f'''Vuelo:{x[0]},Aeropuerto de salida: {x[1]},Codigo IATA:{x[2]},Fecha de salida:{fecha_formateada1}
            Aeropuerto de destino:{x[3]}, Codigo IATA:{x[4]},Fecha de llegada:{fecha_formateada2}''') 
    conn.commit()
    conn.close()

#Listar todos los vuelos disponibles. 
def listar(update, context):
    try:
        user_id= update.effective_user['id']
        logger.info(f"El usuario {user_id},ha solicitado listar un vuelo")
        #context.bot.sendMessage(chat_id=user_id,parse_mode="HTML", text=f"Ingrese el destino del viaje: ")
        texto=update.message.text.replace("/listar ", "")
        conn = psycopg2.connect(
        dbname="Rotu_Go_bot",
        user="postgres",
        password="748596alex",
        host="localhost",
        port="5432"
        )
        textito=texto.split()
        cursor=conn.cursor()
        cursor.execute("SELECT id_vuelo, aeropuerto_origen, codigo_iata_origen, aeropuerto_destino, codigo_iata_destino, lugar_de_origen, lugar_de_llegada, asientos, fecha_de_ida, fecha_de_llegada FROM public.vuelo WHERE vuelo.lugar_de_llegada LIKE %s ESCAPE '' AND vuelo.fecha_de_ida >= CAST(%s AS timestamp)AND vuelo.fecha_de_ida <= CAST(%s AS timestamp)+CAST('1 day' AS INTERVAL) OR vuelo.codigo_iata_destino LIKE %s ESCAPE '' AND vuelo.fecha_de_ida >= CAST(%s AS timestamp) AND vuelo.fecha_de_ida <= CAST(%s AS timestamp)+CAST('1 day' AS INTERVAL)  OR vuelo.aeropuerto_destino LIKE %s ESCAPE '' AND vuelo.fecha_de_ida >= CAST(%s AS timestamp)AND vuelo.fecha_de_ida <= CAST(%s AS timestamp)+CAST('1 day' AS INTERVAL) OR vuelo.lugar_de_origen LIKE %s ESCAPE '' AND vuelo.fecha_de_ida >= CAST(%s AS timestamp)AND vuelo.fecha_de_ida <= CAST(%s AS timestamp)+CAST('1 day' AS INTERVAL) OR vuelo.codigo_iata_origen LIKE %s ESCAPE '' AND vuelo.fecha_de_ida >= CAST(%s AS timestamp) AND vuelo.fecha_de_ida <= CAST(%s AS timestamp)+CAST('1 day' AS INTERVAL) OR vuelo.aeropuerto_origen LIKE %s ESCAPE '' AND vuelo.fecha_de_ida >= CAST(%s AS timestamp)AND vuelo.fecha_de_ida <= CAST(%s AS timestamp)+CAST('1 day' AS INTERVAL)",(textito[0],textito[1],textito[1],textito[0],textito[1],textito[1],textito[0],textito[1],textito[1],textito[0],textito[1],textito[1],textito[0],textito[1],textito[1],textito[0],textito[1],textito[1],))
        row=cursor.fetchall()
        print(row)
        print(textito[0])
        print(textito[1])
        if len(row) == 0:
            context.bot.sendMessage(chat_id=user_id,parse_mode="HTML", text=f"No existe el vuelo buscado")
            photo="https://www.pinterest.es/pin/177470041554056898/"
            bot.send_photo(user_id, photo)

        else:
            for x in row:

                formato_local = "%x %X"
                locale.setlocale(locale.LC_ALL, "esp")
                fecha_sql1=x[8]
                fecha_sql2=x[9]
                fecha_formateada1=fecha_sql1.strftime(formato_local)
                fecha_formateada2=fecha_sql2.strftime(formato_local)
                context.bot.sendMessage(chat_id=user_id,parse_mode="HTML", text=f'''Vuelo:{x[0]},Aeropuerto de salida: {x[1]},Codigo IATA:{x[2]},Fecha de salida:{fecha_formateada1}
                Aeropuerto de destino:{x[3]}, Codigo IATA:{x[4]},Fecha de llegada:{fecha_formateada2}''') 
        conn.commit()
        conn.close()
    except(IndexError):
        name= update.effective_user['first_name']
        update.message.reply_text(f" {name},Faltan datos por ingresar")  
        photo="https://www.pinterest.es/pin/177470041554056898/"
        bot.send_photo(user_id, photo)




def SEARCHD(update, context):
    user_id= update.effective_user['id']
    logger.info(f"El usuario {user_id},ha solicitado listar un vuelo")
    #context.bot.sendMessage(chat_id=user_id,parse_mode="HTML", text=f"Ingrese el destino del viaje: ")
    texto=update.message.text.replace("/SEARCHD ", "")
    print(texto)
    conn = psycopg2.connect(
    dbname="Rotu_Go_bot",
    user="postgres",
    password="748596alex",
    host="localhost",
    port="5432"
    )
    textito=texto.split()
    cursor=conn.cursor()
    query= "SELECT (id_vuelo, aeropuerto_origen, codigo_iata_origen, aeropuerto_destino, codigo_iata_destino, lugar_de_origen, lugar_de_llegada, asientos, fecha_de_ida, fecha_de_llegada) FROM public.vuelo WHERE vuelo.lugar_de_llegada LIKE '{}'"  
    cursor.execute("SELECT id_vuelo, aeropuerto_origen, codigo_iata_origen, aeropuerto_destino, codigo_iata_destino, lugar_de_origen, lugar_de_llegada, asientos, fecha_de_ida, fecha_de_llegada FROM public.vuelo WHERE vuelo.lugar_de_llegada LIKE %s ESCAPE '' AND vuelo.fecha_de_ida >= CAST(%s AS timestamp) AND vuelo.fecha_de_ida <= CAST(%s AS timestamp)+CAST('1 day' AS INTERVAL) OR vuelo.codigo_iata_destino LIKE %s ESCAPE '' AND vuelo.fecha_de_ida >= CAST(%s AS timestamp) AND vuelo.fecha_de_ida <= CAST(%s AS timestamp)+CAST('1 day' AS INTERVAL) OR vuelo.aeropuerto_destino LIKE %s ESCAPE '' AND vuelo.fecha_de_ida >= CAST(%s AS timestamp) AND vuelo.fecha_de_ida <= CAST(%s AS timestamp)+CAST('1 day' AS INTERVAL)",(textito[0],textito[1],textito[1],textito[0],textito[1],textito[1],textito[0],textito[1],textito[1],))
    row= cursor.fetchall()
    print(row)
    if len(row)== 0:
        context.bot.sendMessage(chat_id=user_id,parse_mode="HTML", text=f"No existe el vuelo buscado")
        photo="https://www.pinterest.es/pin/177470041554056898/"
        bot.send_photo(user_id, photo)
    else:
        for x in row:
            formato_local = "%x %X"
            locale.setlocale(locale.LC_ALL, "esp")
            print(x[8])
            fecha_sql1=x[8]
            fecha_sql2=x[9]
            fecha_formateada1=fecha_sql1.strftime(formato_local)
            fecha_formateada2=fecha_sql2.strftime(formato_local)
            context.bot.sendMessage(chat_id=user_id,parse_mode="HTML", text=f'''Vuelo:{x[0]},Aeropuerto de salida: {x[1]},Codigo IATA:{x[2]},Fecha de salida:{fecha_formateada1}
            Aeropuerto de destino:{x[3]}, Codigo IATA:{x[4]},Fecha de llegada:{fecha_formateada2}''') 
    conn.commit()
    conn.close()

#Buscar origen
def SEARCHO(update, context):
    user_id= update.effective_user['id']
    logger.info(f"El usuario {user_id},ha solicitado listar un vuelo")
    #context.bot.sendMessage(chat_id=user_id,parse_mode="HTML", text=f"Ingrese el destino del viaje: ")
    texto=update.message.text.replace("/SEARCHO ", "")
    conn = psycopg2.connect(
    dbname="Rotu_Go_bot",
    user="postgres",
    password="748596alex",
    host="localhost",
    port="5432"
    )
    textito= texto.split()
    cursor=conn.cursor()
    query= "SELECT (id_vuelo, aeropuerto_origen, codigo_iata_origen, aeropuerto_destino, codigo_iata_destino, lugar_de_origen, lugar_de_llegada, asientos, fecha_de_ida, fecha_de_llegada) FROM public.vuelo WHERE vuelo.lugar_de_llegada LIKE '{}'"  
    cursor.execute("SELECT id_vuelo, aeropuerto_origen, codigo_iata_origen, aeropuerto_destino, codigo_iata_destino, lugar_de_origen, lugar_de_llegada, asientos, fecha_de_ida, fecha_de_llegada FROM public.vuelo WHERE vuelo.lugar_de_origen LIKE %s ESCAPE '' AND vuelo.fecha_de_ida >= CAST(%s AS timestamp) AND vuelo.fecha_de_ida <= CAST(%s AS timestamp)+CAST('1 day' AS INTERVAL) OR vuelo.codigo_iata_origen LIKE %s ESCAPE '' AND vuelo.fecha_de_ida >= CAST(%s AS timestamp) AND vuelo.fecha_de_ida <= CAST(%s AS timestamp)+CAST('1 day' AS INTERVAL) OR vuelo.aeropuerto_origen LIKE %s ESCAPE '' AND vuelo.fecha_de_ida >= CAST(%s AS timestamp) AND vuelo.fecha_de_ida <= CAST(%s AS timestamp)+CAST('1 day' AS INTERVAL)",(textito[0],textito[1],textito[1],textito[0],textito[1],textito[1],textito[0],textito[1],textito[1],))
    row= cursor.fetchall()
    print(row)
    if len(row)== 0:
        context.bot.sendMessage(chat_id=user_id,parse_mode="HTML", text=f"No existe el vuelo buscado")
        photo="https://www.pinterest.es/pin/177470041554056898/"
        bot.send_photo(user_id, photo)
    else:
        for x in row:
            formato_local = "%x %X"
            locale.setlocale(locale.LC_ALL, "esp")
            print(x[8])
            fecha_sql1=x[8]
            fecha_sql2=x[9]
            fecha_formateada1=fecha_sql1.strftime(formato_local)
            fecha_formateada2=fecha_sql2.strftime(formato_local)
            context.bot.sendMessage(chat_id=user_id,parse_mode="HTML", text=f'''Vuelo:{x[0]},Aeropuerto de salida: {x[1]},Codigo IATA:{x[2]},Fecha de salida:{fecha_formateada1}
            Aeropuerto de destino:{x[3]}, Codigo IATA:{x[4]},Fecha de llegada:{fecha_formateada2}''') 
    conn.commit()
    conn.close()
#Reservar vuelo solo de ida
def BUY_TICKET(update, context):
    try:
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
        print(textito[2])
        if int(textito[3])>180 or int(textito[3])<0:
            context.bot.sendMessage(chat_id=user_id,parse_mode="HTML", text=f"No existe un vuelo con ese numero de asiento")
            photo="https://www.pinterest.es/pin/177470041554056898/"
            bot.send_photo(user_id, photo)
    except(IndexError):
        context.bot.sendMessage(chat_id=user_id,parse_mode="HTML", text=f"No ha ingresado todos los datos necesarios")
        photo="https://www.pinterest.es/pin/177470041554056898/"
        bot.send_photo(user_id, photo)

    else:
        try:
            vuelo_valido=textito[0]
            cursor.execute("SELECT id_vuelo,asiento FROM public.cliente WHERE cliente.id_vuelo =%s AND cliente.asiento =%s",(vuelo_valido,textito[3],))
            row3=cursor.fetchall()
            print(len(row3))
            if len(row3)==0:
                row2=cursor.fetchall()
                cursor.execute("INSERT INTO public.cliente (id_telegram, nombre, apellido, asiento, id_vuelo) VALUES (%s, %s, %s, %s,%s)",(user_id,textito[1],textito[2],textito[3],vuelo_valido,))
                cursor.execute("SELECT lugar_de_origen,lugar_de_llegada FROM public.vuelo WHERE vuelo.id_vuelo=%s",(vuelo_valido,))
                row9=cursor.fetchall()
                origen=row9[0][0]
                llegada=row9[0][1]
                update.message.reply_text(f" {name},Gracias por comprar el vuelo {origen}-{llegada} <3")   
                photo="https://www.pinterest.com/pin/653162752196322125/"
                bot.send_photo(user_id, photo)
            else:
                update.message.reply_text(f" {name},El vuelo con ese asiento ya ha sido comprado")  
                photo="https://www.pinterest.es/pin/177470041554056898/"
                bot.send_photo(user_id, photo)
            conn.commit()
            conn.close()
        except(IndexError):
            update.message.reply_text(f" {name},Faltan datos por ingresar")  
            photo="https://www.pinterest.es/pin/177470041554056898/"
            bot.send_photo(user_id, photo)

def BUYRT_TICKET(update, context):
    user_id= update.effective_user['id']
    name= update.effective_user['first_name']
    logger.info(f"El usuario {user_id},ha solicitado comprar un vuelo de ida y vuelta")
    texto=update.message.text.replace("/BUYRT_TICKET ", "")
    conn = psycopg2.connect(
        dbname="Rotu_Go_bot",   
        user="postgres",
        password="748596alex",
        host="localhost",
        port="5432"
    )
    textito= texto.split()
    cursor=conn.cursor()
    print(textito[0])
    print(textito[5])
    if int(textito[4])>180 or int(textito[5])>180 or int(textito[4])<=0 or int(textito[5])<=0:
        context.bot.sendMessage(chat_id=user_id,parse_mode="HTML", text=f"No existe un vuelo con ese numero de asiento")
        photo="https://www.pinterest.es/pin/177470041554056898/"
        bot.send_photo(user_id, photo)
    else:
        try:
            vuelo_valido_ida=textito[0]
            vuelo_valido_regreso=textito[1]
            cursor.execute("SELECT id_vuelo,asiento FROM public.cliente WHERE cliente.id_vuelo =%s AND cliente.asiento =%s",(vuelo_valido_ida,textito[4],))
            row3=cursor.fetchall()
            cursor.execute("SELECT id_vuelo,asiento FROM public.cliente WHERE cliente.id_vuelo =%s AND cliente.asiento =%s",(vuelo_valido_regreso,textito[5],))
            row5=cursor.fetchall()
            print(len(row3))
            #Si no existen vuelos comprados con las caracteristicas seleccionadas el usuario se lo registra
            if len(row3)==0 or len(row5)==0:
                cursor.execute("INSERT INTO public.cliente (id_telegram, nombre, apellido, asiento, id_vuelo) VALUES (%s, %s, %s, %s,%s)",(user_id,textito[2],textito[3],textito[4],vuelo_valido_ida,))
                #row6=cursor.fetchall()
                cursor.execute("INSERT INTO public.cliente (id_telegram, nombre, apellido, asiento, id_vuelo) VALUES (%s, %s, %s, %s,%s)",(user_id,textito[1],textito[2],textito[5],vuelo_valido_regreso,))
                #row7=cursor.fetchall()
                update.message.reply_text(f"{name},Gracias por comprar los vuelos de ida y regreso{vuelo_valido_ida}-{vuelo_valido_regreso}")    
                photo="https://www.pinterest.com/pin/653162752196322125/"
                bot.send_photo(user_id, photo)
                conn.commit()
                conn.close()
            else:
                update.message.reply_text(f" {name},El vuelo con ese asiento ya ha sido comprado")  
                photo="https://www.pinterest.es/pin/177470041554056898/"
                bot.send_photo(user_id, photo)
                conn.commit()
                conn.close()
        except(IndexError):
            update.message.reply_text(f" {name},Faltan datos por ingresar")  
            photo="https://www.pinterest.es/pin/177470041554056898/"
            bot.send_photo(user_id, photo)




if __name__ == "__main__":
    #Obtenemos la informacion del bot
    bot= telegram.Bot(token='1658316716:AAGhzdiTVEtzgvvXksHYpfMxOS2sdteSajE')
    print(bot.getMe())

#Enlazamos el updater con el bot
updater= Updater(bot.token, use_context=True)

#Despachador
despachador = updater.dispatcher

#Creamos las funciones del bot
despachador.add_handler(CommandHandler("start", start))
despachador.add_handler(CommandHandler("listar",listar))
despachador.add_handler(CommandHandler("SEARCHD",SEARCHD))
despachador.add_handler(CommandHandler("SEARCHO",SEARCHO))
despachador.add_handler(CommandHandler("BUY_TICKET",BUY_TICKET))
despachador.add_handler(CommandHandler("ListarIda_Venida",ListarIda_Venida))
despachador.add_handler(CommandHandler("BUYRT_TICKET",BUYRT_TICKET))
updater.start_polling() 
updater.idle() #Permite finaliza el bot con Ctrl + C





 


 

     

