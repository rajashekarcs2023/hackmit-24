import os
import pandas as pd
from sqlalchemy import create_engine, text
from pathlib import Path

# Database connection setup
username = 'demo'
password = 'demo'
hostname = os.getenv('IRIS_HOSTNAME', 'localhost')
port = '1972'
namespace = 'USER'
CONNECTION_STRING = f"iris://{username}:{password}@{hostname}:{port}/{namespace}"

def get_db_connection():
    """
    Create and return a connection to the database.
    """
    return create_engine(CONNECTION_STRING)

def create_tables(engine):
    """
    Create the necessary tables in the database if they don't already exist.
    """
    with engine.connect() as conn:
        with conn.begin():
            # Create table for X-ray data
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS xray_data (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    image_path VARCHAR(255),
                    diagnosis VARCHAR(50),
                    feature_vector TEXT
                )
            """))
            # Create table for symptom data
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS symptom_data (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    symptoms TEXT,
                    feature_vector TEXT
                )
            """))

def load_xray_data(xray_base_path):
    """
    Load X-ray data from the folder structure and insert it into the database.
    
    The folder structure is assumed to be:
    - xray_base_path/
        - train/
            - NORMAL/
            - PNEUMONIA/
        - test/
            - NORMAL/
            - PNEUMONIA/
        - val/
            - NORMAL/
            - PNEUMONIA/
    
    :param xray_base_path: Path to the chest_xray folder.
    """
    engine = get_db_connection()
    
    xray_folders = ['train', 'test', 'val']
    diagnosis_labels = ['NORMAL', 'PNEUMONIA']
    
    with engine.connect() as conn:
        with conn.begin():
            for folder in xray_folders:
                for label in diagnosis_labels:
                    folder_path = Path(xray_base_path) / folder / label
                    for image_path in folder_path.glob("*.jpeg"):  # Assuming the X-ray images are in .jpeg format
                        sql = text("""
                            INSERT INTO xray_data (image_path, diagnosis, feature_vector)
                            VALUES (:image_path, :diagnosis, :feature_vector)
                        """)
                        conn.execute(sql, {
                            'image_path': str(image_path),
                            'diagnosis': label,
                            'feature_vector': '[]'  # Initially store an empty feature vector
                        })
    
    print("X-ray data loaded successfully.")

def load_symptom_data(csv_path):
    df = pd.read_csv(csv_path)
    symptom_columns = [col for col in df.columns if col.startswith('symptom')]
    df['combined_symptoms'] = df[symptom_columns].apply(lambda row: ', '.join(row.dropna()), axis=1)

    engine = get_db_connection()
    
    with engine.connect() as conn:
        with conn.begin():
            for _, row in df.iterrows():
                sql = text("""
                    INSERT INTO symptom_data (symptoms, feature_vector)
                    VALUES (:symptoms, :feature_vector)
                """)
                conn.execute(sql, {
                    'symptoms': row['combined_symptoms'],
                    'feature_vector': '[]'
                })
                print(f"Inserted symptoms: {row['combined_symptoms']}")
    
    print("Symptom data loaded successfully.")


def initialize_database():
    """
    Initialize the database by creating necessary tables.
    """
    engine = get_db_connection()
    create_tables(engine)
    return engine
