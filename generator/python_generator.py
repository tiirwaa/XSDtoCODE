import sys
import os
import traceback
from pathlib import Path
from generator.base import CodeGeneratorStrategy
from xsdata.__main__ import main as xsdata_main

class PythonGenerator(CodeGeneratorStrategy):
    def generate(self, xsd_path):
        return self.generate_classes_with_xsdata(xsd_path)

    def generate_classes_with_xsdata(self, xsd_file_path):
        if getattr(sys, 'frozen', False):
            base_path = Path(sys._MEIPASS)
        else:
            base_path = Path(__file__).parent.parent

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

            xsd_path = Path(xsd_temp_path)
            output_path = Path(output_abs_path)
            output_path.mkdir(parents=True, exist_ok=True)

            original_cwd = os.getcwd()
            original_argv = sys.argv.copy()

            try:
                os.chdir(output_path)

                sys.argv = [
                    "xsdata",
                    "generate",
                    str(xsd_path),
                    "--output", "dataclasses",
                    "--package", "generated",
                    "--structure-style", "clusters"
                ]

                if getattr(sys, 'frozen', False):
                    exe_dir = Path(sys._MEIPASS)
                    ruff_dir = exe_dir / "bin"
                    os.environ["PATH"] += os.pathsep + str(ruff_dir)
                    print(f"[DEBUG] PATH: {os.environ['PATH']}")

                if sys.platform == "win32":
                    import subprocess
                    original_popen = subprocess.Popen

                    def patched_popen(*args, **kwargs):
                        kwargs.setdefault("creationflags", subprocess.CREATE_NO_WINDOW)
                        return original_popen(*args, **kwargs)

                    subprocess.Popen = patched_popen  

                try:
                    xsdata_main()  # Puede llamar a sys.exit()
                except SystemExit as e:
                    if e.code != 0:
                        print(f"xsdata terminó con error (código {e.code})")
                        raise

                print("Clases Python generadas con éxito usando xsdata.")
            except Exception as e:
                print("Error al ejecutar xsdata:")
                traceback.print_exc()  # Esto imprimirá el traceback completo
            finally:
                os.chdir(original_cwd)
                sys.argv = original_argv
        finally:
            # Limpiar directorio temporal
            shutil.rmtree(temp_dir)
