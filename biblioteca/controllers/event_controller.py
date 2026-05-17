from events.event_dispatcher import EventDispatcher

# Instancia global del despachador de eventos (Singleton en el módulo)
# Todos los módulos importan este 'dispatcher' para comunicarse.
dispatcher = EventDispatcher()
