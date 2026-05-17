from ui.main_window import MainWindow
from controllers.app_controller import AppController
from controllers.event_controller import dispatcher
from events.custom_events import APP_CLOSED

def on_app_closed(data=None):
    """
    Callback global ejecutado cuando se emite el evento APP_CLOSED.
    Útil para limpiar recursos, guardar estado, o cerrar conexiones (futuro).
    """
    print("\n[EVENTO] La aplicación se está cerrando. Limpiando recursos y terminando subprocesos...")

def main():
    """Punto de entrada de la aplicación."""
    # 1. Suscribirse a eventos del ciclo de vida global
    dispatcher.subscribe(APP_CLOSED, on_app_closed)
    
    # 2. Inicializar el árbol de controladores
    app_controller = AppController()
    
    # 3. Inicializar la interfaz gráfica pasándole el controlador principal
    app = MainWindow(app_controller)
    
    print("Iniciando el mainloop de Tkinter...")
    # 4. Iniciar el bucle de eventos principal (Event-Loop)
    app.mainloop()

if __name__ == "__main__":
    main()
