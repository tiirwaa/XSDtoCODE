<?php

/*
 * XSD to PHP converter - Compatible with xsd2php.phar interface
 * This script simulates xsd2php.phar for XSDtoCODE portable version
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

        // Get elements - handle both name/type and ref attributes
        $elements = $xpath->query('.//xs:element', $complexType);
        $properties = [];
        foreach ($elements as $element) {
            $propName = $element->getAttribute('name');
            $propType = $element->getAttribute('type');
            $propRef = $element->getAttribute('ref');

            if ($propRef) {
                // Handle ref attributes - extract the local name
                $refParts = explode(':', $propRef);
                $propName = end($refParts);
                $propType = 'mixed'; // For refs, we don't know the exact type
            }

            if ($propName && ($propType || $propRef)) {
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

function parseConfigFile($file) {
    $content = file_get_contents($file);

    // Remove BOM if present
    if (substr($content, 0, 3) === "\xEF\xBB\xBF") {
        $content = substr($content, 3);
    }

    $config = [];

    // Simple key-value parser for our config format
    $lines = explode("\n", $content);
    $currentSection = null;

    foreach ($lines as $line) {
        $line = trim($line);
        if (empty($line) || strpos($line, '#') === 0) continue;

        // Check for section headers (lines ending with ':')
        if (preg_match('/^([a-zA-Z_]+):$/', $line, $matches)) {
            $currentSection = $matches[1];
            $config[$currentSection] = [];
        }
        // Check for key-value pairs with colon
        elseif ($currentSection && strpos($line, ':') !== false) {
            list($key, $value) = explode(':', $line, 2);
            $key = trim($key);
            $value = trim($value);

            // Remove leading dashes and spaces for list items
            $key = ltrim($key, '- ');

            if ($currentSection === 'generator' && $key === 'destinations') {
                // Handle destinations as array
                if (!isset($config[$currentSection][$key])) {
                    $config[$currentSection][$key] = [];
                }
                // For now, we'll handle this differently - just store the folder directly
            } elseif ($currentSection === 'generator' && strpos($key, 'folder') !== false) {
                $config[$currentSection]['folder'] = $value;
            } elseif ($currentSection === 'generator' && strpos($key, 'namespace') !== false) {
                $config[$currentSection]['namespace'] = $value;
            } else {
                $config[$currentSection][$key] = $value;
            }
        }
    }

    return $config;
}

function parseYamlValue($value) {
    $value = trim($value);
    if ($value === 'true') return true;
    if ($value === 'false') return false;
    if (is_numeric($value)) {
        return strpos($value, '.') !== false ? (float)$value : (int)$value;
    }
    return $value;
}

// Simulate xsd2php.phar interface
if ($argc >= 2 && $argv[1] === 'convert') {
    // Parse arguments like xsd2php.phar convert config.yml
    if ($argc >= 3) {
        $configFile = $argv[2];
        if (file_exists($configFile)) {
            // Parse YAML-like config (simple implementation)
            $config = parseConfigFile($configFile);
            if (isset($config['xsd']['file']) && isset($config['generator']['folder'])) {
                $xsdFile = $config['xsd']['file'];
                $outputDir = $config['generator']['folder'];
                $namespace = $config['generator']['namespace'] ?? 'Generated';
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
            } else {
                echo "Invalid config file format\n";
                exit(1);
            }
        } else {
            echo "Config file not found: $configFile\n";
            exit(1);
        }
    } else {
        echo "Usage: php xsd2php.php convert <config.yml>\n";
        exit(1);
    }
} elseif ($argc >= 2 && $argv[1] === 'list') {
    if ($argc >= 3) {
        $xsdFile = $argv[2];
        if (file_exists($xsdFile)) {
            $dom = new DOMDocument();
            $dom->load($xsdFile);

            $xpath = new DOMXPath($dom);
            $xpath->registerNamespace('xs', 'http://www.w3.org/2001/XMLSchema');

            echo "Types in $xsdFile:\n";

            // List complex types
            $complexTypes = $xpath->query('//xs:complexType');
            foreach ($complexTypes as $type) {
                $name = $type->getAttribute('name');
                if ($name) {
                    echo "  ComplexType: $name\n";
                }
            }

            // List simple types
            $simpleTypes = $xpath->query('//xs:simpleType');
            foreach ($simpleTypes as $type) {
                $name = $type->getAttribute('name');
                if ($name) {
                    echo "  SimpleType: $name\n";
                }
            }
        } else {
            echo "XSD file not found: $xsdFile\n";
            exit(1);
        }
    } else {
        echo "Usage: php xsd2php.php list <xsd-file>\n";
        exit(1);
    }
} else {
    echo "XSD to PHP Converter (xsd2php.phar compatible)\n\n";
    echo "Usage:\n";
    echo "  php xsd2php.php convert <config.yml>    Convert XSD to PHP using config file\n";
    echo "  php xsd2php.php list <xsd-file>          List types in XSD file\n";
    exit(1);
}

?>
