#!/usr/bin/python
import requests
import time
import re
import pymysql.cursors
import logging
import logging.handlers as handlers

# --------------------
# START CONF
# --------------------
# database connection config
mysql_localhost = "127.0.0.1"
mysql_port = 3306
mysql_username = "root"
mysql_password = "password"

auth_db = "acore_auth"

logging.basicConfig(format='[%(levelname)s][%(asctime)s]: %(message)s',
                    filename='/data/nas_wow_backup/logs/sync.log',
                    encoding='utf-8',
                    level=logging.WARNING)

logHandler = handlers.RotatingFileHandler('/data/nas_wow_backup/logs/sync.log', maxBytes=5000, backupCount=2)
logger = logging.getLogger('sync_logs')
logger.addHandler(logHandler)


def getIp():
    resIp = ""
    hosts = [
            "http://myip.ipip.net/ip",
            "http://ip.42.pl/raw",
            "http://ifconfig.me/ip",
            "http://httpbin.org/ip",
        ]

    for item in hosts:
        try: 
            res = requests.get(item, timeout=5).text
            ipStr = re.search(r'\d+\.\d+\.\d+\.\d+',res).group(0)
            if ipStr and len(ipStr) > 0:
                resIp = ipStr
                break 
        except Exception as err:
            logging.error("request item {0} error: {1}".format(item, err))
    return resIp

localtime = time.asctime( time.localtime(time.time()) )


def refreshDb():
    
    ip = getIp()
    if ip == "":
        logging.error("refreshDb fail, ip is empty")
        return

    # Connect to the database
    connection = pymysql.connect(host=mysql_localhost,
                                user=mysql_username,
                                password=mysql_password,
                                database=auth_db,
                                cursorclass=pymysql.cursors.DictCursor,
                                autocommit=True)

    with connection.cursor() as cursor:
        # Read a single record
        sql_query = "SELECT * FROM `realmlist`"
        cursor.execute(sql_query)
        results = cursor.fetchall()
        logging.info('ip:{0}, results: %s'.format(ip), results)
        for item in results:
            old_ip = item.get("address")
            if old_ip == ip:
                print('new_ip = old_ip = {0} success at {1}'.format(ip, localtime))
            else:
                logging.warning('ip not same,need update ip:{0}, dbIp: {1}'.format(ip, old_ip))
                sql_update = 'UPDATE `realmlist` SET `address`=%s WHERE `id`=%s'
                cursor.execute(sql_update, (ip, item.get('id')))
                # select again
                cursor.execute(sql_query)
                results = cursor.fetchall()
                logging.warning('update success, ip:{0}, new results: %s'.format(ip), results)

time.sleep(0.5)
refreshDb()
time.sleep(0.5)

exit(0) # exit from script



