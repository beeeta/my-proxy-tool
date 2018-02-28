from multiprocessing.pool import ThreadPool
import socket
import requests
import re

def check_vpn_validation(db):
    items = db.fetch_all()
    print('总共收集的数据条数为：{}'.format(len(items)))
    invalid_id = list()
    pool = ThreadPool(10)
    for item in items:
        id = item[0]
        ip = item[1]
        port = item[2]
        # 检查是否可以连接通
        vali_reach = pool.apply(vali_socket,(ip,port))
        if not vali_reach:
            invalid_id.append(id)
            continue
        # 检查代理的有效性
        vali_useful = pool.apply(vali_http,(ip,port))
        if not vali_useful:
            invalid_id.append(id)
    # 更新代理状态
    db.delete(invalid_id)
    print('清楚的无效数据条数为：{}'.format(len(invalid_id)))

def vali_socket(ip,port):
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:
        sock.settimeout(2)
        sock.connect((ip,port))
        print('{}:{} socket 验证成功'.format(ip, port))
        return True
    except:
        print('{}:{} socket 验证失败'.format(ip,port))
        return False
    finally:
        sock.close()

def vali_http(ip,port):
    proxies = {
        'http': 'http://{}:{}'.format(ip,port),
    }
    try:
        res = requests.get('http://2017.ip138.com/ic.asp',proxies=proxies,timeout=2)
    except:
        print('{}:{} http 验证无法连接'.format(ip, port))
        return False
    m_result = re.search(r'\[.*\]',res.text)
    if m_result is not None:
        realip = m_result[1:-1]
        if realip == ip:
            # 请求的ip和代理的ip一致则说明这个代理是有效的
            print('{}:{} http 验证成功'.format(ip, port))
            return True
    print('{}:{} http 验证代理IP透明'.format(ip, port))
    return False

