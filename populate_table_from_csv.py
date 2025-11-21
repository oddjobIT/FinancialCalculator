""" Reads a csv and populates a DB table.
    Status: development
"""

import csv
import mariadb
import sys
import config


#connect to DB
#open csv file for reading
#read each line and insert into table

sourceFileDir = config.dataDirectory
testFile = config.fixedTestFile
runState = config.mode

def requestFileName():
    if runState == "Test":
        fileName = testFile
    else:
        fileName = input("Enter the file name (with .csv extension): ")
    return fileName

DB_CONFIG = {
    'user': config.databaseUser,
    'password': config.databaseUserPass,
    'host': config.databaseHost,
    'database': config.database
}

TABLE_NAME = config.table

def connect_to_db():
    try:
        print(f"host = {DB_CONFIG['host']}")
        conn = mariadb.connect(**DB_CONFIG)
        cursor = conn.cursor()
        return cursor
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)

def insert_csv_data(cursor, fileName):
    with open(sourceFileDir + fileName, 'r', encoding='utf-8') as infile:
        reader = csv.reader(infile)
        next(reader)  # Skip header row  

        #insertQuery = f"INSERT INTO {TABLE_NAME} (Date, Description, Amount, Status) VALUES (?, ?, ?, ?)"

        for row in reader:
            print(row)
            try:
                cursor.execute(
                    f"INSERT INTO {TABLE_NAME} (Date, Description, Amount, Status) VALUES (?, ?, ?, ?)",
                    (row[0], row[1], float(row[2]), row[3])
                )
            except mariadb.Error as e:
                print(f"Error inserting data: {e}")


def main():
    fileName = requestFileName()
    cursor = connect_to_db()
    insert_csv_data(cursor, fileName)
    cursor.connection.commit()
    cursor.connection.close()

if __name__ == "__main__":
    main()

