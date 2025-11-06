import subprocess
import sys
import os
from pathlib import Path
import tempfile
import shutil
import re
import xml.etree.ElementTree as ET
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
        metadata_base_path = Path(output_abs_path) / "metadata"
        metadata_base_path.mkdir(parents=True, exist_ok=True)

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

            # Detectar namespaces para la configuración de xsd2php
            namespaces_map = {}
            base_php_namespace = "Generated"
            try:
                root = ET.fromstring(xsd_content)
                target_namespace = root.attrib.get("targetNamespace")
                if target_namespace:
                    namespaces_map[target_namespace] = base_php_namespace
                xs_namespace = "{http://www.w3.org/2001/XMLSchema}"
                for element in root.findall(f".//{xs_namespace}import"):
                    imported_ns = element.attrib.get("namespace")
                    if imported_ns and imported_ns not in namespaces_map:
                        sanitized = re.sub(r'[^0-9A-Za-z]+', ' ', imported_ns).title().replace(' ', '')
                        if not sanitized:
                            sanitized = "Imported"
                        namespaces_map[imported_ns] = f"{base_php_namespace}\\{sanitized}"
            except ET.ParseError:
                pass

            if not namespaces_map:
                namespaces_map["http://tempuri.org"] = base_php_namespace

            # Copiar el esquema xmldsig si existe
            schema_src = base_path / "schemas" / "xmldsig-core-schema.xsd"
            if schema_src.exists():
                shutil.copy(schema_src, temp_dir)

            # Create config file for xsd2php
            def namespace_destination_path(php_ns: str, base_path: Path) -> Path:
                ns_parts = php_ns.split("\\")
                if ns_parts and ns_parts[0] == base_php_namespace:
                    relative_parts = ns_parts[1:]
                    if relative_parts:
                        return base_path / Path(*relative_parts)
                    return base_path
                return base_path / Path(*ns_parts)

            namespaces_yaml = "\n".join(f"    '{ns}': {php_ns}" for ns, php_ns in namespaces_map.items())
            php_namespaces = sorted(set(namespaces_map.values()))

            destination_map = {}
            metadata_destination_map = {}
            for php_ns in php_namespaces:
                dest_path = namespace_destination_path(php_ns, Path(output_abs_path))
                dest_path.mkdir(parents=True, exist_ok=True)
                destination_map[php_ns] = dest_path.as_posix()

                metadata_dest = namespace_destination_path(php_ns, metadata_base_path)
                metadata_dest.mkdir(parents=True, exist_ok=True)
                metadata_destination_map[php_ns] = metadata_dest.as_posix()

            destinations_php_yaml = "\n".join(f"    {php_ns}: '{path}'" for php_ns, path in destination_map.items())
            destinations_jms_yaml = "\n".join(f"    {php_ns}: '{path}'" for php_ns, path in metadata_destination_map.items())
            config_content = f"""xsd2php:
  namespaces:
{namespaces_yaml}
  destinations_php:
{destinations_php_yaml}
  destinations_jms:
{destinations_jms_yaml}
"""
            config_file = os.path.join(temp_dir, 'config.yml')
            with open(config_file, 'w', encoding='utf-8') as f:
                f.write(config_content)

            kwargs = {
                "capture_output": True,
                "text": True,
                "cwd": str(base_path)
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
