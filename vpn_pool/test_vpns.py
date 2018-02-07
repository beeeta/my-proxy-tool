import pytest

from vpn_pool.db import DB
from vpn_pool.items import VpnPoolItem

@pytest.fixture(autouse=True)
def init_con():
    global db
    db = DB()

def test_add():
    vpn = VpnPoolItem(ip='12.12.12.12',port=1234,stype=1,ptype='https',spost=1,dtimen=123,isactive=1,ctime='2018-12-12 12:12:45')
    db.add(vpn)

def test_fetchall():
    print(db.fetch_all())

def test_delete():
    db.delete((3,5,7))
    db.delete(6)