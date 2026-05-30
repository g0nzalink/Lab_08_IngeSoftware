from datetime import datetime
import pytest 

from src.domain.recompensa import Cena, CalculadoraRecompensas

def test_calcular_puntos_exitosamente():

    mi_cena = Cena(
        monto=1000.0,
        tarjeta_cliente="4582 3523 4335 4453",
        codigo_restaurante="REST-0802",
        fecha_hora=datetime.now()
    )

    resultado_puntos = CalculadoraRecompensas.calcular_puntos(mi_cena)

    assert resultado_puntos == 100.0

def test_calcular_puntos_monto_invalido():

    cena_mala = Cena(
        monto=-53435.0,
        tarjeta_cliente="4582 3523 4335 4453",
        codigo_restaurante="REST-0802",
        fecha_hora=datetime.now()
    )

    with pytest.raises(ValueError, match="El monto de la cena debe ser mayor a cero."):
        CalculadoraRecompensas.calcular_puntos(cena_mala)