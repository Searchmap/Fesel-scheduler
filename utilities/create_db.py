from db_config.connection import connect, deconnect

db = connect()
cursor = db.cursor()

with open('utilities/db.sql', 'r') as f:
	cursor.execute(f.read(), multi=True)
	db.commit()

deconnect(db, cursor)