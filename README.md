# XSDtoCODE

![Logo](iconogui.ico)

*For the Spanish version, see [README.es.md](README.es.md).*

**XSDtoCODE** is a tool written in **Python**, designed to automate the generation of classes from **XSD** (XML Schema Definition) files. Its main purpose is to simplify the integration of XML schemas into modern software projects, allowing developers to work directly with **programming objects and classes** instead of manually manipulating XML. This ensures that the generated classes accurately reflect the defined schema and can be **automatically serialized and deserialized to XML**, eliminating errors and manual effort.

The tool is compatible with multiple programming languages, including **Java**, **C#**, **Python**, **PHP**, and **JSONSchema**, making it ideal for heterogeneous environments and projects that require consistency between systems using different languages. By supporting multiple languages, XSDtoCODE allows:

- Generate **robust and reliable data models** directly from the XSD schema.  
- Reduce human errors associated with manual creation of XML or classes.  
- Maintain automatic synchronization between the XML schema and the classes used in the application.  
- Accelerate the development of applications that consume or produce XML data, including **electronic invoicing** and financial systems.

For each language, XSDtoCODE uses specialized generators:  

- **Java**: [`xjc`](https://docs.oracle.com/javase/8/docs/technotes/tools/unix/xjc.html), which converts XSD schemas into Java classes ready to serialize/deserialize XML.  
- **C#**: [`XmlSchemaClassGenerator`](https://github.com/mganss/XmlSchemaClassGenerator), which creates .NET classes compatible with the XML schema.  
- **Python**: [`xsdata`](https://github.com/tefra/xsdata), which generates modern Python classes with full support for automatic XML serialization and deserialization.  
- **PHP**: `xsd2php.phar` (compiled from [goetas-webservices/xsd2php](https://github.com/goetas-webservices/xsd2php)) executed with portable PHP to generate PHP classes and metadata compatible with JMS Serializer.  
- **JSONSchema**: [`xsd2jsonschema`](https://github.com/tiirwaa/XSDtoCODE/blob/main/node/convert_xsd_to_jsonschema.js), which transforms XSD into JSON schemas, allowing interoperability with applications that use JSON based on XML.

Among the main benefits of using XSDtoCODE are:  

- **Complete automation**: Automatically generates classes and mappings, avoiding manual coding of XML and data structures.  
- **Compatibility**: The class generator currently works on **Windows**, but the generated models are standard and can be compiled and run on any platform compatible with the corresponding language.  
- **Integration with existing systems**: Allows generating classes ready to integrate with **SOAP web services**, **XML-based REST APIs**, internal APIs, or enterprise data exchanges.  
- **Flexibility**: Possibility to customize class names, packages, or namespaces according to project needs.  
- **Error reduction**: By working with automatically generated classes, inconsistencies and errors that arise from writing XML by hand are minimized.  
- **Time savings in maintenance**: Each change in the XSD can be reflected by regenerating the classes, keeping the application synchronized with the updated schema.

XSDtoCODE is ideal for developers and teams working with:  

- **XML-based web services** (SOAP or REST XML)  
- **Electronic invoicing and financial systems** that require reliable XML data exchange  
- **Enterprise information exchange** (EDI, standard XML)  
- **Systems that need reliable XML serialization and deserialization**  
- **Projects that require interoperability between multiple languages and platforms**

In summary, **XSDtoCODE** transforms XSD files into ready-to-use programming classes that can be **automatically serialized and deserialized as XML**, facilitating the integration of XML data into any project and ensuring **consistency, efficiency, and robustness** in software development.

---

![Screen](img/XSDtoCODE.png)

---

## 📦 Dependencies

### UI: `tkinter`

```bash
pip install tkinter
```

Install the following dependencies with `pip`:

```bash
pip install pillow
pip install xsdata
pip install "xsdata[cli]"
```

## 🔣 Currently Available Languages

- Java
- C#
- Python
- PHP
- JSONSchema

---

## 🖥️ Console Usage

```bash
python main.py "file.xsd" "java|python|csharp|php|JSONSchema" "output_folder"
```

```bash
main.exe "file.xsd" "java|python|csharp|php|JSONSchema" "output_folder"
```

## ⚙️ Generate EXE
```bash
generar_exe.bat
```

## Portable PHP

XSDtoCODE includes **fully portable PHP** (version 8.3.27), so **it does not require prior PHP installation** on the host system. The final executable incorporates:

- PHP 8.3.27 Thread Safe for Windows x64
- All necessary standard extensions
- The `xsd2php.phar` compiled from goetas-webservices/xsd2php
- Minimal `php.ini` configuration

During the build in GitHub Actions, the `.phar` is automatically compiled with Composer and Box, and packaged inside `dist/XSDtoCODE/_internal/`. This way we avoid versioning huge files and always distribute the updated version of the PHP generator. This ensures that PHP class generation works on any Windows system without additional external dependencies.


##  
Developed by: [A&G Programación y Desarrollo de Sistemas Informáticos S.A.](https://agsoft.co.cr)  
![Logo](https://agsoft.co.cr/wp-content/uploads/2023/08/logo.png)
