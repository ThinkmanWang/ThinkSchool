# -*- coding: utf-8 -*-

import random

import pymysql

from pythinkutils.mysql.ThinkMysql import ThinkMysql
from pythinkutils.common.log import g_logger
from pythinkutils.common.object2json import *

def get_all_choose_curser():
    conn = ThinkMysql.get_conn_pool_ex().connection("")
    c = conn.cursor(pymysql.cursors.DictCursor)

    try:
        c.execute('''
            select * from t_choose_course
        ''')

        rows = c.fetchall()

        return rows
    except Exception as e:
        g_logger.error(e)
        return None
    finally:
        conn.close()

def insert_exam(nChooseId, fScore):
    g_logger.info("INSERT %d, %d" % (nChooseId, fScore))
    conn = ThinkMysql.get_conn_pool().connection()
    try:
        cur = conn.cursor(pymysql.cursors.DictCursor)

        nRet = cur.execute('''
            INSERT INTO 
                t_exam(cc_id, score)
            VALUES
                (%s, %s)
        ''', (nChooseId, fScore))

        conn.commit()

        return nRet
    except Exception as ex:
        pass
    finally:
        conn.close()

def rand_score(nChoice):
    nScore = random.randint(40, 100)
    while True:
        insert_exam(nChoice, nScore)

        if nScore >= 60:
            break

        nScore = random.randint(40, 100)

def main():
    lstChoise = get_all_choose_curser()
    for dictChoise in lstChoise:
        rand_score(dictChoise["id"])

if __name__ == '__main__':
    main()