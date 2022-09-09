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
    sql = "select id,title,describe,code from notebook where del=0 and language=\'%s\' " % lan
    if cla:
        sql += "and class=\'%s\'" % cla
    c.execute(sql)
    notes = c.fetchall()
    conn.close()
    return [{"id": note[0], "title": note[1], "describe": note[2], "code": note[3]} for note in notes]


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
            print(k, note[k])
            note[k] = note[k].replace("'","''")
            print(k,note[k])

        sql = "insert into notebook values ( null,\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',0,%s,null,0);" % (note["language"],note["class"],note["title"],note["describe"],note["code"],note["time"])
        print(sql)
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
        print(sql)
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
    sql = "select id,title,describe,code from notebook where del=0 and title like %s or describe like %s or code like %s" % (text,text,text)
    print(sql)
    c.execute(sql)
    notes = c.fetchall()
    print(notes)
    conn.close()
    return [{"id": note[0], "title": note[1], "describe": note[2], "code": note[3]} for note in notes]

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
    words = sum([len(s[0]) for s in codes])
    conn.close()
    return nums,words

def add_note_test(database='database'):
    try:
        conn = sqlite3.connect(database)
        c = conn.cursor()
        sql = r"insert into notebook values ( null,'Python','aaa','aaa','aaa','  ''aa'' ',0,1,null,0);"
        print(sql)
        c.execute(sql)
        conn.commit()
        conn.close()
    except Exception as e:
        print(e)
        return False
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
    #get_statistic("../database")
    add_note_test("../database")

# q1 =
#
#
# data = c.fetchall()
# print(data)
# print(len(data[0]))
# conn.commit()
