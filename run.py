from subprocess import Popen,PIPE
from multiprocessing import Process

from vpn_pool.web import app

if __name__ == '__main__':
    # 启动 scrapyd 服务
    p = Popen(['scrapyd'],shell=True)
    # 启动api及web服务
    app.run(debug=True)



