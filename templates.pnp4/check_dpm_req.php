<?php

/* Color needed for the graph */

$COLORS = Array("#FF0000", "#00FF00", "#0000FF", "#0F0F0F");
$NCOLORS = count($COLORS);

$opt[0] = "-l 0 --title \"Number of requests \" --vertical-labe=Number";
$def[0] = "";

$i = 0;
foreach ($DS as $KEY=>$VAL) {

	$def[0] .= "DEF:var$i=$rrdfile:$VAL:AVERAGE ";
	
	if ($i == 0)	{
		$def[0] .= " AREA:var$i$COLORS[$i]:\"$NAME[$KEY]\" ";	
	}else{
		$def[0] .= " STACK:var$i$COLORS[$i]:\"$NAME[$KEY]\" ";
	}

	$def[0] .= " GPRINT:var".$i.":LAST:\"last\: %4.0lf\" " ;
	$def[0] .= " GPRINT:var".$i.":AVERAGE:\"avg\: %4.0lf\" ";
	$def[0] .= " GPRINT:var".$i.":MAX:\"max\: %4.0lf\\n\" ";

       # $def[0] .= " GPRINT:var:MAX:\"%3.4lg max\\n\" ";


	
	$i++;
}
?>
