#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 30 12:39:19 2023

@author: pablo
"""

import sqlite3

def createDB():
    con = sqlite3.connect(database="inventorySystem.db")
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS employee (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, genre TEXT, address TEXT, phone TEXT, userType TEXT, password TEXT)")
    con.commit()

    cur.execute("CREATE TABLE IF NOT EXISTS supplier (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, address TEXT, city TEXT, province TEXT, phone TEXT, email TEXT)")
    con.commit()
    
    cur.execute("CREATE TABLE IF NOT EXISTS category (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT)")
    con.commit()

    cur.execute("CREATE TABLE IF NOT EXISTS product (idProduct INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, category TEXT, supplier TEXT, initialStock TEXT, bufferStock TEXT)")
    con.commit()    
    
createDB()


