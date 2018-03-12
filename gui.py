'''
===============================================================================
!/usr/bin/env python
title           :ScaleReferenceQT.py
description     :Python script for Maya to create a reference bounding box
                 based on designated units
author          :Doug Halley
date            :2018-01-12
version         :5.0
usage           :
notes           :
python_version  :2.7.14
pyqt_version    :4.11.4
===============================================================================
'''

import core

# import Qt.py packages
from Qt import QtWidgets
from Qt import QtCore
from Qt import QtGui

UNIT_MEASUREMENTS = ['cm', 'mm', 'm', 'km', 'in', 'ft', 'yd', 'mi']

class ScaleReference(QtWidgets.QMainWindow):
    '''Class that creates QtWidget and executes functionality.

    This class is meant to create a length, width,
    and height distance measurement tools to display in Maya and
    be used as a scale reference.
    '''

    def __init__(self, parent=None):
        '''Initilizes the PyQt Interface.

        Keyword Arguments:
            parent {None} -- By having no parent, ui can be standalone
                                (default: {None})
        '''

        super(ScaleReference, self).__init__(parent)
        self.init_ui()

    def init_ui(self):
        '''Logic to create QtWidget's UI.

        '''

        self.setWindowTitle('Scale Reference')

        # Label for Scene Units -----------------------------------------------

        scene_units_lbl_layout = QtWidgets.QHBoxLayout()

        scene_units_lbl = QtWidgets.QLabel('Scene\'s Units:')
        scene_units_lbl.setAlignment(QtCore.Qt.AlignCenter)

        self.current_maya_unit = core.get_scene_units()

        units_lbl = QtWidgets.QLabel(self.current_maya_unit)
        units_lbl.setAlignment(QtCore.Qt.AlignCenter)

        scene_units_lbl_layout.layout().addWidget(scene_units_lbl)
        scene_units_lbl_layout.layout().addWidget(units_lbl)

        # User selected Units combobox Layout ---------------------------------

        units_combobox_btn_layout = QtWidgets.QHBoxLayout()

        units_combobox_lbl = QtWidgets.QLabel('Convert Units To:')
        units_combobox = QtWidgets.QComboBox()

        for unit in UNIT_MEASUREMENTS:
            units_combobox.addItem(unit)

        units_combobox_btn_layout.layout().addWidget(units_combobox_lbl)
        units_combobox_btn_layout.layout().addWidget(units_combobox)

        # Prefix Line Edit Layout ---------------------------------------------

        scale_prefix_layout = QtWidgets.QHBoxLayout()

        scale_prefix_lbl = QtWidgets.QLabel('Reference Prefix:')
        self.scale_prefix_le = QtWidgets.QLineEdit('')

        scale_prefix_layout.layout().addWidget(scale_prefix_lbl)
        scale_prefix_layout.layout().addWidget(self.scale_prefix_le)

        # Dimension Line Edits Layout -----------------------------------------

        self.length_le = QtWidgets.QLineEdit('')

        self.width_le = QtWidgets.QLineEdit('')

        self.height_le = QtWidgets.QLineEdit('')

        dimensions_form_layout = self.create_dimension_layouts(
            self.length_le, self.width_le, self.height_le)

        # Buttons Layout ------------------------------------------------------

        button_layout = QtWidgets.QVBoxLayout()
        create_btn = QtWidgets.QPushButton('Create New Reference')
        delete_btn = QtWidgets.QPushButton('Delete Named Reference')

        button_layout.layout().addWidget(create_btn)
        button_layout.layout().addWidget(delete_btn)

        # Central Widget ------------------------------------------------------

        central_widget = QtWidgets.QWidget()
        central_widget.setLayout(QtWidgets.QVBoxLayout())
        central_widget.layout().addLayout(scene_units_lbl_layout)
        central_widget.layout().addLayout(units_combobox_btn_layout)

        central_widget.layout().addLayout(scale_prefix_layout)
        central_widget.layout().addLayout(dimensions_form_layout)
        central_widget.layout().addLayout(button_layout)

        # set central widget
        self.setCentralWidget(central_widget)

        # =====================================================================
        # PyQt Execution Connections
        # =====================================================================

        create_btn.clicked.connect(
            lambda: core.create_locators(units_combobox.currentText()))

        delete_btn.clicked.connect(lambda: core.delete_dimension_grp())

        self.width_le.textChanged.connect(
            lambda: self.check_line_edit_state(self.width_le))
        self.width_le.textChanged.emit(self.width_le.text())

        self.length_le.textChanged.connect(
            lambda: self.check_line_edit_state(self.length_le))
        self.length_le.textChanged.emit(self.length_le.text())

        self.height_le.textChanged.connect(
            lambda: self.check_line_edit_state(self.height_le))
        self.height_le.textChanged.emit(self.height_le.text())

    def create_dimension_layouts(self, length_le, width_le, height_le):
        '''Creates custom layout that contains the length, width, and height QLineEdits

        If Maya scene is Y or Z up the length, width, and
        height QLineEdits will be arranged differently.
        Validator is also set for each QLineEdit.

        Returns:
            tuple -- returns layouts with QLabels and QLineEdits
        '''

        dimension_form_layout = QtWidgets.QFormLayout()

        up_axis = core.get_up_axis()

        if up_axis == 'y':
            dimension_form_layout.addRow('Width (X): ', width_le)
            dimension_form_layout.addRow('Height (Y): ', height_le)
            dimension_form_layout.addRow('Length (Z): ', length_le)

        elif up_axis == 'z':

            dimension_form_layout.addRow('Width (X): ', width_le)
            dimension_form_layout.addRow('Length (Y): ', length_le)
            dimension_form_layout.addRow('Height (Z): ', height_le)

        double_validator = QtGui.QDoubleValidator()
        double_validator.setDecimals(3)
        double_validator.setNotation(QtGui.QDoubleValidator.StandardNotation)

        width_le.setValidator(double_validator)
        length_le.setValidator(double_validator)
        height_le.setValidator(double_validator)

        return dimension_form_layout

    @classmethod
    def check_line_edit_state(cls, line_edit):
        '''Changes Stylesheet of input line edit.

        Validator checks state of line edit and changes line edit's font
        and background for visual confirmation that line edit input is
        acceptable.

        Arguments:
            line_edit {QLineEdit} -- Input QLineEdit to analyze.
        '''

        sender = line_edit
        validator = sender.validator()
        state = validator.validate(sender.text(), 0)[0]
        if state == QtGui.QValidator.Acceptable:
            font_color = '#000000'  # black
            bg_color = '#c4df9b'  # green
            sender.setStyleSheet(
                'QLineEdit { color: %s; background-color: %s }'
                % (font_color, bg_color))
        elif sender.text() == '':
            sender.setStyleSheet('')
        '''
        elif state == QtGui.QValidator.Intermediate:
            color = '#fff79a' # yellow
        elif state == QtGui.QValidator.Invalid:
            color = '#f6989d' # red
        '''

    @classmethod
    def popup_ok_window(cls, message):
        '''Popup Ok message box to display information to user.

        Arguments:
            message {str} -- Input string for QMessageBox to display.
        '''

        popup_window = QtWidgets.QMessageBox()

        popup_window.setText(str(message))
        popup_window.setStandardButtons(QtWidgets.QMessageBox.Ok)

        popup_window.exec_()

    @classmethod
    def popup_yes_no_window(cls, message):
        '''Popup Ok message box to display information to user.

        Arguments:
            message {str} -- Input string for QMessageBox to display.

        Returns:
            bool -- Returns True if Yes or False if No
        '''

        msg = QtWidgets.QMessageBox()

        msg.setText(message)
        # msg.setWindowTitle('MessageBox demo')
        # msg.setDetailedText('The details are as follows:')
        msg.setStandardButtons(
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)

        result = msg.exec_()

        if result == QtWidgets.QMessageBox.Yes:
            return True
        elif result == QtWidgets.QMessageBox.No:
            return False

    @classmethod
    def popup_up_down_window(cls, message):
        '''Popup Ok message box to display information to user.

        Arguments:
            message {str} -- Input string for QMessageBox to display.

        Returns:
            bool -- Returns True if Yes or False if No
        '''

        msg = QtWidgets.QMessageBox()

        msg.setText(message)
        # msg.setWindowTitle('MessageBox demo')
        # msg.setDetailedText('The details are as follows:')
        msg.addButton('Up', QtWidgets.QMessageBox.YesRole)
        msg.addButton('Down', QtWidgets.QMessageBox.NoRole)

        result = msg.exec_()

        if result == QtWidgets.QMessageBox.Yes:
            return True
        elif result == QtWidgets.QMessageBox.No:
            return False

    def reset_line_edits(self):
        '''Resets Qt QLineEdits after Dimension Group creation and deletion.

        '''

        self.scale_prefix_le.setText('')
        self.length_le.setText('')
        self.width_le.setText('')
        self.height_le.setText('')

    def create_locators(self, target_unit):

        grp_name = self.scale_prefix_le.text()
        len_value = float(self.length_le.text())
        width_value = float(self.width_le.text())
        height_value = float(self.height_le.text())

        if grp_name == '':
            self.popup_ok_window('A name was not entered')
            return

        elif core.check_ref_grp_exists(grp_name):
            self.popup_ok_window(
                str(grp_name) + '_refDistance_grp' +
                ' already exists.\nRename the new group or delete ' +
                'the one that already exists')
            return

        if len_value is None or len_value == 0.0 or width_value is None \
            or width_value == 0.0 or height_value is None or \
                height_value == 0.0:
            self.popup_ok_window('Distance Values cannot be Zero')
            return

        if self.current_maya_unit != target_unit:
            message = \
                    'Convert up from ' + str(self.current_maya_unit) + \
                    'to ' + str(target_unit) + '\nOR\n' + \
                    'Convert down from ' + str(target_unit) + ' to ' \
                    + str(self.current_maya_unit) + '?'

            up_or_down = self.popup_up_down_window(message)

            len_value, width_value, height_value = core.convert_units()

            # Test Case: if values after conversion are too small
            # to be used in current scene
            if len_value < .1 or width_value < .1 or height_value < .1:

                message = 'Values are too small to convert to ' \
                    + str(target_unit) + '\'s' + \
                    'while in a scene using ' + \
                    str(self.current_maya_unit) + '\'s.' \
                    + '\nRerun script with different target units ' + \
                    'to convert to ' + 'or use larger values.'

                self.popup_ok_window(message)

                return

            core.create_dimension_grp()

            self.reset_line_edits()
            return

    def delete_dimension_grp(self):
        '''Deletes grp that contains predefined suffix.

        '''

        grp_name = self.scale_prefix_le.text()

        # Test case if reference Name textField is empty
        if grp_name == '':
            self.popup_ok_window('A name was not entered')
            return
        elif core.check_ref_grp_exists(grp_name):
            core.delete_ref_grp(grp_name)

            self.reset_line_edits()
            return
        else:
            self.popup_ok_window(
                str(grp_name) + '_refDistance_grp' + 'does not exist')
            return

MAIN_WINDOW = \
    [o for o in QtWidgets.qApp.topLevelWidgets() if o.objectName() ==
     'MayaWindow'][0]

UI_WINDOW = ScaleReference(MAIN_WINDOW)
UI_WINDOW.show()
