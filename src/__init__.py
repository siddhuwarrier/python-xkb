# Copyright (c) 2010 Siddhu Warrier (http://siddhuwarrier.homelinux.org, 
# siddhuwarrier AT gmail DOT com). 
# 
# This file is part of the typeutils package.
# The utils package is free software: you can redistribute it and/or modify
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

##@package xkb
# @defgroup xkb
# @brief Package for wrapping C X Keyboard Function Calls. 
#
# This package was refactored from OSD Neo2 written by Martin Zuther 
# (http://www.mzuther.de/en/contents/osd-neo2) and uses wrapped
# C XKB function calls to check the status of the Caps Lock
# and Num Lock keys. If anybody can think of a better name to give
# this package, please feel free to rename it!! :)
#
# @author Siddhu Warrier (siddhuwarrier@gmail.com)  
# @date 31/01/2010
from XkbWrapper import *