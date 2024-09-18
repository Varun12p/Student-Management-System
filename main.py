from PyQt6.QtWidgets import QWidget, QLineEdit, QApplication, QLabel, QPushButton, QGridLayout, QMainWindow, \
    QTableWidget, QTableWidgetItem
from PyQt6.QtGui import QAction
import sys
import sqlite3

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
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("ID", "NAME", "COURSE", "MOBILE"))
        self.table.verticalHeader().setVisible(False) # to avoid default row number from displaying
        self.setCentralWidget(self.table)

    # add data
    def load_data(self):
        connection = sqlite3.connect("database.db")
        result = connection.execute("SELECT * FROM students")
        self.table.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number,column_number,QTableWidgetItem(str(data)))
        connection.close()


app = QApplication(sys.argv)
std = MainWindow()
std.load_data()
std.show()
sys.exit(app.exec())