from pathlib import Path
import subprocess
import sys
import os
from generator.base import CodeGeneratorStrategy

class CSharpGenerator(CodeGeneratorStrategy):
    def generate(self, xsd_path):
        return self.generate_classes_with_xmlschema_class_generator(xsd_path)

    def generate_classes_with_xmlschema_class_generator(self, xsd_file_path):
        # Obtener la ruta al ejecutable XmlSchemaClassGenerator.Console.exe
        if getattr(sys, 'frozen', False):
            # Si se ejecuta desde el archivo empaquetado
            base_path = Path(sys._MEIPASS)
        else:
            # Si se ejecuta desde el código fuente
            base_path = Path(__file__).parent.parent

        # Obtener la ruta del ejecutable
        exe_path = base_path / "csharp/XmlSchemaClassGenerator/XmlSchemaClassGenerator.Console.exe"

        xsd_abs_path = os.path.abspath(xsd_file_path)
        output_abs_path = os.path.abspath(self.output_folder)

        command = [
            exe_path,
            "--output", output_abs_path,
            "--namespace=Generated",
            "--separateFiles",
            xsd_abs_path,
        ]

        # Solo en Windows, evita que se abra ventana de cmd
        kwargs = {
            "capture_output": True,
            "text": True
        }
        if sys.platform == "win32":
            kwargs["creationflags"] = subprocess.CREATE_NO_WINDOW


        result = subprocess.run(command, **kwargs)

        if result.returncode != 0:
            print("❌ Error al ejecutar XmlSchemaClassGenerator:")
            print(result.stderr or "No se devolvió ningún mensaje de error.")
        else:
            print("✅ Clases C# generadas con éxito.")
            print(result.stdout)
