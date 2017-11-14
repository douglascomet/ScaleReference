#==============================================================================
#!/usr/bin/env python
#title           :ScaleReferenceQT.py
#description     :Python script for Maya to create a reference bounding box based on designated units
#author          :Doug Halley
#date            :20171114
#version         :3.0
#usage           :
#notes           :
#python_version  :2.7.14
#pyqt_version    :4.11.4
#==============================================================================

import sys
import math
from maya import cmds as cmds
from maya import OpenMaya as om
from functools import partial

#import Qt
from Qt import QtWidgets
from Qt import QtCore
from Qt import QtGui

class Scale_Reference(QtWidgets.QMainWindow):
    def __init__(self, parent = None):
        super(Scale_Reference, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Scale Reference")

        """
        Label for Scene Units
        """
        sceneUnits_lbl_layout = QtWidgets.QHBoxLayout()

        sceneUnits_lbl = QtWidgets.QLabel("Scene's Units:")
        sceneUnits_lbl.setAlignment(QtCore.Qt.AlignCenter)

        units_lbl = QtWidgets.QLabel("Scene's Units:")
        units_lbl.setAlignment(QtCore.Qt.AlignCenter)

        sceneUnits_lbl_layout.layout().addWidget(sceneUnits_lbl)
        sceneUnits_lbl_layout.layout().addWidget(units_lbl)

        """
        User selected Units combobox Layout
        """
        unitsCombobox_btn_layout = QtWidgets.QHBoxLayout()

        unitsCombobox_lbl = QtWidgets.QLabel("Convert Units To:")
        units_comboBox = QtWidgets.QComboBox()

        for x in ['cm', 'mm', 'm', 'km', 'in', 'ft', 'yd', 'mi']:
            units_comboBox.addItem(x)

        unitsCombobox_btn_layout.layout().addWidget(unitsCombobox_lbl)
        unitsCombobox_btn_layout.layout().addWidget(units_comboBox)

        """
        Prefix Line Edit Layout
        """
        scalePrefix_layout = QtWidgets.QHBoxLayout()

        scalePrefix_lbl = QtWidgets.QLabel("Reference Prefix:")
        self.scalePrefix_le = QtWidgets.QLineEdit("")

        scalePrefix_layout.layout().addWidget(scalePrefix_lbl)
        scalePrefix_layout.layout().addWidget(self.scalePrefix_le)

        """
        Dimension Line Edits Layout
        """
        dimensionsList = self.dimensionLayouts()
        dimensions_layout = QtWidgets.QVBoxLayout()
        dimensions_layout.layout().addLayout(dimensionsList[0])
        dimensions_layout.layout().addLayout(dimensionsList[1])
        dimensions_layout.layout().addLayout(dimensionsList[2])

        """
        Buttons Layout
        """
        buttonLayout = QtWidgets.QVBoxLayout()
        self.create_btn = QtWidgets.QPushButton("Create New Reference")
        self.delete_btn = QtWidgets.QPushButton("Delete Named Reference")

        buttonLayout.layout().addWidget(self.create_btn)
        buttonLayout.layout().addWidget(self.delete_btn)
        
        """
        Central Widget
        """
        self.centralWidget = QtWidgets.QWidget()
        self.centralWidget.setLayout(QtWidgets.QVBoxLayout())
        self.centralWidget.layout().addLayout(sceneUnits_lbl_layout)
        self.centralWidget.layout().addLayout(unitsCombobox_btn_layout)

        self.centralWidget.layout().addLayout(scalePrefix_layout)
        self.centralWidget.layout().addLayout(dimensions_layout)
        self.centralWidget.layout().addLayout(buttonLayout)

        # set central widget
        self.setCentralWidget(self.centralWidget)

        self.create_btn.clicked.connect(lambda: self.create3DD(units_comboBox.currentText()))
        self.delete_btn.clicked.connect(
            lambda: self.deleteDimension())
        

        self.width_le.textChanged.connect(lambda: self.checkLineEditState(self.width_le))
        self.width_le.textChanged.emit(self.width_le.text())

        self.length_le.textChanged.connect(lambda: self.checkLineEditState(self.length_le))
        self.length_le.textChanged.emit(self.length_le.text())

        self.height_le.textChanged.connect(lambda: self.checkLineEditState(self.height_le))
        self.height_le.textChanged.emit(self.height_le.text())

    def dimensionLayouts(self):
        
        width_le_layout = QtWidgets.QHBoxLayout()
        height_le_layout = QtWidgets.QHBoxLayout()
        length_le_layout = QtWidgets.QHBoxLayout()
        upAxis = cmds.upAxis(q = True, axis = True)

        if upAxis == 'y':
            width_lbl = QtWidgets.QLabel("Width (X): ")
            self.width_le = QtWidgets.QLineEdit("")

            height_lbl = QtWidgets.QLabel("Height (Y): ")
            self.height_le = QtWidgets.QLineEdit("")

            length_lbl = QtWidgets.QLabel("Length (Z): ")
            self.length_le = QtWidgets.QLineEdit("")

            width_le_layout.layout().addWidget(width_lbl)
            width_le_layout.layout().addWidget(self.width_le)

            height_le_layout.layout().addWidget(height_lbl)
            height_le_layout.layout().addWidget(self.height_le)

            length_le_layout.layout().addWidget(length_lbl)
            length_le_layout.layout().addWidget(self.length_le)

            layoutList = (width_le_layout, height_le_layout, length_le_layout)

        elif upAxis == 'z':
            width_lbl = QtWidgets.QLabel("Width (X): ")
            self.width_le = QtWidgets.QLineEdit("")

            length_lbl = QtWidgets.QLabel("Length (Y): ")
            self.length_le = QtWidgets.QLineEdit("")

            height_lbl = QtWidgets.QLabel("Height (Z): ")
            self.height_le = QtWidgets.QLineEdit("")

            width_le_layout.layout().addWidget(width_lbl)
            width_le_layout.layout().addWidget(self.width_le)

            length_le_layout.layout().addWidget(length_lbl)
            length_le_layout.layout().addWidget(self.length_le)

            height_le_layout.layout().addWidget(height_lbl)
            height_le_layout.layout().addWidget(self.height_le)

            layoutList = (width_le_layout, length_le_layout, height_le_layout)

        doubleValidator = QtGui.QDoubleValidator()
        doubleValidator.setDecimals(3)
        doubleValidator.setNotation(QtGui.QDoubleValidator.StandardNotation)

        self.width_le.setValidator(doubleValidator)
        self.length_le.setValidator(doubleValidator)
        self.height_le.setValidator(doubleValidator)

        return layoutList

    def checkLineEditState(self, lineEdit):
        sender = lineEdit
        validator = sender.validator()
        state = validator.validate(sender.text(), 0)[0]
        if state == QtGui.QValidator.Acceptable:
            fontColor = '#000000' # black
            bgColor = '#c4df9b' # green
            sender.setStyleSheet('QLineEdit { color: %s; background-color: %s }' % (fontColor, bgColor))
        elif sender.text() == "":
            sender.setStyleSheet('')
        """
        elif state == QtGui.QValidator.Intermediate:
            color = '#fff79a' # yellow
        elif state == QtGui.QValidator.Invalid:
            color = '#f6989d' # red
        """

    def popupOkWindow(self, message):

        popupWindow = QtWidgets.QMessageBox()
        
        popupWindow.setText(str(message))
        popupWindow.setStandardButtons(QtWidgets.QMessageBox.Ok)

        popupWindow.exec_()

    def popupYesNoWindow(self, message):
        msg = QtGui.QMessageBox()

        msg.setText(message)
        #msg.setWindowTitle("MessageBox demo")
        #msg.setDetailedText("The details are as follows:")
        msg.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)

        result = msg.exec_()

        if result == QtWidgets.QMessageBox.Yes:
            return True
        elif result == QtWidgets.QMessageBox.No:
            return False

    def create3DD(self, item):
        unit = cmds.currentUnit(query=True, linear=True)
        dimens = ('length', 'width', 'height')
        
        grpName = self.scalePrefix_le.text()
        lenVal = float(self.length_le.text())
        widVal = float(self.width_le.text())
        heiVal = float(self.height_le.text())
        
        if grpName == '':
            self.popupOkWindow('A name was not entered')
        elif cmds.objExists(str(grpName) + '_refDistance_grp'):
            self.popupOkWindow(str(grpName) + '_refDistance_grp' + ' already exists.\nRename the new group or delete the one that already exists')
        else:     
            if (lenVal is None or lenVal == 0.0 or widVal is None or widVal == 0.0 or heiVal is None or heiVal == 0.0):
                self.popupOkWindow('Distance Values cannot be Zero')       
            else:  
                curItem = item
                  
                if  unit != curItem :  
                    upOrDown = cmds.confirmDialog( title='Converersion Direction?', message='Convert up from ' + str(unit) + ' to ' + str(curItem) + '\nOR\n' + 'Convert down from ' + str(curItem) + ' to '  + str(unit) + '?', button=['Up', 'Down'], defaultButton='Up', dismissString='Down')
                    
                    if upOrDown == "Up":    
                        unitConvLen = cmds.convertUnit( str(lenVal), fromUnit = curItem, toUnit= unit )
                        unitConvWid = cmds.convertUnit( str(widVal), fromUnit = curItem, toUnit= unit )
                        unitConvHei = cmds.convertUnit( str(heiVal), fromUnit = curItem, toUnit= unit )
                    elif upOrDown == "Down":
                        unitConvLen = cmds.convertUnit( str(lenVal), fromUnit = unit, toUnit= curItem )
                        unitConvWid = cmds.convertUnit( str(widVal), fromUnit = unit, toUnit= curItem )
                        unitConvHei = cmds.convertUnit( str(heiVal), fromUnit = unit, toUnit= curItem )
                    
                    tempStrLen = unitConvLen.split(curItem)
                    tempStrWid = unitConvWid.split(curItem)
                    tempStrHei = unitConvHei.split(curItem)
                    
                    lenVal = float(tempStrLen[0])
                    widVal = float(tempStrWid[0])
                    heiVal = float(tempStrHei[0])
                    
                    #Test Case: if values after conversion are too small to be used in current scene
                    if lenVal < .1 or widVal < .1 or heiVal < .1:
                        cmds.confirmDialog( title='Confirm', message = 'Values are too small to use ' + str(curItem) + '\'s while in a scene using ' + str(unit) + '\'s.\nPlease Rerun Script with new parameters.', button=['OK'], defaultButton='OK')
                        cmds.refresh()
                        return
                
                for dimen in dimens:
                    tuplStart = ()
                    tuplEnd = ()
                    
                    if dimen == 'length':
                        tuplStart = (lenVal)/2.0, 0, 0
                        tuplEnd = -(lenVal)/2.0, 0, 0
                    elif dimen == 'width':
                        tuplStart = 0, 0, (widVal)/2.0
                        tuplEnd = 0, 0, -((widVal)/2.0)
                    elif dimen == 'height':
                        tuplStart = 0, (heiVal)/2.0, 0
                        tuplEnd = 0, -((heiVal)/2.0), 0

                    #create Length Locators
                    startDimen = cmds.spaceLocator(n = str(grpName) + '_start' + dimen + '_loc_01', p = tuplStart)
                    endDimen = cmds.spaceLocator(n = str(grpName) + '_end' + dimen + '_loc_01', p = tuplEnd)
                
                    #create length distanceDimension at generic 3d point to be repurposed
                    cmds.distanceDimension( startPoint = [1,1,1], endPoint = [0,0,0] )
                    
                    #rename default distanceDimension locators' transform and shape
                    tempLoc1 = cmds.rename( 'locator1', 'tempLoc_01' )  
                    tempRel1 = cmds.listRelatives(tempLoc1)
                    locName1 = cmds.rename(tempRel1, tempLoc1 + 'Shape' )
                    
                    tempLoc2 = cmds.rename( 'locator2', 'tempLoc_02' )
                    tempRel2 = cmds.listRelatives(tempLoc2)
                    locName2 = cmds.rename(tempRel2, tempLoc2 + 'Shape' )
                    
                    #rename distanceDimension Node
                    distDimen = cmds.rename( 'distanceDimension1', str(grpName) + '_dist' + dimen + '_01' )
                    tempRel = cmds.listRelatives(distDimen)
                    cmds.rename(tempRel, distDimen + 'Shape' )
                
                    #disconnect default distanceDimension locator and distanceDimension Node
                    cmds.disconnectAttr(str(locName1) + '.worldPosition', str(distDimen) + 'Shape' + '.startPoint')
                    cmds.disconnectAttr(str(locName2) + '.worldPosition', str(distDimen) + 'Shape' + '.endPoint')

                    #connect new Locators to distanceDimension Node
                    cmds.connectAttr(startDimen[0] + 'Shape.worldPosition', str(distDimen) + 'Shape' + '.startPoint')
                    cmds.connectAttr(endDimen[0] + 'Shape.worldPosition', str(distDimen) + 'Shape' + '.endPoint')
                    
                    #delete default Locators
                    cmds.delete(tempLoc1, tempLoc2)
                    
                    if dimen == 'length':
                            #group Lenth distanceDimension objects
                            lenGrp = cmds.group( startDimen, endDimen, distDimen, n = str(grpName) + '_' + dimen + 'Dist_grp' )
                            self.colorOveride(13, startDimen, endDimen, distDimen)              
                    elif dimen == 'width':
                            widGrp = cmds.group( startDimen, endDimen, distDimen, n = str(grpName) + '_' + dimen + 'Dist_grp' )
                            self.colorOveride(6, startDimen, endDimen, distDimen)
                    elif dimen == 'height':
                            heiGrp = cmds.group( startDimen, endDimen, distDimen, n = str(grpName) + '_' + dimen + 'Dist_grp' )
                            self.colorOveride(14, startDimen, endDimen, distDimen)

                cmds.group( lenGrp, widGrp, heiGrp, n = str(grpName) + '_refDistance_grp' )

    def colorOveride(self, index, *args):
        """
        @params: index - color index
        @params: different locators and distanceNodes
        
        enables color Override to corresponding axis
        """
        
        for x in args:
            if 'dist' in x:
                cmds.setAttr(str(x) + ".overrideEnabled",1)
                cmds.setAttr(str(x) + ".overrideColor", index)
            else:
                cmds.setAttr(x[0] + ".overrideEnabled",1)
                cmds.setAttr(x[0] + ".overrideColor", index)

    def deleteDimension(self, *args):
        grpName = self.scalePrefix_le.text()
        
        #test case if reference Name textField is empty 
        if grpName == '':
            self.popupOkWindow('A name was not entered')
        elif cmds.objExists(str(grpName) + '_refDistance_grp'):
            cmds.delete(str(grpName) + '_refDistance_grp')
        else:
            self.popupOkWindow(
                str(grpName) + '_refDistance_grp' + 'does not exist')

main_window = [o for o in QtWidgets.qApp.topLevelWidgets() if o.objectName()=="MayaWindow"][0]

mw = Scale_Reference(main_window)
mw.show()
