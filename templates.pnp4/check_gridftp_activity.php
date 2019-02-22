<?php
/* Check_gridftp_transfer and check_rfio_transfer */

/* Color needed for the graph */
$COLORS = Array("#FF0000", "#00FF00", "#0000FF");
$NCOLORS = count($COLORS);

/* Type of file: depending on the file size */
$TYPES = Array("large" => "Large file",
                "medium" => "Medium file",
                "small" => "Small file");

/* Different kind of operations: 2 possible, read and write */
$OPERATIONS = Array("read" => "read",
                    "write" => "write");

/* Define a user readable data to plot*/
$DATA = Array("transfer-count" => "Number of",
               "transfered-bytes" => "Bytes",
               "link-throughput" => "Link throughput used for");

/* Define a user readable units */
$UNITS = Array( "" => "num",
                "B" => "Bytes",
                "B_s" => "Bytes / second",      // for pnp4nagios0.4 compatibility
                "B/s" => "Bytes / second");     // for pnp4nagios0.6 compatibility

/* Find the correct DS for each combination of type, operation and stat 
        <DS>2</DS>
        <NAME>large_read_transfered-bytes</NAME>

        $graph["transfered-bytes"]["read"]["large"] = 2;
*/
$graph = Array();
foreach ($DS as $KEY=>$VAL){
  list($type, $opp, $stat) = explode("_", $NAME[$KEY]);
  $graph[$stat][$opp][$type] = $KEY;
}

/* Graph code main loop*/
$i = 1;

/* There is one graph for each couple of data and operation */
foreach ($DATA as $KEY_DATA=>$VAL_DATA){
        foreach ($OPERATIONS as $KEY_OPP=>$VAL_OPP){        

                $j=0;           // index of a plot on the graph
                $def[$i] = "";  // Definition of a new graphic

                /* There is one line per data type (small, medium, large) */
                foreach ($TYPES as $KEY_TYPE => $VAL_TYPE){

                        /* Retreive the current Datasource identifier with the associated unit */
                        $current_ds = $graph[$KEY_DATA][$KEY_OPP][$KEY_TYPE];
                        $graph_unit = $UNIT[$current_ds];
                        $displayed_unit = $UNITS[$graph_unit];

                        /* Variable definition with this DS id*/
                        $def[$i] .= " DEF:var".$j."=$rrdfile:$DS[$current_ds]:AVERAGE";

                        /*To stack the data on a plot, the first area has to be define with the AREA type*/
                        if( $j == 0)
                        {
                                $def[$i] .= " AREA:var".$j.$COLORS[$j].":\"".$VAL_TYPE."\"";
                        }
                        else
                        {
                                $def[$i] .= " STACK:var".$j.$COLORS[$j].":\"".$VAL_TYPE."\"";
                        }

                        /* Print data in the graph legend*/
			$def[$i] .= " GPRINT:var".$j.":LAST:\"%4.0lf %s$graph_unit last\" " ;
                  	$def[$i] .= " GPRINT:var".$j.":AVERAGE:\"%3.4lg %s$graph_unit avg\" ";
                        $def[$i] .= " GPRINT:var".$j.":MAX:\"%3.4lg %s$graph_unit max\\n\" ";
                        $j++;
                }

                /* Define some graph's information: title, ylabel */
                $opt[$i] = "--title \"".$VAL_DATA." ".$VAL_OPP."\" --vertical-label \"".$displayed_unit."\"";
                $i++;
        }
}
?>

