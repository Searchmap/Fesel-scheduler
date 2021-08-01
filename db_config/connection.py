import db_config.config as cfg

import mysql.connector

def connect():
	try:
		db = mysql.connector.connect(
			host=cfg.host,
			user=cfg.user,
			passwd=cfg.password,
			database=cfg.database,
			auth_plugin=cfg.auth_plugin
		)
	except mysql.connector.Error as e:
		print(e)

	return db

def deconnect(db, cursor):
	if db.is_connected():
		cursor.close()
		db.close()