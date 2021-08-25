# -*- coding: utf-8 -*-
import random

import pymysql

from pythinkutils.mysql.ThinkMysql import ThinkMysql
from pythinkutils.common.log import g_logger
from pythinkutils.common.object2json import *

def get_all_teacher():
    conn = ThinkMysql.get_conn_pool_ex().connection("")
    c = conn.cursor(pymysql.cursors.DictCursor)

    try:
        c.execute('''
                SELECT
                    *
                FROM
                    t_teacher
            ''')

        rows = c.fetchall()

        return rows
    except Exception as e:
        g_logger.error(e)
        return None
    finally:
        conn.close()

def rand_course(nNum):
    setCourse = set()
    while len(setCourse) < nNum:
        setCourse.add(random.randint(1, 20))

    return setCourse

def insert_teach(nTeacher, nCourse):
    g_logger.info("INSERT %d, %d" % (nTeacher, nCourse))

    conn = ThinkMysql.get_conn_pool().connection()
    try:
        cur = conn.cursor(pymysql.cursors.DictCursor)

        nRet = cur.execute('''
                INSERT INTO 
                    t_teach(teacher_id, course_id)
                VALUES
                    (%s, %s)
            ''', (nTeacher, nCourse))

        conn.commit()

        return nRet
    except Exception as ex:
        pass
    finally:
        conn.close()

def main():
    lstTeacher = get_all_teacher()
    for dictTeacher in lstTeacher:
        setCourse = rand_course(random.randint(4, 8))
        for nCourse in setCourse:
            insert_teach(dictTeacher["id"], nCourse)


if __name__ == '__main__':
    main()