import subprocess
import sys
import os
from pathlib import Path
import tempfile
import shutil
import re
from generator.base import CodeGeneratorStrategy

class PHPGenerator(CodeGeneratorStrategy):
    def generate(self, xsd_path):
        return self.generate_classes_with_xsd2php(xsd_path)

    def generate_classes_with_xsd2php(self, xsd_file_path):
        """
        Utiliza xsd2php.phar con PHP portable para generar clases PHP.
        """
        base_path = Path(__file__).parent.parent
        
        if getattr(sys, 'frozen', False):
            # Cuando está empaquetado, buscar archivos en el directorio _internal
            exe_dir = Path(sys.executable).parent
            internal_dir = exe_dir / "_internal"
            php_exe = internal_dir / "php" / "php.exe"
            xsd2php_phar = exe_dir / "xsd2php.phar"
        else:
            php_exe = base_path / "php" / "php.exe"
            xsd2php_phar = base_path / "xsd2php.phar"

        xsd_abs_path = os.path.abspath(xsd_file_path)
        output_abs_path = os.path.abspath(self.output_folder)

        # Crear directorio temporal y copiar archivos necesarios
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

            # Create config file for xsd2php
            config_content = f"""xsd2php:
  destinations_php:
    folder: {output_abs_path}
    namespace: Generated
"""
            config_file = os.path.join(temp_dir, 'config.yml')
            with open(config_file, 'w', encoding='utf-8') as f:
                f.write(config_content)

            kwargs = {
                "capture_output": True,
                "text": True,
                "cwd": temp_dir
            }
            if sys.platform == "win32":
                kwargs["creationflags"] = subprocess.CREATE_NO_WINDOW

            env = os.environ.copy()
            env["PHP_TOOL_OPTIONS"] = "-d file.encoding=UTF-8"

            result = subprocess.run([
                str(php_exe),
                str(xsd2php_phar),
                "convert",
                config_file,
                xsd_temp_path
            ], env=env, **kwargs)

            if result.returncode != 0:
                print("Error al ejecutar xsd2php:")
                if result.stderr:
                    print(result.stderr)
                if result.stdout:
                    print("Salida estándar:")
                    print(result.stdout)
                if not result.stderr and not result.stdout:
                    print("No se devolvió ningún mensaje de error.")
                raise Exception(f"xsd2php falló con código de salida {result.returncode}")
            else:
                print("Clases PHP generadas con éxito.")
                if result.stdout:
                    print(result.stdout)
                return True
        finally:
            # Limpiar directorio temporal
            shutil.rmtree(temp_dir)