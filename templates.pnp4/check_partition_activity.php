<?php

$COLORS = Array("read"  => "#00FF00",
		"write" =>"#FF0000");

$devices = Array();
foreach($DS as $KEY=>$VAL) {
	list($dev, $mode) = explode('_', $NAME[$KEY]);

	if(!array_key_exists($dev, $devices)) {
		$devices[$dev] = Array();
	}

	$devices[$dev][$mode] = $KEY;
}

$i = 1;
foreach($devices as $DEV=>$MODE) {
	$opt[$i] = "-l 0 --title \"Partition activity for $hostname/$DEV\" --vertical-label \"Bytes / second\"";
	$ds_name[$i] = $DEV;

	$def[$i] = "";
	foreach($MODE as $m=>$key) {
		$def[$i] .= "DEF:$m=$rrdfile:" . $DS[$key]['DS'] . ":AVERAGE ";
		$def[$i] .= "LINE1:${m}$COLORS[$m]:\"" . ucwords($m) . " activity\\n\" ";
	}

	$i++;
}
?>
