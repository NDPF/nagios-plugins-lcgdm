<?php

$COLORS = Array("in"  => "#00FF00",
		"out" =>"#0000FF",
                "err" => "#FF0000");

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
	# In and out
	$opt[$i] = "-l 0 --title \"Network activity for $hostname/$DEV\" --vertical-label \"Bytes / second\"";
	$ds_name[$i] = $DEV;

	$def[$i] = "";
	foreach(Array('in', 'out') as $m) {
		$def[$i] .= "DEF:$m=$rrdfile:" . $DS[$devices[$DEV][$m]]['DS'] . ":AVERAGE ";
		$def[$i] .= "LINE1:${m}$COLORS[$m]:\"" . ucwords($m) . "put traffic\\n\" ";
	}

	$i++;

	# Error
	$opt[$i] = "-l 0 --title \"Packages dropped per second for $hostname/$DEV\"";
	$ds_name[$i] = $DEV;

        $def[$i] = "";
	$def[$i] .= "DEF:$m=$rrdfile:" . $DS[$devices[$DEV]['err']]['DS'] . ":AVERAGE ";
	$def[$i] .= "LINE1:${m}$COLORS[err]:\"Packages dropped\\n\" ";

        $i++;
}
?>
