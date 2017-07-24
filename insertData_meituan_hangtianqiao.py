# -*- coding: utf-8 -*-
"""
Created on Tue Jul 04 19:02:08 2017
@author: wangyu
"""
import xlrd
import MySQLdb
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def db_connect():
    conn = MySQLdb.connect(host = '59.110.213.32', 
                           port = 3306, 
                           user = 'fishwang',
                           passwd = 'Wang$fisH',
                           db = 'msmk',)
    return conn

def get_table_handler():
    inputfile = "data/meituan_hangtianqiao.xlsx"
    bk = xlrd.open_workbook(inputfile)
    try:
        sh = bk.sheet_by_name("crawler-data-1499771414497-7331")
    except:
        print "no sheet in %s named Worksheet" % inputfile
    return sh

if __name__ == "__main__":
    sh = get_table_handler()
    nrows = sh.nrows
    ncols = sh.ncols
    print "nrows %d, ncols %d" % (nrows,ncols)
       
    conn = db_connect()
    conn.set_character_set('utf8')
    cur = conn.cursor()
    for x in range(1, nrows):
        id = x + 8150
        relation = 0
        country = "中国"
        province = "北京"
        city = "北京"
        street = sh.cell_value(x, 4)
        name = sh.cell_value(x, 0)
        telephone = sh.cell_value(x, 5)
        imgurl = sh.cell_value(x, 1)
        state = 0
        latitude = float(sh.cell_value(x, 6))
        longitude = float(sh.cell_value(x, 7))
        rate = 0.0
        monthly_order_num = 0
        if sh.cell(x, 8).ctype == 0:
        	monthly_order_num = 0
        else:
        	monthly_order_num = int(sh.cell_value(x, 8))
        open_time = sh.cell_value(x, 3)
        avg_delivery_duration = int(sh.cell_value(x, 9))
        if sh.cell(x, 11).ctype == 0:
        	starting_price = 1000
        else:
        	starting_price = int(sh.cell_value(x, 11))
        if sh.cell(x, 12).ctype == 0:
        	deliver_fee = 1000
        else:
        	deliver_fee = float(sh.cell_value(x, 12))
        activities = sh.cell_value(x, 14)
        if sh.cell(x, 15).ctype != 0:
        	menu_json_sql = sh.cell_value(x, 15)
        else:
        	menu_json_sql = ""
        if sh.cell(x, 16).ctype != 0:
        	business_id = sh.cell_value(x, 16)
        else:
        	business_id = ""
        sql = "insert into restaurant(id, relation, country, province, city, street, name, telephone, imgurl, \
        state, latitude, longitude, rate, monthly_order_num, open_time, avg_delivery_duration, starting_price,\
        deliver_fee, activities, menu_json, business_id) values ('%d', '%d', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%d', '%f',\
        '%f', '%d', '%d', '%s', '%d', '%d', '%d', '%s', '%s', '%s')" % \
        (id, relation, country, province, city, street, name, telephone, imgurl, state, latitude, longitude, \
         rate, monthly_order_num, open_time, avg_delivery_duration, starting_price, deliver_fee, activities, menu_json_sql, business_id)
        try:
        	cur.execute(sql)
        	conn.commit()
        except:
        	print sql
        	conn.rollback()

    cur.close()
    conn.close()
    
