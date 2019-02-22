cmake_minimum_required(VERSION 2.6)

project(nagios-plugins-lcgdm)

# architecture detection
if(UNIX AND NOT WIN32)
  if(CMAKE_SIZEOF_VOID_P MATCHES 4)
	set (LIB_SUFFIX "")
	set (PKG_ARCH "i386")
  else(CMAKE_SIZEOF_VOID_P MATCHES 4)
	set (LIB_SUFFIX 64)
	set (PKG_ARCH "x86_64")
  endif(CMAKE_SIZEOF_VOID_P MATCHES 4)
endif(UNIX AND NOT WIN32)

add_subdirectory(plugins)
add_subdirectory(configs)
add_subdirectory(templates.pnp4)
add_subdirectory(examples)
