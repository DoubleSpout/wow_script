#!/usr/bin/python

import time
import os

# --------------------
# START CONF
# --------------------
# database connection config
mysql_localhost = "127.0.0.1"
mysql_username = "root"
mysql_password = "password"

world_db = "acore_world"
char_db = "acore_characters"
auth_db = "acore_auth"


os.system("mysqldump --no-tablespaces --column-statistics=0 -h {} -u {} -p'{}' {} > /data/nas_wow_backup/sql/world.sql".format(
    mysql_localhost,
    mysql_username,
    mysql_password,
    world_db
))


os.system("mysqldump --no-tablespaces --column-statistics=0 -h {} -u {} -p'{}' {} > /data/nas_wow_backup/sql/characters.sql".format(
    mysql_localhost,
    mysql_username,
    mysql_password,
    char_db
))
os.system("mysqldump --no-tablespaces --column-statistics=0 -h {} -u {} -p'{}' {} > /data/nas_wow_backup/sql/auth.sql".format(
    mysql_localhost,
    mysql_username,
    mysql_password,
    auth_db
))


time.sleep(1)

localtime = time.asctime( time.localtime(time.time()) )
print("backup success at ", localtime)



exit(0) # exit from script

