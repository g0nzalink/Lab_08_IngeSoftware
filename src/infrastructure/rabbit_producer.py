import pika
import json
from datetime import datetime
from dotenv import load_dotenv

from src.domain.recompensa import Cena

def enviar_cena_a_rabbitmq(cena: Cena):

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
        print(f" [:D] Restaurante envió los datos de la cena exitosamente: {mensaje_json}")
        
    except Exception as e:
        print(f" [D:] Error de conexión: {e}")
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
    enviar_cena_a_rabbitmq(mi_cena)