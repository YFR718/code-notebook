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


def add_note(note, database='database'):
    try:
        conn = sqlite3.connect(database)
        c = conn.cursor()
        sql = "insert into notebook values ( null,\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',0,%s,null,0);" % (note["language"],note["class"],note["title"],note["describe"],note["code"],note["time"])
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


if __name__ == '__main__':
    # print(get_languages('../database'))
    # print(get_classes("Python", database='../database'))
    # print(get_list("Python", database='../database'))
    # print(del_note(2, '../database'))
    # note = {"language": "Python", "class": "noteClass", "title": "title", "describe": "describe", "code": "code",
    #         "time": "-1"}
    #
    # print(add_note(note, database='../database'))

    print(search("code","../database"))

# q1 =
#
#
# data = c.fetchall()
# print(data)
# print(len(data[0]))
# conn.commit()
