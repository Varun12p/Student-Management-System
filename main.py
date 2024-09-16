from PyQt6.QtWidgets import QWidget, QLineEdit, QApplication, QLabel, QPushButton, QGridLayout, QMainWindow, \
    QTableWidget
from PyQt6.QtGui import QAction
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")

        file_button = self.menuBar().addMenu("&File")
        help_button = self.menuBar().addMenu("&Help")

        file_content = QAction("Add Student",self)
        file_button.addAction(file_content)

        help_content = QAction("Contact Us", self )
        help_button.addAction(help_content)

        # ADD TABLE
        table = QTableWidget()
        table.setColumnCount(4)
        table.setHorizontalHeaderLabels(("ID", "NAME", "COURSE", "MOBILE"))
        self.setCentralWidget(table)




app = QApplication(sys.argv)
std = MainWindow()
std.show()
sys.exit(app.exec())