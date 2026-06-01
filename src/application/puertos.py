from abc import ABC, abstractmethod
from src.domain.recompensa import Cena

class PuertoMensajeria(ABC):
    
    @abstractmethod
    def publicar_evento_cena(self, cena: Cena) -> None:
        pass