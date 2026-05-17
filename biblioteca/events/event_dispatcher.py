class EventDispatcher:
    """
    Despachador de eventos central.
    Implementa el patrón Observador/Pub-Sub para desacoplar componentes.
    """
    def __init__(self):
        self._listeners = {}

    def subscribe(self, event_type, callback):
        """Suscribe un callback a un tipo de evento específico."""
        if event_type not in self._listeners:
            self._listeners[event_type] = []
        self._listeners[event_type].append(callback)

    def unsubscribe(self, event_type, callback):
        """Cancela la suscripción de un callback a un tipo de evento."""
        if event_type in self._listeners:
            self._listeners[event_type].remove(callback)

    def emit(self, event_type, data=None):
        """Emite un evento, llamando a todos los callbacks suscritos."""
        if event_type in self._listeners:
            for callback in self._listeners[event_type]:
                try:
                    callback(data)
                except Exception as e:
                    print(f"Error executing callback for event '{event_type}': {e}")
