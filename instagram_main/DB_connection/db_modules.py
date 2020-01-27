import psycopg2
from instagram_main.credentials import get_cred_from_lasspass
import pandas as pd


def connect_db(app):
    # login info
    username, password = get_cred_from_lasspass("Postgresql")
    con = False
    if app == "":
        try:
            con_str = f"user={username} password={password} host='naspostgresql.cjecpy7kizpe.us-east-2.rds.amazonaws.com' port=5432 dbname=instagram_bot connect_timeout=1"
            con = psycopg2.connect(con_str)
            return con
        except:
            return False
    else:
        (print("unknown app name" + app))


def disconnect_db(con):
    con.close()


def get_records(con, query):
    try:
        df = pd.read_sql_query(query, con, index_col=None)
        return df
    except Exception as e:
        print("Query problem")
        pass
