<?php
foreach ($DS as $KEY=>$VAL) {

	$maximum  = "";
	
	if ($MAX[$KEY] != "") {
		$maximum = $MAX[$KEY];
	}

	$label = str_replace("_", " ", $NAME[$KEY]);
	$opt[$KEY] = "--title \"Space for space token" . $label . "\" --vertical-label=Bytes";
	$ds_name[$KEY] = $label;
	$def[$KEY]  = "DEF:free=$rrdfile:$VAL:AVERAGE ";
    $def[$KEY] .= "CDEF:used=$maximum,free,- ";
	$def[$KEY] .= "AREA:used#005500:\"Used space\" ";
	$def[$KEY] .= "GPRINT:used:LAST:\"%3.2lf %S $UNIT[$KEY] \" ";
	$def[$KEY] .= "AREA:free#00FF00:\"Free space\":STACK ";
	$def[$KEY] .= "GPRINT:free:LAST:\"%3.2lf %S $UNIT[$KEY] \\n\" ";

	$def[$KEY] .= "LINE1:" . ($maximum - $WARN[$KEY]) . "#FFFF00:\"Warning\\n\" ";
	$def[$KEY] .= "LINE1:" . ($maximum - $CRIT[$KEY]) . "#FF0000:\"Critical\" ";
}
?>
