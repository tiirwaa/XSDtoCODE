const fs = require('fs');
const path = require('path');
const { Xsd2JsonSchema } = require('xsd2jsonschema');

async function convert(xsdFilePath, outputDir) {
  const xs2js = new Xsd2JsonSchema({
    jsonSchemaVersion: 'draft-04'
  });

  // Leer archivo XSD
  const xsdContent = fs.readFileSync(xsdFilePath, 'utf-8');
  const fileName = path.basename(xsdFilePath);

  // Procesar
  let convertedSchemas;
  try {
    convertedSchemas = xs2js.processAllSchemas({
      schemas: { [fileName]: xsdContent }
    });
  } catch (e) {
    console.error('Error al procesar el XSD:');
    console.error(e.stack || e);
    throw e; // re-lanzar para que llegue al catch final
  }

  const jsonSchema = convertedSchemas[fileName].getJsonSchema();

  // Guardar JSON Schema
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }
  const outputPath = path.join(outputDir, fileName.replace(/\.xsd$/, '.json'));
  fs.writeFileSync(outputPath, JSON.stringify(jsonSchema, null, 2), 'utf-8');

  console.log(`JSON Schema generado: ${outputPath}`);
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
