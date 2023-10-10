#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  8 17:25:22 2023

@author: pablo
"""

    def agregar_producto(self):
        # Implementa la lógica para agregar un producto aquí
        # Puedes acceder a elementos de la interfaz de usuario, como self.varProductName.text()
        # Asegúrate de validar y agregar los datos correctamente a la base de datos

        # Por ejemplo, aquí se muestra cómo insertar un nuevo producto
        product_name = self.lineEditProductName.text()
        product_category = self.comboBoxProductCategory.currentText()
        product_supplier = self.comboBoxProductSupplier.currentText()
        product_initial_stock = self.lineEditProductInitialStock.text()
        product_buffer_stock = self.lineEditProductBufferStock.text()

        if not product_name or not product_initial_stock or not product_buffer_stock:
            QMessageBox.critical(self, "Error", "Todos los campos son requeridos")
            return

        try:
            self.cur.execute("INSERT INTO product (name, category, supplier, initialStock, bufferStock) VALUES (?, ?, ?, ?, ?)",
                             (product_name, product_category, product_supplier, product_initial_stock, product_buffer_stock))
            self.conn.commit()
            QMessageBox.information(self, "Éxito", "Producto agregado exitosamente")
            self.clear_fields()
            self.load_data()
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Error", f"Error al agregar el producto: {str(e)}")