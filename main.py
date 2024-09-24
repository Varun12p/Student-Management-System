from PyQt6.QtWidgets import QWidget, QLineEdit, QApplication, QLabel, QPushButton, QGridLayout, QMainWindow, \
    QTableWidget, QTableWidgetItem, QDialog, QVBoxLayout, QComboBox, QToolBar, QStatusBar, QMessageBox
from PyQt6.QtGui import QAction, QIcon
import sys
import sqlite3
from PyQt6.QtCore import Qt

class DatabaseConnection():
    def __init__(self , database_file="database.db"):
        self.database_file = database_file

    def connect(self):
        connection = sqlite3.connect("database.db")
        return connection

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")
        self.setMinimumSize(800,600)

        file_button = self.menuBar().addMenu("&File")
        help_button = self.menuBar().addMenu("&Help")
        edit_button = self.menuBar().addMenu("&Edit")

        add_student = QAction(QIcon("icons/add.png"),"Add Student",self)
        add_student.triggered.connect(self.insert)
        file_button.addAction(add_student)

        help_content = QAction("Contact Us", self )
        help_button.addAction(help_content)
        #the line bellow is for Mac user.
        # help_content.triggered.connect(QAction.menuRole.NoRole)

        help_content.triggered.connect(self.about)

        edit_content = QAction(QIcon("icons/search.png"), "Search",self)
        edit_button.addAction(edit_content)
        edit_content.triggered.connect(self.search)

        # ADD TABLE
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("ID", "NAME", "COURSE", "MOBILE"))
        self.table.verticalHeader().setVisible(False) # to avoid default row number from displaying

        self.setCentralWidget(self.table)

        #Add Toolbar
        toolbar = QToolBar()
        toolbar.setMovable(True)
        self.addToolBar(toolbar)

        # Add elements of toolbar
        toolbar.addAction(add_student)
        toolbar.addAction(edit_content)

        # Add status bar.
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)

        # Detect a clicked cell
        self.table.cellClicked.connect(self.cell_clicked)

    # add data
    def load_data(self):
        connection = DatabaseConnection().connect()
        result = connection.execute("SELECT * FROM students")
        self.table.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number,column_number,QTableWidgetItem(str(data)))
        connection.close()

    def insert(self):
        dialog = InsertDialog(self)
        dialog.exec()

    def search(self):
        dialog = SearchDialog(self)
        dialog.exec()

    def cell_clicked(self):
        edit_button = QPushButton("Edit Record")
        delete_button = QPushButton("Delete Record")

        edit_button.clicked.connect(self.edit)
        delete_button.clicked.connect(self.delete)

        children = self.findChildren(QPushButton)
        if children:
            for child in children:
                self.statusbar.removeWidget(child)

        self.statusbar.addWidget(edit_button)
        self.statusbar.addWidget(delete_button)

    def edit(self):
        dialog = EditDialog(self)
        dialog.exec()

    def delete(self):
        dialog = DeleteDialog(self)
        dialog.exec()

    def about(self):
        dialog = AboutDialog()
        dialog.exec()


class AboutDialog(QMessageBox):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("About")
        content = """
        This app is created while learning python on Day 48.
        """
        self.setText(content)


class EditDialog(QDialog):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle("Update Student Data")
        self.setFixedHeight(300)
        self.setFixedWidth(300)

        layout = QVBoxLayout()

        # get the name from the selected student
        index = self.main_window.table.currentRow()
        student_name = self.main_window.table.item(index,1).text()

        self.student_id = self.main_window.table.item(index,0).text()

        self.name = QLineEdit(student_name)
        self.name.setPlaceholderText("Name")
        layout.addWidget(self.name)

        # Get the course of the selected student
        course_name = self.main_window.table.item(index,2).text()
        self.course_name = QComboBox()
        courses = ["Biology", "Math", "Astronomy", "Physics"]
        self.course_name.addItems(courses)
        self.course_name.setCurrentText(course_name)
        layout.addWidget(self.course_name)

        # Get the mobile number of selected student
        mobile = self.main_window.table.item(index,3).text()
        self.mobile = QLineEdit(mobile)
        self.mobile.setPlaceholderText("Mobile No.")
        layout.addWidget(self.mobile)

        button = QPushButton("Update")
        button.clicked.connect(self.update_data)
        layout.addWidget(button)

        self.setLayout(layout)

    def update_data(self):
        connection = DatabaseConnection().connect()
        cursor = connection.cursor()
        cursor.execute("UPDATE students SET name=?, course = ?, mobile = ? WHERE id = ?",
                       (self.name.text(),self.course_name.itemText(self.course_name.currentIndex()),
                        self.mobile.text(), self.student_id))
        connection.commit()
        cursor.close()
        connection.close()
        self.main_window.load_data()
        self.close()


class DeleteDialog(QDialog):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle("Delete Student Data")

        layout = QGridLayout()
        confirmation = QLabel("Are you sure you want to delete?")
        yes = QPushButton("YES")
        no = QPushButton("NO")

        layout.addWidget(confirmation, 0, 0, 1, 2)
        layout.addWidget(yes, 1, 0)
        layout.addWidget(no, 1, 1)

        self.setLayout(layout)

        yes.clicked.connect(self.delete_student)
        no.clicked.connect(self.close)

    def close_window(self):
        self.close()


    def delete_student(self):
        connection = DatabaseConnection().connect()
        cursor = connection.cursor()

        # Get index and student id of the selected student
        index = self.main_window.table.currentRow()
        student_id = self.main_window.table.item(index,0).text()
        cursor.execute("DELETE FROM students WHERE id = ?",(student_id,))
        connection.commit()
        cursor.close()
        connection.close()
        self.main_window.load_data()
        self.close()

        # Confirmation Message
        confirmation_widget = QMessageBox()
        confirmation_widget.setWindowTitle("Success.")
        confirmation_widget.setText("Deleted successfully.")
        confirmation_widget.exec()


class InsertDialog(QDialog):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle("Insert New Student Data")
        self.setFixedHeight(300)
        self.setFixedWidth(300)

        layout = QVBoxLayout()

        self.name = QLineEdit()
        self.name.setPlaceholderText("Name")
        layout.addWidget(self.name)

        self.course_name = QComboBox()
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

        connection = DatabaseConnection().connect()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO students (name, course, mobile) VALUES (?,?,?)",
                       (name,course,mobile))
        connection.commit()
        cursor.close()
        connection.close()

        self.main_window.load_data()
        self.close()

class SearchDialog(QDialog):
    def __init__(self,main_window):
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle("Search the student")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        button = QPushButton("Search")
        layout.addWidget(button)
        button.clicked.connect(self.search)

        self.setLayout(layout)

    def search(self):
        name = self.student_name.text()
        connection = DatabaseConnection().connect()
        cursor = connection.cursor()
        results = cursor.execute("SELECT * FROM students WHERE name = ?",(name,))
        rows = list(results)

        items = self.main_window.table.findItems(name, Qt.MatchFlag.MatchFixedString)
        for item in items:
            self.main_window.table.item(item.row(),1).setSelected(True)

        cursor.close()
        connection.close()


app = QApplication(sys.argv)
std = MainWindow()
std.load_data()
std.show()
sys.exit(app.exec())