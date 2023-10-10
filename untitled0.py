#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  6 08:58:58 2023

@author: pablo
"""


import sys
import sqlite3
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableWidgetItem

class ClassCategoryProduct(QMainWindow):
    def __init__(self, parent=None):
        super(ClassCategoryProduct, self).__init__(parent)
        loadUi("category.ui", self)

        self.pushButtonAddCategory.clicked.connect(self.add)
       # self.pushButtonDeleteCategory.clicked.connect(self.update)
      #  self.pushButtonUpdateCategory.clicked.connect(self.delete)
     #   self.pushButtonClear.clicked.connect(self.clear_input_fields)
      #  self.pushButtonSearch.clicked.connect(self.search_by_id_or_name)
       # self.pushButtonClearTable.clicked.connect(self.clearTable)
        #self.pushButtonLoadData.clicked.connect(self.load_data)
        
        ##########################
        ###variables a almacenar##
        ##########################
        self.varCategoryId = self.lineEditCategoryId
        self.varCategoryName = self.lineEditCategoryName

    def add(self):
        con = sqlite3.connect(database="inventorySystem.db")
        cur = con.cursor()
    
        try:
            # Verifica si los campos requeridos (nombre en este caso) están vacíos.
            if self.varCategoryName.text() == "":
                QMessageBox.critical(self, "Error", "El nombre del empleado es un campo requerido")
            else:
                # Inserta un nuevo registro en la tabla "employee" sin incluir el campo "id".
                cur.execute("INSERT INTO category(categoryName) VALUES(?)",
                            (self.varName.text()))
    
                # Guarda la transacción en la base de datos.
                con.commit()
    
                # Muestra un mensaje de éxito y carga nuevamente la información.
                QMessageBox.information(self, "Éxito", "Categoria agregada exitosamente")
                self.load_data()
    
        except Exception as ex:
            QMessageBox.critical(self, "Error", f"Error: {str(ex)}")

    def show(self):
        # Conectar a la base de datos SQLite
        try:
            conn = sqlite3.connect("inventorySystem.db")
            cursor = conn.cursor()

            # Ejecutar una consulta para seleccionar todos los registros de la tabla "category"
            cursor.execute("SELECT * FROM category")
            rows = cursor.fetchall()

            # Configurar la cantidad de filas y columnas en la tabla
            self.tableWidgetCategory.setRowCount(len(rows))
            self.tableWidgetCategory.setColumnCount(len(rows[0]))

            # Configurar encabezados de columna si es necesario
            column_headers = [description[0] for description in cursor.description]
            self.tableWidgetCategory.setHorizontalHeaderLabels(column_headers)

            # Llenar la tabla con los datos de la base de datos
            for i, row in enumerate(rows):
                for j, value in enumerate(row):
                    item = QTableWidgetItem(str(value))
                    self.tableWidgetCategory.setItem(i, j, item)

            conn.close()

        except sqlite3.Error as e:
            print("Error de SQLite:", e)

            
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    employee = ClassCategoryProduct()
    employee.show()
    sys.exit(app.exec_())