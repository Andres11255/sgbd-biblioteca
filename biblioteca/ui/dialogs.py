import tkinter as tk
from tkinter import ttk

class AboutDialog(tk.Toplevel):
    """Diálogo de ejemplo que demuestra el uso de lambdas y eventos en una ventana secundaria."""
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Acerca de")
        self.geometry("300x150")
        self.resizable(False, False)
        
        ttk.Label(self, text="Sistema de Gestión de Biblioteca Digital\n\nArquitectura Event-Driven\nPython + Tkinter", justify=tk.CENTER).pack(expand=True)
        
        # LAMBDA OBLIGATORIO: Uso de lambda para cerrar la ventana sin crear un método separado
        ttk.Button(self, text="Cerrar", command=lambda: self.destroy()).pack(pady=10)
        
        # LAMBDA OBLIGATORIO: Usar lambda en un evento bind
        self.bind("<FocusIn>", lambda e: print("El diálogo 'Acerca de' recibió el foco."))
