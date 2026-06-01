import pika
import json
import os
from datetime import datetime
from dotenv import load_dotenv

from src.domain.recompensa import Cena, CalculadoraRecompensas

load_dotenv()

class ConsumidorRabbitMQ:

    def __init__(self):
        self.usuario = os.getenv("RABBIT_USER")
        self.password = os.getenv("RABBIT_PASSWORD")
        self.host = os.getenv("RABBIT_HOST")
        self.nombre_cola = "cola_recompensas_gonzalo"

    def _procesar_mensaje(self, ch, method, properties, body):
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

    def iniciar_consumo(self):
        credenciales = pika.PlainCredentials(self.usuario, self.password)
        parametros = pika.ConnectionParameters(self.host, 5672, "/", credenciales)
        
        try:
            conexion = pika.BlockingConnection(parametros)
            canal = conexion.channel()
            
            canal.queue_declare(queue=self.nombre_cola, durable=True)
            
            canal.basic_consume(
                queue=self.nombre_cola, 
                on_message_callback=self._procesar_mensaje, 
                auto_ack=True
            )
            
            print(f' [:D] Sistema de Recompensas esperando en la cola "{self.nombre_cola}". Presiona CTRL+C para salir.')
            canal.start_consuming()
            
        except Exception as e:
            print(f" [!] Error de conexión en el consumidor: {e}")

if __name__ == "__main__":
    consumidor = ConsumidorRabbitMQ()
    consumidor.iniciar_consumo()