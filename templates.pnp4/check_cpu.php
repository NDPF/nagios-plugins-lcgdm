<?php
$opt[1] = "-r -u 100 -l 0 --title \"CPU for " . $hostname . "\" --vertical-label=%";

$def[1]  = "DEF:user=$rrdfile:$DS[1]:AVERAGE ";
$def[1] .= "DEF:nice=$rrdfile:$DS[2]:AVERAGE ";
$def[1] .= "DEF:sys=$rrdfile:$DS[3]:AVERAGE " ;
$def[1] .= "DEF:idle=$rrdfile:$DS[4]:AVERAGE ";
$def[1] .= "DEF:iowa=$rrdfile:$DS[5]:AVERAGE ";
$def[1] .= "DEF:irq=$rrdfile:$DS[6]:AVERAGE " ;
$def[1] .= "DEF:sirq=$rrdfile:$DS[7]:AVERAGE ";

$def[1] .= "LINE1:user#0000FF:\"User\" ";
$def[1] .= "LINE1:nice#555555:\"Nice\" ";
$def[1] .= "LINE1:sys#FFFF00:\"System\" ";
$def[1] .= "LINE1:idle#00FF00:\"Idle\" ";
$def[1] .= "LINE1:iowa#FF0000:\"IO wait\" ";
$def[1] .= "LINE1:irq#FF00FF:\"IRQ\" ";
$def[1] .= "LINE1:sirq#FF9100:\"Soft IRQ\" ";
?>
