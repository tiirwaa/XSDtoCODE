<?php
/**
 * Simple XSD to PHP class generator
 * This is a basic implementation for XSDtoCODE portable version
 */

function generatePHPClasses($xsdFile, $outputDir, $namespace = 'Generated') {
    $dom = new DOMDocument();
    $dom->load($xsdFile);

    $xpath = new DOMXPath($dom);
    $xpath->registerNamespace('xs', 'http://www.w3.org/2001/XMLSchema');

    // Get all complex types
    $complexTypes = $xpath->query('//xs:complexType');

    if (!is_dir($outputDir)) {
        mkdir($outputDir, 0777, true);
    }

    $generatedFiles = [];

    foreach ($complexTypes as $complexType) {
        $className = $complexType->getAttribute('name');
        if (!$className) continue;

        $phpCode = "<?php\n\n";
        $phpCode .= "namespace $namespace;\n\n";
        $phpCode .= "class $className\n";
        $phpCode .= "{\n";

        // Get elements
        $elements = $xpath->query('.//xs:element', $complexType);
        $properties = [];

        foreach ($elements as $element) {
            $propName = $element->getAttribute('name');
            $propType = $element->getAttribute('type');

            if ($propName && $propType) {
                // Convert XSD types to PHP types
                $phpType = convertXsdTypeToPhp($propType);
                $properties[] = "    /** @var $phpType */\n";
                $properties[] = "    public $$propName;\n\n";
            }
        }

        $phpCode .= implode('', $properties);
        $phpCode .= "}\n";

        $fileName = $outputDir . DIRECTORY_SEPARATOR . $className . '.php';
        file_put_contents($fileName, $phpCode);
        $generatedFiles[] = $fileName;
    }

    return $generatedFiles;
}

function convertXsdTypeToPhp($xsdType) {
    $typeMap = [
        'xs:string' => 'string',
        'xs:int' => 'int',
        'xs:integer' => 'int',
        'xs:decimal' => 'float',
        'xs:boolean' => 'bool',
        'xs:date' => 'string',
        'xs:dateTime' => 'string',
    ];

    return isset($typeMap[$xsdType]) ? $typeMap[$xsdType] : 'mixed';
}

// Main execution
if ($argc < 3) {
    echo "Usage: php xsd2php.php <xsd_file> <output_dir> [namespace]\n";
    exit(1);
}

$xsdFile = $argv[1];
$outputDir = $argv[2];
$namespace = isset($argv[3]) ? $argv[3] : 'Generated';

try {
    $files = generatePHPClasses($xsdFile, $outputDir, $namespace);
    echo "Generated " . count($files) . " PHP class files:\n";
    foreach ($files as $file) {
        echo "  " . basename($file) . "\n";
    }
} catch (Exception $e) {
    echo "Error: " . $e->getMessage() . "\n";
    exit(1);
}
?>