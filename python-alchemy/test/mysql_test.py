#pip install SQLAlchemy
#pip install PyMySQL

import sqlalchemy

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:marvin@localhost/yourDB'

# Test your connection to your MySQL/MariaDB instance
engine = sqlalchemy.create_engine(SQLALCHEMY_DATABASE_URI, echo=True)
print(engine.table_names())

###################################################################################################################################################
#                  CREATE A MYSQL/MARIADB DATABASE
#
# MAC :
# brew install mariadb
# sudo mysql -u root
# mysql.server start
# https://phoenixnap.com/kb/how-to-create-mariadb-user-grant-privileges#:~:text=To%20create%20a%20new%20MariaDB,to%20a%20local%20MySQL%20server.

# WINDOWS
# https://downloads.mariadb.org/interstitial/mariadb-10.5.5/winx64-packages/mariadb-10.5.5-winx64.msi/from/http%3A//ams2.mirrors.digitalocean.com/mariadb/

###################################################################################################################################################
#                  CONNECT FROM PYCHARM
#  View > Tool Window > Database
# https://www.jetbrains.com/help/pycharm/connecting-to-a-database.html#connect-to-mysql-database
###################################################################################################################################################
