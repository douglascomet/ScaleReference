"""
# ==============================================================================
# !/usr/bin/env python
# title           :ScaleReferenceQT.py
# description     :Python script for Maya to create a reference bounding box
#                  based on designated units
# author          :Doug Halley
# date            :20171114
# version         :3.0
# usage           :
# notes           :
# python_version  :2.7.14
# pyqt_version    :4.11.4
# ==============================================================================
"""

from maya import cmds

# import Qt.py packages
from Qt import QtWidgets
from Qt import QtCore
from Qt import QtGui

class ScaleReference(QtWidgets.QMainWindow):
    """Class that creates QtWidget and executes functionality.

    This class is meant to create a length, width, and height distance measurement
    tools to display in Maya and be used as a scale reference.
    """

    def __init__(self, parent=None):
        super(ScaleReference, self).__init__(parent)
        self.init_ui()

    def init_ui(self):
        """Logic to create QtWidget's UI.

        """

        self.setWindowTitle("Scale Reference")

        # Label for Scene Units -----------------------------------------------

        scene_units_lbl_layout = QtWidgets.QHBoxLayout()

        scene_units_lbl = QtWidgets.QLabel("Scene's Units:")
        scene_units_lbl.setAlignment(QtCore.Qt.AlignCenter)

        self.current_maya_unit = cmds.currentUnit(query=True, linear=True)

        units_lbl = QtWidgets.QLabel(self.current_maya_unit)
        units_lbl.setAlignment(QtCore.Qt.AlignCenter)

        scene_units_lbl_layout.layout().addWidget(scene_units_lbl)
        scene_units_lbl_layout.layout().addWidget(units_lbl)

        # User selected Units combobox Layout ----------------------------------

        units_combobox_btn_layout = QtWidgets.QHBoxLayout()

        units_combobox_lbl = QtWidgets.QLabel("Convert Units To:")
        units_combobox = QtWidgets.QComboBox()

        for unit in ['cm', 'mm', 'm', 'km', 'in', 'ft', 'yd', 'mi']:
            units_combobox.addItem(unit)

        units_combobox_btn_layout.layout().addWidget(units_combobox_lbl)
        units_combobox_btn_layout.layout().addWidget(units_combobox)

        # Prefix Line Edit Layout ----------------------------------------------

        scale_prefix_layout = QtWidgets.QHBoxLayout()

        scale_prefix_lbl = QtWidgets.QLabel("Reference Prefix:")
        self.scale_prefix_le = QtWidgets.QLineEdit("")

        scale_prefix_layout.layout().addWidget(scale_prefix_lbl)
        scale_prefix_layout.layout().addWidget(self.scale_prefix_le)

        # Dimension Line Edits Layout ------------------------------------------

        self.length_le = QtWidgets.QLineEdit("")

        self.width_le = QtWidgets.QLineEdit("")

        self.height_le = QtWidgets.QLineEdit("")

        dimensions_form_layout = self.create_dimension_layouts(
            self.length_le, self.width_le, self.height_le)

        # Buttons Layout -------------------------------------------------------

        button_layout = QtWidgets.QVBoxLayout()
        self.create_btn = QtWidgets.QPushButton("Create New Reference")
        self.delete_btn = QtWidgets.QPushButton("Delete Named Reference")

        button_layout.layout().addWidget(self.create_btn)
        button_layout.layout().addWidget(self.delete_btn)

        # Central Widget -------------------------------------------------------

        self.central_widget = QtWidgets.QWidget()
        self.central_widget.setLayout(QtWidgets.QVBoxLayout())
        self.central_widget.layout().addLayout(scene_units_lbl_layout)
        self.central_widget.layout().addLayout(units_combobox_btn_layout)

        self.central_widget.layout().addLayout(scale_prefix_layout)
        self.central_widget.layout().addLayout(dimensions_form_layout)
        self.central_widget.layout().addLayout(button_layout)

        # set central widget
        self.setCentralWidget(self.central_widget)

        # =======================================================================
        # PyQt Execution Connections
        # =======================================================================

        self.create_btn.clicked.connect(
            lambda: self.create_dimension_grp(units_combobox.currentText()))

        self.delete_btn.clicked.connect(lambda: self.delete_dimension_grp())

        self.width_le.textChanged.connect(lambda: self.check_line_edit_state(self.width_le))
        self.width_le.textChanged.emit(self.width_le.text())

        self.length_le.textChanged.connect(lambda: self.check_line_edit_state(self.length_le))
        self.length_le.textChanged.emit(self.length_le.text())

        self.height_le.textChanged.connect(lambda: self.check_line_edit_state(self.height_le))
        self.height_le.textChanged.emit(self.height_le.text())

    def create_dimension_layouts(self, length_le, width_le, height_le):
        """Creates custom layout that contains the length, width, and height QLineEdits

        If Maya scene is Y or Z up the length, width, and height QLineEdits will be arranged
        differently. Validator is also set for each QLineEdit.

        Returns:
            tuple -- returns layouts with QLabels and QLineEdits
        """

        dimension_form_layout = QtWidgets.QFormLayout()

        up_axis = cmds.upAxis(q=True, axis=True)

        if up_axis == 'y':
            dimension_form_layout.addRow("Width (X): ", width_le)

            dimension_form_layout.addRow("Height (Y): ", height_le)

            dimension_form_layout.addRow("Length (Z): ", length_le)

        elif up_axis == 'z':

            dimension_form_layout.addRow("Width (X): ", width_le)

            dimension_form_layout.addRow("Length (Y): ", length_le)

            dimension_form_layout.addRow("Height (Z): ", height_le)

        double_validator = QtGui.QDoubleValidator()
        double_validator.setDecimals(3)
        double_validator.setNotation(QtGui.QDoubleValidator.StandardNotation)

        width_le.setValidator(double_validator)
        length_le.setValidator(double_validator)
        height_le.setValidator(double_validator)

        return dimension_form_layout

    @classmethod
    def check_line_edit_state(cls, line_edit):
        """Changes Stylesheet of input line edit.

        Validator checks state of line edit and changes line edit's font
        and background for visual confirmation that line edit input is acceptable.

        Arguments:
            line_edit {QLineEdit} -- Input QLineEdit to analyze.
        """

        sender = line_edit
        validator = sender.validator()
        state = validator.validate(sender.text(), 0)[0]
        if state == QtGui.QValidator.Acceptable:
            font_color = '#000000' # black
            bg_color = '#c4df9b' # green
            sender.setStyleSheet('QLineEdit { color: %s; background-color: %s }' \
                % (font_color, bg_color))
        elif sender.text() == "":
            sender.setStyleSheet('')
        """
        elif state == QtGui.QValidator.Intermediate:
            color = '#fff79a' # yellow
        elif state == QtGui.QValidator.Invalid:
            color = '#f6989d' # red
        """

    @classmethod
    def popup_ok_window(cls, message):
        """Popup Ok message box to display information to user.

        Arguments:
            message {str} -- Input string for QMessageBox to display.
        """

        popup_window = QtWidgets.QMessageBox()

        popup_window.setText(str(message))
        popup_window.setStandardButtons(QtWidgets.QMessageBox.Ok)

        popup_window.exec_()

    @classmethod
    def popup_yes_no_window(cls, message):
        """Popup Ok message box to display information to user.

        Arguments:
            message {str} -- Input string for QMessageBox to display.

        Returns:
            bool -- Returns True if Yes or False if No
        """

        msg = QtWidgets.QMessageBox()

        msg.setText(message)
        #msg.setWindowTitle("MessageBox demo")
        #msg.setDetailedText("The details are as follows:")
        msg.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)

        result = msg.exec_()

        if result == QtWidgets.QMessageBox.Yes:
            return True
        elif result == QtWidgets.QMessageBox.No:
            return False

    @classmethod
    def popup_up_down_window(cls, message):
        """Popup Ok message box to display information to user.

        Arguments:
            message {str} -- Input string for QMessageBox to display.

        Returns:
            bool -- Returns True if Yes or False if No
        """

        msg = QtWidgets.QMessageBox()

        msg.setText(message)
        #msg.setWindowTitle("MessageBox demo")
        #msg.setDetailedText("The details are as follows:")
        msg.addButton("Up", QtWidgets.QMessageBox.YesRole)
        msg.addButton("Down", QtWidgets.QMessageBox.NoRole)

        result = msg.exec_()

        if result == QtWidgets.QMessageBox.Yes:
            return True
        elif result == QtWidgets.QMessageBox.No:
            return False

    def create_dimension_grp(self, target_unit):
        """Create Dimension Group for a reference of scale.

        Dimension Group is a set of 3 custom distance measurements to represent
        length, width, and height.

        Arguments:
            item {[type]} -- [description]
        """

        dimens = ('length', 'width', 'height')

        grp_name = self.scale_prefix_le.text()
        len_value = float(self.length_le.text())
        width_value = float(self.width_le.text())
        height_val = float(self.height_le.text())

        if grp_name == '':
            self.popup_ok_window('A name was not entered')

        elif cmds.objExists(str(grp_name) + '_refDistance_grp'):

            self.popup_ok_window(str(grp_name) + '_refDistance_grp' + \
            ' already exists.\nRename the new group or delete the one that already exists')

        else:
            if len_value is None or len_value == 0.0 or width_value is None or \
                width_value == 0.0 or height_val is None or height_val == 0.0:

                self.popup_ok_window('Distance Values cannot be Zero')

            else:

                if self.current_maya_unit != target_unit:
                    message = 'Convert up from ' + str(self.current_maya_unit) + ' to ' \
                        + str(target_unit) + '\nOR\n' + 'Convert down from ' + \
                            str(target_unit) + ' to ' + str(self.current_maya_unit) + '?'

                    up_or_down = self.popup_up_down_window(message)

                    if up_or_down:
                        unit_convert_length = cmds.convertUnit(
                            str(len_value), fromUnit=target_unit, \
                                toUnit=self.current_maya_unit)
                        unit_conv_width = cmds.convertUnit(str(width_value), \
                            fromUnit=target_unit, toUnit=self.current_maya_unit)
                        unit_conv_height = cmds.convertUnit(str(height_val), \
                            fromUnit=target_unit, toUnit=self.current_maya_unit)

                    else:
                        unit_convert_length = cmds.convertUnit( \
                            str(len_value), fromUnit=self.current_maya_unit, \
                                toUnit=target_unit)
                        unit_conv_width = cmds.convertUnit(str(width_value), \
                            fromUnit=self.current_maya_unit, toUnit=target_unit)
                        unit_conv_height = cmds.convertUnit(str(height_val), \
                            fromUnit=self.current_maya_unit, toUnit=target_unit)

                    temp_str_length = unit_convert_length.split(target_unit)
                    temp_str_width = unit_conv_width.split(target_unit)
                    temp_str_height = unit_conv_height.split(target_unit)

                    len_value = float(temp_str_length[0])
                    width_value = float(temp_str_width[0])
                    height_val = float(temp_str_height[0])

                    #Test Case: if values after conversion are too small to be used in current scene
                    if len_value < .1 or width_value < .1 or height_val < .1:

                        message = 'Values are too small to convert to ' \
                            + str(target_unit) + '\'s' + 'while in a scene using ' \
                                + str(self.current_maya_unit) + '\'s.' \
                                    +'\nRerun script with different target units to convert to ' \
                                        + 'or use larger values.'

                        self.popup_ok_window(message)

                        cmds.refresh()
                        return

                for dimen in dimens:
                    tuple_start_pos = ()
                    tuple_end_pos = ()

                    if dimen == 'length':
                        tuple_start_pos = (len_value)/2.0, 0, 0
                        tuple_end_pos = -(len_value)/2.0, 0, 0
                    elif dimen == 'width':
                        tuple_start_pos = 0, 0, (width_value)/2.0
                        tuple_end_pos = 0, 0, -((width_value)/2.0)
                    elif dimen == 'height':
                        tuple_start_pos = 0, (height_val)/2.0, 0
                        tuple_end_pos = 0, -((height_val)/2.0), 0

                    #create Length Locators
                    start_dimen_loc = cmds.spaceLocator(n=str(grp_name) + \
                        '_start' + dimen + '_loc_01', p=tuple_start_pos)

                    end_dimen_loc = cmds.spaceLocator(n=str(grp_name) + \
                        '_end' + dimen + '_loc_01', p=tuple_end_pos)

                    #create length distanceDimension at generic 3d point to be repurposed
                    cmds.distanceDimension(startPoint=[1, 1, 1], endPoint=[-1, -1, -1])

                    #rename default distanceDimension locators' transform and shape
                    temp_loc_1 = cmds.rename('locator1', 'tempLoc_01')
                    temp_rel_1 = cmds.listRelatives(temp_loc_1)
                    loc_name_1 = cmds.rename(temp_rel_1, temp_loc_1 + 'Shape')

                    temp_loc_2 = cmds.rename('locator2', 'tempLoc_02')
                    temp_rel_2 = cmds.listRelatives(temp_loc_2)
                    loc_name_2 = cmds.rename(temp_rel_2, temp_loc_2 + 'Shape')

                    #rename distanceDimension Node
                    dist_dimen_new_name = cmds.rename('distanceDimension1', \
                        str(grp_name) + '_dist' + dimen + '_01')
                    temp_rel = cmds.listRelatives(dist_dimen_new_name)
                    cmds.rename(temp_rel, dist_dimen_new_name + 'Shape')

                    #disconnect default distanceDimension locator and distanceDimension Node
                    cmds.disconnectAttr(str(loc_name_1) + '.worldPosition', \
                        str(dist_dimen_new_name) + 'Shape' + '.startPoint')
                    cmds.disconnectAttr(str(loc_name_2) + '.worldPosition', \
                        str(dist_dimen_new_name) + 'Shape' + '.endPoint')

                    #connect new Locators to distanceDimension Node
                    cmds.connectAttr(start_dimen_loc[0] + 'Shape.worldPosition', \
                        str(dist_dimen_new_name) + 'Shape' + '.startPoint')
                    cmds.connectAttr(end_dimen_loc[0] + 'Shape.worldPosition', \
                        str(dist_dimen_new_name) + 'Shape' + '.endPoint')

                    #delete default Locators
                    cmds.delete(temp_loc_1, temp_loc_2)

                    if dimen == 'length':
                        #group Lenth distanceDimension objects
                        length_grp = cmds.group(start_dimen_loc, end_dimen_loc, \
                            dist_dimen_new_name, n=str(grp_name) + '_' + dimen + 'Dist_grp')

                        self.set_color_overide(13, start_dimen_loc, \
                            end_dimen_loc, dist_dimen_new_name)

                    elif dimen == 'width':
                        width_grp = cmds.group(start_dimen_loc, end_dimen_loc, \
                            dist_dimen_new_name, n=str(grp_name) + '_' + dimen + 'Dist_grp')

                        self.set_color_overide(6, start_dimen_loc, \
                            end_dimen_loc, dist_dimen_new_name)

                    elif dimen == 'height':
                        height_grp = cmds.group(start_dimen_loc, end_dimen_loc, \
                            dist_dimen_new_name, n=str(grp_name) + '_' + dimen + 'Dist_grp')

                        self.set_color_overide(14, start_dimen_loc, \
                            end_dimen_loc, dist_dimen_new_name)

                cmds.group(length_grp, width_grp, height_grp, n=str(grp_name) + '_refDistance_grp')

                self.reset_line_edits()

    @classmethod
    def set_color_overide(cls, index, *args):
        """Sets overrideColor attribute.

        Arguments:
            index {int} -- Input index determines color of overrideColor attribute.
            *args {Maya objects} -- Inputs that would have their colors changed.
        """

        for loc in args:
            if 'dist' in loc:
                cmds.setAttr(str(loc) + ".overrideEnabled", 1)
                cmds.setAttr(str(loc) + ".overrideColor", index)
            else:
                cmds.setAttr(loc[0] + ".overrideEnabled", 1)
                cmds.setAttr(loc[0] + ".overrideColor", index)

    def delete_dimension_grp(self):
        """Deletes grp that contains predefined suffix.

        """

        grp_name = self.scale_prefix_le.text()

        #test case if reference Name textField is empty
        if grp_name == '':
            self.popup_ok_window('A name was not entered')
        elif cmds.objExists(str(grp_name) + '_refDistance_grp'):
            cmds.delete(str(grp_name) + '_refDistance_grp')

            self.reset_line_edits()
        else:
            self.popup_ok_window(
                str(grp_name) + '_refDistance_grp' + 'does not exist')

    def reset_line_edits(self):
        """Resets Qt QLineEdits after Dimension Group creation and deletion.

        """

        self.scale_prefix_le.setText('')
        self.length_le.setText('')
        self.width_le.setText('')
        self.height_le.setText('')


MAIN_WINDOW = [o for o in QtWidgets.qApp.topLevelWidgets() if o.objectName() == "MayaWindow"][0]

UI_WINDOW = ScaleReference(MAIN_WINDOW)
UI_WINDOW.show()
