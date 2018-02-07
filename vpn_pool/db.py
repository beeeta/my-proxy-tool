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
            con.execute('insert into {} values(null,\'{ip}\',{port},{stype},\'{ptype}\',{spost},\
            {dtimen},{isactive},\'{ctime}\')'.format(self.table_name,**dict(item.items())))

    def fetch_all(self):
        with self.connection() as con:
            items = con.execute('select * from {}'.format(self.table_name))
            return items.fetchall()

    def delete(self,ids):
        with self.connection(True) as con:
            if isinstance(ids,list) or isinstance(ids,tuple):
                ids_param = (len(ids)*'?,')[:-1]
                con.execute(('delete from {} where id in ('+ ids_param +')').format(self.table_name),tuple(ids))
            else:
                con.execute('delete from {} where id =? '.format(self.table_name), (ids,))
