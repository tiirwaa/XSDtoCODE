<?php

$phar = new Phar('xsd2php.phar');
$phar->buildFromDirectory('vendor');
$phar->setStub("#!/usr/bin/env php\n<?php Phar::mapPhar(); include 'phar://xsd2php.phar/bin/xsd2php'; __HALT_COMPILER(); ?>");

echo "Phar created: xsd2php.phar\n";

?>