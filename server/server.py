#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import chunzhen_ip
from flask import Flask
from flask import jsonify
from flask import request
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    app.config['JSON_AS_ASCII'] = False
    try:
        ip = request.headers['X-Forwarded-For'].split(',')[0]
    except:
        ip = request.remote_addr
    IPL = chunzhen_ip.IPLocator("../qqwry.dat/qqwry_lastest.dat")
    ip = str(ip)
    ip = request.environ.get('HTTP_X_REAL_IP', ip)
    try:
        address = IPL.getIpAddr(IPL.str2ip(ip))
        range = IPL.getIpRange(IPL.str2ip(ip))
        print "此IP %s 属于 %s\n所在网段: %s" % (ip,address, range)
        state = "ok"
    except:
        address = 0
        range = 0
        state = "not found"
    json_return = {'state': state, 'ip': ip, 'local': address, 'network': range}
    return jsonify(json_return)

if __name__ == '__main__':
    app.wsgi_app = ProxyFix(app.wsgi_app)
    app.run(host='0.0.0.0', port= 80)

