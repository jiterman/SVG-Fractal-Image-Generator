from math import cos, sin, pi, radians

class Tortuga:
    """"""
    def __init__ (self, angulo, orientacion = pi/2, x = 0, y = 0):
        """Crea una nueva instancia de tortuga, recibiendo angulo, y puede 
        recibir orientacion y posición de x e y, si no los recibe los establece por default. """
        self.x = x
        self.y = y
        self.orientacion = orientacion
        self.angulo = angulo

    def avanzar (self):
        """Cambia la posición de x e y una unidad teniendo en cuenta el ángulo en que nuestra tortuga está orientada."""
        self.x += round(cos(self.orientacion) * 10, 2)
        self.y += round(sin(self.orientacion) * (-10), 2) #Y crece en negativo
    
    def girar_izq (self):
        """Gira a la orientación hacia la izquierda la cantidad de grados del ángulo."""
        self.orientacion += self.angulo

    def girar_der (self):
        """Gira a la orientación hacia la derecha la cantidad de grados del ángulo."""
        self.orientacion -= self.angulo

    def cambiar_sentido (self):
        """Rota 180 grados."""
        self.orientacion += pi
    
    def apilar_tortuga (self):
        """Crea otra tortuga que arranca con el mismo estado (posición y orientación) que la tortuga que estaba 
        previamente en el tope. """
        return Tortuga(self.angulo, self.orientacion, self.x, self.y)