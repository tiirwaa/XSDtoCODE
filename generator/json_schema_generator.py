import sys
from pathlib import Path
import subprocess
import os

class JSONSchemaGenerator:
    def __init__(self, output_folder):
        # Detectar ruta base según si está empaquetado o no
        if getattr(sys, 'frozen', False):
            # Ejecutándose desde PyInstaller (o similar)
            base_path = Path(sys._MEIPASS)
        else:
            # Ejecutándose desde código fuente
            base_path = Path(__file__).parent.parent

        self.base_path = base_path
        self.output_folder = Path(output_folder)
        self.output_folder.mkdir(parents=True, exist_ok=True)

        # Path al ejecutable node portable según plataforma
        if sys.platform == "win32":
            self.node_executable = self.base_path / "node" / "node.exe"
        else:
            self.node_executable = self.base_path / "node" / "bin" / "node"

    def generate(self, xsd_path):
        if getattr(sys, 'frozen', False):
            base_path = Path(sys._MEIPASS)
        else:
            base_path = Path(__file__).parent.parent

        xsd_abs_path = os.path.abspath(xsd_path)
        output_abs_path = os.path.abspath(self.output_folder)

        # Crear directorio temporal y copiar archivos necesarios
        import tempfile
        import shutil
        import re
        temp_dir = tempfile.mkdtemp()
        try:
            # Copiar el XSD del usuario al temp dir, modificando schemaLocation si es necesario
            xsd_temp_path = os.path.join(temp_dir, os.path.basename(xsd_abs_path))
            with open(xsd_abs_path, 'r', encoding='utf-8') as f:
                xsd_content = f.read()
            # Reemplazar rutas de xmldsig-core-schema.xsd con relativa
            xsd_content = re.sub(r'schemaLocation="[^"]*xmldsig-core-schema\.xsd"', 'schemaLocation="xmldsig-core-schema.xsd"', xsd_content)
            with open(xsd_temp_path, 'w', encoding='utf-8') as f:
                f.write(xsd_content)

            # Copiar el esquema xmldsig si existe
            schema_src = base_path / "schemas" / "xmldsig-core-schema.xsd"
            if schema_src.exists():
                shutil.copy(schema_src, temp_dir)

            xsd_path = Path(xsd_temp_path)
            script_path = self.base_path / "node" / "convert_xsd_to_jsonschema.js"

             # Solo en Windows, evita que se abra ventana de cmd
            kwargs = {
                "capture_output": True,
                "text": True,
                "encoding":'utf-8',
                "errors":'replace'
            }
            if sys.platform == "win32":
                kwargs["creationflags"] = subprocess.CREATE_NO_WINDOW

            # Ejecutar el comando con el node portable incluido
            result = subprocess.run([
                str(self.node_executable),
                str(script_path),
                str(xsd_path),
                str(output_abs_path)
            ], **kwargs)    # Reemplaza caracteres inválidos en lugar de lanzar error

            if result.returncode != 0:
                print("Error al convertir XSD a JSON Schema:")
                print(result.stderr)
                return False

            print("JSON Schema generado correctamente.")
            print(result.stdout)
            return True
        finally:
            # Limpiar directorio temporal
            shutil.rmtree(temp_dir)