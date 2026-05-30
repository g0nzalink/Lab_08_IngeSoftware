from dataclasses import dataclass
from datetime import datetime

@dataclass
class Cena:
    monto: float
    tarjeta_cliente: str
    codigo_restaurante: str
    fecha_hora: datetime

class CalculadoraRecompensas:
    
    PORCENTAJE_RECOMPENSA = 0.10 

    @staticmethod
    def calcular_puntos(cena: Cena) -> float:
        if cena.monto <= 0:
            raise ValueError("El monto de la cena debe ser mayor a cero.")
        
        puntos = cena.monto * CalculadoraRecompensas.PORCENTAJE_RECOMPENSA
        return round(puntos, 2)