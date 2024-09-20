from PyQt6.QtWidgets import QWidget, QLineEdit, QApplication, QLabel, QPushButton, QGridLayout, QMainWindow, \
    QTableWidget, QTableWidgetItem, QDialog, QVBoxLayout, QComboBox
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
        file_content.triggered.connect(self.insert)
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

    def insert(self):
        dialog = InsertDialog()
        dialog.exec()

class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Insert New Student Data")
        self.setFixedHeight(300)
        self.setFixedWidth(300)

        layout = QVBoxLayout()

        self.name = QLineEdit()
        self.name.setPlaceholderText("Name")
        layout.addWidget(self.name)

        self.course_name= QComboBox()
        courses = ["Biology","Math","Astronomy","Physics"]
        self.course_name.addItems(courses)
        layout.addWidget(self.course_name)

        self.mobile = QLineEdit()
        self.mobile.setPlaceholderText("Mobile No.")
        layout.addWidget(self.mobile)

        button = QPushButton("Register")
        button.clicked.connect(self.add_data)
        layout.addWidget(button)

        self.setLayout(layout)

    def add_data(self):
        name = self.name.text()
        course = self.course_name.itemText(self.course_name.currentIndex())
        mobile = self.mobile.text()

        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("INSERt INTO students (name, course, mobile) VALUES (?,?,?)",
                       (name,course,mobile))
        connection.commit()
        cursor.close()
        connection.close()
        MainWindow.load_data()

app = QApplication(sys.argv)
std = MainWindow()
std.load_data()
std.show()
sys.exit(app.exec())