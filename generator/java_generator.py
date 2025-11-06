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
            # Si se ejecuta desde el archivo empaquetado
            base_path = Path(sys._MEIPASS)
        else:
            # Si se ejecuta desde el código fuente
            base_path = Path(__file__).parent.parent

        jdk_path = base_path / "jdk1.8.0_202"
        if getattr(sys, 'frozen', False):
            # Si se ejecuta desde el archivo empaquetado
            base_path = Path(sys._MEIPASS)
        else:
            # Si se ejecuta desde el código fuente
            base_path = Path(__file__).parent.parent

        jdk_path = base_path / "jdk1.8.0_202"

        xsd_abs_path = os.path.abspath(xsd_file_path)
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

            kwargs = {
                "capture_output": True,
                "text": True,
                "cwd": temp_dir
            }
            if sys.platform == "win32":
                kwargs["creationflags"] = subprocess.CREATE_NO_WINDOW

            env = os.environ.copy()
            # env["JAVA_TOOL_OPTIONS"] = "-Dfile.encoding=UTF-8"  # Commented out to avoid issues
            env["JAVA_HOME"] = str(base_path / "jdk1.8.0_202")
            env["JRE_HOME"] = str(base_path / "jdk1.8.0_202")
            env["PATH"] = str(base_path / "jdk1.8.0_202" / "bin") + os.pathsep + env.get("PATH", "")    
            
            java_exe = base_path / "jdk1.8.0_202" / "bin" / "java.exe"
            xjc_exe = base_path / "jdk1.8.0_202" / "bin" / "xjc.exe"
            
            if xjc_exe.exists():
                # Usar xjc.exe directamente si está disponible
                print(f"Usando xjc.exe: {xjc_exe}")
                cmd = [
                    str(xjc_exe),
                    "-d", str(output_abs_path),
                    "-p", "com.example.generated",
                    "-extension",
                    "-nv",  # No validation to avoid JDK 8 bug
                    str(xsd_temp_path)
                ]
                print(f"Ejecutando comando: {' '.join(cmd)}")
                result = subprocess.run(cmd, env=env, **kwargs)
            else:
                # Usar java con clase internal como fallback
                tools_jar = base_path / "jdk1.8.0_202" / "lib" / "tools.jar"
                dt_jar = base_path / "jdk1.8.0_202" / "lib" / "dt.jar"
                classpath = f"{tools_jar}{os.pathsep}{dt_jar}"

                print(f"java_exe: {java_exe}")
                print(f"exists: {java_exe.exists()}")
                cmd = [
                    str(java_exe),
                    "-cp", str(classpath),
                    "com.sun.tools.internal.xjc.Driver",
                    "-d", str(output_abs_path),
                    "-p", "com.example.generated",
                    "-extension",
                    str(xsd_temp_path)
                ]
                print(f"Ejecutando comando: {' '.join(cmd)}")
                result = subprocess.run(cmd, env=env, **kwargs)

            if result.returncode != 0:
                print("Error al ejecutar xjc:")
                if result.stderr:
                    print(result.stderr)
                if result.stdout:
                    print("Salida estándar:")
                    print(result.stdout)
                if not result.stderr and not result.stdout:
                    print("No se devolvió ningún mensaje de error.")
                raise Exception("xjc falló con código de salida {}".format(result.returncode))
            else:
                print("Clases Java generadas con éxito.")
                if result.stdout:
                    print(result.stdout)
                return True
        finally:
            # Limpiar directorio temporal
            shutil.rmtree(temp_dir)
        

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
