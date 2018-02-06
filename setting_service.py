import connect_service
import pymysql

def get_pill_dispenser_status():
    conn = connect_service.get_connect_sql()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute("SELECT * FROM robot_setting ")
    for r in cur:
        if(str(r['Pill_dispenser_status'])=="1"):
            return True
        elif(str(r['Pill_dispenser_status'])=="0"):
            return False
    cur.close()
    conn.close()

def get_pill_id():
    conn = connect_service.get_connect_sql()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute("SELECT * FROM robot_setting ")
    for r in cur:
        return int(r['Pill_id'])
    cur.close()
    conn.close()

def set_robot_connect_true_status():
    conn = connect_service.get_connect_sql()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute("UPDATE robot_setting SET Robot_connect_status = 1 WHERE Robot_setting_id = 1")
    conn.commit()
    cur.close()
    conn.close()

def set_robot_connect_false_status():
    conn = connect_service.get_connect_sql()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute("UPDATE robot_setting SET Robot_connect_status = 0 WHERE Robot_setting_id = 1")
    conn.commit()
    cur.close()
    conn.close()

def set_pill_dispenser_true_status(pill_id):
    conn = connect_service.get_connect_sql()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute("UPDATE robot_setting SET Pill_dispenser_status = 1 , Pill_id = "+str(pill_id)+" WHERE Robot_setting_id = 1")
    conn.commit()
    cur.close()
    conn.close()

def set_pill_dispenser_false_status():
    conn = connect_service.get_connect_sql()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute("UPDATE robot_setting SET Pill_dispenser_status = 0 , Pill_id = 0 WHERE Robot_setting_id = 1")
    conn.commit()
    cur.close()
    conn.close()
