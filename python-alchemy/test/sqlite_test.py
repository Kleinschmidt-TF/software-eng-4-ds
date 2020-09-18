import sqlite3 as sql

# Test your connection to your SQLite instance

con = sql.connect('user.db')
mycur = con.cursor()
mycur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
available_tables=(mycur.fetchall())
# mycur.execute("SELECT name FROM users;")
# users=(mycur.fetchall())
print(available_tables)
# print(users)

###################################################################################################################################################
#               CREATE A SQLite DB in PYCHARM
#
# https://www.jetbrains.com/help/pycharm/connecting-to-a-database.html#connect-to-sqlite-database
#
##################################################################################################################################################