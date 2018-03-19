'''
This script is licensed CC 0 1.0, so that you can learn from it.

------ CC 0 1.0 ---------------

The person who associated a work with this deed has dedicated the work to the public domain by waiving all of his or her rights to the work worldwide under copyright law, including all related and neighboring rights, to the extent allowed by law.

You can copy, modify, distribute and perform the work, even for commercial purposes, all without asking permission.

https://creativecommons.org/publicdomain/zero/1.0/legalcode
'''
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QLineEdit, QScrollArea, QGridLayout, QFileDialog,
                             QLabel, QDialogButtonBox)
from tenscripts import tenscriptsdialog
import krita


class UITenScripts(object):

    def __init__(self):
        self.kritaInstance = krita.Krita.instance()
        self.mainDialog = tenscriptsdialog.TenScriptsDialog(self, self.kritaInstance.activeWindow().qwindow())

        self.buttonBox = QDialogButtonBox(self.mainDialog)
        self.layout = QVBoxLayout(self.mainDialog)
        self.baseWidget = QWidget()
        self.baseArea = QWidget()
        self.scrollArea =  QScrollArea()
        self.scriptsLayout = QGridLayout()

        self.buttonBox.accepted.connect(self.mainDialog.accept)
        self.buttonBox.rejected.connect(self.mainDialog.reject)

        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.scrollArea.setWidgetResizable(True)

    def initialize(self, tenscripts):
        self.tenscripts = tenscripts

        self._loadGridLayout()
        self._fillScripts()

        self.baseArea.setLayout(self.scriptsLayout)
        self.scrollArea.setWidget(self.baseArea)

        self.layout.addWidget(self.scrollArea)
        self.layout.addWidget(self.buttonBox)

        self.mainDialog.show()
        self.mainDialog.activateWindow()
        self.mainDialog.exec_()

    def addNewRow(self, key):
        rowPosition = self.scriptsLayout.rowCount()
        rowLayout = QHBoxLayout()
        label = QLabel()
        directoryTextField = QLineEdit()
        directoryDialogButton = QPushButton("...")

        directoryTextField.setReadOnly(True)
        label.setText(self.tenscripts.actions[key].shortcut().toString())
        directoryTextField.setToolTip("Selected Path")
        directoryDialogButton.setToolTip("Select the script")
        directoryDialogButton.clicked.connect(self._selectScript)

        self.scriptsLayout.addWidget(label, rowPosition, 0, Qt.AlignLeft|Qt.AlignTop)
        self.scriptsLayout.addWidget(directoryTextField, rowPosition, 1, Qt.AlignLeft|Qt.AlignTop)
        self.scriptsLayout.addWidget(directoryDialogButton, rowPosition, 2, Qt.AlignLeft|Qt.AlignTop)

    def saved_scripts(self):
        _saved_scripts = []
        index = 0

        for row in range(self.scriptsLayout.rowCount()-1):
            textField = self.scriptsLayout.itemAt(index + 1).widget()
            if textField.text():
                _saved_scripts.append(textField.text())
            index += 3

        return _saved_scripts

    def _selectScript(self):
        dialog = QFileDialog(self.mainDialog)
        dialog.setNameFilter('Python files (*.py)')

        if dialog.exec():
            selectedFile = dialog.selectedFiles()[0]
            obj = self.mainDialog.sender()
            textField = self.scriptsLayout.itemAt(self.scriptsLayout.indexOf(obj)-1).widget()
            textField.setText(selectedFile)

    def _loadGridLayout(self):
        for item in range(0, 10):
            self.addNewRow(item)

    def _fillScripts(self):
        scripts = self.tenscripts.scripts
        index = 0

        for row in range(self.scriptsLayout.rowCount()-1):
            if row >= len(scripts):
                return

            textField = self.scriptsLayout.itemAt(index + 1).widget()
            textField.setText(scripts[row])
            index += 3
