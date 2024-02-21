find_package(PkgConfig)

PKG_CHECK_MODULES(PC_GR_SONIK gnuradio-sonik)

FIND_PATH(
    GR_SONIK_INCLUDE_DIRS
    NAMES gnuradio/sonik/api.h
    HINTS $ENV{SONIK_DIR}/include
        ${PC_SONIK_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    GR_SONIK_LIBRARIES
    NAMES gnuradio-sonik
    HINTS $ENV{SONIK_DIR}/lib
        ${PC_SONIK_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
          )

include("${CMAKE_CURRENT_LIST_DIR}/gnuradio-sonikTarget.cmake")

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(GR_SONIK DEFAULT_MSG GR_SONIK_LIBRARIES GR_SONIK_INCLUDE_DIRS)
MARK_AS_ADVANCED(GR_SONIK_LIBRARIES GR_SONIK_INCLUDE_DIRS)
