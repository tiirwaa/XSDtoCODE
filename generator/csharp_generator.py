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

        # Crear directorio temporal y copiar archivos necesarios
        import tempfile
        import shutil
        temp_dir = tempfile.mkdtemp()
        try:
            # Copiar el XSD del usuario al temp dir, modificando schemaLocation si es necesario
            xsd_temp_path = os.path.join(temp_dir, os.path.basename(xsd_abs_path))
            with open(xsd_abs_path, 'r', encoding='utf-8') as f:
                xsd_content = f.read()
            # Reemplazar rutas absolutas de xmldsig-core-schema.xsd con relativa
            import re
            xsd_content = re.sub(r'schemaLocation="[^"]*xmldsig-core-schema\.xsd"', 'schemaLocation="xmldsig-core-schema.xsd"', xsd_content)
            with open(xsd_temp_path, 'w', encoding='utf-8') as f:
                f.write(xsd_content)

            # Copiar el esquema xmldsig si existe
            schema_src = base_path / "csharp" / "xmldsig-core-schema.xsd"
            if schema_src.exists():
                shutil.copy(schema_src, temp_dir)

            command = [
                exe_path,
                "--output", output_abs_path,
                "--namespace=Generated",
                "--separateFiles",
                "--verbose",
                xsd_temp_path,
            ]

            # Solo en Windows, evita que se abra ventana de cmd
            kwargs = {
                "capture_output": True,
                "text": True,
                "cwd": temp_dir
            }
            if sys.platform == "win32":
                kwargs["creationflags"] = subprocess.CREATE_NO_WINDOW


            result = subprocess.run(command, **kwargs)

            if result.returncode != 0:
                print("❌ Error al ejecutar XmlSchemaClassGenerator:")
                if result.stderr:
                    print(result.stderr)
                if result.stdout:
                    print("Salida estándar:")
                    print(result.stdout)
                if not result.stderr and not result.stdout:
                    print("No se devolvió ningún mensaje de error.")
                raise Exception("XmlSchemaClassGenerator falló con código de salida {}".format(result.returncode))
            else:
                print("✅ Clases C# generadas con éxito.")
                print(result.stdout)
        finally:
            # Limpiar directorio temporal
            shutil.rmtree(temp_dir)
