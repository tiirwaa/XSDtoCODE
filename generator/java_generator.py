import subprocess
import sys
import os
from pathlib import Path
import fileinput
import datetime
from generator.base import CodeGeneratorStrategy

class JavaGenerator(CodeGeneratorStrategy):
    def generate(self, xsd_path):
        success = self.generate_classes_with_xjc(xsd_path)
        if success:
            self.replace_headers_in_generated_files()
        return success

    def generate_classes_with_xjc(self, xsd_file_path):
        """
        Utiliza xjc desde el JDK local para generar clases Java.
        """
        if getattr(sys, 'frozen', False):
            base_path = Path(sys._MEIPASS)
        else:
            base_path = Path(__file__).parent.parent

        jdk_path = base_path / "jdk1.8.0_202" / "bin" / "xjc"

        kwargs = {
            "capture_output": True,
            "text": True
        }
        if sys.platform == "win32":
            kwargs["creationflags"] = subprocess.CREATE_NO_WINDOW

        env = os.environ.copy()
        env["JAVA_TOOL_OPTIONS"] = "-Dfile.encoding=UTF-8"    
        
        result = subprocess.run([
            str(jdk_path),
            "-d", str(self.output_folder),
            "-p", "com.example.generated",
            "-extension",
            str(xsd_file_path)
        ], env=env, **kwargs)

        if result.returncode != 0:
            print("❌ Error al ejecutar xjc:")
            print(result.stderr)
            return False
        else:
            print("✅ Clases Java generadas con éxito.")
            print(result.stdout)
            return True
        

    def generar_header_personalizado(self):
        ahora = datetime.datetime.now().strftime("%Y.%m.%d a las %I:%M:%S %p %Z")
        # Como %Z (zona horaria) puede salir vacío, mejor puedes poner tu zona fija:
        ahora = datetime.datetime.now().strftime("%Y.%m.%d a las %I:%M:%S %p CST")  # Ajusta zona si quieres

        header = [
            "//",
            "// Este archivo ha sido generado por XSDtoCODE de A&G Programación y Desarrollo de Sistemas Informáticos S.A.",
            "// utilizando la arquitectura JavaTM para la implantación de la referencia de enlace (JAXB) XML v2.2.8-b130911.1802",
            "// Visite https://agsoft.co.cr",
            "// Todas las modificaciones realizadas en este archivo se perderán si se vuelve a compilar el esquema de origen.",
            f"// Generado el: {ahora}",
            "//"
        ]
        return header    

    def replace_headers_in_generated_files(self):
        """
        Reemplaza el header JAXB estándar en todos los archivos Java generados.
        """
        nuevo_header = self.generar_header_personalizado()

        java_files = Path(self.output_folder).rglob("*.java")
        for file_path in java_files:
            self.replace_jaxb_header(file_path, nuevo_header)

    @staticmethod
    def replace_jaxb_header(file_path, new_header_lines):
        with open(file_path, 'r', encoding='latin-1') as f:
            lines = f.readlines()

        inside_header = False
        header_start_idx = None
        header_end_idx = None

        # Detectar el rango del header (del primer // hasta el siguiente //)
        for i, line in enumerate(lines):
            stripped = line.strip()
            if not inside_header and stripped == "//":
                inside_header = True
                header_start_idx = i
            elif inside_header and stripped == "//":
                header_end_idx = i
                break

        if header_start_idx is not None and header_end_idx is not None:
            # Reemplazar las líneas del header
            new_lines = lines[:header_start_idx] + [l + '\n' for l in new_header_lines] + lines[header_end_idx+1:]
        else:
            # No se encontró header, solo insertar al inicio
            new_lines = [l + '\n' for l in new_header_lines] + lines

        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
