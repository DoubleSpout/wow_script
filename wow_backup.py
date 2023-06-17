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
back_up_path = "/data/nas_wow_backup/sql"
sql_template = "mysqldump --no-tablespaces --column-statistics=0 -h {} -u {} -p'{}' {} > {}/{}.sql"


os.system(sql_template.format(
    mysql_localhost,
    mysql_username,
    mysql_password,
    world_db,
    back_up_path,
    world_db
))


os.system(sql_template.format(
    mysql_localhost,
    mysql_username,
    mysql_password,
    char_db,
    back_up_path,
    char_db
))
os.system(sql_template.format(
    mysql_localhost,
    mysql_username,
    mysql_password,
    auth_db,
    back_up_path,
    auth_db
))


time.sleep(1)

localtime = time.asctime( time.localtime(time.time()) )
print("backup success at ", localtime)



exit(0) # exit from script

