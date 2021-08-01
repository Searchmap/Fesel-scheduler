import db_config.config as cfg

import mysql.connector

db = mysql.connector.connect(
		host=cfg.host,
		user=cfg.user,
		passwd=cfg.password,
		auth_plugin=cfg.auth_plugin
	)

cursor = db.cursor()

with open('./utilities/db.sql', 'r') as f:
	cursor.execute(f.read(), multi=True)
	db.commit()

cursor.close()