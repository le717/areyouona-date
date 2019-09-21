<?php
date_default_timezone_set('UTC');
$locationData = json_decode(file_get_contents("php://input"));

// Format all the data
$date = date("Y-m-d h:i:s A e", $locationData->time / 1000);
$lat = "Latitude: {$locationData->lat}";
$lng = "Longitude: {$locationData->lng}";
$acc = "Accuracy (meters): {$locationData->acc}";

// Generate the log format
$str = <<<EOT
[$date] $lat $lng $acc

EOT;

// Log the data
$locationDataFile = 'location.log';
file_put_contents($locationDataFile, $str, FILE_APPEND | LOCK_EX);
exit;
