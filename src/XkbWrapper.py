import ctypes.util
import types
import logging.handlers
from typeutils.TypeChecker import require

# Copyright (c) 2010 Siddhu Warrier (http://siddhuwarrier.homelinux.org, 
# siddhuwarrier AT gmail DOT com). 
# 
# This file is part of the xkb package.
# The xkb package is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# This code has been produced heavily modifying:
# On screen display for learning the keyboard layout Neo2
# Copyright (c) 2009 Martin Zuther (http://www.mzuther.de/)
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# Thank you for using free software!

__all__ = ["XkbWrapper"]

## @brief Class for providing a simple Xkb Wrapper.
#
# This class provides a simple XKB wrapper, and has been created by extensively
# refactoring the Neo OSD2 XKB wrapper. 
# @ingroup xkb
# @author Siddhu Warrier (siddhuwarrier@gmail.com)
# @date 31/01/2009.
class XkbWrapper:
    ##@brief XkbOpenDisplay error codes as a dictionary
    # See http://linux.die.net/man/3/xkbopendisplay for more details.
    # The values for these are obtained from file /usr/include/X11/XKBlib.h (Ubuntu 9.04):
    #these error codes are not visible in a __dict__(). Best we can do for obj abstraction
    #in Py, or so methinks.
    __errcodes_xkbOpenDisplay = {
        "Xkb0D_Success": 0, #success - XkbOpenDisplay worked!
        "XkbOD_BadLibraryVersion": 1, #XkbLibraryVersion returned False. 
        "XkbOD_ConnectionRefused": 2, #the display could not be opened.
        "XkbOD_NonXkbServer": 3, #the library and the server have incompatible extension versions.
        "XkbOD_BadServerVersion": 4 #the extension is not present in the X server. 
        }
    ##@brief XKB constants as a dictionary
    constants_xkb = {"XkbUseCoreKbd":0x0100}
    
    ## @brief XkbWrapper constructor. Extensively refactored from Neo OSD2.
    # 
    # This constructor maps the C functions to Python equivalents, and thereby
    # sets stuff up for future calls.
    # 
    # @date 31/01/2010    
    def __init__(self):
        #set the logger up
        self.logger = logging.getLogger("utils")
        self.logger.setLevel(logging.FATAL) #by default, only FATAL messages are processed
        #add the handler
        self.loggerHandler = logging.handlers.RotatingFileHandler("/tmp/logging-utils.log")
        #self.loggerHandler = logging.StreamHandler()
        #create a formatter
        self.loggerFormatter = logging.Formatter("%(asctime)s- %(name)s %(levelname)s: %(message)s")
        #set the formatter to the handler
        self.loggerHandler.setFormatter(self.loggerFormatter)
        #add the handler
        self.logger.addHandler(self.loggerHandler)
        
        # dynamically link to "X Keyboard Extension" library
        library_xf86misc = ctypes.CDLL(ctypes.util.find_library('Xxf86misc'))

        ####################################################################################
        # Parameter defintions
        # define the parameters the function(s) take, and whether they're in, out, or inout.
        # 1 => in, 2=> out, 3=>inout
        ####################################################################################

        #The prototype of the XkbOpenDisplay function may be found here:
        # http://linux.die.net/man/3/xkbopendisplay
        xkbOpenDisplay_params = ((1, 'display_name'), (2, 'event_rtrn'),
            (2, 'error_rtrn'), (3, 'major_in_out'), 
            (3, 'minor_in_out'), (2, 'reason_rtrn'))
        #The prototype of the XkbGetIndicatorState function may be found here:
        # http://linux.die.net/man/3/xkbgetindicatorstate
        xkbGetIndicatorState_params = ((1, 'display'), (1, 'device_spec'),(3, 'state_return'))

        ####################################################################################
        # Prototype defintions        
        #define the prototype; specifying the types of the arguments that should go in and out.
        ####################################################################################
        #define the XkbOpenDisplay prototype
        xkbOpenDisplay_prototype = ctypes.CFUNCTYPE(
                ctypes.c_uint, #return type
                ctypes.c_char_p,#display_name:h/w display name
                ctypes.POINTER(ctypes.c_int),#event_rtrn:backfilled with the extension base event code 
                ctypes.POINTER(ctypes.c_int),#error_rtrn:backfilled with the extension base error code
                ctypes.POINTER(ctypes.c_int),#major_in_out:compile time lib major version in, server major version out
                ctypes.POINTER(ctypes.c_int),#minor_in_out:compile time lib min version in, server minor version out
                ctypes.POINTER(ctypes.c_int))#reason_rtrn:backfilled with a status code 
                                            #(see __errcodes_xkbOpenDisplay to see acceptable values) 
        
        #define the XkbGetIndicatorState prototype
        xkbGetIndicatorState_prototype = ctypes.CFUNCTYPE(
                        ctypes.c_bool,#return type: Will not work in Python 2.5
                        ctypes.c_uint,#display: connection to the X server; obtained using xkbOpenDisplay
                        ctypes.c_uint,#device_spec: device ID, or XkbUseCoreKbd 
                        ctypes.POINTER(ctypes.c_uint))#backfilled with a mask of the indicator state 
        
        ####################################################################################
        # Actual Definitions.
        # Define the actual C functions using low-level wrappers.        
        #This is a hidden method as we want the API to expose
        # the high-level python wrapper that performs type checking etc.
        ####################################################################################
        #define XkbOpenDisplay C function
        self.__XkbOpenDisplay__ = xkbOpenDisplay_prototype(('XkbOpenDisplay', library_xf86misc),
            xkbOpenDisplay_params)
        self.__XkbGetIndicatorState__ = xkbGetIndicatorState_prototype(('XkbGetIndicatorState', 
            library_xf86misc), xkbGetIndicatorState_params)
        
        ####################################################################################
        # Error Checker methods.
        # Add error checkers.        
        ####################################################################################
        self.__XkbOpenDisplay__.errcheck = self.errCheck_openDisplayAndInitXkb
        
        
    ## @brief high-level Python function to encapsulate XkbOpenDisplay(...) function. 
    #
    # Opens a connection to an X server, checks for a compatible version of the Xkb extension 
    #  in both the library and the server, and initializes the extension for use.
    # 
    # The equiv C function's prototype may be found here: http://linux.die.net/man/3/xkbopendisplay
    # Please note that we are using C-style var names to maintain consistency with the C
    # functions it is wrapping. The most important change tothis function is using my TypeChecker
    # decorator to perform type checking, instead of using boilerplate asserts!
    #
    # However, the wrapper function name uses CamelCase with the first letter uncapitalised.
    #
    # @param[in] display_name (NoneType or StringType): The name of the display to connect to.
    # @param[in,out] major_in_out (Int): compile time lib major version in, server major version out
    # @param[in,out] minor_in_out (Int): compile time lib min version in, server minor version out 
    # @date 31/01/2010
    @require(validKwargs = [], display_name = (types.StringType, types.NoneType), major_in_out = types.IntType, minor_in_out = types.IntType) 
    def openDisplayAndInitXkb(self, display_name, major_in_out, minor_in_out):
        self.logger.info("Opening display...")
        # convert function arguments to "ctypes", ...
        __display_name__ = ctypes.c_char_p(display_name)
        __major_in_out__ = ctypes.c_int(major_in_out)
        __minor_in_out__ = ctypes.c_int(minor_in_out)
        
        # ... call low-level function ...
        ret = self.__XkbOpenDisplay__(__display_name__, __major_in_out__, \
                                         __minor_in_out__)
        
        # ... and return converted return value and function arguments
        self.logger.info("...done")
        return {'display_handle': ret[0].value, \
                    'server_major_version': ret[1][3].value, \
                    'server_minor_version': ret[1][4].value}

    ## @brief high-level Python function to encapsulate XkbGetIndicatorStates function. 
    # Obtains the current state of the keyboard indicators 
    # 
    # The equiv C function's prototype may be found here:
    # http://linux.die.net/man/3/xkbgetindicatorstate
    # Please note that we are using C-style var names to maintain consistency with the C
    # functions it is wrapping. The most important change to this function is using my TypeChecker
    # decorator to perform type checking, instead of using boilerplate asserts!
    #
    # However, the wrapper function name uses CamelCase with the first letter uncapitalised.
    #
    # @param[in] display_handle (LongType): The display handler to connect to 
    # (get it using openDisplayAndInitXkb).
    # @param[in] device_spec (Int): The device spec. By default XkbUseCoreKbd
    # (get it using constants_xkb)
    # @retval indicatorMask (ctypes.c_ulong): The indicator mask 
    # (by default on Linux: 1 for Caps Lock on, 2 for Num Lock on)
    # @date 31/01/2010    
    @require(validKwargs = [], display_handle = types.LongType, device_spec = types.IntType)
    def getIndicatorStates(self, display_handle, device_spec):
        self.logger.info("Getting indicator states...")
        # convert function arguments to "ctypes", ...
        __display_handle__ = ctypes.c_uint(display_handle)
        __device_spec__ = ctypes.c_uint(device_spec)
        __state_return = ctypes.c_uint()
        
        # ... call low-level function ...
        indicatorMask = self.__XkbGetIndicatorState__(__display_handle__, __device_spec__, __state_return)
        
        #...and return this value
        self.logger.info("...done")
        return indicatorMask
    
    ## @brief Error checker for openDisplayAndInitXkb.
    #
    # @param[in,out] result 
    # @param[in] func
    # @param[in,out] args 
    # @date 31/01/2010
    def errCheck_openDisplayAndInitXkb(self, result, func, args):
        # print debugging information if requested
        # function didn't return display handle, so let's see why
        # not
        self.logger.debug( '  [XkbOpenDisplay]')
        self.logger.debug( '  Display:       %#010x' % result)
        self.logger.debug( '  display_name:  %s' % args[0].value)
        self.logger.debug( '  event_rtrn:    %d' % args[1].value)
        self.logger.debug( '  error_rtrn:    %d' % args[2].value)
        self.logger.debug( '  major_in_out:  %d' % args[3].value)
        self.logger.debug( '  minor_in_out:  %d' % args[4].value)
        self.logger.debug( '  reason_rt:     %d' % args[5].value)

        #resut should normally be the display; 0 indicates epic fail.
        if result == 0:
            # values were taken from file /usr/include/X11/XKBlib.h (Ubuntu 9.04):
            # $XFree86: xc/lib/X11/XKBlib.h,v 3.5 2003/04/17 02:06:31 dawes Exp $ #
            errorID = args[5].value
            for errorCode in self.__errcodes_xkbOpenDisplay.keys():
                if errorID == self.__errcodes_xkbOpenDisplay[errorCode]:
                    break
            self.logger.debug( "Error code" + errorCode)

            error_message = '"XkbOpenDisplay" reported an error (%s).'%errorCode
            raise OSError(error_message)
        
        # return display handle and all function arguments
        return (ctypes.c_uint(result), args)

    ##@brief Changes logging level and logging handler (optional).
    #
    #@param logLevel (int): logLevel should be a recognised log level.
    #@param handler (logging.handlers): The logging handler. 
    def changeLoggingPreferences(self, logLevel, handler = None):
        self.logger.setLevel(logLevel)
        if handler != None:
            self.logger.removeHandler(self.loggerHandler)
            self.loggerHandler = handler
            self.loggerHandler.setFormatter(self.loggerFormatter)
            self.logger.addHandler(self.loggerHandler)
        
        self.logger.debug("Changed logger level")
    

#test exec
if __name__ == "__main__":
    xkbWrapper = XkbWrapper()

    try:
        ret = xkbWrapper.openDisplayAndInitXkb(None, 1, 0)
    except OSError as osError:
        print osError.args[0]
    
    displayHandle = ret['display_handle']
    
    deviceSpec = xkbWrapper.constants_xkb['XkbUseCoreKbd']
    
    print type(xkbWrapper.getIndicatorStates(displayHandle, deviceSpec))
    
    