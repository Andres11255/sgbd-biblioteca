import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as messagebox
from ui.widgets import PlaceholderEntry
from controllers.event_controller import dispatcher
from events.custom_events import TABLE_UPDATED

class BooksView(ttk.Frame):
    """
    Vista principal de la gestión de libros.
    No contiene lógica de negocio, se comunica con el controlador.
    """
    def __init__(self, parent, books_controller):
        super().__init__(parent)
        self.books_controller = books_controller
        
        self.setup_ui()
        
        # Suscribirse al evento para reaccionar cuando cambian los datos
        dispatcher.subscribe(TABLE_UPDATED, self.update_table)

    def setup_ui(self):
        # Frame del Formulario
        self.form_frame = ttk.LabelFrame(self, text="Detalles del Libro")
        self.form_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.id_var = tk.StringVar()
        
        ttk.Label(self.form_frame, text="Título:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.title_entry = PlaceholderEntry(self.form_frame, placeholder="Ingrese el título...")
        self.title_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.EW)
        
        # EVENTO OBLIGATORIO: Evento de teclado <KeyRelease>
        self.title_entry.bind("<KeyRelease>", self.on_key_release)
        
        ttk.Label(self.form_frame, text="Autor:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.author_entry = PlaceholderEntry(self.form_frame, placeholder="Ingrese el autor...")
        self.author_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.EW)
        
        ttk.Label(self.form_frame, text="Año:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.year_entry = PlaceholderEntry(self.form_frame, placeholder="Ej: 2023")
        self.year_entry.grid(row=2, column=1, padx=5, pady=5, sticky=tk.EW)
        
        self.form_frame.columnconfigure(1, weight=1)
        
        # Frame de Botones (Acciones CRUD visuales)
        self.btn_frame = ttk.Frame(self.form_frame)
        self.btn_frame.grid(row=3, column=0, columnspan=2, pady=10)
        
        # CALLBACK OBLIGATORIO 1: callback de botón (self.on_add)
        self.btn_add = ttk.Button(self.btn_frame, text="Agregar", command=self.on_add)
        self.btn_add.pack(side=tk.LEFT, padx=5)
        
        # EVENTO OBLIGATORIO: Evento click del mouse <Button-1>
        self.btn_add.bind("<Button-1>", lambda e: print("Clic izquierdo detectado en el botón 'Agregar'"))
        
        # CALLBACK OBLIGATORIO 2: callback de botón (self.on_update)
        self.btn_update = ttk.Button(self.btn_frame, text="Actualizar", command=self.on_update)
        self.btn_update.pack(side=tk.LEFT, padx=5)
        
        # CALLBACK OBLIGATORIO 3: callback de botón (self.on_delete)
        self.btn_delete = ttk.Button(self.btn_frame, text="Eliminar", command=self.on_delete)
        self.btn_delete.pack(side=tk.LEFT, padx=5)
        
        # LAMBDA OBLIGATORIO: lambda para limpiar el formulario sin crear un callback complejo si es simple
        self.btn_clear = ttk.Button(self.btn_frame, text="Limpiar", command=lambda: self.clear_form())
        self.btn_clear.pack(side=tk.LEFT, padx=5)
        
        # Frame de la Tabla
        self.table_frame = ttk.Frame(self)
        self.table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        columns = ("id", "title", "author", "year")
        self.tree = ttk.Treeview(self.table_frame, columns=columns, show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("title", text="Título")
        self.tree.heading("author", text="Autor")
        self.tree.heading("year", text="Año")
        
        self.tree.column("id", width=50, anchor=tk.CENTER)
        self.tree.column("title", width=200)
        self.tree.column("author", width=150)
        self.tree.column("year", width=100, anchor=tk.CENTER)
        
        self.tree.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        
        scrollbar = ttk.Scrollbar(self.table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # EVENTO OBLIGATORIO: Selección Treeview <<TreeviewSelect>>
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)
        
    def on_key_release(self, event):
        """Maneja el evento de soltar tecla en el Entry de título."""
        # Se imprime solo a modo de demostración de la captura del evento de teclado
        # print(f"Tecla presionada: {event.keysym}")
        pass
        
    def get_form_data(self):
        """Extrae la información del formulario ignorando los placeholders."""
        title = self.title_entry.get() if self.title_entry.get() != self.title_entry.placeholder else ""
        author = self.author_entry.get() if self.author_entry.get() != self.author_entry.placeholder else ""
        year = self.year_entry.get() if self.year_entry.get() != self.year_entry.placeholder else ""
        return {"id": self.id_var.get(), "title": title, "author": author, "year": year}

    def on_add(self):
        """Delegado que notifica al controlador para agregar un libro."""
        data = self.get_form_data()
        self.books_controller.add_book(data)
        self.clear_form()

    def on_update(self):
        """Delegado que notifica al controlador para actualizar."""
        data = self.get_form_data()
        if not data.get("id"):
            messagebox.showwarning("Advertencia", "Seleccione un libro de la tabla para actualizar.")
            return
        self.books_controller.update_book(data)
        self.clear_form()

    def on_delete(self):
        """Delegado que notifica al controlador para eliminar."""
        book_id = self.id_var.get()
        if not book_id:
            messagebox.showwarning("Advertencia", "Seleccione un libro de la tabla para eliminar.")
            return
            
        if messagebox.askyesno("Confirmar", f"¿Desea eliminar el libro seleccionado?"):
            self.books_controller.delete_book(book_id)
            self.clear_form()

    def clear_form(self):
        """Limpia todos los campos del formulario."""
        self.id_var.set("")
        self.title_entry.foc_out(None)
        self.author_entry.foc_out(None)
        self.year_entry.foc_out(None)
        
    def on_tree_select(self, event):
        """Maneja la selección de un item en el Treeview para pasarlo al formulario."""
        try:
            selected = self.tree.selection()
            if selected:
                item = self.tree.item(selected[0])
                values = item['values']
                if values:
                    self.id_var.set(values[0])
                    
                    self.title_entry.delete(0, tk.END)
                    self.title_entry.insert(0, values[1])
                    self.title_entry['foreground'] = self.title_entry.default_fg_color
                    
                    self.author_entry.delete(0, tk.END)
                    self.author_entry.insert(0, values[2])
                    self.author_entry['foreground'] = self.author_entry.default_fg_color
                    
                    self.year_entry.delete(0, tk.END)
                    self.year_entry.insert(0, values[3])
                    self.year_entry['foreground'] = self.year_entry.default_fg_color
        except Exception as e:
            messagebox.showerror("Error UI", f"Error al seleccionar elemento: {e}")

    def update_table(self, books):
        """Actualiza la tabla visual reaccionando al evento del despachador."""
        try:
            # Limpiar tabla
            for item in self.tree.get_children():
                self.tree.delete(item)
                
            # Insertar nuevos datos
            for book in books:
                self.tree.insert("", tk.END, values=(book["id"], book["title"], book["author"], book["year"]))
        except Exception as e:
            messagebox.showerror("Error UI", f"No se pudo renderizar la tabla: {e}")
