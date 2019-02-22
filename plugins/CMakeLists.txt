cmake_minimum_required(VERSION 2.6)

install(
	FILES 		lcgdmcommon.py check_cpu check_process check_network 
			check_hostcert
	DESTINATION 	usr/lib${LIB_SUFFIX}/nagios/plugins/lcgdm/
	PERMISSIONS 	OWNER_EXECUTE OWNER_WRITE OWNER_READ 
			GROUP_EXECUTE GROUP_READ
			WORLD_EXECUTE WORLD_READ
)

install(
	FILES 		check_dpm_perf check_dpns_perf check_dpm_pool 
			check_dpm_infosys check_space_token
	DESTINATION 	usr/lib${LIB_SUFFIX}/nagios/plugins/lcgdm/
	PERMISSIONS 	OWNER_EXECUTE OWNER_WRITE OWNER_READ 
			GROUP_EXECUTE GROUP_READ
			WORLD_EXECUTE WORLD_READ
)

install(
	FILES 		check_partition_activity check_gridftp_activity
			check_gridftp_transfer check_rfio_activity
	DESTINATION 	usr/lib${LIB_SUFFIX}/nagios/plugins/lcgdm/
	PERMISSIONS 	OWNER_EXECUTE OWNER_WRITE OWNER_READ 
			GROUP_EXECUTE GROUP_READ
			WORLD_EXECUTE WORLD_READ
)


install(
	FILES 		check_lfc_perf check_oracle_expiration check_lfc_sam LFC-probe
	DESTINATION 	usr/lib${LIB_SUFFIX}/nagios/plugins/lcgdm/
	PERMISSIONS 	OWNER_EXECUTE OWNER_WRITE OWNER_READ 
			GROUP_EXECUTE GROUP_READ
			WORLD_EXECUTE WORLD_READ
)


install(
	FILES 		check_dpm check_dpns check_rfio check_gridftp
	DESTINATION 	usr/lib${LIB_SUFFIX}/nagios/plugins/lcgdm/
	PERMISSIONS 	OWNER_EXECUTE OWNER_WRITE OWNER_READ 
			GROUP_EXECUTE GROUP_READ
			WORLD_EXECUTE WORLD_READ
)
