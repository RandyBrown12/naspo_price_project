CREATE TABLE IF NOT EXISTS excel_files (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    data BYTEA NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS NASPO_information (
    id SERIAL PRIMARY KEY,
    vendor_name VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    manufacturer_part_number TEXT NOT NULL,
    list_price MONEY,
    naspo_price MONEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE OR REPLACE FUNCTION notify_excel_file_inserted()
RETURNS TRIGGER AS $$
BEGIN
    PERFORM pg_notify('excel_file_inserted', NEW.name);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS excel_file_inserted_trigger ON excel_files;
CREATE TRIGGER excel_file_inserted_trigger
AFTER INSERT ON excel_files
FOR EACH ROW EXECUTE FUNCTION notify_excel_file_inserted();

LISTEN excel_file_inserted;