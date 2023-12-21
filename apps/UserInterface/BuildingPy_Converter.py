import sys
from pathlib import Path
import sys
import os
import configparser
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QPushButton, QFileDialog, QTextEdit, QLabel
from PyQt6.QtGui import QIcon, QPalette, QColor
from PyQt6.QtCore import QDateTime, Qt, QThread, pyqtSignal
import subprocess

from bp_single_file import *

class CustomOutputStream:
    def __init__(self, output_func):
        self.output_func = output_func

    def write(self, text):
        if text.strip():
            self.output_func(text)

    def flush(self):
        pass


class SubprocessThread(QThread):
    finished = pyqtSignal(str)

    def run(self):
        try:
            subprocess.run("C:/Struct4u/XFEM4U/wframe3d.exe", shell=True, check=True)
            self.finished.emit("Subprocess finished successfully")
        except subprocess.CalledProcessError as e:
            self.finished.emit(f"Subprocess failed: {e}")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BuildingPy Converter")
        self.setGeometry(400, 200, 800, 400)
        self.setFixedSize(800, 400)
        self.initUI()

    def initUI(self):
        sys.stdout = CustomOutputStream(self.outputAdd)

        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(45, 45, 45))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(240, 240, 240))
        palette.setColor(QPalette.ColorRole.Button, QColor(75, 75, 75))
        palette.setColor(QPalette.ColorRole.ButtonText, QColor(240, 240, 240))
        palette.setColor(QPalette.ColorRole.Highlight, QColor(60, 150, 200))
        palette.setColor(QPalette.ColorRole.HighlightedText, QColor(240, 240, 240))
        self.setPalette(palette)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        section_layout = QHBoxLayout()

        left_section = QWidget()
        left_layout = QVBoxLayout()
        left_section.setLayout(left_layout)

        left_label = QLabel("From:")
        left_label.setStyleSheet("font-size: 16px; color: white;")
        left_layout.addWidget(left_label)

        dropdown_style = "QComboBox { border-radius: 5px; font-size: 16px; height: 25px; }"

        self.left_dropdown = QComboBox()
        self.left_dropdown.addItems(["Scia"])
        self.left_dropdown.setStyleSheet(dropdown_style)
        left_layout.addWidget(self.left_dropdown)
        self.left_dropdown.setObjectName("self.left_dropdown")

        section_layout.addWidget(left_section)

        # transfer_icon = QLabel()
        # transfer_icon.setPixmap(QIcon("transfer.ico").pixmap(32, 32))
        # section_layout.addWidget(transfer_icon)

        right_section = QWidget()
        right_layout = QVBoxLayout()
        right_section.setLayout(right_layout)

        right_label = QLabel("To:")
        right_label.setStyleSheet("font-size: 16px; color: white;")
        right_layout.addWidget(right_label)

        self.right_dropdown = QComboBox()
        self.right_dropdown.addItems(["XFEM4U", "Speckle"])
        self.right_dropdown.setStyleSheet(dropdown_style)
        right_layout.addWidget(self.right_dropdown)

        section_layout.addWidget(right_section)

        layout.addLayout(section_layout)

        convert_button = QPushButton("Convert")
        convert_button.clicked.connect(self.convert)
        button_height = 50
        convert_button.setMinimumHeight(button_height)
        convert_button.setMaximumHeight(button_height)        
        convert_button.setStyleSheet("font-size: 16px;")
        layout.addWidget(convert_button)

        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setStyleSheet("background-color: lightgray; border-radius: 5px; font-size: 15px; color: gray;")
        layout.addWidget(self.output_text)

    def scia_to_xfem4u(self):
        filepath, _ = QFileDialog.getOpenFileName(self, "Select XML File", filter="XML Files (*.xml)")
        if filepath:
            new_text = f"Selected XML file: {filepath}"
            self.outputAdd(new_text)

            project = BuildingPy("TempCommit", "0")
            LoadXML(filepath, project)

            base_file_name = "Struct4U_XFEM4U_export.xml"
            documents_dir = os.path.expanduser("~/Documents")

            file_name = base_file_name
            counter = 1

            while os.path.exists(os.path.join(documents_dir, file_name)):
                file_name = f"Struct4U_XFEM4U_export_{counter}.xml"
                counter += 1

            path = os.path.join(documents_dir, file_name).replace("\\", "/")

            xmlS4U = xmlXFEM4U()
            xmlS4U.addBeamsPlates(project.objects)
            xmlS4U.addProject("Examples of building.py")
            xmlS4U.addPanels(project.objects)
            xmlS4U.addSurfaceLoad(project.objects)
            xmlS4U.addLoadCasesCombinations()
            xmlS4U.XML()
            XMLString = xmlS4U.xmlstr

            file = open(path, "w")
            a = file.write(XMLString)
            file.close()
            new_text = f"Custom XML file '{file_name}' has been created in the Documents directory."
            self.outputAdd(new_text)


            ini_file_path = os.path.join(os.getenv('LOCALAPPDATA'), 'Struct4u', 'DirectCommands_XFEM4U.ini')
            config = configparser.ConfigParser()

            config['Struct4u'] = {
                'Import_XML': f'{path}'
            }

            if os.path.exists(ini_file_path):
                with open(ini_file_path, 'w') as config_file:
                    config.write(config_file)
            else:
                os.makedirs(os.path.dirname(ini_file_path), exist_ok=True)
                with open(ini_file_path, 'w') as config_file:
                    config.write(config_file)

            new_text = f".ini file '{ini_file_path}' has been updated/created."
            self.outputAdd(new_text)

            self.subprocess_thread = SubprocessThread()
            self.subprocess_thread.finished.connect(self.on_subprocess_finished)
            self.subprocess_thread.start()

        else:
            new_text = f"No XML file selected"
            self.outputAdd(new_text)

    def on_subprocess_finished(self, message):
        self.outputAdd(message)

    def outputAdd(self, text):
        current_datetime = QDateTime.currentDateTime().toString("dd-MM-yyyy hh:mm:ss")
        current_text = self.output_text.toPlainText()
        new_text = f"{current_datetime} | {text}"
        updated_text = f"{new_text}\n{current_text}"
        self.output_text.setPlainText(updated_text)

    def convert(self):
        left_dropdown_index = self.left_dropdown.currentIndex()
        right_dropdown_index = self.right_dropdown.currentIndex()

        left_dropdown_text = self.left_dropdown.currentText()
        right_dropdown_text = self.right_dropdown.currentText()
        new_text = f"Convert from: '{left_dropdown_text}' to '{right_dropdown_text}'"

        self.outputAdd(new_text)

        if left_dropdown_index == 0 and right_dropdown_index == 0:
            self.scia_to_xfem4u()
            self.outputAdd(f"Conversion successfully completed from '{left_dropdown_text}' to '{right_dropdown_text}'")
        else:
            self.outputAdd(f"Conversion between '{left_dropdown_text}' and '{right_dropdown_text}' has not been performed yet")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setWindowIcon(QIcon("icon.ico"))
    window.show()
    sys.exit(app.exec())