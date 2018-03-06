from subprocess import Popen,PIPE
from multiprocessing import Process
import time
from threading import Timer,Thread
import json

import requests

from vpn_pool.web import app

def scheduler():
    pros = requests.get('http://localhost:6800/listprojects.json').json().get('projects')
    for pro in pros:
        sps = requests.get('http://localhost:6800/listspiders.json?project={}'.format(pro)).json().get('spiders')
        for sp in sps:
            res = requests.post('http://localhost:6800/schedule.json',data=json.dumps({'project':pro,'spider':sp})).json()
            assert res.get('status') == 'ok'

    Timer(60*60*24,scheduler,()).start()



if __name__ == '__main__':
    # 启动 scrapyd 服务
    p = Popen(['scrapyd'],shell=True)
    # 启动api及web服务
    app.run(debug=True)
    # 向scrapyd定时发送数抓去请求，更新proxy信息
    time.sleep(60*1)
    scheduler()





