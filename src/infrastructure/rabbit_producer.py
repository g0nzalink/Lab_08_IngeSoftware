import pika
import json
import os
from datetime import datetime
from dotenv import load_dotenv

from src.domain.recompensa import Cena
from src.application.puertos import PuertoMensajeria

load_dotenv()

class AdaptadorRabbitMQ(PuertoMensajeria):
    
    def publicar_evento_cena(self, cena: Cena) -> None:
        usuario = os.getenv("RABBIT_USER")
        password = os.getenv("RABBIT_PASSWORD")
        host = os.getenv("RABBIT_HOST")

        credenciales = pika.PlainCredentials(usuario, password)
        parametros = pika.ConnectionParameters(host, 5672, "/", credenciales)
        
        try:
            conexion = pika.BlockingConnection(parametros)
            canal = conexion.channel()
            
            nombre_cola = "cola_recompensas_gonzalo" 
            canal.queue_declare(queue=nombre_cola, durable=True)
            
            mensaje_dict = {
                "monto": cena.monto,
                "tarjeta_cliente": cena.tarjeta_cliente,
                "codigo_restaurante": cena.codigo_restaurante,
                "fecha_hora": cena.fecha_hora.isoformat()
            }
            mensaje_json = json.dumps(mensaje_dict)
            
            canal.basic_publish(exchange="", routing_key=nombre_cola, body=mensaje_json)
            print(f" [:D] Adaptador RabbitMQ publicó el evento exitosamente: {mensaje_json}")
            
        except Exception as e:
            print(f" [!] Error de conexión en el adaptador: {e}")
        finally:
            if "conexion" in locals() and conexion.is_open:
                conexion.close()

if __name__ == "__main__":
    mi_cena = Cena(
        monto=250.0, 
        tarjeta_cliente="9876-5432-1098-7654", 
        codigo_restaurante="REST-CENTRAL", 
        fecha_hora=datetime.now()
    )
    
    publicador = AdaptadorRabbitMQ()
    
    publicador.publicar_evento_cena(mi_cena)