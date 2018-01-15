import sys
import pymysql

def get_lang():
    conn = pymysql.connect(host='127.0.0.1', user='root', passwd=None, db='kati',charset='utf8')
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute("SELECT * FROM robot_setting ")
    for r in cur:
        return r['Robot_lang']
    cur.close()
    conn.close()
