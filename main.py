from generator.base import CodeGeneratorStrategy
from generator.java_generator import JavaGenerator
from generator.python_generator import PythonGenerator
from generator.csharp_generator import CSharpGenerator
from generator.json_schema_generator import JSONSchemaGenerator
from generator.php_generator import PHPGenerator
import sys
import os

def main(xsd_path, language, output_folder):

    # Asegurarse de que el directorio de salida exista
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Paso 2: Seleccionar la estrategia según el lenguaje
    generators = {
        'java': JavaGenerator(output_folder),
        'python': PythonGenerator(output_folder),
        'csharp': CSharpGenerator(output_folder),
        'JSONSchema': JSONSchemaGenerator(output_folder),
        'php': PHPGenerator(output_folder)
    }

    language_lower = language.lower()
    generators_lower = {k.lower(): v for k, v in generators.items()}

    if language_lower not in generators_lower:
        print(f"Lenguaje no soportado: {language}")
        print(f"Lenguajes disponibles: {', '.join(generators.keys())}")
        return

    generator: CodeGeneratorStrategy = generators_lower[language_lower]
    
    # Paso 3: Generar código
    generator.generate(xsd_path)
    
    print(f"Código generado en la carpeta: {output_folder}")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Uso: python main.py <archivo.xsd> <lenguaje> <carpeta_salida>")
        print("Uso: main.exe <archivo.xsd> <lenguaje> <carpeta_salida>")
    else:
        main(sys.argv[1], sys.argv[2], sys.argv[3])
