cmake_minimum_required(VERSION 2.6)

configure_file (
               "${PROJECT_SOURCE_DIR}/examples/lcgdm-commands.cfg.in"
               "${PROJECT_BINARY_DIR}/examples/lcgdm-commands.cfg"
)

install(
	FILES 		generic-service.cfg lcgdm-hosts.cfg lcgdm-services.cfg
			${PROJECT_BINARY_DIR}/examples/lcgdm-commands.cfg
	DESTINATION 	etc/nagios
)
