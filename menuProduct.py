import sys
import sqlite3
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QMenuBar, QMessageBox, QTableWidgetItem

class ClassProduct(QMainWindow):
    def __init__(self, parent=None):
        super(ClassProduct, self).__init__(parent)
        loadUi("product.ui", self)  # Carga el archivo .ui

        # Configura la barra de menú
        menu_bar = self.menuBar()
        archivo_menu = menu_bar.addMenu("Archivo")

        # Acción para agregar un producto
        actionAgregarProducto = QAction("Agregar Producto", self)
        actionAgregarProducto.triggered.connect(self.add)
        archivo_menu.addAction(actionAgregarProducto)

        # Conectar a la base de datos SQLite
        self.conn = sqlite3.connect("inventorySystem.db")
        self.cur = self.conn.cursor()

        # Cargar datos en la tabla al inicio
        self.load_data()

    def add(self):
        try:
            product_name = self.lineEditProductName.text()
            product_category = self.comboBoxProductCategory.currentText()
            product_supplier = self.comboBoxProductSupplier.currentText()
            initial_stock = self.lineEditProductInitialStock.text()

            if product_category == "Seleccionar" or product_supplier == "Seleccionar" or not product_name or not initial_stock:
                QMessageBox.critical(self, "Error", "Todos los campos son requeridos")
            else:
                self.cur.execute("SELECT * FROM product WHERE name = ?", (product_name,))
                row = self.cur.fetchone()
                if row is not None:
                    QMessageBox.critical(self, "Error", "Producto existente, elija uno diferente")
                else:
                    self.cur.execute("INSERT INTO product(name, category, supplier, initialStock, bufferStock) VALUES(?, ?, ?, ?, ?)",
                                     (product_name, product_category, product_supplier, initial_stock, 0))  # Cambiado 0 por bufferStock, ajusta esto según tus necesidades
                    self.conn.commit()
                    QMessageBox.information(self, "Éxito", "Producto agregado exitosamente")
                    self.load_data()
        except Exception as ex:
            QMessageBox.critical(self, "Error", f"Error: {str(ex)}")

    def load_data(self):
        try:
            self.cur.execute("SELECT * FROM product")
            products = self.cur.fetchall()

            self.tableWidgetProduct.setRowCount(len(products))
            self.tableWidgetProduct.setColumnCount(6)
            self.tableWidgetProduct.setHorizontalHeaderLabels(["ID", "Nombre", "Categoría", "Proveedor", "Stock Inicial", "Stock Mínimo"])

            for row, product in enumerate(products):
                for col, data in enumerate(product):
                    item = QTableWidgetItem(str(data))
                    self.tableWidgetProduct.setItem(row, col, item)
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Error", f"Error al cargar los datos: {str(e)}")

    def closeEvent(self, event):
        self.conn.close()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    product = ClassProduct()
    product.show()
    sys.exit(app.exec_())
