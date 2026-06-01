import pika
import json
import os
from datetime import datetime
from dotenv import load_dotenv

from src.domain.recompensa import Cena, CalculadoraRecompensas

load_dotenv()

def main():

    usuario = os.getenv("RABBIT_USER")
    password = os.getenv("RABBIT_PASSWORD")
    host = os.getenv("RABBIT_HOST")

    credenciales = pika.PlainCredentials(usuario, password)
    parametros = pika.ConnectionParameters(host, 5672, "/", credenciales)
    
    conexion = pika.BlockingConnection(parametros)
    canal = conexion.channel()
    
    nombre_cola = "cola_recompensas_gonzalo"
    canal.queue_declare(queue=nombre_cola, durable=True)
    
    def callback(ch, method, properties, body):
        texto_recibido = body.decode()
        print(f" [*] Mensaje crudo recibido desde RabbitMQ: {texto_recibido}")
        
        try:
            datos = json.loads(texto_recibido)
            
            cena_recibida = Cena(
                monto=datos["monto"],
                tarjeta_cliente=datos["tarjeta_cliente"],
                codigo_restaurante=datos["codigo_restaurante"],
                fecha_hora=datetime.fromisoformat(datos["fecha_hora"])
            )
            
            puntos = CalculadoraRecompensas.calcular_puntos(cena_recibida)
            print(f" [:D] ÉXITO: Se calcularon {puntos} puntos para la tarjeta {cena_recibida.tarjeta_cliente}\n")
            
        except Exception as e:
            print(f" [D:] Error al procesar la recompensa: {e}\n")

    canal.basic_consume(queue=nombre_cola, on_message_callback=callback, auto_ack=True)
    
    print(f' [:D] Sistema de Recompensas esperando en la cola "{nombre_cola}". Presiona CTRL+C para salir.')
    canal.start_consuming()

if __name__ == "__main__":
    main()