import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as messagebox
from ui.books_view import BooksView
from ui.dialogs import AboutDialog
from controllers.event_controller import dispatcher
from events.custom_events import APP_CLOSED, LOAD_BOOKS

class MainWindow(tk.Tk):
    """
    Ventana principal de la aplicación.
    Orquesta la interfaz gráfica y maneja eventos globales de la ventana.
    """
    def __init__(self, app_controller):
        super().__init__()
        self.app_controller = app_controller
        
        self.title("Sistema de Gestión de Biblioteca Digital")
        self.geometry("700x500")
        
        # EVENTO OBLIGATORIO: Captura del evento de cierre de ventana
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self.setup_ui()
        
        # EVENTO OBLIGATORIO: Evento timer de Tkinter usando after
        # Ejecuta un lambda después de 1 segundo (1000ms)
        self.after(1000, lambda: self.status_var.set("Sistema inicializado y listo."))
        
        # EVENTO PERSONALIZADO: Emitir solicitud para cargar los datos en el Treeview al inicio
        dispatcher.emit(LOAD_BOOKS)

    def setup_ui(self):
        # Configuración del menú
        menubar = tk.Menu(self)
        self.config(menu=menubar)
        
        file_menu = tk.Menu(menubar, tearoff=0)
        
        # LAMBDA en Action/Command
        file_menu.add_command(label="Acerca de...", command=lambda: AboutDialog(self))
        file_menu.add_separator()
        file_menu.add_command(label="Salir", command=self.on_closing)
        
        menubar.add_cascade(label="Archivo", menu=file_menu)
        
        # Configuración de la vista de libros (Frame Principal)
        self.books_view = BooksView(self, self.app_controller.books_controller)
        self.books_view.pack(fill=tk.BOTH, expand=True)
        
        # Barra de estado
        self.status_var = tk.StringVar()
        self.status_var.set("Iniciando componentes...")
        status_bar = ttk.Label(self, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
    def on_closing(self):
        """Callback ejecutado al intentar cerrar la ventana."""
        try:
            if messagebox.askokcancel("Salir", "¿Estás seguro de que deseas salir?"):
                # Emitir el evento de cierre al despachador antes de destruir
                dispatcher.emit(APP_CLOSED)
                self.destroy()
        except Exception as e:
            print(f"Error al cerrar la ventana: {e}")
            self.destroy()
