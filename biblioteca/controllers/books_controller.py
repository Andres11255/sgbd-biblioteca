import tkinter.messagebox as messagebox
from events.custom_events import BOOK_ADDED, BOOK_UPDATED, BOOK_DELETED, TABLE_UPDATED, LOAD_BOOKS
from controllers.event_controller import dispatcher

class BooksController:
    """
    Controlador para la gestión de libros. Contiene la lógica de negocio.
    Reacciona a los eventos de la UI y emite nuevos eventos al despachador.
    """
    def __init__(self):
        # Base de datos simulada (lista temporal)
        self.books = [
            {"id": 1, "title": "1984", "author": "George Orwell", "year": "1949"},
            {"id": 2, "title": "Brave New World", "author": "Aldous Huxley", "year": "1932"}
        ]
        self.next_id = 3
        
        # Suscribirse al evento de carga inicial de libros
        dispatcher.subscribe(LOAD_BOOKS, self.load_books)

    def load_books(self, data=None):
        """Carga los libros y emite un evento para que la UI se actualice."""
        try:
            # Emite el evento TABLE_UPDATED pasando la lista actual de libros
            dispatcher.emit(TABLE_UPDATED, self.books)
        except Exception as e:
            messagebox.showerror("Error", f"Fallo al cargar libros: {e}")

    def add_book(self, book_data):
        """Lógica para agregar un nuevo libro."""
        try:
            # Validación de datos
            if not book_data.get("title") or not book_data.get("author"):
                raise ValueError("El título y autor son campos obligatorios.")
            
            new_book = {
                "id": self.next_id,
                "title": book_data["title"],
                "author": book_data["author"],
                "year": book_data.get("year", "")
            }
            self.books.append(new_book)
            self.next_id += 1
            
            # Emitir eventos de éxito y actualizar la tabla
            dispatcher.emit(BOOK_ADDED, new_book)
            self.load_books()
            
        except ValueError as ve:
            messagebox.showerror("Error de Validación", str(ve))
        except Exception as e:
            messagebox.showerror("Error del Sistema", f"Fallo al agregar el libro: {e}")

    def update_book(self, book_data):
        """Lógica para actualizar un libro existente."""
        try:
            book_id = book_data.get("id")
            if not book_id:
                raise ValueError("El ID del libro es requerido para actualizar.")
                
            book_id = int(book_id)
            for book in self.books:
                if book["id"] == book_id:
                    book["title"] = book_data.get("title", book["title"])
                    book["author"] = book_data.get("author", book["author"])
                    book["year"] = book_data.get("year", book["year"])
                    
                    dispatcher.emit(BOOK_UPDATED, book)
                    self.load_books()
                    return
            raise ValueError("No se encontró el libro con ese ID.")
            
        except ValueError as ve:
            messagebox.showerror("Error de Validación", str(ve))
        except Exception as e:
            messagebox.showerror("Error del Sistema", f"Fallo al actualizar el libro: {e}")

    def delete_book(self, book_id):
        """Lógica para eliminar un libro por ID."""
        try:
            if not book_id:
                raise ValueError("El ID del libro es requerido para eliminar.")
                
            book_id = int(book_id)
            initial_len = len(self.books)
            self.books = [b for b in self.books if b["id"] != book_id]
            
            if len(self.books) < initial_len:
                dispatcher.emit(BOOK_DELETED, {"id": book_id})
                self.load_books()
            else:
                raise ValueError("No se encontró el libro a eliminar.")
                
        except ValueError as ve:
            messagebox.showerror("Error de Validación", str(ve))
        except Exception as e:
            messagebox.showerror("Error del Sistema", f"Fallo al eliminar el libro: {e}")
