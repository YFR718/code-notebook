# import sqlite3
#
#
# conn = sqlite3.connect('../database')
# c = conn.cursor()
# c.execute("insert into templates values ( null,'Python','test2','test2','test2','print(\"hello word\")',0,0,null);" )
# conn.commit()
# conn.close()
import hashlib

s = "123"

def sha256(s):
    sha = hashlib.sha256()
    sha.update(s.encode("utf-8"))
    return sha.hexdigest()

print(sha256(s))