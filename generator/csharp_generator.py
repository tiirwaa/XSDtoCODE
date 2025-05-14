from pathlib import Path
import subprocess
import os
from generator.base import CodeGeneratorStrategy

class CSharpGenerator(CodeGeneratorStrategy):
    def generate(self, xsd_path):
        return self.generate_classes_with_xmlschema_class_generator(xsd_path)

    def generate_classes_with_xmlschema_class_generator(self, xsd_file_path):
        exe_path = os.path.abspath("csharp/XmlSchemaClassGenerator/XmlSchemaClassGenerator.Console.exe")
        xsd_abs_path = os.path.abspath(xsd_file_path)
        output_abs_path = os.path.abspath(self.output_folder)

        command = [
            exe_path,
            "--output", output_abs_path,
            "--namespace=Generated",
            "--separateFiles",
            xsd_abs_path,
        ]

        print(f"Ejecutando comando: {' '.join(command)}")

        result = subprocess.run(command, capture_output=True, text=True)

        if result.returncode != 0:
            print("❌ Error al ejecutar XmlSchemaClassGenerator:")
            print(result.stderr or "No se devolvió ningún mensaje de error.")
        else:
            print("✅ Clases C# generadas con éxito.")
            print(result.stdout)
