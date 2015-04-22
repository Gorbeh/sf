
#   This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 3 of the License, or  (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License along with this program. If not, see <http://www.gnu.org/licenses/>.
#
#   $Id: WindowManager.py 30 2009-04-20 05:16:40Z patryn $
#*****************************************************************************

# -*- coding: utf-8 -*-

import PyQt4
import sys
from PyQt4          import QtGui, QtCore
from Ui_MainWindow  import Ui_MainWindow
from Ui_TableWindow  import Ui_TableWindow
from Ui_PortDialog  import Ui_PortDialog
from Ui_ParamDialog  import Ui_ParamDialog
from Ui_AboutWindow  import Ui_AboutDialog
from Ui_SimSettingsWindow  import Ui_SimSettingsWindow
from CreateOutput   import *
from Common         import *

ROW_ADD, ROW_EDIT = range(2)

#--------------------------------------------------------------------
class WindowManagerClass:
	def __init__(self,  MainWindow):
		self.MainWindow = MainWindow
		self.Settings = DataHolderClass()
		self.WindowIndex = MAIN_WINDOW
		self.Ui = None
		Screen = QtGui.QDesktopWidget().screenGeometry()
		Size =  self.MainWindow.geometry()
		self.MainWindow.move((Screen.width() - Size.width()) / 2, (Screen.height() - Size.height()) / 2)

	def ShowAbout(self):
		AboutDialog = QtGui.QDialog()
		Ui = Ui_AboutDialog()
		Ui.setupUi(AboutDialog)
		AboutDialog.exec_()

	def ShowAboutQt(self):
		QtGui.QMessageBox.aboutQt(None)

	#---------------------- Main Window -------------------
	def CreateMainWindow(self):
		self.Ui.setupUi(self.MainWindow)
		self.Ui.lineEditName.setText(self.Settings.sfunctionName)
		self.Ui.comboBoxSampleTime.addItems(SampleTimesList)
		self.Ui.comboBoxSampleTime.setEditText(self.Settings.sfunctionSampleTime)
		self.Ui.comboBoxOffsetTime.addItems(OffsetTimesList)
		self.Ui.comboBoxOffsetTime.setEditText(self.Settings.sfunctionOffsetTime)
		self.Ui.comboBoxCont.addItems(StatesList)
		self.Ui.comboBoxCont.setEditText(self.Settings.sfunctionContStateNum)
		self.Ui.comboBoxDisc.addItems(StatesList)
		self.Ui.comboBoxDisc.setEditText(self.Settings.sfunctionDiscStateNum)
		QtCore.QObject.connect(self.Ui.pushButtonNext, QtCore.SIGNAL('clicked()'), self.NextWindow)

	def ProcessMainWindowValues(self):
		self.Settings.sfunctionName = self.Ui.lineEditName.text()
		self.Settings.sfunctionSampleTime = self.Ui.comboBoxSampleTime.currentText()
		self.Settings.sfunctionOffsetTime = self.Ui.comboBoxOffsetTime.currentText()
		self.Settings.sfunctionContStateNum = self.Ui.comboBoxCont.currentText()
		self.Settings.sfunctionDiscStateNum = self.Ui.comboBoxDisc.currentText()

		if not IsValidName(self.Settings.sfunctionName):
			QtGui.QMessageBox.critical(self.MainWindow, "Error", "Invalid sfunction Name",	QtGui.QMessageBox.Ok,	QtGui.QMessageBox.Ok)
			return False
		if (not IsValidNumber(self.Settings.sfunctionSampleTime)) and (self.Settings.sfunctionSampleTime not in SampleTimesList):
			QtGui.QMessageBox.critical(self.MainWindow, "Error", "Invalid Sample Time",	QtGui.QMessageBox.Ok,	QtGui.QMessageBox.Ok)
			return False
		if (not IsValidNumber(self.Settings.sfunctionOffsetTime)) and (self.Settings.sfunctionOffsetTime not in OffsetTimesList):
			QtGui.QMessageBox.critical(self.MainWindow, "Error", "Invalid Offset Time",	QtGui.QMessageBox.Ok,	QtGui.QMessageBox.Ok)
			return False
		if (not IsValidNumber(self.Settings.sfunctionContStateNum)) and (self.Settings.sfunctionContStateNum not in StatesList):
			QtGui.QMessageBox.critical(self.MainWindow, "Error", "Invalid number of Continuous States",	QtGui.QMessageBox.Ok,	QtGui.QMessageBox.Ok)
			return False
		if (not IsValidNumber(self.Settings.sfunctionDiscStateNum)) and (self.Settings.sfunctionDiscStateNum not in StatesList):
			QtGui.QMessageBox.critical(self.MainWindow, "Error", "Invalid number of Discrete States",	QtGui.QMessageBox.Ok,	QtGui.QMessageBox.Ok)
			return False
		return True

	#---------------------- Ports, Parameters and PWork Windows -------------------
	def ReadTableRow(self, CurrentRow):
		ValuesList = []
		if(self.WindowIndex == PORTS_WINDOW):
			ValuesList.append(self.Ui.tableWidgetTable.item(CurrentRow,  PORT_NAME_COL).text())
			ValuesList.append(self.Ui.tableWidgetTable.item(CurrentRow,  PORT_DIR_COL).text())
			ValuesList.append(self.Ui.tableWidgetTable.item(CurrentRow,  PORT_TYPE_COL).text())
			ValuesList.append(self.Ui.tableWidgetTable.item(CurrentRow,  PORT_WIDTH_COL).text())
			ValuesList.append(self.Ui.tableWidgetTable.item(CurrentRow,  PORT_COUNT_COL).text())
		if(self.WindowIndex == PARAMS_WINDOW):
			ValuesList.append(self.Ui.tableWidgetTable.item(CurrentRow,  PARAM_NAME_COL).text())
			ValuesList.append(self.Ui.tableWidgetTable.item(CurrentRow,  PARAM_TYPE_COL).text())
			ValuesList.append(self.Ui.tableWidgetTable.item(CurrentRow,  PARAM_MDLINIT).text())
			ValuesList.append(self.Ui.tableWidgetTable.item(CurrentRow,  PARAM_MDLSTART).text())
			ValuesList.append(self.Ui.tableWidgetTable.item(CurrentRow,  PARAM_MDLOUTPUTS).text())
		return ValuesList

	def ShowInputDialog(self):
		InputDialog = QtGui.QDialog()
		if(self.WindowIndex == PORTS_WINDOW):
			self.InputUi = Ui_PortDialog()
			self.InputUi.setupUi(InputDialog)
			self.InputUi.comboBoxDirection.addItems(PortDirectonList)
			self.InputUi.comboBoxType.addItems(PortTypeList)
			if (self.TableAction == ROW_EDIT):
				CurrentRow = self.Ui.tableWidgetTable.currentRow()
				ValuesList = self.ReadTableRow(CurrentRow)
				self.InputUi.lineEditPortName.setText(ValuesList[PORT_NAME_COL])
				self.InputUi.comboBoxDirection.setCurrentIndex(PortDirectonList.index(ValuesList[PORT_DIR_COL]))
				self.InputUi.comboBoxType.setCurrentIndex(PortTypeList.index(ValuesList[PORT_TYPE_COL]))
				self.InputUi.spinBoxWidth.setValue(int(ValuesList[PORT_WIDTH_COL]))
				self.InputUi.spinBoxCount.setValue(int(ValuesList[PORT_COUNT_COL]))
		elif (self.WindowIndex == PARAMS_WINDOW):
			self.InputUi = Ui_ParamDialog()
			self.InputUi.setupUi(InputDialog)
			self.InputUi.comboBoxType.addItems(ParamTypeList)
			if (self.TableAction == ROW_EDIT):
				CurrentRow = self.Ui.tableWidgetTable.currentRow()
				ValuesList = self.ReadTableRow(CurrentRow)
				self.InputUi.lineEditParamName.setText(ValuesList[PARAM_NAME_COL])
				self.InputUi.comboBoxType.setCurrentIndex(ParamTypeList.index(ValuesList[PARAM_TYPE_COL]))
				if (ValuesList[PARAM_MDLINIT] == "Yes"):
					self.InputUi.checkBoxmdlInitializeSizes.setCheckState(QtCore.Qt.Checked)
				else:
					self.InputUi.checkBoxmdlInitializeSizes.setCheckState(QtCore.Qt.Unchecked)
				if (ValuesList[PARAM_MDLSTART] == "Yes"):
					self.InputUi.checkBoxmdlStart.setCheckState(QtCore.Qt.Checked)
				else:
					self.InputUi.checkBoxmdlStart.setCheckState(QtCore.Qt.Unchecked)
				if (ValuesList[PARAM_MDLOUTPUTS] == "Yes"):
					self.InputUi.checkBoxmdlOutputs.setCheckState(QtCore.Qt.Checked)
				else:
					self.InputUi.checkBoxmdlOutputs.setCheckState(QtCore.Qt.Unchecked)

		QtCore.QObject.connect(self.InputUi.buttonBox, QtCore.SIGNAL('accepted()'), self.ItemAdded)
		InputDialog.exec_()

	def TableWindowAddItem(self):
		self.TableAction = ROW_ADD
		self.ShowInputDialog()

	def TableWindowEditItem(self):
		if (self.Ui.tableWidgetTable.currentRow() == -1):
			QtGui.QMessageBox.critical(self.MainWindow, "Error", "Select a row to edit",	QtGui.QMessageBox.Ok,	QtGui.QMessageBox.Ok)
			return
		self.TableAction = ROW_EDIT
		self.ShowInputDialog()

	def TableWindowRemoveItem(self):
		if (self.Ui.tableWidgetTable.currentRow() == -1):
			QtGui.QMessageBox.critical(self.MainWindow, "Error", "Select a row to remove",	QtGui.QMessageBox.Ok,	QtGui.QMessageBox.Ok)
			return
		CurrentRow = self.Ui.tableWidgetTable.currentRow()
		self.Ui.tableWidgetTable.removeRow(CurrentRow)
		self.Ui.tableWidgetTable.setCurrentCell(CurrentRow - 1,  0)

	def ItemMoveUp(self):
		CurrentRow = self.Ui.tableWidgetTable.currentRow()
		if (CurrentRow == -1):
			QtGui.QMessageBox.critical(self.MainWindow, "Error", "Select a row to move up",	QtGui.QMessageBox.Ok,	QtGui.QMessageBox.Ok)
			return
		if(CurrentRow == 0):
			return
		Items = self.ReadTableRow(CurrentRow)
		self.Ui.tableWidgetTable.insertRow(CurrentRow - 1)
		for Index, Item in enumerate(Items):
			self.Ui.tableWidgetTable.setItem(CurrentRow - 1, Index, QtGui.QTableWidgetItem(str(Item)))
		self.Ui.tableWidgetTable.removeRow(CurrentRow + 1)
		self.Ui.tableWidgetTable.setCurrentCell(CurrentRow - 1,  0)

	def ItemMoveDown(self):
		CurrentRow = self.Ui.tableWidgetTable.currentRow()
		if (CurrentRow == -1):
			QtGui.QMessageBox.critical(self.MainWindow, "Error", "Select a row to move down",	QtGui.QMessageBox.Ok,	QtGui.QMessageBox.Ok)
			return
		if(CurrentRow == self.Ui.tableWidgetTable.rowCount() - 1):
			return
		Items = self.ReadTableRow(CurrentRow)
		self.Ui.tableWidgetTable.insertRow(CurrentRow + 2)
		for Index, Item in enumerate(Items):
			self.Ui.tableWidgetTable.setItem(CurrentRow + 2, Index, QtGui.QTableWidgetItem(str(Item)))
		self.Ui.tableWidgetTable.removeRow(CurrentRow)
		self.Ui.tableWidgetTable.setCurrentCell(CurrentRow + 1,  0)

	def ItemAdded(self):
		if(self.WindowIndex == PORTS_WINDOW):
			if not IsValidName(self.InputUi.lineEditPortName.text()):
				QtGui.QMessageBox.critical(self.MainWindow, "Error", "Invalid Port Name",	QtGui.QMessageBox.Ok,	QtGui.QMessageBox.Ok)
				return False
			Port = []
			Port.append(self.InputUi.lineEditPortName.text())
			Port.append(self.InputUi.comboBoxDirection.currentText())
			Port.append(self.InputUi.comboBoxType.currentText())
			Port.append(self.InputUi.spinBoxWidth.value())
			Port.append(self.InputUi.spinBoxCount.value())
			if (self.TableAction == ROW_ADD):
				self.Ui.tableWidgetTable.insertRow(self.Ui.tableWidgetTable.rowCount())
				Row = self.Ui.tableWidgetTable.rowCount() - 1
			else:
				Row = self.Ui.tableWidgetTable.currentRow()
			for Index, Item in enumerate(Port):
				self.Ui.tableWidgetTable.setItem(Row, Index, QtGui.QTableWidgetItem(str(Item)))
		elif(self.WindowIndex == PARAMS_WINDOW):
			if not IsValidName(self.InputUi.lineEditParamName.text()):
				QtGui.QMessageBox.critical(self.MainWindow, "Error", "Invalid Parameter Name",	QtGui.QMessageBox.Ok,	QtGui.QMessageBox.Ok)
				return False
			Param = []
			Param.append(self.InputUi.lineEditParamName.text())
			Param.append(self.InputUi.comboBoxType.currentText())
			if (self.InputUi.checkBoxmdlInitializeSizes.checkState() == 2):
				Param.append("Yes")
			else:
				Param.append("No")
			if (self.InputUi.checkBoxmdlStart.checkState() == 2):
				Param.append("Yes")
			else:
				Param.append("No")
			if (self.InputUi.checkBoxmdlOutputs.checkState() == 2):
				Param.append("Yes")
			else:
				Param.append("No")
			if (self.TableAction == ROW_ADD):
				self.Ui.tableWidgetTable.insertRow(self.Ui.tableWidgetTable.rowCount())
				Row = self.Ui.tableWidgetTable.rowCount() - 1
			else:
				Row = self.Ui.tableWidgetTable.currentRow()
			for Index, Item in enumerate(Param):
				self.Ui.tableWidgetTable.setItem(Row, Index, QtGui.QTableWidgetItem(str(Item)))
		self.Ui.tableWidgetTable.resizeColumnsToContents()

	def CreateTableWindow(self):
		self.Ui.setupUi(self.MainWindow)
		self.Ui.tableWidgetTable.setRowCount(0)
		if(self.WindowIndex == PORTS_WINDOW):
			self.MainWindow.setWindowTitle("Simulink sfunction Generation Wizard - Step 2")
			self.Ui.groupBoxGroup.setTitle("Ports Settings")
			self.Ui.tableWidgetTable.setColumnCount(5)
			self.Ui.tableWidgetTable.setHorizontalHeaderLabels(["Port Name", "Direction", "Type", "Width", "Count"])
			InitList = self.Settings.PortList
		elif (self.WindowIndex == PARAMS_WINDOW):
			self.MainWindow.setWindowTitle("Simulink sfunction Wizard - Step 3")
			self.Ui.groupBoxGroup.setTitle("sfunction Parameters")
			self.Ui.tableWidgetTable.setColumnCount(5)
			self.Ui.tableWidgetTable.setHorizontalHeaderLabels(["Parameter", "Type",  "mdlInitSizes()", "mdlStart()", "mdlOutputs()"])
			InitList = self.Settings.ParamList

		for ListItem in InitList:
			self.Ui.tableWidgetTable.insertRow(self.Ui.tableWidgetTable.rowCount())
			Row = self.Ui.tableWidgetTable.rowCount() - 1
			for Index, Item in enumerate(ListItem):
				self.Ui.tableWidgetTable.setItem(Row, Index, QtGui.QTableWidgetItem(str(Item)))

		self.Ui.tableWidgetTable.resizeColumnsToContents()
		QtCore.QObject.connect(self.Ui.pushButtonNext, QtCore.SIGNAL('clicked()'), self.NextWindow)
		QtCore.QObject.connect(self.Ui.pushButtonBack, QtCore.SIGNAL('clicked()'), self.PreviousWindow)
		QtCore.QObject.connect(self.Ui.pushButtonAdd, QtCore.SIGNAL('clicked()'), self.TableWindowAddItem)
		QtCore.QObject.connect(self.Ui.pushButtonEdit, QtCore.SIGNAL('clicked()'), self.TableWindowEditItem)
		QtCore.QObject.connect(self.Ui.pushButtonRemove, QtCore.SIGNAL('clicked()'), self.TableWindowRemoveItem)
		QtCore.QObject.connect(self.Ui.pushButtonUp, QtCore.SIGNAL('clicked()'), self.ItemMoveUp)
		QtCore.QObject.connect(self.Ui.pushButtonDown, QtCore.SIGNAL('clicked()'), self.ItemMoveDown)

	def ProcessTableValues(self):
		ResultList = []
		for I in range(0, self.Ui.tableWidgetTable.rowCount()):
			PortValues = self.ReadTableRow(I)
			ResultList.append(PortValues)
		if(self.WindowIndex == PORTS_WINDOW):
			self.Settings.PortList = ResultList
		elif (self.WindowIndex == PARAMS_WINDOW):
			self.Settings.ParamList = ResultList
		return True

	#---------------------- Simulation settings Window -------------------
	def CreateSimSettingsWindow(self):
		self.Ui.setupUi(self.MainWindow)
		self.CheckBoxList = []
		self.CheckBoxList.append(self.Ui.checkBoxOpt_1); self.CheckBoxList.append(self.Ui.checkBoxOpt_2); self.CheckBoxList.append(self.Ui.checkBoxOpt_3)
		self.CheckBoxList.append(self.Ui.checkBoxOpt_4); self.CheckBoxList.append(self.Ui.checkBoxOpt_5); self.CheckBoxList.append(self.Ui.checkBoxOpt_6)
		self.CheckBoxList.append(self.Ui.checkBoxOpt_7); self.CheckBoxList.append(self.Ui.checkBoxOpt_8); self.CheckBoxList.append(self.Ui.checkBoxOpt_9)
		self.CheckBoxList.append(self.Ui.checkBoxOpt_10); self.CheckBoxList.append(self.Ui.checkBoxOpt_11); self.CheckBoxList.append(self.Ui.checkBoxOpt_12)
		self.CheckBoxList.append(self.Ui.checkBoxOpt_13); self.CheckBoxList.append(self.Ui.checkBoxOpt_14); self.CheckBoxList.append(self.Ui.checkBoxOpt_15)
		self.CheckBoxList.append(self.Ui.checkBoxOpt_16); self.CheckBoxList.append(self.Ui.checkBoxOpt_17); self.CheckBoxList.append(self.Ui.checkBoxOpt_18)
		self.CheckBoxList.append(self.Ui.checkBoxOpt_19); self.CheckBoxList.append(self.Ui.checkBoxOpt_20); self.CheckBoxList.append(self.Ui.checkBoxOpt_21)
		self.CheckBoxList.append(self.Ui.checkBoxOpt_22)

		for Index, Item in enumerate(self.CheckBoxList):
			 Item.setText(OptionsList[Index])
			 Item.setCheckState(self.Settings.SimSettings[Index])
		QtCore.QObject.connect(self.Ui.pushButtonFinish, QtCore.SIGNAL('clicked()'), self.Finish)
		QtCore.QObject.connect(self.Ui.pushButtonBack, QtCore.SIGNAL('clicked()'), self.PreviousWindow)

	def ProcessSimSettingsValues(self):
		for Index, Item in enumerate(self.CheckBoxList):
			  self.Settings.SimSettings[Index] = Item.checkState()		
		return True

	#---------------------- Generic Window Management -------------------
	def ProcessValues(self):
		if(self.WindowIndex == MAIN_WINDOW):
			return self.ProcessMainWindowValues()
		elif(self.WindowIndex == PORTS_WINDOW) or (self.WindowIndex == PARAMS_WINDOW):
			return self.ProcessTableValues()
		elif(self.WindowIndex == SIMULATION_SETTINGS_WINDOW):
			return self.ProcessSimSettingsValues()

		return True

	def NextWindow(self):
		if not self.ProcessValues():
			return False
		self.WindowIndex = self.WindowIndex + 1
		self.CreateWindow()

	def PreviousWindow(self):
		if not self.ProcessValues():
			return False
		self.WindowIndex = self.WindowIndex - 1
		self.CreateWindow()

	def Finish(self):
		if not self.ProcessValues():
			return False
		CreateFiles(self.Settings)
		QtGui.QMessageBox.information(self.MainWindow, "Done!", "Output files created successfully.",	QtGui.QMessageBox.Ok,	QtGui.QMessageBox.Ok)

	def CreateWindow(self):
		if(self.WindowIndex == MAIN_WINDOW):
			self.Ui=Ui_MainWindow()
			self.CreateMainWindow()
		elif(self.WindowIndex == PORTS_WINDOW) or (self.WindowIndex == PARAMS_WINDOW):
			self.Ui=Ui_TableWindow()
			self.CreateTableWindow()
		elif(self.WindowIndex == SIMULATION_SETTINGS_WINDOW):
			self.Ui=Ui_SimSettingsWindow()
			self.CreateSimSettingsWindow()
		QtCore.QObject.connect(self.Ui.actionAbout, QtCore.SIGNAL('activated()'), self.ShowAbout)
		QtCore.QObject.connect(self.Ui.actionAbout_Qt, QtCore.SIGNAL('activated()'), self.ShowAboutQt)

