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
        xsd_path = Path(xsd_file_path)
        output_path = Path(self.output_folder)
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
                    print(f"❌ xsdata terminó con error (código {e.code})")
                    raise

            print("✅ Clases Python generadas con éxito usando xsdata.")
        except Exception as e:
            print("❌ Error al ejecutar xsdata:")
            traceback.print_exc()  # Esto imprimirá el traceback completo
        finally:
            os.chdir(original_cwd)
            sys.argv = original_argv
