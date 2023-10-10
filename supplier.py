#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  1 05:15:26 2023

@author: pablo
"""

from tkinter import *
from tkinter import ttk, messagebox
import sqlite3

class SupplierClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x800+220+130")
        self.root.title("Sistema de Inventario | Desarrollado por Pablo Perez")
        self.root.config(bg="white")
        self.root.focus_force()

        # Variables
        self.varSupplierInvoice = StringVar()
        self.varSupplierName = StringVar()
        self.varSupplierContact = StringVar()
        self.varSupplierDescription = StringVar()
        self.varSearchBy = StringVar()
        self.varSearchTxt = StringVar()

        # Buscar Proveedor
        searchFrame = LabelFrame(self.root, text="Buscar empleado", font=("arial", 12, "bold"), bd=2, relief=RIDGE,
                                 bg="white")
        searchFrame.place(x=250, y=20, width=600, height=70)

        # Opciones
        cmbSearch = ttk.Combobox(searchFrame, textvariable=self.varSearchBy,
                                 values=("Seleccionar opciones", "Nombre", "ID"), state="readonly",
                                 justify=CENTER, font=("arial", 15))
        cmbSearch.place(x=10, y=10, width=180)
        cmbSearch.current(0)

        txtSearch = Entry(searchFrame, textvariable=self.varSearchTxt, font=("times new roman", 15), bg="lightyellow")
        txtSearch.place(x=200, y=10)

        buttonSearch = Button(searchFrame, text="Buscar", command=self.search, font=("times new roman", 15),
                              bg="#4caf50", fg="white", cursor="hand2")
        buttonSearch.place(x=410, y=9, width=150, height=30)

        # Titulo
        title = Label(self.root, text="Detalles proveedores", font=("times new roman", 15), bg="#0f4d7d", fg="white")
        title.place(x=50, y=100, width=1000)

        # Contenido
        labels = ["No. Factura", "Nombre", "Contacto", "Descripcion"]
        y_position = 200

        for label_text in labels:
            label = Label(self.root, text=label_text, font=("times new roman", 15), bg="white")
            label.place(x=0, y=y_position)

            if label_text == "Descripción":
                entry = Text(self.root, font=("times new roman", 15), bg="lightyellow", height=4)
                entry.place(x=150, y=y_position, width=180)
                self.varSupplierDescription = entry
            else:
                entry = Entry(self.root, font=("times new roman", 15), bg="lightyellow", textvariable=self.varSupplierInvoice if label_text == "No. Factura" else None)
                entry.place(x=150, y=y_position, width=180)
                if label_text == "Nombre":
                    self.varSupplierName = entry

                elif label_text == "Contacto":
                    self.varSupplierContact = entry

            y_position += 50

        # Botones
        buttons = ["Guardar", "Actualizar", "Borrar", "Limpiar"]
        x_positions = [500, 620, 740, 860]

        for button_text, x_pos in zip(buttons, x_positions):
            button = Button(self.root, text=button_text, command=lambda t=button_text: self.button_click(t), font=("times new roman", 15),
                            bg="#4caf50", fg="white", cursor="hand2")
            button.place(x=x_pos, y=405, width=150, height=30)

        # Detalles empleados
        employeeFrame = Frame(self.root, bd=3, relief=RIDGE)
        employeeFrame.place(x=0, y=600, relwidth=1, height=150)

        scrollX = Scrollbar(employeeFrame, orient=HORIZONTAL)
        scrollY = Scrollbar(employeeFrame, orient=VERTICAL)

        # Crear la tabla de proveedores

        self.supplierTable = ttk.Treeview(employeeFrame, columns=("invoice", "name", "contact", "desc"),
                                          yscrollcommand=scrollY.set, xscrollcommand=scrollX.set)

        scrollX.pack(side=BOTTOM, fill=X)
        scrollY.pack(side=RIGHT, fill=Y)
        scrollX.config(command=self.supplierTable.xview)
        scrollY.config(command=self.supplierTable.yview)

        self.supplierTable.heading("invoice", text="No. de factura")
        self.supplierTable.heading("name", text="Nombre")
        self.supplierTable.heading("contact", text="Contacto")
        self.supplierTable.heading("desc", text="Descripcion")

        self.supplierTable["show"] = "headings"
        self.supplierTable.pack(fill=BOTH, expand=1)

        columns_width = [90, 90, 90, 180]

        for col, width in zip(self.supplierTable["columns"], columns_width):
            self.supplierTable.column(col, width=width)

        self.supplierTable.pack(fill=BOTH, expand=1)
        self.supplierTable.bind("<ButtonRelease-1>", self.get_data)
        self.show()

    def button_click(self, button_text):
        if button_text == "Guardar":
            self.add()
        elif button_text == "Actualizar":
            self.update()
        elif button_text == "Borrar":
            self.delete()
        elif button_text == "Limpiar":
            self.clear()

    def add(self):
        con = sqlite3.connect(database="inventorySystem.db")
        cur = con.cursor()
        try:
            if self.varSupplierInvoice.get() == "": #or self.varSupplierName.get() == "":
                messagebox.showerror("Error", "El No. de factura es un campo requerido", parent=self.root)
            else:
                cur.execute("SELECT * FROM supplier where invoice =?", (self.varSupplierInvoice.get(),))
                row = cur.fetchone()
                if row is not None:
                    messagebox.showerror("Error", "Este empleado tiene un ID asignado, elija uno diferente", parent=self.root)
                else:
                    cur.execute("INSERT INTO supplier(invoice, name, contact, desc) VALUES(?, ?, ?, ?)",
                                (self.varSupplierInvoice.get(), self.varSupplierName.get(), self.varSupplierContact.get(), self.varSupplierDescription.get()))
                    con.commit()
                    messagebox.showinfo("Éxito", "Proveedor agregado exitosamente", parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error: {str(ex)}")

    def show(self):
        con = sqlite3.connect(database="inventorySystem.db")
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM supplier")
            rows = cur.fetchall()
            self.supplierTable.delete(*self.supplierTable.get_children())
            for row in rows:
                self.supplierTable.insert("", END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error debido a: {str(ex)}", parent=self.root)

    def get_data(self, ev):
        f = self.supplierTable.focus()
        content = (self.supplierTable.item(f))
        row = content["values"]
        self.varSupplierInvoice.set(row[0])
        self.varSupplierName.set(row[1])
        self.varSupplierContact.set(row[2])
        self.varSupplierDescription.set(row[3])

    def update(self):
        con = sqlite3.connect(database="inventorySystem.db")
        cur = con.cursor()
        try:
            if self.varSupplierInvoice.get() == "" or self.varSupplierName.get() == "":
                messagebox.showerror("Error", "Invoice son campos requeridos", parent=self.root)
            else:
                cur.execute("SELECT * FROM supplier where invoice =?", (self.varSupplierInvoice.get(),))
                row = cur.fetchone()
                if row is None:
                    messagebox.showerror("Error", "Invoice no válido", parent=self.root)
                else:
                    cur.execute("UPDATE supplier SET name=?, contact=?, desc=? WHERE invoice=?",
                                (self.varSupplierName.get(), self.varSupplierContact.get(), self.varSupplierDescription.get(),  self.varSupplierInvoice.get()))
                    con.commit()
                    messagebox.showinfo("Éxito", "Datos de empleado actualizados exitosamente", parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error: {str(ex)}", parent=self.root)

    def delete(self):
        con = sqlite3.connect(database="inventorySystem.db")
        cur = con.cursor()
        try:
            if self.varSupplierInvoice.get() == "" or self.varSupplierName.get() == "":
                messagebox.showerror("Error", "ID del empleado y Nombre son campos requeridos", parent=self.root)
            else:
                cur.execute("SELECT * FROM supplier where invoice =?", (self.varSupplierInvoice.get(),))
                row = cur.fetchone()
                if row is None:
                    messagebox.showerror("Error", "ID de empleado no válido", parent=self.root)
                else:
                    op = messagebox.askyesno("Confirmar", "¿Realmente quiere borrar el registro del empleado?", parent=self.root)
                    if op:
                        cur.execute("DELETE FROM supplier where invoice =?", (self.varSupplierInvoice.get(),))
                        con.commit()
                        messagebox.showinfo("Éxito", "Empleado eliminado satisfactoriamente", parent=self.root)
                        self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error: {str(ex)}", parent=self.root)

    def clear(self):
        self.varSupplierInvoice.set("")
        self.varSupplierName.set("")
        self.varSupplierContact.set("1.0", END)
        self.varSupplierDescription.set("")
        self.varSearchTxt.set("")
        self.varSearchBy.set("Seleccionar opciones")
        self.show()

    def search(self):
        con = sqlite3.connect(database="inventorySystem.db")
        cur = con.cursor()
        try:
            if self.varSearchBy.get() == "Seleccionar opciones":
                messagebox.showerror("Error", "Seleccione una opción", parent=self.root)
            elif self.varSearchTxt.get() == "":
                messagebox.showerror("Error", "El campo de búsqueda es requerido", parent=self.root)
            else:
                cur.execute("SELECT * FROM supplier WHERE " + self.varSearchBy.get() + " LIKE '%" + self.varSearchTxt.get() + "%'")
                rows = cur.fetchall()
                if len(rows) != 0:
                    self.supplierTable.delete(*self.supplierTable.get_children())
                    for row in rows:
                        self.supplierTable.insert("", END, values=row)
                else:
                    messagebox.showerror("Error", "No se encontraron resultados")
        except Exception as ex:
            messagebox.showerror("Error", f"Error: {str(ex)}", parent=self.root)

if __name__ == "__main__":
    root = Tk()
    obj = SupplierClass(root)
    root.mainloop()
