import sys
from pathlib import Path
import subprocess

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
        xsd_path = Path(xsd_path)
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
            str(self.output_folder)
        ], **kwargs)    # Reemplaza caracteres inválidos en lugar de lanzar error

        if result.returncode != 0:
            print("❌ Error al convertir XSD a JSON Schema:")
            print(result.stderr)
            return False

        print("✅ JSON Schema generado correctamente.")
        print(result.stdout)
        return True
