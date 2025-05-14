import os
from abc import ABC, abstractmethod

class CodeGeneratorStrategy(ABC):
    """
    Interfaz de estrategia para los generadores de código.
    Cada lenguaje deberá implementar esta clase.
    """

    def __init__(self, output_folder):
        self.output_folder = output_folder


    @abstractmethod
    def generate(self, xsd_path):
        """
        Genera el código fuente a partir del modelo XSD parseado.
        :param model: Lista de XSDClass
        :return: Código fuente como string
        """
        pass
