import sys
import sqlite3
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QApplication, QMessageBox, QAction, QMainWindow
from PyQt5.QtCore import Qt

from ClassCategory import *

class ClassMain(QMainWindow):
    def __init__(self, parent=None):
        super(ClassMain, self).__init__(parent)
        loadUi("main.ui", self)
    
        # Configura la barra de menú
        menu_bar = self.menuBar()
        archivo_menu = menu_bar.addMenu("Categoría")

        # Acción para agregar categoría de producto
        actionCategoryProductAdd = QAction("actionAltaCategoriaDeProducto", self)
        actionCategoryProductAdd.triggered.connect(self.openCategoryProductAdd)
        archivo_menu.addAction(actionCategoryProductAdd)    

    def openCategoryProductAdd(self):
        # Crea una instancia de ClassCategoryProductAdd y muestra la ventana
        category_add_window = ClassCategoryProductAdd()
        category_add_window.show()    
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    product = ClassMain()
    product.show()
    sys.exit(app.exec_())
