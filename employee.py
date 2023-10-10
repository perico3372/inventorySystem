#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  5 15:24:36 2023

@author: pablo
"""

import sys
import sqlite3
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableWidgetItem

class ClassEmployee(QMainWindow):
    def __init__(self, parent=None):
        super(ClassEmployee, self).__init__(parent)
        loadUi("employee.ui", self)

        self.pushButtonSave.clicked.connect(self.add)
        self.pushButtonUpdate.clicked.connect(self.update)
        self.pushButtonDelete.clicked.connect(self.delete)
        self.pushButtonClear.clicked.connect(self.clear_input_fields)
        self.pushButtonSearch.clicked.connect(self.search_by_id_or_name)
        self.pushButtonClearTable.clicked.connect(self.clearTable)
        self.pushButtonLoadData.clicked.connect(self.load_data)

        # Elementos de interfaz para eliminar por ID o nombre
        self.lineEditSearch = self.lineEditSearch
        self.pushButtonSearch = self.pushButtonSearch
        self.pushButtonSearch.clicked.connect(self.delete_by_id_or_name)

        # Variables para almacenar datos
        self.varId = self.lineEditIdEmployee
        self.varName = self.lineEditName
        self.varGenre = self.comboBoxGenre
        self.varAddress = self.lineEditAddress
        self.varPhone = self.lineEditPhone
        self.varUserType = self.comboBoxUserType
        self.varPassword = self.lineEditPassword

        # Llamar al método show para cargar los datos al inicio
        self.show()
        self.load_data()
        self.clear_input_fields()
        #self.employeeTable.itemClicked.connect(self.get_data)

    def add(self):
        con = sqlite3.connect(database="inventorySystem.db")
        cur = con.cursor()
        try:
            if self.varId.text() == "" or self.varName.text() == "":
                QMessageBox.critical(self, "Error", "ID del empleado y Nombre son campos requeridos")
            else:
                cur.execute("SELECT * FROM employee WHERE id = ?", (self.varId.text(),))
                row = cur.fetchone()
                if row is not None:
                    QMessageBox.critical(self, "Error", "Este empleado tiene un ID asignado, elija uno diferente")
                else:
                    cur.execute("INSERT INTO employee(id, name, genre, address, phone, userType, password) VALUES(?, ?, ?, ?, ?, ?, ?)",
                                (self.varId.text(), self.varName.text(), self.varGenre.currentText(), self.varAddress.text(), self.varPhone.text(), self.varUserType.currentText(), self.varPassword.text()))
                    con.commit()
                    QMessageBox.information(self, "Éxito", "Empleado agregado exitosamente")
                    self.load_data()
        except Exception as ex:
            QMessageBox.critical(self, "Error", f"Error: {str(ex)}")

    def load_data(self):
        # Conectar a la base de datos SQLite
        try:
            conn = sqlite3.connect("inventorySystem.db")
            cursor = conn.cursor()

            # Ejecutar una consulta para seleccionar todos los registros de la tabla "employee"
            cursor.execute("SELECT * FROM employee")
            rows = cursor.fetchall()

            # Configurar la cantidad de filas y columnas en la tabla
            self.employeeTable.setRowCount(len(rows))
            self.employeeTable.setColumnCount(len(rows[0]))

            # Configurar encabezados de columna si es necesario
            column_headers = [description[0] for description in cursor.description]
            self.employeeTable.setHorizontalHeaderLabels(column_headers)

            # Llenar la tabla con los datos de la base de datos
            for i, row in enumerate(rows):
                for j, value in enumerate(row):
                    item = QTableWidgetItem(str(value))
                    self.employeeTable.setItem(i, j, item)

            conn.close()

        except sqlite3.Error as e:
            print("Error de SQLite:", e)

    def update(self):
        con = sqlite3.connect(database="inventorySystem.db")
        cur = con.cursor()
        try:
            if self.varId.text() == "" or self.varName.text() == "":
                QMessageBox.critical(self, "Error", "ID del empleado y Nombre son campos requeridos")
            else:
                cur.execute("SELECT * FROM employee WHERE id = ?", (self.varId.text(),))
                row = cur.fetchone()
                if row is None:
                    QMessageBox.critical(self, "Error", "ID de empleado no válido")
                else:
                    cur.execute("UPDATE employee SET name=?, genre=?, address=?, phone=?, userType=?, password=? WHERE id=?",
                                (self.varName.text(), self.varGenre.currentText(), self.varAddress.text(), self.varPhone.text(), self.varUserType.currentText(), self.varPassword.text(), self.varId.text()))
                    con.commit()
                    QMessageBox.information(self, "Éxito", "Datos de empleado actualizados exitosamente")
                    self.load_data()
        except Exception as ex:
            QMessageBox.critical(self, "Error", f"Error: {str(ex)}")

    def delete(self):
        con = sqlite3.connect(database="inventorySystem.db")
        cur = con.cursor()
        try:
            selected_row = self.employeeTable.currentRow()
            if selected_row >= 0:
                employee_id = self.employeeTable.item(selected_row, 0).text()
                cur.execute("DELETE FROM employee WHERE id = ?", (employee_id,))
                con.commit()
                QMessageBox.information(self, "Éxito", "Empleado eliminado satisfactoriamente")
                self.load_data()
                self.clear_input_fields()
            else:
                QMessageBox.critical(self, "Error", "Por favor, seleccione una fila para eliminar.")
        except Exception as ex:
            QMessageBox.critical(self, "Error", f"Error: {str(ex)}")

    def delete_by_id_or_name(self):
        con = sqlite3.connect(database="inventorySystem.db")
        cur = con.cursor()
        try:
            search_value = self.lineEditSearch.text()
            if search_value == "":
                QMessageBox.critical(self, "Error", "Por favor, ingrese un ID o nombre para buscar.")
            else:
                cur.execute("SELECT * FROM employee WHERE id = ? OR name = ?", (search_value, search_value))
                rows = cur.fetchall()
                if not rows:
                    QMessageBox.information(self, "Información", "No se encontraron registros para eliminar.")
                else:
                    op = QMessageBox.question(self, "Confirmar", f"¿Realmente quiere borrar los siguientes registros?\n{', '.join([str(row[0]) for row in rows])}")
                    if op == QMessageBox.Yes:
                        for row in rows:
                            cur.execute("DELETE FROM employee WHERE id = ?", (row[0],))
                        con.commit()
                        QMessageBox.information(self, "Éxito", "Registros eliminados satisfactoriamente.")
                        self.load_data()
                        self.clear_input_fields()
        except Exception as ex:
            QMessageBox.critical(self, "Error", f"Error: {str(ex)}")

    def clear_input_fields(self):
        self.varId.clear()
        self.varName.clear()
        self.varAddress.clear()
        self.varPhone.clear()
        self.varPassword.clear()
        self.varGenre.setCurrentIndex(0)
        self.varUserType.setCurrentIndex(0)

    def search_by_id_or_name(self):
        con = sqlite3.connect(database="inventorySystem.db")
        cur = con.cursor()
        try:
            search_value = self.lineEditSearch.text()
            if search_value == "":
                QMessageBox.critical(self, "Error", "Por favor, ingrese un ID o nombre para buscar.")
            else:
                cur.execute("SELECT * FROM employee WHERE id = ? OR name = ?", (search_value, search_value))
                rows = cur.fetchall()
                if not rows:
                    QMessageBox.information(self, "Información", "No se encontraron registros.")
                else:
                    self.clearTable()
                    self.populate_table(rows)
        except Exception as ex:
            QMessageBox.critical(self, "Error", f"Error: {str(ex)}")

    def clearTable(self):
        self.employeeTable.setRowCount(0)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    employee = ClassEmployee()
    employee.show()
    sys.exit(app.exec_())
