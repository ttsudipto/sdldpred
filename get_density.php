<?php
    $x = array();
    $y = array();
    $f = fopen("output/density/density.tsv", "r");
    fgetcsv($f, 0, "\t");
    while (($data = fgetcsv($f, 0, "\t")) !== false) {
        array_push($x, floatval($data[0]));
        array_push($y, floatval($data[1]));
    }
    echo json_encode(array("x" => $x, "y" => $y));
?>
