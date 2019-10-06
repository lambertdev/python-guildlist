#!/usr/bin/env python
#coding: utf-8

import os, sys
import sqlite3, locale, uuid
import types
import config

createtable=['create table if not exists guildinfo (guildname varchar(64),gene_num integer not null default 0)',
             'create table if not exists members (id integer primary key autoincrement, masterid integer not null, nickname varchar(64) not null, realname varchar(64) not null,sex bool default 0, generation integer not null)',
             'create table if not exists verinfo(version varchar(32), sys varchar(32))',
            ] 

class DB():
    def __init__(self, path):
        self.localcharset = locale.getdefaultlocale()[1]
        self.charset = 'utf-8'
        self.path = path
        if type(path) == types.UnicodeType:
            self.path = path.encode(self.charset)
        self.db = sqlite3.connect(self.path)
        self.version = '' 
        self.init()
        
    def init(self):
        for s in createtable:
            self.execute(s)
        sql = "select * from verinfo"
        ret = self.query(sql, True)
        if not ret:
            isql = "insert into verinfo(version, sys) values (?,?)"
            self.execute_param(isql, (config.VERSION, sys.platform,))
            self.version = config.VERSION
        else:
            self.version = ret[0]['version']
            isql = "update verinfo set version='%s'" % (config.VERSION)
            self.execute(sql)
            
    def close(self):
        self.db.close()
        self.db = None
        
    def execute(self, sql, autocommit=True):
        self.db.execute(sql)
        if autocommit:
            self.commit()
    
    def commit(self):
        self.db.commit()
        
    def query(self,sql,iszip=True):
        if type(sql) == types.UnicodeType:
            sql = sql.encode(self.charset, 'ignore')
 
        cur = self.db.cursor()
        cur.execute(sql)
 
        res = cur.fetchall()
        ret = []

        if res and iszip:
            des = cur.description
            names = [x[0] for x in des]
 
            for line in res:
                ret.append(dict(zip(names, line))) 
        else:
            ret = res 

        cur.close()
        return ret 
    
    def query_one(self, sql):
        if type(sql) == types.UnicodeType:
            sql = sql.encode(self.charset, 'ignore')
 
        cur = self.db.cursor()
        cur.execute(sql)
        one = cur.fetchone()
        cur.close()
        ret = []
        if one:
            des = cur.description
            names = [x[0] for x in des]
            ret.append(dict(zip(names, res)))
        return ret
    
    def query_many(self,sql,size=1,iszip=True):
        if type(sql) == types.UnicodeType:
            sql = sql.encode(self.charset, 'ignore')
 
        cur = self.db.cursor()
        cur.execute(sql)
        res = cur.fetchmany(size)
        ret = []
        if res and iszip:
            des = cur.description
            names = [x[0] for x in des]
 
            for line in res:
                ret.append(dict(zip(names, line))) 
        else:
            ret = res 

        cur.close()
        return ret 
    
    def rollback(self):
        self.db.rollback()
        
    def execute_param(self, sql, param, autocommit=True):
        self.db.execute(sql, param)
        if autocommit:
            self.db.commit()
            
            
def test():
    db = DB('test.db')

    db.execute('create table if not exists testme (id integer primary key autoincrement, name varchar(256))')
    db.execute("insert into testme(name) values ('Lambert')")

    print db.query("select * from testme")
    print db.query("select * from verinfo")
    
    db.close()



if __name__ == '__main__':
    test()
