#!/usr/bin/python
# Import required libraries

import sys
import time
import connect_service
from threading import Thread
import pymysql
import notification_service
import serial_service

    
def pill_dispenser(slot_id):
    if check_num_of_pill(get_pill_id_with_slot_id(slot_id)):
        move_step_motor(slot_id)
        print("dispensing..")
        update_pill(get_pill_id_with_slot_id(slot_id))    
    else:
        print("pill out of stock")

def move_step_motor(slot_id):
    conn = connect_service.get_connect_sql()
    cur = conn.cursor(pymysql.cursors.DictCursor)    
    cur.execute("SELECT * FROM slot INNER JOIN pill ON slot.Pill_id = pill.Pill_id WHERE Slot_id = '"+str(slot_id)+"'")
    for r in cur:
        serial_service.moving_step_motor(r['Slot_num'],r['Pill_dispenseramount'])
    cur.close()
    conn.close()
        
def pill_dispenser_with_schedule_id(schedule_id):
    conn = connect_service.get_connect_sql()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute("SELECT * FROM `dispenser` INNER JOIN slot ON dispenser.Slot_id=slot.Slot_id WHERE Schedule_id = '"+str(schedule_id)+"' AND Slot_visiblestatus = '1' ORDER BY Slot_num")
    for r in cur:
        pill_dispenser(r['Slot_id'])
    cur.close()
    conn.close()

def pill_dispenser_with_pill_id(pill_id):
    conn = connect_service.get_connect_sql()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute("SELECT * FROM `slot` WHERE Pill_id = '"+str(pill_id)+"' AND Slot_visiblestatus = '1' LIMIT 1")
    if (cur.rowcount > 0):
        for r in cur:
            pill_dispenser(r['Slot_id'])
        return True
    else:
        return False
    cur.close()
    conn.close()

def update_pill(pill_id):
    conn = connect_service.get_connect_sql()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute("UPDATE pill SET Pill_left = Pill_left-Pill_dispenseramount WHERE Pill_id = '"+str(pill_id)+"'")
    conn.commit()
    cur.close()
    conn.close()
    
def get_slot_num(slot_id):
    conn = connect_service.get_connect_sql()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute("SELECT * FROM `slot`WHERE Slot_id="+str(slot_id))
    for r in cur:
        return r['Slot_num']
    cur.close()
    conn.close()

def get_pill_id_with_slot_id(slot_id):
    conn = connect_service.get_connect_sql()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute("SELECT * FROM `slot` where Slot_id='"+str(slot_id)+"'")
    for r in cur:
        return r['Pill_id']
    cur.close()
    conn.close()

def check_num_of_pill(pill_id):
    conn = connect_service.get_connect_sql()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute("SELECT * FROM `pill` WHERE Pill_id = '"+str(pill_id)+"'")
    for r in cur:
        if r['Pill_left'] / r['Pill_dispenseramount']  == 1:
            try:
              return True
            finally:
              notification_service.sent_all_pill_out_of_stock_in_background(pill_id)
        elif r['Pill_left'] / r['Pill_dispenseramount']  == 0:
            try:
              return False
            finally:
              notification_service.sent_all_pill_out_of_stock_in_background(pill_id)
            
        else:
            if r['Pill_left'] < 5:
              try:
                return True
              finally:
                notification_service.sent_all_pill_almost_out_of_stock_in_background(pill_id)
            else:
              return True
    cur.close()
    conn.close()

def check_pil_exisit_and_num_of_pill(pill_id):
    conn = connect_service.get_connect_sql()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute("SELECT * FROM `slot`WHERE Pill_id="+str(pill_id)+" AND Slot_visiblestatus = '1' LIMIT 1")
    if(cur.rowcount > 0):
      for r in cur:
          return True
    else:
          return False
    cur.close()
    conn.close()
