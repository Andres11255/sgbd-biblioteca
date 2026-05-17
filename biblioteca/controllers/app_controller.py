from controllers.books_controller import BooksController

class AppController:
    """
    Controlador raíz de la aplicación.
    Se encarga de inicializar e instanciar los subcontroladores.
    """
    def __init__(self):
        self.books_controller = BooksController()
