#configure.ac file for python-xkb
AC_INIT(python-xkb,1.0.0)
AC_SUBST(VERSION,1.0.0)
#check for python version 2.6. setup.py does this check as well
#but this will tell us where python is located. This is useful for
#the makefile
AM_PATH_PYTHON([2.6])

#check for doxygen program
AC_PATH_PROG([DOXYGEN_BINARY], [doxygen])

######### USER OPTIONS ################
#check if the user specifies a specific Doxygen config file
AC_ARG_ENABLE(deb-install, 
	[  --enable-deb-install         Enable Debian-style Python installs (into dist-packages).])

########OPTION CHECKING##############
#check if the deb-install flag has been enabled.
if test "$enable_deb_install" == "yes"
then
	AC_MSG_NOTICE([Enabling debian install...])
	AC_SUBST(DEBIAN_FLAG, "--install-layout=deb")
else
	AC_SUBST(DEBIAN_FLAG, "")
fi 

#check if the user has specified a prefix
if test "$prefix" != NONE
then
	AC_SUBST(PREFIX_FLAG, "--prefix="$prefix)
	if test "$prefix" == "/usr/local"
	then
		AC_SUBST(PY_PKG_DIR, $prefix"/lib/python"$PYTHON_VERSION"/dist-packages")
	elif test "$enable_deb_install" == "yes"
	then
		AC_SUBST(PY_PKG_DIR, $prefix"/lib/python"$PYTHON_VERSION"/dist-packages")
	else
		AC_SUBST(PY_PKG_DIR, $prefix"/lib/python"$PYTHON_VERSION"/site-packages")
	fi
else
	AC_SUBST(PREFIX_FLAG, "")
	AC_SUBST(PY_PKG_DIR, "/usr/local/lib/python"$PYTHON_VERSION"/dist-packages")
fi

#substituted flags for Make.

#output all of this into Makefile.in, producing Makefile.
AC_OUTPUT(Makefile)
#produce setup.py
AC_OUTPUT(setup.py)