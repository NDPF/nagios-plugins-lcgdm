<?php
foreach ($DS as $KEY=>$VAL) {

	$maximum  = "";
	
	if ($MAX[$KEY] != "") {
		$maximum = $MAX[$KEY];
	}

	$label = str_replace("_", " ", $NAME[$KEY]);
	$opt[$KEY] = "-l 0 --title \"Space for " . $label . "\" --vertical-labe=Bytes";
	$ds_name[$KEY] = $label;
	$def[$KEY]  = "DEF:free=$rrdfile:$VAL:AVERAGE ";
	$def[$KEY] .= "CDEF:used=$maximum,free,- ";
	$def[$KEY] .= "AREA:used#005500:\"Used space\" ";
	$def[$KEY] .= "GPRINT:used:LAST:\"%3.2lf %S $UNIT[$KEY] \" ";
	$def[$KEY] .= "AREA:free#00FF00:\"Free space\":STACK ";
	$def[$KEY] .= "GPRINT:free:LAST:\"%3.2lf %S $UNIT[$KEY] \\n\" ";

	$def[$KEY] .= "LINE1:" . ($maximum - $WARN_MIN[$KEY]) . "#FFFF00:\"Warning\\n\" ";
	$def[$KEY] .= "LINE1:" . ($maximum - $CRIT_MIN[$KEY]) . "#FF0000:\"Critical\" ";
}
?>
