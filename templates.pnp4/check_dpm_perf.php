<?php
/* Check_dpm_perf and check_dpns_perf */

/* Color needed for the graph (6 plot max by default) */
$COLORS = Array("#FF0000", "#00FF00", "#0000FF", "#FF00FF", "#FFFF00", "#00FFFF");
$NCOLORS = count($COLORS);

/* Define a user readable data to plot*/
$DATA = Array("operation-count" => "Number of operation",
	          "total-time" => "Total time consume");

/* Define a user readable units */
$UNITS = Array( "" => "numbers",
                "s" => "seconds");

/* Find the correct DS for each combination of type, operation and stat 
        <DS>1</DS>
        <NAME>creat_total-time</NAME>

        $graph["total-time"]["creat"] = 1;
*/
$graph = Array();
foreach ($DS as $KEY=>$VAL){
  list($function, $stat) = explode("_", $NAME[$KEY]);
  $graph[$stat][$function] = $KEY;
}

/* Graph code main loop*/
$i = 1;

/* There is one graph for each type of data */
foreach ($DATA as $KEY_DATA=>$VAL_DATA){

	$j=0;
	$def[$i] = "";

	/* There is one line per monitored function */
	foreach ($graph[$KEY_DATA] as $KEY_FUNC => $VAL_FUNC){ 
		
		/* Retreive the current Datasource identifier with the associated unit */
		$current_ds = $graph[$KEY_DATA][$KEY_FUNC];
		$graph_unit = $UNIT[$current_ds];
        $displayed_unit = $UNITS[$graph_unit];

		/* Variable definition with this DS id*/
   		$def[$i] .= " DEF:var".$j."=$rrdfile:$DS[$current_ds]:AVERAGE" ;

		/*To stack the data on a plot, the first area has to be define with the AREA type*/
		if( $j == 0)
		{
			$def[$i] .= " AREA:var".$j.$COLORS[$j].":\"".$KEY_FUNC."\"";
		}
		else
		{
 			$def[$i] .= " STACK:var".$j.$COLORS[$j].":\"".$KEY_FUNC."\"";
		}

		/* Print data in the graph legend*/
		$def[$i] .= " GPRINT:var".$j.":LAST:\"%3.4lg %s$graph_unit \\n\" ";
		$j++;
	}

	/* Define some graph's information: title, ylabel */
    $opt[$i] = "--title \"".$VAL_DATA." per function\" --vertical-label \"".$displayed_unit."\"";
	$i++;
	}
?>
