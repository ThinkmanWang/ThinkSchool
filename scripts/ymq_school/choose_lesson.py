# -*- coding: utf-8 -*-

import random

import pymysql

from pythinkutils.mysql.ThinkMysql import ThinkMysql
from pythinkutils.common.log import g_logger
from pythinkutils.common.object2json import *

def rand_course(nNum):
    setCourse = set()
    while len(setCourse) < nNum:
        setCourse.add(random.randint(1, 20))

    return setCourse

def rand_teacher(nCourse):
    conn = ThinkMysql.get_conn_pool_ex().connection("")
    c = conn.cursor(pymysql.cursors.DictCursor)

    try:
        c.execute('''
            select * from lesson_choose where l_id = %s ORDER BY RAND() LIMIT 1
        ''', (nCourse, ))

        rows = c.fetchall()

        return rows[0]
    except Exception as e:
        g_logger.error(e)
        return None
    finally:
        conn.close()

def insert_choose_course(nStudent, nTeachId):
    g_logger.info("INSERT %d, %d" % (nStudent, nTeachId))
    conn = ThinkMysql.get_conn_pool().connection()
    try:
        cur = conn.cursor(pymysql.cursors.DictCursor)

        nRet = cur.execute('''
            INSERT INTO 
                lesson_open(s_id, choose_id)
            VALUES
                (%s, %s)
        ''', (nStudent, nTeachId))

        conn.commit()

        return nRet
    except Exception as ex:
        pass
    finally:
        conn.close()

def get_all_student():
    conn = ThinkMysql.get_conn_pool_ex().connection("")
    c = conn.cursor(pymysql.cursors.DictCursor)

    try:
        c.execute('''
            select * from students
        ''')

        rows = c.fetchall()

        return rows
    except Exception as e:
        g_logger.error(e)
        return None
    finally:
        conn.close()

def main():
    lstStudent = get_all_student()
    for dictStudent in lstStudent:
        setCourse = rand_course(random.randint(12, 20))
        for nCourse in setCourse:
            dictTeach = rand_teacher(nCourse)
            insert_choose_course(dictStudent["s_id"], dictTeach["choose_id"])

if __name__ == '__main__':
    main()