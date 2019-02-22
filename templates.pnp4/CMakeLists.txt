cmake_minimum_required(VERSION 2.6)

file(GLOB templates *.php)

install(
	FILES ${templates}
	DESTINATION usr/share/nagios/html/pnp4nagios/templates.lcgdm
)
