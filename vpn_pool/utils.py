from multiprocessing.pool import ThreadPool
import requests
import re

UNAVAILABLE = 0
TRANSPARENT = 1
SECRET = 2

def check_vpn_validation(db):
    items = db.fetch_all()
    print('总共收集的数据条数为：{}'.format(len(items)))
    invalid_ids = list()
    trans_ids = list()
    secret_ids = list()
    pool = ThreadPool(10)
    for item in items:
        id = item[0]
        ip = item[1]
        port = item[2]
        # 检查代理的有效性
        vali_status = pool.apply(vali_http,(ip,port))
        if vali_status == UNAVAILABLE:
            invalid_ids.append(id)
        elif vali_status == TRANSPARENT:
            trans_ids.append(id)
        else:
            secret_ids.append(id)
    # 更新代理状态
    db.delete(invalid_ids)
    db.update_stype(TRANSPARENT,trans_ids)
    db.update_stype(SECRET,secret_ids)
    print('清楚的无效数据条数为：{}'.format(len(invalid_ids)))
    print('透明代理数据条数为：{}'.format(len(trans_ids)))
    print('私密代理数据条数为：{}'.format(len(secret_ids)))

def vali_http(ip,port):
    proxies = {
        'http': 'http://{}:{}'.format(ip,port),
    }
    try:
        res = requests.get('http://2017.ip138.com/ic.asp',proxies=proxies,timeout=2)
    except:
        print('{}:{} http 验证无法连接'.format(ip, port))
        return UNAVAILABLE
    m_result = re.search(r'\[.*\]',res.text)
    if m_result is not None:
        realip = m_result.group()[1:-1]
        if realip == ip:
            # 请求的ip和代理的ip一致则说明这个代理是有效的
            print('{}:{} http 验证成功'.format(ip, port))
            return SECRET
    print('{}:{} http 验证代理IP透明'.format(ip, port))
    return TRANSPARENT

