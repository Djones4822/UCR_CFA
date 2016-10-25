import psycopg2

def connect(dbname, user, host, password):
    try:
        conn = psycopg2.connect("dbname={dbname}, user={user}, host={host}, password={password}".format(
            dbname=dbname,
            user=user,
            host=host,
            password=password
        ))
        return conn
    except:
        log.critical('database connection failed')
        exit(1)

def read():
    pass

def write():
    pass
