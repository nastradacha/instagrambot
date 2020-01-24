import psycopg2
from instagram_main.credentials import get_cred_from_lasspass
import pandas as pd


def connect_db(app):
    # login info
    username = get_cred_from_lasspass("Postgresql")["user"]
    password = get_cred_from_lasspass("Postgresql")["pass"]
    print(username)
    con = False
    if app == "":
        try:
            con_str = f"user={username} password={password} host='naspostgresql.cjecpy7kizpe.us-east-2.rds.amazonaws.com' port=5432 dbname=Testdb connect_timeout=1"
            con = psycopg2.connect(con_str)
            return con
        except:
            return False
    else:
        (print("unknown app name" + app))


def disconnect_db(con):
    con.close()


# print(connect_db(''))
# sqlq = """select * from information_schema.tables"""
##  got table_schema-public  table_name -test_table with below query
sqlq = """select table_schema, table_name FROM information_schema.tables where table_schema not in ('information_schema','pg_catalog')and table_type = 'BASE TABLE' order by table_schema,table_name; """
get_dbname = """select datname from pg_database;"""  ## Instagram , Testdb and postgres are some of dbnames found with this query
test_connect = connect_db("")
df = pd.read_sql_query(sqlq, test_connect)
print(df)
