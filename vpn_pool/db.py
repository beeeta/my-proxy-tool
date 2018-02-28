import sqlite3 as sqlite
from threading import RLock
from contextlib import contextmanager

class DB(object):
    def __init__(self):
        self.filename = 'vpns_pool.db'
        self.table_name = 'vpns'
        self._lock = RLock()
        self.init_table()

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
            con.execute("create table if not exists `%s` (id INTEGER PRIMARY KEY,"
                        "ip,port,stype,ptype,spost,dtimen,isactive,ctime)" % self.table_name)

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
            res = con.execute('select * from {}'.format(self.table_name))
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
                        con.execute(('delete from {} where id in ('+ ids_param +')').format(self.table_name),tuple(del_ids))
                        ids = ids[100:]
                else:
                    ids_param = (len(ids) * '?,')[:-1]
                    con.execute(('delete from {} where id in (' + ids_param + ')').format(self.table_name),tuple(ids))
            else:
                con.execute('delete from {} where id =? '.format(self.table_name), (ids,))

    def find_by_ip_port(self,ip,port):
        with self.connection(True) as con:
            res = con.execute('select * from {} where ip=? and port=? '.format(self.table_name),(ip,port))
            return res.fetchall()

    def update_stype(self,ids,stype):
        if not ids:
            return
        params = [(stype,id) for id in ids]
        with self.connection(True) as con:
            con.executemany('update {} set stype=? where id=?'.format(self.table_name),params)