import tkinter as tk
from tkinter import ttk

class PlaceholderEntry(ttk.Entry):
    """
    Widget de Entry personalizado que maneja eventos de Focus
    para crear un efecto de placeholder (texto de fondo).
    """
    def __init__(self, master=None, placeholder="Escribe aquí...", color='grey', *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        
        self.placeholder = placeholder
        self.placeholder_color = color
        self.default_fg_color = self['foreground']
        
        # EVENTOS OBLIGATORIOS: Foco <FocusIn> y <FocusOut>
        self.bind("<FocusIn>", self.foc_in)
        self.bind("<FocusOut>", self.foc_out)
        
        self.put_placeholder()
        
    def put_placeholder(self):
        self.insert(0, self.placeholder)
        self['foreground'] = self.placeholder_color
        
    def foc_in(self, event):
        """Callback al recibir el foco."""
        if self['foreground'] == self.placeholder_color:
            self.delete('0', 'end')
            self['foreground'] = self.default_fg_color
            
    def foc_out(self, event):
        """Callback al perder el foco."""
        if not self.get():
            self.put_placeholder()
