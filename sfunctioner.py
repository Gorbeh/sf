#******************************************************************************
#   This file is part of sfunctioner project
#   Copyright (C) 2009 Alireza Pouladi
#
#   This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 3 of the License, or  (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License along with this program. If not, see <http://www.gnu.org/licenses/>.
#
#   $Id: sfunctioner.py 27 2009-04-17 04:28:47Z patryn $
#******************************************************************************

# -*- coding: utf-8 -*-

import PyQt4
import sys
from PyQt4          				import QtGui, QtCore
sys.path.append('.src/')
#sys.path.append('.resources/')
from src.WindowManager 	import *

#--------------------------------------------------------------------
class MainWindowClass(QtGui.QMainWindow):
	def __init__(self, WinParent = None):
		QtGui.QMainWindow.__init__(self, WinParent)

#--------------------------------------------------------------------
if __name__ == "__main__":
	App = QtGui.QApplication(sys.argv)
	MainWindow = MainWindowClass()
	WindowManager = WindowManagerClass(MainWindow)
	WindowManager.CreateWindow()
	MainWindow.show()
	sys.exit(App.exec_())
