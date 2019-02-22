<?php
# Array of colors
$COLORS = Array("#FF0000", "#00FF00", "#0000FF", "#FF00FF", "#FFFF00", "#00FFFF");
$NCOLORS = count($COLORS);

# Human-readable labels
$LABELS = Array("cpu" => "CPU percentage",
		"mem" => "Memory percentage",
		"thr" => "Threads",
		"fd"  => "File descriptors",
		"conn" => "Number of connections",
		"instances" => "Instances");

$UNITS = Array("cpu" => "%",
		"mem" => "%",
		"thr" => "",
		"fd"  => "",
		"conn" => "",
		"instances" => "");

# Arrange by type
$array = Array();
foreach ($DS as $KEY=>$VAL) {
	list($proc, $type) = explode('_', $NAME[$KEY]);

	if(!array_key_exists($type, $array)) {
		$array[$type] = Array();
	}

	$array[$type][$proc] = $KEY;
}

# Display
$i = 1;
foreach($array as $TYPE=>$PROC_LIST) {
	$opt[$i] = "--title \"$LABELS[$TYPE]\" --vertical-label=$UNITS[$TYPE]";
	$ds_name[$i] = $TYPE;

	# All together
	$def[$i] = "";
	$j = 0;
        foreach($PROC_LIST as $PROC=>$KEY) {
                $def[$i] .= "DEF:$PROC=$rrdfile:" . $DS[$array[$TYPE][$PROC]] . ":AVERAGE ";
                $def[$i] .= "LINE1:$PROC" . $COLORS[$j % $NCOLORS] . ":\"$PROC\" ";

		$unit = $UNIT[$array[$TYPE][$PROC]];
		if($unit == '%%') {
			$def[$i] .= "GPRINT:$PROC:LAST:\"%3.2lf %%\" ";
		} else {
			$def[$i] .= "GPRINT:$PROC:LAST:\"%3.lf\" ";
		}
		$j++;
        } 

        $i++;

}
?>
