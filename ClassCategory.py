#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  9 17:23:58 2023

@author: pablo
"""

import sys
import sqlite3
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableWidgetItem

class ClassCategoryProductAdd(QMainWindow):
    def __init__(self, parent=None):
        super(ClassCategoryProductAdd, self).__init__(parent)
        loadUi("category/categoryAdd.ui", self)

        self.pushButtonCategoryProductAdd.clicked.connect(self.add)
        self.actionAltaCategoriaProducto.triggered.connect(self.add)

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
            
            
if __name__ == "__main__":
    app = QApplication(sys.argv)
    category_product = ClassCategoryProductAdd()
    category_product.show()
    sys.exit(app.exec_())