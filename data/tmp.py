import sqlite3


conn = sqlite3.connect('../database')
c = conn.cursor()
c.execute("insert into notebook values ( null,'Python','test2','test2','test2','print(\"hello word\")',0,0,null);" )
conn.commit()
conn.close()
