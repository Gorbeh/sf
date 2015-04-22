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
#   $Id: Common.py 31 2009-04-22 00:55:19Z patryn $
#*****************************************************************************

# -*- coding: utf-8 -*-

from PyQt4          import QtGui, QtCore
import string

SampleTimesList = ["CONTINUOUS_SAMPLE_TIME",  "INHERITED_SAMPLE_TIME", "VARIABLE_SAMPLE_TIME"]
OffsetTimesList = ["0.0",  "FIXED_IN_MINOR_STEP_OFFSET"]
StatesList = ["0",  "DYNAMICALLY_SIZED"]
PortDirectonList = ["Input", "Output"]
PortTypeList = ["SS_DOUBLE", "SS_SINGLE", "SS_INT8", "SS_UINT8", "SS_INT16", "SS_UINT16",
					    "SS_INT32", "SS_UINT32", "SS_BOOLEAN"]
PortCTypeList = ["real_T", "real32_T", "int8_T", "uint8_T", "int16_T", "uint16_T", "int32_T", "uint32_T", "boolean_T"]
ParamTypeList = PortTypeList
ParamTypeList.extend(["String"])
ParamCTypeList = PortCTypeList
ParamCTypeList.extend(["char *"])
TokenList = ["SFUNCTION_NAME", "SFUNCTION_CONT_STATE_NUM", "SFUNCTION_DISC_STATE_NUM",
				   "SFUNCTION_SAMPLE_TIME", "SFUNCTION_OFFSET_TIME", "SFUNCTION_PARAM_NUM",
				   "SFUNCTION_PWORK_LENGTH", "SET_PORTS", "PARAMETER_INDEX_SETUP", "PWORK_INDEX_SETUP",
				   "SET_SIMULATION_OPTIONS",  "SET_PORT_ARRAY_POINTERS",  "SET_PORT_POINTERS", 
				   "PARAMETER_SETUP_INIT", "PARAMETER_SETUP_START", "PARAMETER_SETUP_OUTPUTS",
				   "PARAMETER_DEL_INIT", "PARAMETER_DEL_START", "PARAMETER_DEL_OUTPUTS",
				   "PARAM_PTR_DEFINE_INIT", "PARAM_PTR_DEFINE_START", "PARAM_PTR_DEFINE_OUTPUTS"]
				   
OptionsList = ["SS_OPTION_ALLOW_CONSTANT_PORT_SAMPLE_TIME"		  ,  "SS_OPTION_ALLOW_INPUT_SCALAR_EXPANSION",
					 "SS_OPTION_ALLOW_PARTIAL_DIMENSIONS_CALL"	  ,  "SS_OPTION_ALLOW_PORT_SAMPLE_TIME_IN_TRIGSS",
					 "SS_OPTION_ASYNC_RATE_TRANSITION"			  ,  "SS_OPTION_ASYNCHRONOUS",
					 "SS_OPTION_CALL_TERMINATE_ON_EXIT"			  ,  "SS_OPTION_CAN_BE_CALLED_CONDITIONALLY",
					 "SS_OPTION_DISALLOW_CONSTANT_SAMPLE_TIME"	  ,  "SS_OPTION_DISCRETE_VALUED_OUTPUT",
					 "SS_OPTION_EXCEPTION_FREE_CODE"			  , "SS_OPTION_FORCE_NONINLINED_FCNCALL",
					 "SS_OPTION_NONVOLATILE"					  ,  "SS_OPTION_PLACE_ASAP",
					 "SS_OPTION_PORT_SAMPLE_TIMES_ASSIGNED"		  ,  "SS_OPTION_REQ_INPUT_SAMPLE_TIME_MATCH",
					 "SS_OPTION_RUNTIME_EXCEPTION_FREE_CODE"	  ,  "SS_OPTION_SIM_VIEWING_DEVICE",
					 "SS_OPTION_SFUNCTION_INLINED_FOR_RTW"		  ,  "SS_OPTION_SUPPORTS_ALIAS_DATA_TYPES",
					 "SS_OPTION_USE_TLC_WITH_ACCELERATOR"		  ,  "SS_OPTION_WORKS_WITH_CODE_REUSE"]

MAIN_WINDOW, PORTS_WINDOW, PARAMS_WINDOW,  SIMULATION_SETTINGS_WINDOW = range(4)
PORT_NAME_COL, PORT_DIR_COL, PORT_TYPE_COL, PORT_WIDTH_COL, PORT_COUNT_COL = range(5)
PARAM_NAME_COL, PARAM_TYPE_COL, PARAM_MDLINIT, PARAM_MDLSTART, PARAM_MDLOUTPUTS = range(5)

#--------------------------------------------------------------------
class DataHolderClass():
	def __init__(self):
		self.sfunctionName			= ""
		self.sfunctionSampleTime 	= "INHERITED_SAMPLE_TIME"
		self.sfunctionOffsetTime 	= "0.0"
		self.sfunctionContStateNum	= "0"
		self.sfunctionDiscStateNum	= "0"
		self.sfunctionPWorkLength	= "0"
		self.PortList				= []
		self.ParamList				= []
		self.SimSettings			= []
		for I in range (0, 22):
			self.SimSettings.append(QtCore.Qt.Unchecked)

#--------------------------------------------------------------------
def IsValidName(Name):
	Str = str(Name)
	if (Str == ""):
		return False
	if (not Str[0].isalpha() and Str[0] != "_") :
		return False
	Str = Str.replace("_", "")
	if  not Str.isalnum() :
		return False
	return True

#--------------------------------------------------------------------
def IsValidNumber(Number):
	Str = str(Number)
	if (Str == ""):
		return False
	Str = Str.replace("+", "")
	Str = Str.replace(".", "")
	if  not Str.isdigit() :
		return False
	return True
