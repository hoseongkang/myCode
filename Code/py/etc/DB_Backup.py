import pyodbc

server = '130.1.22.33,2433'
database = 'rpaportal_dev'
username = 'sa'
password = '@sygrpa22!'
bak_path = 'D:\\Program Files\\Microsoft SQL Server\\MSSQL13.MSSQLSERVER\\MSSQL\\Backup\\rpaportal_dev.bak'

def backup_database(server, database, username, password, backup_path):
    connection_string = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'
    try:
        with pyodbc.connect(connection_string, autocommit=True) as conn:
            cursor = conn.cursor()
            backup_sql = f"""
            BACKUP DATABASE [{database}] TO DISK = N'{backup_path}'
            WITH NOFORMAT, NOINIT, 
            NAME = N'{database}-전체 데이터베이스 백업', 
            SKIP, NOREWIND, NOUNLOAD, STATS = 10
            """
            cursor.execute(backup_sql)
            conn.commit()
            print(f"Database {database} backed up successfully to {backup_path}")
    except Exception as e:
        print("Error:", e)

backup_database(server, database, username, password, bak_path)
"WITH NOFORMAT, NOINIT,  NAME = N'rpaportal_dev-전체 데이터베이스 백업', SKIP, NOREWIND, NOUNLOAD,  STATS = 10"

# connection = pyodbc.connect(driver='{ODBC Driver 17 for SQL Server}', server=server, database=database,UID=username, PWD=password, trusted_connection='yes', autocommit=True)
# backup = "BACKUP DATABASE [rpaportal_dev] TO DISK = N'rpaportal_dev.bak'"
# cursor = connection.cursor().execute(backup)
# connection.close()

