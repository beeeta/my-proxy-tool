import sqlite3 as sqlite
from threading import RLock
from contextlib import contextmanager
from datetime import datetime
import os,sys

PAR_DIR = os.path.abspath(os.path.dirname(__file__))

class DB(object):
    def __init__(self):
        self.filename = os.path.abspath(os.path.join(PAR_DIR,'..','vpns_pool.db'))
        self.table_vpns = 'vpns'
        self.table_date = 'last_update_date'
        self._lock = RLock()
        self.init_table()
        self.date_format = '%Y-%m-%d'

    @contextmanager
    def connection(self,commit_on_success=False):
        with self._lock:
            con = sqlite.connect(self.filename)
            try:
                yield con
                if commit_on_success:
                    con.commit()
            finally:
                con.close()


    def init_table(self):
        with self.connection() as con:
            con.execute("create table if not exists {} (id INTEGER PRIMARY KEY,\
                        ip,port,stype,ptype,spost,dtimen,isactive,ctime)".format(self.table_vpns))
            con.execute('create table if not exists {} (id INTEGER PRIMARY KEY,last_date)'.format(self.table_date))

    def add(self,item):
        with self.connection(True) as con:
            if isinstance(item,list):
                ilist = list()
                for i in item:
                    par = (i.get('ip',''),i.get('port',''),i.get('stype',''),i.get('ptype',''),i.get('spost',''),i.get('dtimen',''),\
                           i.get('isactive',''),i.get('ctime',''))
                    ilist.append(par)
                con.executemany('insert into vpns values(null,?,?,?,?,?,\
                ?,?,?)',ilist)
            else:
                par = (item.get('ip', ''), item.get('port', ''), item.get('stype', ''), item.get('ptype', ''), item.get('spost', ''),
                       item.get('dtimen', ''), \
                       item.get('isactive', ''), item.get('ctime', ''))
                con.execute('insert into vpns values(null,?,?,?,?,?,\
                ?,?,?)',par)

    def fetch_all(self):
        with self.connection() as con:
            res = con.execute('select * from {}'.format(self.table_vpns))
            return res.fetchall()

    # ids数据量过大时，一次删除会有 sqlite3.OperationalError: too many SQL variables 错误，应分批删除
    def delete(self,ids):
        with self.connection(True) as con:
            if isinstance(ids,list) or isinstance(ids,tuple) or isinstance(ids,set):
                if len(ids)<1:
                    return
                if len(ids) > 100:
                    while len(ids) >0:
                        del_ids = ids[:100]
                        ids_param = (len(del_ids)*'?,')[:-1]
                        con.execute(('delete from {} where id in ('+ ids_param +')').format(self.table_vpns), tuple(del_ids))
                        ids = ids[100:]
                else:
                    ids_param = (len(ids) * '?,')[:-1]
                    con.execute(('delete from {} where id in (' + ids_param + ')').format(self.table_vpns), tuple(ids))
            else:
                con.execute('delete from {} where id =? '.format(self.table_vpns), (ids,))

    def find_by_ip_port(self,ip,port):
        with self.connection(True) as con:
            res = con.execute('select * from {} where ip=? and port=? '.format(self.table_vpns), (ip, port))
            return res.fetchall()

    def update_stype(self,stype,ids):
        if not ids:
            return
        params = [(stype,id) for id in ids]
        with self.connection(True) as con:
            con.executemany('update {} set stype=? where id=?'.format(self.table_vpns), params)

    def find_by_stype(self,stype):
        with self.connection(True) as con:
            res = con.execute('select ip,port from {} where stype=?'.format(self.table_vpns),(stype,))
            return res.fetchall()


    def update_last_date(self):
        with self.connection(True) as con:
            res = con.execute('select id,last_date from last_update_date order by id DESC')
            last_items = res.fetchall()
            current_date = datetime.now().strftime(self.date_format)
            if not last_items:
                con.execute('insert into last_update_date values(null,?)',(current_date,))
            else:
                last_item = last_items[0]
                con.execute('update last_update_date set last_date=? where id=?',(current_date,last_item[0]))

    def is_crawled_today(self):
        with self.connection(True) as con:
            res = con.execute('select last_date from last_update_date order by id DESC')
            last_datas = res.fetchall()
            if last_datas:
                last_data = last_datas[0]
                current_date = datetime.now().strftime(self.date_format)
                if current_date == last_data:
                    return True
            return False