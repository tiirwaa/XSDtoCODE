import subprocess
import sys
import os
from pathlib import Path
import tempfile
import shutil
import re
import copy
import xml.etree.ElementTree as ET
from generator.base import CodeGeneratorStrategy
import logging

XMLNS = "http://www.w3.org/2000/xmlns/"
XS_NS = "http://www.w3.org/2001/XMLSchema"
XS = {"xs": XS_NS}

ET.register_namespace("xs", XS_NS)

QNAME_ATTRS = {
    "type",
    "base",
    "ref",
    "itemType",
    "memberTypes",
    "substitutionGroup",
}
LIST_QNAME_ATTRS = {"memberTypes"}
DEFAULT_OCCURS = {"minOccurs": "1", "maxOccurs": "1"}


def strip_ns(tag: str) -> str:
    if "}" in tag:
        return tag.split("}", 1)[1]
    return tag


def extract_namespace_decls(xsd_content: str) -> dict[str, str]:
    namespace_decls: dict[str, str] = {}
    for prefix, uri in re.findall(r'xmlns(?::([A-Za-z0-9_.-]+))?="([^"]+)"', xsd_content):
        key = prefix or ""
        namespace_decls[key] = uri
        if prefix:
            try:
                ET.register_namespace(prefix, uri)
            except ValueError:
                # Ignore invalid prefix registrations
                pass
    namespace_decls.setdefault("xs", XS_NS)
    return namespace_decls


def resolve_qname(
    value: str,
    namespace_decls: dict[str, str],
    target_namespace: str | None,
) -> str:
    value = value.strip()
    if ":" in value:
        prefix, local = value.split(":", 1)
        namespace = namespace_decls.get(prefix)
        if namespace:
            return f"{{{namespace}}}{local}"
        return value
    if target_namespace:
        return f"{{{target_namespace}}}{value}"
    return value


def normalize_attributes(
    node: ET.Element,
    namespace_decls: dict[str, str],
    target_namespace: str | None,
) -> tuple[tuple[str, str], ...]:
    tag_local = strip_ns(node.tag)
    remove_keys = {"id"}
    if tag_local in {"complexType", "simpleType"}:
        remove_keys.add("name")

    normalized: dict[str, str] = {}
    for attr, value in node.attrib.items():
        if attr == "xmlns" or attr.startswith(f"{{{XMLNS}}}"):
            continue

        attr_local = strip_ns(attr)
        if attr_local in remove_keys:
            continue

        text = value.strip()
        if attr_local in DEFAULT_OCCURS:
            default_val = DEFAULT_OCCURS[attr_local]
            if text == default_val:
                continue

        if attr_local in QNAME_ATTRS:
            if attr_local in LIST_QNAME_ATTRS:
                parts = [resolve_qname(part, namespace_decls, target_namespace) for part in text.split()]
                text = " ".join(sorted(parts))
            else:
                text = resolve_qname(text, namespace_decls, target_namespace)
        else:
            text = text.lower() if text.lower() in {"true", "false"} else text

        normalized[attr_local] = text

    return tuple(sorted(normalized.items()))


def canonicalize_node(
    node: ET.Element,
    namespace_decls: dict[str, str],
    target_namespace: str | None,
) -> tuple:
    tag_local = strip_ns(node.tag)
    attrs = normalize_attributes(node, namespace_decls, target_namespace)

    child_reprs: list[tuple] = []
    for child in node:
        if strip_ns(child.tag) == "annotation":
            continue
        child_reprs.append(
            canonicalize_node(child, namespace_decls, target_namespace)
        )

    if tag_local == "complexType":
        attribute_children = [c for c in child_reprs if c[0] in {"attribute", "attributeGroup"}]
        other_children = [c for c in child_reprs if c[0] not in {"attribute", "attributeGroup"}]
        attribute_children.sort()
        return (tag_local, attrs, tuple(other_children), tuple(attribute_children))

    if tag_local in {"choice", "all"}:
        child_reprs.sort()
        return (tag_local, attrs, tuple(child_reprs))

    if tag_local in {"simpleType", "simpleContent", "complexContent"}:
        return (tag_local, attrs, tuple(child_reprs))

    return (tag_local, attrs, tuple(child_reprs))


def canonicalize_complex_type(
    complex_type: ET.Element,
    namespace_decls: dict[str, str],
    target_namespace: str | None,
) -> str:
    representation = canonicalize_node(complex_type, namespace_decls, target_namespace)
    return repr(representation)





class PHPGenerator(CodeGeneratorStrategy):
    def generate(self, xsd_path):
        return self.generate_classes_with_xsd2php(xsd_path)

    def generate_classes_with_xsd2php(self, xsd_file_path):
        """
        Utiliza xsd2php.phar con PHP portable para generar clases PHP.
        """
        # Configurar logging
        log_file = Path(self.output_folder) / 'generation.log'
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        
        # Handler para archivo
        file_handler = logging.FileHandler(str(log_file))
        file_handler.setLevel(logging.INFO)
        file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        file_handler.setFormatter(file_formatter)
        
        # Handler para consola
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        console_handler.setFormatter(console_formatter)
        
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        print("Iniciando generación de clases PHP")
        logging.info("Iniciando generación de clases PHP")
        if getattr(sys, 'frozen', False):
            # Si se ejecuta desde el archivo empaquetado
            base_path = Path(sys._MEIPASS)
            # Ajustar rutas para archivos bundled
            if xsd_file_path.startswith("schemas\\") or xsd_file_path.startswith("schemas/"):
                xsd_file_path = str(base_path / xsd_file_path)
        else:
            # Si se ejecuta desde el código fuente
            base_path = Path(__file__).parent.parent
        
        php_exe = base_path / "php" / "php.exe"
        xsd2php_phar = base_path / "xsd2php.phar"

        print(f"php_exe: {php_exe}, exists: {php_exe.exists()}")
        logging.info(f"php_exe: {php_exe}, exists: {php_exe.exists()}")
        print(f"xsd2php_phar: {xsd2php_phar}, exists: {xsd2php_phar.exists()}")
        logging.info(f"xsd2php_phar: {xsd2php_phar}, exists: {xsd2php_phar.exists()}")

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
            # Promover complexType anónimos a tipos globales
            xsd_content = promote_anonymous_complex_types(xsd_content)
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

            # Copiar xsd2php.phar al temp_dir
            phar_src = base_path / "xsd2php.phar"
            phar_dest = os.path.join(temp_dir, "xsd2php.phar")
            shutil.copy(phar_src, temp_dir)

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
            
            print(f"Config content:\n{config_content}")
            logging.info(f"Config content:\n{config_content}")

            kwargs = {
                "capture_output": True,
                "text": True,
                "cwd": temp_dir
            }
            if sys.platform == "win32":
                kwargs["creationflags"] = subprocess.CREATE_NO_WINDOW

            env = os.environ.copy()
            env["PHP_TOOL_OPTIONS"] = "-d file.encoding=UTF-8"

            print("Ejecutando comando xsd2php...")
            logging.info("Ejecutando comando xsd2php...")
            result = subprocess.run([
                str(php_exe),
                "xsd2php.phar",
                "convert",
                config_file,
                xsd_temp_path
            ], env=env, **kwargs)

            if result.returncode != 0:
                error_msg = "Error al ejecutar xsd2php:"
                print(error_msg)
                logging.error(error_msg)
                if result.stderr:
                    print(result.stderr)
                    logging.error(result.stderr)
                if result.stdout:
                    print("Salida estándar:")
                    print(result.stdout)
                    logging.info("Salida estándar: " + result.stdout)
                if not result.stderr and not result.stdout:
                    no_error_msg = "No se devolvió ningún mensaje de error."
                    print(no_error_msg)
                    logging.warning(no_error_msg)
                raise Exception(f"xsd2php falló con código de salida {result.returncode}")
            else:
                success_msg = "Clases PHP generadas con éxito."
                print(success_msg)
                logging.info(success_msg)
                print(f"Return code: {result.returncode}")
                logging.info(f"Return code: {result.returncode}")
                if result.stdout:
                    print("Salida estándar:")
                    print(result.stdout)
                    logging.info("Salida estándar: " + result.stdout)
                if result.stderr:
                    print("Salida de error:")
                    print(result.stderr)
                    logging.error("Salida de error: " + result.stderr)
                return True
        finally:
            # Limpiar directorio temporal
            shutil.rmtree(temp_dir)
def promote_anonymous_complex_types(xsd_content: str) -> str:
    """
    Promote anonymous xs:complexType definitions to named global complex types.
    This avoids generating intermediate FooAType classes when running xsd2php.
    """
    namespace_decls = extract_namespace_decls(xsd_content)

    try:
        root = ET.fromstring(xsd_content)
    except ET.ParseError:
        return xsd_content

    target_namespace = root.attrib.get("targetNamespace")
    if not target_namespace:
        return xsd_content

    ET.register_namespace("", target_namespace)
    if root.attrib.get("xmlns") != target_namespace:
        root.set("xmlns", target_namespace)
    if "ds" in namespace_decls:
        root.set("xmlns:ds", namespace_decls["ds"])

    existing_type_names = {
        ct.attrib["name"]
        for ct in root.findall("xs:complexType", XS)
        if "name" in ct.attrib
    }

    structure_to_name: dict[str, str] = {}

    for complex_type in root.findall("xs:complexType", XS):
        name = complex_type.attrib.get("name")
        if not name:
            continue
        structure_key = canonicalize_complex_type(
            complex_type,
            namespace_decls,
            target_namespace,
        )
        structure_to_name.setdefault(structure_key, name)

    def ensure_prefix() -> str:
        """Ensure there is a prefix pointing to target namespace (default to tns)."""
        for attr, value in root.attrib.items():
            if attr.startswith(f"{{{XMLNS}}}") and value == target_namespace:
                prefix = attr.split("}", 1)[1]
                if prefix:
                    ET.register_namespace(prefix, target_namespace)
                    return prefix

        base_prefix = "tns"
        candidate = base_prefix
        index = 1
        while root.attrib.get(f"{{{XMLNS}}}{candidate}") is not None:
            candidate = f"{base_prefix}{index}"
            index += 1

        ET.register_namespace(candidate, target_namespace)
        root.set(f"xmlns:{candidate}", target_namespace)
        return candidate

    prefix = ensure_prefix()

    def unique_type_name(element_name: str | None) -> str:
        base = f"{element_name}Type" if element_name else "AnonymousType"
        candidate = base
        index = 1
        while candidate in existing_type_names:
            candidate = f"{base}{index}"
            index += 1
        existing_type_names.add(candidate)
        return candidate

    def assign_type_name(element_name: str | None, inline_complex: ET.Element) -> str:
        structure_key = canonicalize_complex_type(
            inline_complex,
            namespace_decls,
            target_namespace,
        )
        if structure_key in structure_to_name:
            return structure_to_name[structure_key]

        type_name = unique_type_name(element_name)
        new_complex = copy.deepcopy(inline_complex)
        new_complex.attrib["name"] = type_name
        root.append(new_complex)
        structure_to_name[structure_key] = type_name
        return type_name

    changed = False
    while True:
        iteration_changed = False
        for element in root.findall(".//xs:element", XS):
            if "type" in element.attrib:
                continue

            inline_complex = None
            for child in list(element):
                if child.tag == f"{{{XS_NS}}}complexType":
                    inline_complex = child
                    break

            if inline_complex is None:
                continue

            element_name = element.attrib.get("name")
            type_name = assign_type_name(element_name, inline_complex)
            element.remove(inline_complex)
            element.set("type", f"{prefix}:{type_name}")
            iteration_changed = True
            changed = True

        if not iteration_changed:
            break

    if not changed:
        return xsd_content

    return ET.tostring(root, encoding="utf-8", xml_declaration=True).decode("utf-8")
