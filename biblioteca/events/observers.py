from abc import ABC, abstractmethod

class Observer(ABC):
    """
    Clase base abstracta para los observadores (opcional si se usa duck-typing).
    Define la interfaz que los componentes deben implementar para reaccionar a eventos.
    """
    @abstractmethod
    def update(self, event_type, data):
        pass
