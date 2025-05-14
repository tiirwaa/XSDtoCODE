import subprocess
import sys
from pathlib import Path
from generator.base import CodeGeneratorStrategy

class JavaGenerator(CodeGeneratorStrategy):
    def generate(self, xsd_path):
        return self.generate_classes_with_xjc(xsd_path)

    def generate_classes_with_xjc(self, xsd_file_path):
        """
        Utiliza xjc desde el JDK local para generar clases Java.
        """
        # Ruta al binario de Java en tu JDK dentro de tu carpeta de proyecto
        # Obtener la ruta correcta al binario de xjc
        if getattr(sys, 'frozen', False):
            # Si se está ejecutando desde un archivo empaquetado
            base_path = Path(sys._MEIPASS)
        else:
            # Si se está ejecutando desde el código fuente
            base_path = Path(__file__).parent.parent

        # Ruta al binario xjc dentro de la carpeta jdk del proyecto
        jdk_path = base_path / "jdk1.8.0_202" / "bin" / "xjc"

        
        # Ejecutar xjc directamente
        result = subprocess.run([
            jdk_path,
            "-d", self.output_folder,
            "-p", "com.example.generated",    # Paquete de clases generado
            "-extension",                     # Habilitar las extensiones JAXB
            xsd_file_path
        ], capture_output=True, text=True)

        if result.returncode != 0:
            print("❌ Error al ejecutar xjc:")
            print(result.stderr)
        else:
            print("✅ Clases Java generadas con éxito.")
            print(result.stdout)
