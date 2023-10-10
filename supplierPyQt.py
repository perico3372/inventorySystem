#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  6 17:07:40 2023

@author: pablo
"""



import sys
import sqlite3
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableWidgetItem

class ClassSupplier(QMainWindow):
    def __init__(self, parent=None):
        super(ClassSupplier, self).__init__(parent)
        loadUi("supplier.ui", self)

        
        self.varSupplierName = self.lineEditSupplierName
        self.varSupplierAddres = self.lineEditSupplierAddress
        self.varSupplierCity = self.lineEditSupplierCity
        self.varSupplierProvince = self.lineEditSupplierProvince
        self.varSupplierPhone = self.lineEditSupplierPhone
        self.varSupplierEmail = self.lineEditSupplierEmail
        
        
        self.pushButtonSupplierAdd.clicked.connect(self.add)
        self.pushButtonLoadData.clicked.connect(self.loadData)
        self.pushButtonSupplierUpdate.clicked.connect(self.update)
        
    def add(self):
        con = sqlite3.connect(database="inventorySystem.db")
        cur = con.cursor()

        try:
            # Verifica si el campo requerido (nombre) está vacío.
            if self.varSupplierName.text() == "":
                QMessageBox.critical(self, "Error", "Proveedor es un campo requerido")
            else:
                # Inserta un nuevo registro en la tabla "category" incluyendo el campo "categoryName".
                cur.execute("INSERT INTO supplier(name, address, city, province, phone, email) VALUES(?, ?, ?, ?, ?, ?)",
                            (self.varSupplierName.text(), 
                             self.varSupplierAddres.text(), 
                             self.varSupplierCity.text(),
                             self.varSupplierProvince.text(),
                             self.varSupplierPhone.text(),
                             self.varSupplierEmail.text()))

                # Guarda la transacción en la base de datos.
                con.commit()

                # Muestra un mensaje de éxito y carga nuevamente la información.
                QMessageBox.information(self, "Éxito", "Categoría agregada exitosamente")
                self.show()        

        except Exception as ex:
            QMessageBox.critical(self, "Error", f"Error: {str(ex)}")


    def loadData(self):
        # Conectar a la base de datos SQLite
        try:
            conn = sqlite3.connect("inventorySystem.db")
            cursor = conn.cursor()

            # Ejecutar una consulta para seleccionar todos los registros de la tabla "employee"
            cursor.execute("SELECT * FROM supplier")
            rows = cursor.fetchall()

            # Configurar la cantidad de filas y columnas en la tabla
            self.tableWidgetSupplier.setRowCount(len(rows))
            self.tableWidgetSupplier.setColumnCount(len(rows[0]))

            # Configurar encabezados de columna si es necesario
            column_headers = [description[0] for description in cursor.description]
            self.tableWidgetSupplier.setHorizontalHeaderLabels(column_headers)

            # Llenar la tabla con los datos de la base de datos
            for i, row in enumerate(rows):
                for j, value in enumerate(row):
                    item = QTableWidgetItem(str(value))
                    self.tableWidgetSupplier.setItem(i, j, item)

            conn.close()

        except sqlite3.Error as e:
            print("Error de base de datos:", e)

#
    def update(self):
        con = sqlite3.connect(database="inventorySystem.db")
        cur = con.cursor()
        try:
            if self.varSupplierName.text() == "":
                QMessageBox.critical(self, "Error", "El nombre del proveedor es un campo requerido")
            else:
                # Get the selected row from the tableWidgetSupplier
                selected_row = self.tableWidgetSupplier.currentRow()
                if selected_row >= 0:
                    # Retrieve the ID of the selected supplier (assuming ID is in the first column)
                    supplierId = self.tableWidgetSupplier.item(selected_row, 0).text()

                    # Update the specific field in the database
                    field_to_update = "name"  # Cambia esto al campo específico que deseas actualizar
                    new_value = self.varSupplierName.text()

                    cur.execute(f"UPDATE supplier SET {field_to_update}=? WHERE id=?", 
                                (new_value, supplierId
                                ))

                    con.commit()
                    QMessageBox.information(self, "Éxito", f"Campo {field_to_update} actualizado exitosamente")
                    self.loadData()
                else:
                    QMessageBox.warning(self, "Advertencia", "Selecciona un proveedor de la lista para actualizar")
        except Exception as ex:
            QMessageBox.critical(self, "Error", f"Error: {str(ex)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    supplier = ClassSupplier()
    supplier.show()
    sys.exit(app.exec_())



if __name__ == "__main__":
    app = QApplication(sys.argv)
    supplier = ClassSupplier()
    supplier.show()
    sys.exit(app.exec_())

    