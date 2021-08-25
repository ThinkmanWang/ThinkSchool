# -*- coding: utf-8 -*-

import pymysql
import random

from faker import Faker

from pythinkutils.mysql.ThinkMysql import ThinkMysql
from pythinkutils.common.log import g_logger
from pythinkutils.common.object2json import *
from pythinkutils.common.log import g_logger
from pythinkutils.common.datetime_utils import *

def rand_teacher(nNum):
    fake = Faker()
    lstTeacher = []
    for i in range(nNum):
        dictTeacher = {
            "name": fake.name()
            , "sex": random.randint(0, 1)
            , "title_id": random.randint(1, 4)
        }

        lstTeacher.append(dictTeacher)

    return lstTeacher

def insert_teacher(dictTeacher):
    conn = ThinkMysql.get_conn_pool().connection()
    try:
        cur = conn.cursor(pymysql.cursors.DictCursor)

        nRet = cur.execute('''
                INSERT INTO 
                    t_teacher(name, sex, title_id)
                VALUES
                    (%s, %s, %s)
            ''', (dictTeacher["name"], dictTeacher["sex"], dictTeacher["title_id"]))

        conn.commit()

        return nRet
    except Exception as ex:
        pass
    finally:
        conn.close()

def main():
    lstTeacher = rand_teacher(100)
    for dictTeacher in lstTeacher:
        insert_teacher(dictTeacher)

if __name__ == '__main__':
    main()