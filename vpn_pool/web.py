"""
提供管理爬虫的接口
提供代理数据接口
"""
from flask import Flask,request,make_response,jsonify

from vpn_pool import db

app = Flask(__name__)
datebase = db.DB()

@app.route('/proxies')
def proxies():
    stype = request.args.get('stype') # 代理类型：透明，非透明
    if not stype:
        # 默认只使用非透明代理
        ip_ports = datebase.find_by_stype(2)
        return jsonify([{'ip':ip_port[0],'port':ip_port[1]} for ip_port in ip_ports])
    elif stype in ('1','2'):
        ip_ports = datebase.find_by_stype(int(stype))
        return jsonify([{'ip': ip_port[0], 'port': ip_port[1]} for ip_port in ip_ports])
    else:
        return make_response('unknown request',403)