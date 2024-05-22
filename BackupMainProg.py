import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableWidgetItem
from PyQt5 import uic, QtCore, QtWidgets
import mysql.connector
from mysql.connector import errorcode

def load_ui(window_instance, ui_file):
    uic.loadUi(ui_file, window_instance)

class DatabaseManager:
    def __init__(self):
        self.connection = None
        self.connect()

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='password',
                database='StudentsDatabase'
            )
            print("Database connection successful")
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your Username/Password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)

    def execute_query(self, query, params=None):
        cursor = self.connection.cursor()
        cursor.execute(query, params)
        self.connection.commit()
        cursor.close()

    def fetch_query(self, query, params=None):
        cursor = self.connection.cursor()
        cursor.execute(query, params)
        results = cursor.fetchall()
        cursor.close()
        return results

db_manager = DatabaseManager()

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(171, 224)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(10, 130, 151, 51))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(10, 10, 151, 51))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(10, 70, 151, 51))
        self.pushButton_2.setObjectName("pushButton_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 171, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton_3.setText(_translate("MainWindow", "Shifter"))
        self.pushButton.setText(_translate("MainWindow", "Transfer"))
        self.pushButton_2.setText(_translate("MainWindow", "Admission"))

class MainWindows(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton_3.clicked.connect(self.openShifterWindow)
        self.pushButton_2.clicked.connect(self.openAdmissionWindow)
        self.pushButton.clicked.connect(self.openTransferWindow)

        self.shifterWindow = None
        self.admissionWindow = None
        self.transferWindow = None

    def openShifterWindow(self):
        if self.shifterWindow is None:
            self.shifterWindow = ShifterWindow()
            self.shifterWindow.pushButton_7.clicked.connect(self.shifterWindow.add_record)
            self.shifterWindow.pushButton_8.clicked.connect(self.shifterWindow.delete_record)
            self.shifterWindow.pushButton_10.clicked.connect(self.shifterWindow.search_record)
            self.shifterWindow.pushButton_11.clicked.connect(self.shifterWindow.back_to_menu)
        self.shifterWindow.load_table_data()  # Load data when window is shown
        self.shifterWindow.show()

    def openAdmissionWindow(self):
        if self.admissionWindow is None:
            self.admissionWindow = AdmissionWindow()
            self.admissionWindow.pushButton_7.clicked.connect(self.admissionWindow.add_record)
            self.admissionWindow.pushButton_8.clicked.connect(self.admissionWindow.delete_record)
            self.admissionWindow.pushButton_10.clicked.connect(self.admissionWindow.search_record)
            self.admissionWindow.pushButton_11.clicked.connect(self.admissionWindow.back_to_menu)
        self.admissionWindow.load_table_data()  # Load data when window is shown
        self.admissionWindow.show()

    def openTransferWindow(self):
        if self.transferWindow is None:
            self.transferWindow = TransferWindow()
            self.transferWindow.pushButton_7.clicked.connect(self.transferWindow.add_record)
            self.transferWindow.pushButton_8.clicked.connect(self.transferWindow.delete_record)
            self.transferWindow.pushButton_10.clicked.connect(self.transferWindow.search_record)
            self.transferWindow.pushButton_11.clicked.connect(self.transferWindow.back_to_menu)
        self.transferWindow.load_table_data()  # Load data when window is shown
        self.transferWindow.show()

class ShifterWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        load_ui(self, 'ShifterWindow.ui')

    def add_record(self):
        student_code = self.admissionlineEdit.text()
        last_name = self.admissionlineEdit_2.text()
        first_name = self.admissionlineEdit_3.text()
        middle_name = self.admissionlineEdit_6.text()
        course = self.admissionlineEdit_4.text()
        year = self.admissionlineEdit_5.text()

        if student_code and last_name and first_name and middle_name and course and year:
            query = "INSERT INTO shifters (student_code, last_name, first_name, middle_name, course, year) VALUES (%s, %s, %s, %s, %s, %s)"
            params = (student_code, last_name, first_name, middle_name, course, year)
            db_manager.execute_query(query, params)
            self.load_table_data()
        else:
            QMessageBox.warning(self, "Input Error", "Please fill in all fields.")

    def delete_record(self):
        selected_row = self.tableWidget.currentRow()
        if selected_row >= 0:
            student_code = self.tableWidget.item(selected_row, 0).text()
            query = "DELETE FROM shifters WHERE student_code = %s"
            params = (student_code,)
            db_manager.execute_query(query, params)
            self.load_table_data()
        else:
            QMessageBox.warning(self, "Selection Error", "Please select a row to delete.")

    def search_record(self):
        student_code = self.admissionlineEdit.text()
        last_name = self.admissionlineEdit_2.text()
        first_name = self.admissionlineEdit_3.text()
        middle_name = self.admissionlineEdit_6.text()
        course = self.admissionlineEdit_4.text()
        year = self.admissionlineEdit_5.text()

        query = "SELECT * FROM shifters WHERE (student_code = %s OR %s = '') AND (last_name = %s OR %s = '') AND (first_name = %s OR %s = '') AND (middle_name = %s OR %s = '') AND (course = %s OR %s = '') AND (year = %s OR %s = '')"
        params = (student_code, student_code, last_name, last_name, first_name, first_name, middle_name, middle_name, course, course, year, year)
        records = db_manager.fetch_query(query, params)

        self.tableWidget.setRowCount(0)
        for row_data in records:
            row_position = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row_position)
            for column, data in enumerate(row_data):
                self.tableWidget.setItem(row_position, column, QTableWidgetItem(str(data)))

    def back_to_menu(self):
        self.close()

    def load_table_data(self):
        query = "SELECT * FROM shifters"
        records = db_manager.fetch_query(query)
        self.tableWidget.setRowCount(0)
        for row_data in records:
            row_position = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row_position)
            for column, data in enumerate(row_data):
                self.tableWidget.setItem(row_position, column, QTableWidgetItem(str(data)))

class AdmissionWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        load_ui(self, 'AdmissionWindow.ui')

    def add_record(self):
        student_code = self.admissionlineEdit.text()
        last_name = self.admissionlineEdit_2.text()
        first_name = self.admissionlineEdit_3.text()
        middle_name = self.admissionlineEdit_6.text()
        course = self.admissionlineEdit_4.text()
        year = self.admissionlineEdit_5.text()

        if student_code and last_name and first_name and middle_name and course and year:
            query = "INSERT INTO admitted_students (student_code, last_name, first_name, middle_name, course, year) VALUES (%s, %s, %s, %s, %s, %s)"
            params = (student_code, last_name, first_name, middle_name, course, year)
            db_manager.execute_query(query, params)
            self.load_table_data()
        else:
            QMessageBox.warning(self, "Input Error", "Please fill in all fields.")

    def delete_record(self):
        selected_row = self.tableWidget.currentRow()
        if selected_row >= 0:
            student_code = self.tableWidget.item(selected_row, 0).text()
            query = "DELETE FROM admitted_students WHERE student_code = %s"
            params = (student_code,)
            db_manager.execute_query(query, params)
            self.load_table_data()
        else:
            QMessageBox.warning(self, "Selection Error", "Please select a row to delete.")

    def search_record(self):
        student_code = self.admissionlineEdit.text()
        last_name = self.admissionlineEdit_2.text()
        first_name = self.admissionlineEdit_3.text()
        middle_name = self.admissionlineEdit_6.text()
        course = self.admissionlineEdit_4.text()
        year = self.admissionlineEdit_5.text()

        query = "SELECT * FROM admitted_students WHERE (student_code = %s OR %s = '') AND (last_name = %s OR %s = '') AND (first_name = %s OR %s = '') AND (middle_name = %s OR %s = '') AND (course = %s OR %s = '') AND (year = %s OR %s = '')"
        params = (student_code, student_code, last_name, last_name, first_name, first_name, middle_name, middle_name, course, course, year, year)
        records = db_manager.fetch_query(query, params)

        self.tableWidget.setRowCount(0)
        for row_data in records:
            row_position = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row_position)
            for column, data in enumerate(row_data):
                self.tableWidget.setItem(row_position, column, QTableWidgetItem(str(data)))

    def back_to_menu(self):
        self.close()

    def load_table_data(self):
        query = "SELECT * FROM admitted_students"
        records = db_manager.fetch_query(query)
        self.tableWidget.setRowCount(0)
        for row_data in records:
            row_position = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row_position)
            for column, data in enumerate(row_data):
                self.tableWidget.setItem(row_position, column, QTableWidgetItem(str(data)))

class TransferWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        load_ui(self, 'TransferWindow.ui')

    def add_record(self):
        student_code = self.admissionlineEdit.text()
        last_name = self.admissionlineEdit_2.text()
        first_name = self.admissionlineEdit_3.text()
        middle_name = self.admissionlineEdit_6.text()
        course = self.admissionlineEdit_4.text()
        year = self.admissionlineEdit_5.text()

        if student_code and last_name and first_name and middle_name and course and year:
            query = "INSERT INTO transfer_students (student_code, last_name, first_name, middle_name, course, year) VALUES (%s, %s, %s, %s, %s, %s)"
            params = (student_code, last_name, first_name, middle_name, course, year)
            db_manager.execute_query(query, params)
            self.load_table_data()
        else:
            QMessageBox.warning(self, "Input Error", "Please fill in all fields.")

    def delete_record(self):
        selected_row = self.tableWidget.currentRow()
        if selected_row >= 0:
            student_code = self.tableWidget.item(selected_row, 0).text()
            query = "DELETE FROM transfer_students WHERE student_code = %s"
            params = (student_code,)
            db_manager.execute_query(query, params)
            self.load_table_data()
        else:
            QMessageBox.warning(self, "Selection Error", "Please select a row to delete.")

    def search_record(self):
        student_code = self.admissionlineEdit.text()
        last_name = self.admissionlineEdit_2.text()
        first_name = self.admissionlineEdit_3.text()
        middle_name = self.admissionlineEdit_6.text()
        course = self.admissionlineEdit_4.text()
        year = self.admissionlineEdit_5.text()

        query = "SELECT * FROM transfer_students WHERE (student_code = %s OR %s = '') AND (last_name = %s OR %s = '') AND (first_name = %s OR %s = '') AND (middle_name = %s OR %s = '') AND (course = %s OR %s = '') AND (year = %s OR %s = '')"
        params = (student_code, student_code, last_name, last_name, first_name, first_name, middle_name, middle_name, course, course, year, year)
        records = db_manager.fetch_query(query, params)

        self.tableWidget.setRowCount(0)
        for row_data in records:
            row_position = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row_position)
            for column, data in enumerate(row_data):
                self.tableWidget.setItem(row_position, column, QTableWidgetItem(str(data)))

    def back_to_menu(self):
        self.close()

    def load_table_data(self):
        query = "SELECT * FROM transfer_students"
        records = db_manager.fetch_query(query)
        self.tableWidget.setRowCount(0)
        for row_data in records:
            row_position = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row_position)
            for column, data in enumerate(row_data):
                self.tableWidget.setItem(row_position, column, QTableWidgetItem(str(data)))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = MainWindows()
    mainWin.show()
    sys.exit(app.exec_())
