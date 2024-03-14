find_package(PkgConfig)

PKG_CHECK_MODULES(PC_GR_SONIKS gnuradio-soniks)

FIND_PATH(
    GR_SONIKS_INCLUDE_DIRS
    NAMES gnuradio/soniks/api.h
    HINTS $ENV{SONIKS_DIR}/include
        ${PC_SONIKS_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    GR_SONIKS_LIBRARIES
    NAMES gnuradio-soniks
    HINTS $ENV{SONIKS_DIR}/lib
        ${PC_SONIKS_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
          )

include("${CMAKE_CURRENT_LIST_DIR}/gnuradio-soniksTarget.cmake")

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(GR_SONIKS DEFAULT_MSG GR_SONIKS_LIBRARIES GR_SONIKS_INCLUDE_DIRS)
MARK_AS_ADVANCED(GR_SONIKS_LIBRARIES GR_SONIKS_INCLUDE_DIRS)
