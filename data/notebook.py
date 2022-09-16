import sqlite3


# 连接建立的效率问题


def get_languages(database='database'):
    conn = sqlite3.connect(database)
    c = conn.cursor()
    c.execute("select distinct language from notebook where del=0;")
    languages = c.fetchall()
    conn.close()
    return [lan[0] for lan in languages]


def get_classes(lan, database='database'):
    conn = sqlite3.connect(database)
    c = conn.cursor()

    c.execute("select distinct class from notebook where del=0 and language=\'%s\';" % lan)
    classes = c.fetchall()
    conn.close()
    return [cla[0] for cla in classes]


def get_list(lan, cla=None, database='database'):
    conn = sqlite3.connect(database)
    c = conn.cursor()
    sql = "select id,title,describe,code,love,language from notebook where del=0 and language=\'%s\' " % lan
    if cla:
        sql += "and class=\'%s\'" % cla
    c.execute(sql)
    notes = c.fetchall()
    conn.close()
    return [{"id": note[0], "title": note[1], "describe": note[2], "code": note[3],"love":note[4],"lan":note[5].lower()} for note in notes]


def del_note(id, database='database'):
    try:
        conn = sqlite3.connect(database)
        c = conn.cursor()
        sql = "update notebook set del=1 where id=\'%s\' " % id
        c.execute(sql)
        conn.commit()
        conn.close()
    except Exception as e:
        print(e)
        return False
    return True


def add_note(note:dict, database='database'):
    try:
        conn = sqlite3.connect(database)
        c = conn.cursor()
        for k,v in note.items():
            note[k] = note[k].replace("'","''")
        sql = "insert into notebook values ( null,\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',0,%s,0,0,null);" % (note["language"],note["class"],note["title"],note["describe"],note["code"],note["time"])
        c.execute(sql)
        conn.commit()
        conn.close()
    except Exception as e:
        print(e)
        return False
    return True

def change_note(note, database='database'):
    try:
        conn = sqlite3.connect(database)
        c = conn.cursor()
        sql = "update notebook set language = \'%s\',class = \'%s\',title = \'%s\',describe = \'%s\',code = \'%s\',utctime = \'%s\' where id = %s;" % (note["language"],note["class"],note["title"],note["describe"],note["code"],note["time"],note["id"])
        c.execute(sql)
        conn.commit()
        conn.close()
    except Exception as e:
        print(e)
        return False
    return True


def search(text, database='database'):
    conn = sqlite3.connect(database)
    text = "'%"+text+"%'"
    c = conn.cursor()
    sql = "select id,title,describe,code,love,language from notebook where del=0 and (title like %s or describe like %s or code like %s)" % (text,text,text)
    c.execute(sql)
    notes = c.fetchall()
    conn.close()
    return [{"id": note[0], "title": note[1], "describe": note[2], "code": note[3],"love":note[4],"lan":note[5].lower()} for note in notes]

# 待处理各种查询失败
def get_a_note(id, database='database'):
    conn = sqlite3.connect(database)
    c = conn.cursor()
    sql = "select id,language,class,title,describe,code from notebook where del=0 and id=\'%s\'  limit 1" % id

    c.execute(sql)
    note = c.fetchall()
    conn.close()
    return {"id": note[0][0], "language": note[0][1], "class": note[0][2],"title": note[0][3], "describe": note[0][4], "code": note[0][5]},list(note[0][5])

def get_statistic(database='database'):
    conn = sqlite3.connect(database)
    c = conn.cursor()
    sql1 = "select count(*) from notebook "
    sql2 = "select code from notebook"
    c.execute(sql1)
    nums = c.fetchall()[0][0]
    c.execute(sql2)
    codes = c.fetchall()
    lines = 0
    for c in codes:
        lines+=len(c[0].split())+1
    conn.close()
    return nums,lines

def add_note_test(database='database'):
    try:
        conn = sqlite3.connect(database)
        c = conn.cursor()
        sql = r"insert into notebook values ( null,'Python','aaa','aaa','aaa','  ''aa'' ',0,1,null,0);"
        c.execute(sql)
        conn.commit()
        conn.close()
    except Exception as e:
        print(e)
        return False
    return True

def get_all_note(database='database'):
    conn = sqlite3.connect(database)
    c = conn.cursor()
    sql = "select * from notebook order by language,class"
    c.execute(sql)
    data = c.fetchall()
    conn.close()
    return data



def love_note(id,database='database'):
    conn = sqlite3.connect(database)
    c = conn.cursor()
    sql1 = "select love from notebook where id = \'%s\' " % id
    c.execute(sql1)
    loves = c.fetchall()[0][0]
    sql2 = "update notebook set love=%s where id=\'%s\' " % (loves+1,id)
    c.execute(sql2)
    conn.commit()
    conn.close()
    return True



if __name__ == '__main__':
    #print(get_languages('../database'))
    # print(get_classes("Python", database='../database'))
    # print(get_list("Python", database='../database'))
    # print(del_note(2, '../database'))
    # note = {"id":4,"language": "Python", "class": "noteClass", "title": "title", "describe": "describe", "code": "code",
    #         "time": "-1"}

    # print(add_note(note, database='../database'))

    # print(search("code","../database"))
    # print(get_a_note("0","../database"))
    # print(change_note(note,"../database"))
    # print(get_statistic("../database"))
    # add_note_test("../database")
    # print(get_all_note("../database"))
    print(love_note(2,"../database"))

# q1 =
#
#
# data = c.fetchall()
# print(data)
# print(len(data[0]))
# conn.commit()
