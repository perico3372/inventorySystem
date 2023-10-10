#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  5 16:31:47 2023

@author: pablo
"""

import sys
import sqlite3
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtCore import Qt


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

            if product_category == "Seleccionar" or product_supplier == "Seleccionar" or not product_name or not initial_stock:
                QMessageBox.critical(self, "Error", "Todos los campos son requeridos")
            else:
                cur.execute("SELECT * FROM product WHERE name = ?", (product_name,))
                row = cur.fetchone()
                if row is not None:
                    QMessageBox.critical(self, "Error", "Producto existente, elija uno diferente")
                else:
                    cur.execute("INSERT INTO product(name, category, supplier, initialStock, bufferStock) VALUES(?, ?, ?, ?, ?)",
                                (product_category, product_supplier, product_name, initial_stock))
                    con.commit()
                    QMessageBox.information(self, "Éxito", "Producto agregado exitosamente")
        except Exception as ex:
            QMessageBox.critical(self, "Error", f"Error: {str(ex)}")
            
    def loadData(self):
        # Conectar a la base de datos SQLite
        try:
            conn = sqlite3.connect("inventorySystem.db")
            cursor = conn.cursor()

            # Ejecutar una consulta para seleccionar todos los registros de la tabla "employee"
            cursor.execute("SELECT * FROM product")
            rows = cursor.fetchall()

            # Configurar la cantidad de filas y columnas en la tabla
            self.tableWidgetProduct.setRowCount(len(rows))
            self.tableWidgetProduct.setColumnCount(len(rows[0]))

            # Configurar encabezados de columna si es necesario
            column_headers = [description[0] for description in cursor.description]
            self.tableWidgetProduct.setHorizontalHeaderLabels(column_headers)

            # Llenar la tabla con los datos de la base de datos
            for i, row in enumerate(rows):
                for j, value in enumerate(row):
                    item = QTableWidgetItem(str(value))
                    self.tableWidgetProduct.setItem(i, j, item)

            conn.close()

        except sqlite3.Error as e:
            print("Error de base de datos:", e)



            
    def update(self):
        con = sqlite3.connect(database="inventorySystem.db")
        cur = con.cursor()
        try:
            product_id = self.varProductId.text()
            product_name = self.varProductName.text()
            product_category = self.varProductCategory.currentText()
            product_supplier = self.varProductSupplier.currentText()
            product_price = self.varProductPrice.text()
            product_quantity = self.varProductQuantity.text()
    
            if not product_id and not product_name:
                QMessageBox.critical(self, "Error", "ID Producto o Nombre del Producto son campos requeridos")
            else:
                if product_id:
                    cur.execute("SELECT * FROM product WHERE idProduct = ?", (product_id,))
                elif product_name:
                    cur.execute("SELECT * FROM product WHERE name = ?", (product_name,))
                
                row = cur.fetchone()
                if row is None:
                    QMessageBox.critical(self, "Error", "Producto no encontrado")
                else:
                    cur.execute("UPDATE product SET category=?, supplier=?, name=?, price=?, quantity=? WHERE idProduct=?",
                                (product_category, product_supplier, product_name, product_price, product_quantity, row[0]))
                    con.commit()
                    QMessageBox.information(self, "Éxito", "Datos actualizados del producto exitosamente")
        except Exception as ex:
            QMessageBox.critical(self, "Error", f"Error: {str(ex)}")
    




    def delete(self):
        con = sqlite3.connect(database="inventorySystem.db")
        cur = con.cursor()
        try:
            if self.varSupplierInvoice.get() == "" or self.varSupplierName.get() == "":
                QMessageBox.critical(self, "Error", "ID del empleado y Nombre son campos requeridos")
            else:
                cur.execute("SELECT * FROM supplier where invoice =?", (self.varSupplierInvoice.get(),))
                row = cur.fetchone()
                if row is None:
                    QMessageBox.critical(self, "Error", "ID de producto no válido")
                else:
                    op = QMessageBox.question(self, "Confirmar", "¿Realmente quiere borrar el registro del producto?", QMessageBox.Yes | QMessageBox.No)
                    if op == QMessageBox.Yes:
                        cur.execute("DELETE FROM supplier where invoice =?", (self.varSupplierInvoice.get(),))
                        con.commit()
                        QMessageBox.information(self, "Éxito", "Producto eliminado satisfactoriamente")
                        self.show()
        except Exception as ex:
            QMessageBox.critical(self, "Error", f"Error: {str(ex)}")






if __name__ == "__main__":
    app = QApplication(sys.argv)
    product = ClassProduct()
    product.show()
    sys.exit(app.exec_())
