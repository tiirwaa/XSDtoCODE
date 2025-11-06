const fs = require('fs');
const path = require('path');
const { Xsd2JsonSchema } = require('xsd2jsonschema');

async function convert(xsdFilePath, outputDir) {
  const versions = ['draft-04', 'draft-06', 'draft-07'];
  let lastError;

  for (const version of versions) {
    try {
      const xs2js = new Xsd2JsonSchema({
        jsonSchemaVersion: version
      });

      // Leer archivo XSD
      const xsdContent = fs.readFileSync(xsdFilePath, 'utf-8');
      const fileName = path.basename(xsdFilePath);

      // Procesar
      const convertedSchemas = xs2js.processAllSchemas({
        schemas: { [fileName]: xsdContent }
      });

      const jsonSchema = convertedSchemas[fileName].getJsonSchema();

      // Guardar JSON Schema
      if (!fs.existsSync(outputDir)) {
        fs.mkdirSync(outputDir, { recursive: true });
      }
      const outputPath = path.join(outputDir, fileName.replace(/\.xsd$/, '.json'));
      fs.writeFileSync(outputPath, JSON.stringify(jsonSchema, null, 2), 'utf-8');

      console.log(`JSON Schema generado con versión ${version}: ${outputPath}`);
      return; // Éxito, salir
    } catch (e) {
      lastError = e;
      console.log(`Versión ${version} falló, intentando siguiente...`);
    }
  }

  // Si ninguna versión funcionó
  console.error('Error al procesar el XSD con todas las versiones probadas:');
  console.error(lastError.stack || lastError);
  throw lastError;
}

const [,, xsdFilePath, outputDir] = process.argv;

if (!xsdFilePath || !outputDir) {
  console.error('Uso: node convert_xsd_to_jsonschema.js <ruta_xsd> <carpeta_salida>');
  process.exit(1);
}

convert(xsdFilePath, outputDir).catch(err => {
  console.error('Error al convertir XSD a JSON Schema:');
  console.error(err.stack || err);
  process.exit(1);
});
