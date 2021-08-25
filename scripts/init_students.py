# -*- coding: utf-8 -*-

import pymysql
import random

from faker import Faker

from pythinkutils.mysql.ThinkMysql import ThinkMysql
from pythinkutils.common.log import g_logger
from pythinkutils.common.object2json import *
from pythinkutils.common.log import g_logger
from pythinkutils.common.datetime_utils import *

def get_classes():
    conn = ThinkMysql.get_conn_pool_ex().connection("")
    c = conn.cursor(pymysql.cursors.DictCursor)

    try:
        c.execute('''
                SELECT
                    *
                FROM
                    t_class
            ''')

        rows = c.fetchall()

        return rows
    except Exception as e:
        g_logger.error(e)
        return None
    finally:
        conn.close()

def rand_student(nClassId, nNum):
    fake = Faker()
    conn = ThinkMysql.get_conn_pool().connection()

    try:
        for i in range(nNum):
            cur = conn.cursor(pymysql.cursors.DictCursor)

            szName = fake.name()
            szBirthday = timestamp2date(random.randint(946656000, 978278340))
            nSex = random.randint(0, 1)

            g_logger.info("INSERT %d %s %s %d" % (nClassId, szName, szBirthday, nSex))

            nRet = cur.execute('''
                INSERT INTO 
                    t_student(class_id, name, birthday, sex)
                VALUES
                    (%s, %s, %s, %s)
            ''', (nClassId, szName, szBirthday, nSex))

            conn.commit()
    except Exception as ex:
        pass
    finally:
        conn.close()


def main():
    lstClass = get_classes()
    for dictClass in lstClass:
        g_logger.info(str(obj2json(dictClass)).encode('latin-1').decode('unicode_escape'))
        rand_student(dictClass["id"], random.randint(40, 60))

if __name__ == '__main__':
    main()