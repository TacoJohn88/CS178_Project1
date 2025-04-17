import pymysql
import pymysql.cursors
import creds
import boto3


dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
user_table = dynamodb.Table('UserLanguages')

def get_conn():
    """
    Establish and return a connection to the MySQL RDS database
    using credentials from creds.py.
    Uses DictCursor to return query results as dictionaries.
    """
    return pymysql.connect(
        host=creds.host,
        user=creds.user,
        password=creds.password,
        db=creds.db,
        cursorclass=pymysql.cursors.DictCursor
    )

def execute_query(query, args=()):
    """
    Execute a SQL query using a connection to RDS.
    Closes the connection automatically after running the query.
    Returns the results as a list of dictionaries.
    """
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(query, args)
            rows = cur.fetchall()
        return rows
    finally:
        conn.close()

def get_all_languages():
    return execute_query("SELECT DISTINCT Language FROM countrylanguage ORDER BY Language ASC")