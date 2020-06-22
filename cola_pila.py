class _Nodo:
    """Representa un nodo.
    Atributos: dato y nodo próximo."""

    def __init__(self, dato = None, prox = None):
        """Crea un nuevo nodo."""
        self.dato = dato
        self.prox = prox

    def __str__ (self):
        """Permite imprimir el dato que contiene el nodo."""
        return str(self.dato)

class Cola:
    """Representa un cola. Atributo: primer elemento."""
    def __init__ (self):
        """Crea una cola."""
        self.primero = None

    def encolar (self, x):
        """Recibe un dato, y lo encola."""
        nuevo = _Nodo(x)
        if not self.primero:
            self.primero = nuevo
        else:
            actual = self.primero
            while actual.prox:
                actual = actual.prox
            actual.prox = nuevo

    def esta_vacia (self):
        """Verifica si la cola está vacía.
        Devuelve un booleano."""
        return self.primero is None

    def desencolar (self):
        """Desencola el primer elemento. Si la cola está vacía, lanza ValueError.
        Devuelve el dato que contenía el primer elemento."""
        if self.esta_vacia():
            raise ValueError('La cola está vacía.')
        dato = self.primero.dato
        self.primero = self.primero.prox
        return dato
    
    def ver_primero (self):
        if self.esta_vacia():
            raise IndexError('La cola está vacía.')
        return self.primero.dato

class Pila:
    """Representa una pila con operaciones de apilar, desapilar y verificar si está vacía."""
    def __init__(self):
        """Crea una pila vacía."""
        self.items = []

    def esta_vacia(self):
        """Devuelve True si la lista está vacía, False si no."""
        return len(self.items) == 0

    def apilar(self, x):
        """Apila el elemento x."""
        self.items.append(x)
        
    def desapilar(self):
        """Devuelve el elemento tope y lo elimina de la pila. Si la pila está vacía levanta una excepción."""
        if self.esta_vacia():
            raise IndexError("La pila está vacía")
        return self.items.pop()

    def ver_tope(self):
        if self.esta_vacia():
            raise IndexError('La pila está vacía.')
        return self.items[-1]