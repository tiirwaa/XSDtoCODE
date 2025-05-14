from pathlib import Path
import subprocess
import os
from generator.base import CodeGeneratorStrategy

class PythonGenerator(CodeGeneratorStrategy):
    def generate(self, xsd_path):
        return self.generate_classes_with_xsdata(xsd_path)

    def generate_classes_with_xsdata(self, xsd_file_path):
        from pathlib import Path

        xsd_path = Path(xsd_file_path)
        output_path = Path(self.output_folder)

        # Crea el directorio si no existe
        output_path.mkdir(parents=True, exist_ok=True)

        command = [
            "xsdata",
            "generate",
            str(xsd_path),
            "--output", "dataclasses",
            "--package", "generated",  # Esto crea el folder "generated" en el cwd o destino
            "--structure-style", "clusters"  # Opcional, genera 1 archivo por clase
        ]

        print(f"Ejecutando comando: {' '.join(command)}")
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            cwd=str(output_path) 
        )

        if result.returncode != 0:
            print("❌ Error al ejecutar xsdata:")
            print(result.stderr)
        else:
            print("✅ Clases Python generadas con éxito usando xsdata.")
            print(result.stdout)
