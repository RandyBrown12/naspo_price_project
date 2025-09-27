import io
import pandas as pd
import psycopg2
import dotenv
import os
from sqlalchemy import create_engine

def execute_sql_file(cursor, conn, sql_file_path):
    try:
        with open(sql_file_path, 'r') as sql_file:
            sql_script = sql_file.read()

        cursor.execute(sql_script)
        conn.commit()
        print(f"Executed SQL script from {sql_file_path}")
    except Exception as e:
        print(f"Error executing SQL script from {sql_file_path}: {e}")
        conn.rollback()
        raise 

def main():
    dotenv.load_dotenv()
    
    db_params = {
        "database": os.environ.get("POSTGRES_DB", "N/A"),
        "user": os.environ.get("POSTGRES_USER", "N/A"),
        "password": os.environ.get("POSTGRES_PASSWORD", "N/A"),
        "host": os.environ.get("POSTGRES_HOST", "N/A"),
        "port": os.environ.get("POSTGRES_PORT", "N/A")
    }

    conn = psycopg2.connect(**db_params)
    engine = create_engine(f"postgresql+psycopg2://{db_params['user']}:{db_params['password']}@{db_params['host']}:{db_params['port']}/{db_params['database']}")

    cursor = conn.cursor()

    execute_sql_file(cursor, conn, 'data/schema.sql')

    # Perform Excel file insertion
    data_directory = "data"
    files = [file for file in os.listdir(data_directory) if os.path.isfile(os.path.join(data_directory, file)) and file.endswith('.xlsx')]
    for file_name in files:
        with open(os.path.join(data_directory, file_name), 'rb') as file:
            file_data = file.read()
            cursor.execute("""
                INSERT INTO excel_files (name, data) VALUES (%s, %s)
            """, (file_name, psycopg2.Binary(file_data)))
            conn.commit()

    # Listen for notifications for a set amount of excel files
    excel_file_count = 0
    while excel_file_count < len(files):
        conn.poll()
        while conn.notifies:
            notify = conn.notifies.pop(0)
            print(f"Notification received name: {notify.payload}")

            cursor.execute("""
                SELECT data FROM excel_files WHERE name = %s
            """, (notify.payload,))

            json_data = cursor.fetchone()

            df = pd.read_excel(io.BytesIO(json_data[0]), engine='openpyxl')

            print(f"Read Excel file into DataFrame with {len(df)} rows.")

            df = df.rename(columns={
                'Vendor': 'vendor_name',
                'Description': 'description',
                'Manufacturer Part Number': 'manufacturer_part_number',
                'List Price': 'list_price',
                'NASPO Price': 'naspo_price'
            })

            # Strip whitespace from all string columns
            df = df.map(lambda value: value.strip() if isinstance(value, str) else value)
            
            # Handle missing values initially
            df = df.fillna('N/A')

            # Strip \xa0 from list_price and naspo_price columns
            df["list_price"] = df["list_price"].astype(str).str.rstrip('\xa0')
            df["naspo_price"] = df["naspo_price"].astype(str).str.rstrip('\xa0')

            # Remove any commas and dollar signs from price columns
            df["list_price"] = df["list_price"].str.replace(r'[$,]', '', regex=True)
            df["naspo_price"] = df["naspo_price"].str.replace(r'[$,]', '', regex=True)

            # Remove rows where list_price or naspo_price contain alphabetic characters that are not N/A
            df = df[~df[['list_price', 'naspo_price']].apply(lambda row: row.str.contains(r'[a-zA-Z]', na=False) & (row != 'N/A')).any(axis=1)]

            # Convert price columns to numeric, replacing invalid values with None for MONEY type
            df["list_price"] = pd.to_numeric(df["list_price"], errors='coerce')
            df["naspo_price"] = pd.to_numeric(df["naspo_price"], errors='coerce')

            df.to_sql('naspo_information', engine, if_exists='append', index=False)

            excel_file_count += 1

    cursor.execute("UNLISTEN excel_file_inserted;")
    cursor.close()
    conn.close()
    
if __name__ == "__main__":
    main()