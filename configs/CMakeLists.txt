cmake_minimum_required(VERSION 2.6)

#
# generate nrpe configuration files from templates
#
configure_file (
               "${PROJECT_SOURCE_DIR}/configs/lcgdm-headnode.cfg.in"
               "${PROJECT_BINARY_DIR}/configs/lcgdm-headnode.cfg"
)

configure_file (
               "${PROJECT_SOURCE_DIR}/configs/lcgdm-common.cfg.in"
               "${PROJECT_BINARY_DIR}/configs/lcgdm-common.cfg"
)

configure_file (
               "${PROJECT_SOURCE_DIR}/configs/lcgdm-disk.cfg.in"
               "${PROJECT_BINARY_DIR}/configs/lcgdm-disk.cfg"
)

configure_file (
	       "${PROJECT_SOURCE_DIR}/configs/lcgdm-lfc.cfg.in"
               "${PROJECT_BINARY_DIR}/configs/lcgdm-lfc.cfg"
)
	
#
# nrpe configuration files
#
install(
	FILES 		${PROJECT_BINARY_DIR}/configs/lcgdm-headnode.cfg
	DESTINATION	etc/nrpe.d/
	PERMISSIONS 	OWNER_WRITE OWNER_READ 
			GROUP_READ
			WORLD_READ
)

install(
	FILES 		${PROJECT_BINARY_DIR}/configs/lcgdm-common.cfg
	DESTINATION 	etc/nrpe.d/
	PERMISSIONS 	OWNER_WRITE OWNER_READ 
			GROUP_READ
			WORLD_READ
)

install(
	FILES 		${PROJECT_BINARY_DIR}/configs/lcgdm-disk.cfg
	DESTINATION 	etc/nrpe.d/
	PERMISSIONS 	OWNER_WRITE OWNER_READ 
			GROUP_READ
			WORLD_READ
)

install(
	FILES 		${PROJECT_BINARY_DIR}/configs/lcgdm-lfc.cfg
	DESTINATION 	etc/nrpe.d/
	PERMISSIONS 	OWNER_WRITE OWNER_READ 
			GROUP_READ
			WORLD_READ
)
