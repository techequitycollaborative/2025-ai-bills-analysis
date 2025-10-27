import pandas as pd
from db.connect import connect

def get_table(config, table_name, schema='public'):
    """ Query a specific table and return as pandas DataFrame using connect function """
    conn = connect(config)
    
    if conn is None:
        print("Failed to connect to database")
        return None
    
    try:
        # Query the table
        query = f'SELECT * FROM {schema}.{table_name}'
        df = pd.read_sql_query(query, conn)
        
        print(f'Successfully retrieved {len(df)} rows from {schema}.{table_name}')
        return df
        
    except Exception as error:
        print(f'Error querying table: {error}')
        return None
        
    finally:
        conn.close()
        print("Connection closed")