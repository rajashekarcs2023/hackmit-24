# test_iris_connection.py

from sqlalchemy import create_engine, text
import os

def test_iris_connection():
    # Connection parameters
    username = 'demo'
    password = 'demo'
    hostname = os.getenv('IRIS_HOSTNAME', 'localhost')
    port = '1972'
    namespace = 'USER'
    
    # Create connection string
    CONNECTION_STRING = f"iris://{username}:{password}@{hostname}:{port}/{namespace}"
    
    try:
        # Attempt to create an engine
        engine = create_engine(CONNECTION_STRING)
        
        # Try to connect and execute a simple query
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("Connection successful!")
            print("Query result:", result.scalar())
        
        return True
    except Exception as e:
        print(f"Connection failed. Error: {e}")
        return False

if __name__ == "__main__":
    test_iris_connection()