#!/usr/bin/env python
# -*- coding: utf8 -*-

import sqlite3
import time
import RPi.GPIO as GPIO
import MFRC522
import os

con = sqlite3.connect('NFC_GATOR_DATABASE.db')
con.row_factory = sqlite3.Row
cur = con.cursor()

MIFAREReader = MFRC522.MFRC522()

Edit = False
Read = False

cur.execute(" CREATE TABLE IF NOT EXISTS Osoby (id INTEGER PRIMARY KEY ASC,nazwa varchar(250) NOT NULL, rfid INTEGER NOT NULL)")


os.system('clear')
print "Co chcesz zrobic?"
print "1. Edytuj baze tagow"
print "2. Wczytaj istniejacy"
wybor = raw_input("Wybor: ")
if wybor == '1':
	Edit = True
if wybor == '2':
	Read = True
os.system('clear')


while Edit:
	

	print "1. Dodaj tag"
	print "2. Usun tag"
	print "3. Lista osob"
	print "4. Wyjdz"
	wybor = raw_input("Wybor: ")


	if wybor == '1':
		os.system('clear')
		print "Przyloz tag do czytnika"
		Write = True
		while Write:
			
			(status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

			(status,uid) = MIFAREReader.MFRC522_Anticoll()
			if status == MIFAREReader.MI_OK:
				print "Wykryto tag"
				ID = int(str(uid[0]) + str(uid[1]) + str(uid[2]) + str(uid[3]))
				cur.execute('SELECT Osoby.rfid FROM Osoby') 
				r = cur.fetchall()
				registered = False
				for rfid in r:
					if str(rfid['rfid']) == str(ID):
						print "Ten tag zostal juz zarejestrowany"
						print ""
						registered = True
						break
				if registered == False:	
						nazwa = raw_input("Nazwa nowego uzytkownika dla %s: "% (ID))
						cur.execute('INSERT INTO Osoby VALUES(NULL, ?,?);', (nazwa, ID))
						con.commit()
						print "Zarejestrowno nowego uzytkownika"
						print ""
				Write = False

	if wybor == '2':
		os.system('clear')
		print "Lista osob: "
		cur.execute('SELECT Osoby.rfid,nazwa FROM Osoby')
		osoby = cur.fetchall()
		for osoba in osoby:
			print osoba['rfid'], osoba['nazwa']
		print ""
		wybor = raw_input("""Wpisz rfid osoby by ja usunac, lub "exit" by wyjsc: """)
		if wybor != 'exit':
			for osoba in osoby:
				if wybor == str(osoba['rfid']):
					cur.execute('DELETE FROM Osoby WHERE rfid=?', (wybor,))
					con.commit()
					print "Usunieto"
					print ""
					break
		else:
			break

	if wybor == '3':
		os.system('clear')
		print "Lista osob: "
		cur.execute('SELECT Osoby.rfid,nazwa FROM Osoby')
		osoby = cur.fetchall()
		for osoba in osoby:
			print osoba['rfid'], osoba['nazwa']

	if wybor == '4':
		break
		
os.system('clear')
print "Przyloz tag do czytnika"

while Read:
	
	(status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
	Exists = True
	(status,uid) = MIFAREReader.MFRC522_Anticoll()
	if status == MIFAREReader.MI_OK:
		print "Wykryto tag"
		ID = str(uid[0]) + str(uid[1]) + str(uid[2]) + str(uid[3])	
		cur.execute('SELECT Osoby.rfid FROM Osoby') 
		r = cur.fetchall()
		for rfid in r:
			if str(rfid['rfid']) == ID:
				cur.execute('SELECT Osoby.nazwa FROM Osoby WHERE Osoby.rfid=?', (ID,))
				K = cur.fetchone()[0]
				print "Tag rozpoznany"
				print "Witaj " + K + " :D"
				Exists = True
				break
			else:
				Exists = False

		if Exists == False:
			print "Nie rozpoznano tagu :C"	
		print ""
		print "Przyloz tag do czytnika"
	
	time.sleep(1)

os.system('clear')


