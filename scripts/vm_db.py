﻿  #!/usr/bin/env python
# -*- coding: utf-8 -*- 
# Author: Will

from VMware import VMware
from VMware.unit import str2list
import MySQLdb, time

def vm_db():
    vm = VMware()
    ip = vm.connect.ip
    sql_table = 'h' + ip.replace('.', '_')
    sql_ip = vm.connect.value("sql.ip")
    sql_user = vm.connect.value("sql.user")
    sql_passwd = vm.connect.value("sql.passwd")
    con = MySQLdb.connect(host=sql_ip, user=sql_user, passwd=sql_passwd)
    cursor = con.cursor()
    cursor.execute("create database if not exists vmware")
    con.select_db('vmware')
    '''
    power:   0/1 off/on
    flag:    0/1 unactive/active
    '''
    cursor.execute("create table if not exists %s (vmid char(5) auto_increment not null primary key,\
                                                  display varchar(30),\
                                                  register varchar(30), \
                                                  power char(1),\
                                                  flag char(1))" % sql_table)
    db_sync(vm, con, cursor, sql_table)
    cursor.close()

def db_sync(vm, con, cursor, sql_table):
    vm._data()
    cursor.execute("update %s set flag='0'" % sql_table)
    for i in range(len(vm.connect.id_list)):
        if vm.connect.dis_list[i] in vm.connect.poweron_list:
            cursor.execute("replace into %s(vmid,display,register,power,flag) values('%s','%s','%s','%s','%s')" % 
                                (sql_table,
                                vm.connect.id_list[i],
                                vm.connect.dis_list[i],
                                vm.connect.reg_list[i],
                                '1', '1'))
        else:
            cursor.execute("replace into %s(vmid,display,register,power,flag) values('%s','%s','%s','%s','%s')" % 
                               (sql_table,
                                vm.connect.id_list[i],
                                vm.connect.dis_list[i],
                                vm.connect.reg_list[i],
                                '0', '1'))
    con.commit()

if __name__ == '__main__':
    vm_db()