#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  7 09:39:40 2023

@author: pablo
"""

import sys
import sqlite3
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableWidgetItem

class ClassProduct(QMainWindow):
    def __init__(self, parent=None):
        super(ClassProduct, self).__init__(parent)
        loadUi("product.ui", self)
        ############### 
        ###Variables###
        ###############
        self.varProductName = self.lineEditProductName
        self.varProductCategory = self.comboBoxProductCategory
        self.varProductSupplier = self.comboBoxProductSupplier
        self.varProductInitialStock = self.lineEditProductInitialStock
        self.varProductBufferStock = self.lineEditProductBufferStock
        self.categoryList = []
        self.supplierList = []
        #############
        ###Botones###
        #############
        self.pushButtonProductAdd.clicked.connect(self.add)
        # Llama a la función para cargar las listas en los combobox
        self.fetchCategorySupplier()
        #self.loadData()         

    def fetchCategorySupplier(self):
        con = sqlite3.connect(database="inventorySystem.db")
        cur = con.cursor()
        try:
            cur.execute("SELECT name FROM category")
            cat = cur.fetchall()
            self.categoryList.append("Empty")
            self.supplierList.append("Empty")
            if len(cat) > 0:
                del self.categoryList[:]
                self.categoryList.append("Seleccionar Opcion")
                for i in cat:
                    self.categoryList.append(i[0])
                       
            cur.execute("SELECT name FROM supplier")
            sup = cur.fetchall()
            if len(sup) > 0:
                del self.supplierList[:]
                self.supplierList.append("Seleccionar Opcion")
                for i in sup:
                    self.supplierList.append(i[0])

            # Configurar las listas de proveedores y categorías en los ComboBox
            self.varProductCategory.clear()
            self.varProductCategory.addItems(self.categoryList)
            self.varProductSupplier.clear()
            self.varProductSupplier.addItems(self.supplierList)

        except Exception as ex:
            QMessageBox.critical(self, "Error", f"Error debido a: {str(ex)}")

    def add(self):
        con = sqlite3.connect(database="inventorySystem.db")
        cur = con.cursor()
        try:
            product_name = self.varProductName.text()
            product_category = self.varProductCategory.currentText()
            product_supplier = self.varProductSupplier.currentText()
            initial_stock = self.varProductInitialStock.text()

            if product_category == "Seleccionar Opcion" or product_supplier == "Seleccionar Opcion" or not product_name or not initial_stock:
                QMessageBox.critical(self, "Error", "Todos los campos son requeridos")
            else:
                cur.execute("SELECT * FROM product WHERE name = ?", (product_name,))
                row = cur.fetchone()
                if row is not None:
                    QMessageBox.critical(self, "Error", "Producto existente, elija uno diferente")
                else:
                    cur.execute("INSERT INTO product(name, category, supplier, initialStock, bufferStock) VALUES(?, ?, ?, ?, ?)",
                                (product_name, product_category, product_supplier, initial_stock, self.varProductBufferStock.text()))
                    con.commit()
                    QMessageBox.information(self, "Éxito", "Producto agregado exitosamente")
                    self.loadData()  # Recargar datos en la tabla
        except Exception as ex:
            QMessageBox.critical(self, "Error", f"Error: {str(ex)}")

    def loadData(self):
        try:
            conn = sqlite3.connect("inventorySystem.db")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM product")
            rows = cursor.fetchall()

            self.tableWidgetProduct.setRowCount(len(rows))
            self.tableWidgetProduct.setColumnCount(len(rows[0]))

            column_headers = [description[0] for description in cursor.description]
            self.tableWidgetProduct.setHorizontalHeaderLabels(column_headers)

            for i, row in enumerate(rows):
                for j, value in enumerate(row):
                    item = QTableWidgetItem(str(value))
                    self.tableWidgetProduct.setItem(i, j, item)

            conn.close()

        except sqlite3.Error as e:
            print("Error de base de datos:", e)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    product = ClassProduct()
    product.show()
    sys.exit(app.exec_())
