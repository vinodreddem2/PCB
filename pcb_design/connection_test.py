import pyodbc

# Update with your database connection info
conn_str = (
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=localhost;'
    'DATABASE=PCB;'
    'UID=admin;'
    'PWD=Server.2'
)

try:
    connection = pyodbc.connect(conn_str)
    print("Connection successful!")
except Exception as e:
    print(f"Connection failed: {e}")
