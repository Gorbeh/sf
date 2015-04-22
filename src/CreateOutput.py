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
#   $Id: CreateOutput.py 37 2009-04-28 03:35:07Z patryn $
#******************************************************************************

# -*- coding: utf-8 -*-

from __future__     import with_statement
from PyQt4          import QtGui, QtCore
from Common         import *
import os,sys,re

PARAM_INIT, PARAM_START, PARAM_OUTPUTS= range(3)

#--------------------------------------------------------------------
def CreateSimOptionsString(Settings):
	OptStr = ""
	for Index, Item in enumerate(Settings.SimSettings):
		if (Settings.SimSettings[Index] != QtCore.Qt.Unchecked):
			OptStr =OptStr + OptionsList[Index] + " | "
	if(len(OptStr) == 0):
		return ""
	OptStr = OptStr[0:len(OptStr) - 3]
	Result = "\t//Set the simulation options\n\tssSetOptions(S, " + OptStr + ");"
	return Result

#--------------------------------------------------------------------
def  CreatePortsString(Settings):
	Result = ""
	InPortNum = 0
	OutPortNum = 0
	for Port in Settings.PortList:
		if (Port[PORT_DIR_COL] == "Input"):
			InPortNum = InPortNum + int(Port[PORT_COUNT_COL])
		else:
			OutPortNum = OutPortNum + int(Port[PORT_COUNT_COL])
	Result = "\t//Set up the ports\n\tif (!ssSetNumInputPorts(S, "+ str(InPortNum)+"))\n\t\treturn;\n"
	Result = Result + "\tif (!ssSetNumOutputPorts(S, "+ str(OutPortNum)+"))\n\t\treturn;\n"
	if(InPortNum != 0) or (OutPortNum != 0):
		Result = Result + "\tunsigned int PortIndex = 0;\n"
		for Port in Settings.PortList:
			if(int(Port[PORT_COUNT_COL]) != 1):
				Tabs = "\t\t"
				Result = Result + "\n\tfor(unsigned int I = 0; I < " + Port[PORT_COUNT_COL] + "; I++)\n\t{\n"
			else:
				Tabs = "\t"
				Result = Result + "\n"
			if (Port[PORT_DIR_COL] == "Input"):
				Result = Result + Tabs + "ssSetInputPortWidth(S, PortIndex, " + Port[PORT_WIDTH_COL] + ");\n" + Tabs\
													+ "ssSetInputPortDataType(S, PortIndex, " + Port[PORT_TYPE_COL] + ");\n" + Tabs\
													+ "ssSetInputPortDirectFeedThrough(S, PortIndex , 1);\n" + Tabs\
													+ "ssSetInputPortRequiredContiguous(S, PortIndex, 1);\n"
			else:
				Result = Result + Tabs + "ssSetOutputPortWidth(S, PortIndex, " + Port[PORT_WIDTH_COL] + ");\n" + Tabs\
													+ "ssSetOutputPortDataType(S, PortIndex, " + Port[PORT_TYPE_COL] + ");\n"
			Result = Result + Tabs + "PortIndex++;\n"
			if(int(Port[PORT_COUNT_COL]) != 1):
				Result = Result + "\t}\n"
	return Result

#--------------------------------------------------------------------
def  CreatePortArrayPointersString(Settings):
	if (len(Settings.PortList) == 0):
		return ""
	Result = "//Pointers to the ports\n"
	for Port in Settings.PortList:
		Type = PortCTypeList[PortTypeList.index(Port[PORT_TYPE_COL])]
		Result = Result + "\t" + Type + " *\t" + Port[PORT_NAME_COL]
		if(int(Port[PORT_COUNT_COL]) != 1):
			Result = Result + "[" + Port[PORT_COUNT_COL] + "]"
		Result = Result + ";\n"
	return Result

#--------------------------------------------------------------------
def  CreatePortPointersString(Settings):
	if (len(Settings.PortList) == 0):
		return ""
	Result = "//Port connections\n\tunsigned int PortIndex = 0;\n"
	InPortNum = 0
	OutPortNum = 0
	for Port in Settings.PortList:
		Type = PortCTypeList[PortTypeList.index(Port[PORT_TYPE_COL])]
		Count = int(Port[PORT_COUNT_COL])
		if(Count != 1):
			Tabs = "\t\t"
			Result = Result + "\tfor(unsigned int I = 0; I < " + Port[PORT_COUNT_COL] + "; I++)\n\t{\n"
		else:
			Tabs = "\t"
		Result = Result + Tabs + Port[PORT_NAME_COL]
		if(Count != 1):
			Result = Result + "[I]"
		Result = Result + " = "
		Result = Result + "(" + Type + " *) "
		if (Type != "real_T") and (Type != "real32_T"):
			if (Port[PORT_DIR_COL] == "Input"):
				Result = Result + "ssGetInputPortSignal"
			else:
				Result = Result + "ssGetOutputPortSignal"
		else:
			if (Port[PORT_DIR_COL] == "Input"):
				Result = Result + "ssGetInputPortRealSignal"
			else:
				Result = Result + "ssGetOutputPortRealSignal"
		Result = Result + "(S, PortIndex);\n" + Tabs + "PortIndex++;\n"
		if(Count != 1):
				Result = Result + "\t}\n"
	return Result

#--------------------------------------------------------------------
def CreateParameterIndexString(Settings):
	Result = ""
	for Index, Item in enumerate(Settings.ParamList):
		Result = Result + "#define PARAM_" + str(Item[PARAM_NAME_COL] ).upper() + "\t\t" + str(Index) + "\n"
	return Result

#--------------------------------------------------------------------
def CreateParameterPtrString(Settings, Func):
	Result = ""
	Count = 0
	for Item in Settings.ParamList:
		if (Item[PARAM_MDLINIT + Func]  == "Yes"):
			Count = Count + 1
	if(Count != 0):
		Result = "real_T\t\t*pr;\n"
	return Result

#--------------------------------------------------------------------
def CreateParameterString(Settings, Func):
	Result = ""
	for Index, Item in enumerate(Settings.ParamList):
		if (Item[PARAM_MDLINIT + Func]  == "Yes"):
			if(Result == ""):
				Result = "\t//Parameter setup\n"
			ParamIndex = "PARAM_" + str(Item[PARAM_NAME_COL] ).upper()
			Type = ParamCTypeList[ParamTypeList.index(Item[PARAM_TYPE_COL])]
			if(Type != "char *"):
				Result = Result + "\tpr = mxGetPr(ssGetSFcnParam(S, " + ParamIndex + "));\n"
				Result = Result + "\t" + Type + " " + Item[PARAM_NAME_COL] + " = ("+ Type + ") pr[0];\n"
			else:
				Result = Result + "\t" + Type + " " + Item[PARAM_NAME_COL] + " = mxArrayToString(ssGetSFcnParam(S, " + ParamIndex + "));\n"
	return Result

#--------------------------------------------------------------------
def CreateParameterDelString(Settings, Func):
	Result = ""
	for Item in Settings.ParamList:
		if (Item[PARAM_MDLINIT + Func]  == "Yes"):
			Type = ParamCTypeList[ParamTypeList.index(Item[PARAM_TYPE_COL])]
			if(Type == "char *"):
				if(Result == ""):
					Result = "\t//Freeing memory\n"
				Result = Result + "\tmxFree(" + Item[PARAM_NAME_COL] + ");\n"
	return Result

#--------------------------------------------------------------------
def ProcessToken(Token, Settings):
	if Token == "SFUNCTION_NAME":
		Result = Settings.sfunctionName
	elif Token == "SFUNCTION_CONT_STATE_NUM":
		Result = Settings.sfunctionContStateNum
	elif Token == "SFUNCTION_DISC_STATE_NUM":
		Result = Settings.sfunctionDiscStateNum
	elif Token == "SFUNCTION_SAMPLE_TIME":
		Result = Settings.sfunctionSampleTime
	elif Token == "SFUNCTION_OFFSET_TIME":
		Result = Settings.sfunctionOffsetTime
	elif Token == "SFUNCTION_PARAM_NUM":
		Result = str(len(Settings.ParamList))
	elif Token == "SFUNCTION_PWORK_LENGTH":
		Result = Settings.sfunctionPWorkLength
	elif Token == "SET_SIMULATION_OPTIONS":
		Result = CreateSimOptionsString(Settings)
	elif Token == "SET_PORTS":
		Result = CreatePortsString(Settings)
	elif Token == "SET_PORT_ARRAY_POINTERS":
		Result = CreatePortArrayPointersString(Settings)
	elif Token == "SET_PORT_POINTERS":
		Result = CreatePortPointersString(Settings)
	elif Token == "PARAMETER_INDEX_SETUP":
		Result = CreateParameterIndexString(Settings)
	elif Token == "PARAM_PTR_DEFINE_INIT":
		Result = CreateParameterPtrString(Settings, PARAM_INIT)
	elif Token == "PARAM_PTR_DEFINE_START":
		Result = CreateParameterPtrString(Settings, PARAM_START)
	elif Token == "PARAM_PTR_DEFINE_OUTPUTS":
		Result = CreateParameterPtrString(Settings, PARAM_OUTPUTS)
	elif Token == "PARAMETER_SETUP_INIT":
		Result = CreateParameterString(Settings, PARAM_INIT)
	elif Token == "PARAMETER_SETUP_START":
		Result = CreateParameterString(Settings, PARAM_START)
	elif Token == "PARAMETER_SETUP_OUTPUTS":
		Result = CreateParameterString(Settings, PARAM_OUTPUTS)
	elif Token == "PARAMETER_DEL_INIT":
		Result = CreateParameterDelString(Settings, PARAM_INIT)
	elif Token == "PARAMETER_DEL_START":
		Result = CreateParameterDelString(Settings, PARAM_START)
	elif Token == "PARAMETER_DEL_OUTPUTS":
		Result = CreateParameterDelString(Settings, PARAM_OUTPUTS)
	else:
		Result = Token
	return Result

#--------------------------------------------------------------------
def CreateOutput(InputFileName, OutputFileName, Settings):
	OutputFile = open(OutputFileName,"w")
	with open(InputFileName, "r") as InputFile:
		for Line in InputFile:
			Portions = Line.split("$")
			for Portion in Portions:
				if Portion in TokenList:
					Result = ProcessToken(Portion, Settings)
				else:
					Result = Portion
				OutputFile.write(Result)

	OutputFile.close()

#--------------------------------------------------------------------
def CreateFiles(Settings):
	if not os.path.exists("Output"):
		os.makedirs("Output")
	CreateOutput("Templates/Template.h", "Output/" + Settings.sfunctionName + ".h", Settings)
	CreateOutput("Templates/Template.cpp", "Output/" + Settings.sfunctionName + ".cpp", Settings)
