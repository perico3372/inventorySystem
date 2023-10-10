#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  6 09:31:35 2023

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
        self.pushButtonLoadData.clicked.connect(self.load_data)
        self.pushButtonUpdateCategory.clicked.connect(self.update)
        
        
        
        
        # Variables para almacenar
        self.varCategoryName = self.lineEditCategoryName

    def add(self):
        con = sqlite3.connect(database="inventorySystem.db")
        cur = con.cursor()

        try:
            # Verifica si el campo requerido (nombre) está vacío.
            if self.varCategoryName.text() == "":
                QMessageBox.critical(self, "Error", "El nombre de la categoría es un campo requerido")
            else:
                # Inserta un nuevo registro en la tabla "category" incluyendo el campo "categoryName".
                cur.execute("INSERT INTO category(name) VALUES(?)",
                            (self.varCategoryName.text(),))

                # Guarda la transacción en la base de datos.
                con.commit()

                # Muestra un mensaje de éxito y carga nuevamente la información.
                QMessageBox.information(self, "Éxito", "Categoría agregada exitosamente")
                self.show()

        except Exception as ex:
            QMessageBox.critical(self, "Error", f"Error: {str(ex)}")
    
    def load_data(self):
        # Conectar a la base de datos SQLite
        try:
            conn = sqlite3.connect("inventorySystem.db")
            cursor = conn.cursor()

            # Ejecutar una consulta para seleccionar todos los registros de la tabla "employee"
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
            print("Error de base de datos:", e)


    
    def update(self):
        con = sqlite3.connect(database="inventorySystem.db")
        cur = con.cursor()
        try:
            if self.varCategoryName.text() == "":
                QMessageBox.critical(self, "Error", "El nombre de la categoría es un campo requerido")
            else:
                # Get the selected row from the tableWidgetCategory
                selected_row = self.tableWidgetCategory.currentRow()
                if selected_row >= 0:
                    # Retrieve the ID of the selected category (assuming ID is in the first column)
                    category_id = self.tableWidgetCategory.item(selected_row, 0).text()

                    # Update the category name in the database
                    cur.execute("UPDATE category SET name=? WHERE id=?", (self.varCategoryName.text(), category_id))
                    con.commit()
                    QMessageBox.information(self, "Éxito", "Datos de la categoría actualizados exitosamente")
                    self.load_data()
                else:
                    QMessageBox.warning(self, "Advertencia", "Selecciona una categoría de la lista para actualizar")
        except Exception as ex:
            QMessageBox.critical(self, "Error", f"Error: {str(ex)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    category_product = ClassCategoryProduct()
    category_product.show()
    sys.exit(app.exec_())
