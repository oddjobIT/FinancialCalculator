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

DB_CONFIG = {
    'user': config.databaseUser,
    'password': config.databaseUserPass,
    'host': config.databaseHost,
    'database': config.database
}

def requestFileName():
    """If the filemode is Test then use the test file listed in config.py
       Otherwise request the file name from the user
       No error checking is done here.
    """
    if runState == "Test":
        fileName = testFile
    else:
        fileName = input("Enter the file name (with .csv extension): ")
    return fileName


def requestTableName():
    """If the filemode is Test then use the table listed in config.py
       Otherwise request the table name from the user
       No error checking is done here.
    """
    if runState == "Test":
        tableName = config.table
    else:
        tableName = input("Enter the table name for account: ")
    return tableName


def connect_to_db():
    """ Connect to MariaDB Platform """
    try:
        print(f"host = {DB_CONFIG['host']}")
        conn = mariadb.connect(**DB_CONFIG)
        cursor = conn.cursor()
        return cursor
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)

def insert_csv_data(cursor, fileName, tableName):
    """ Insert data from CSV file into the specified table """
    with open(sourceFileDir + fileName, 'r', encoding='utf-8') as infile:
        reader = csv.reader(infile)
        next(reader)  # Skip header row  
        for row in reader:
            print(row)
            try:
                cursor.execute(
                    f"INSERT INTO {tableName} (Date, Description, Amount, Status) VALUES (?, ?, ?, ?)",
                    (row[0], row[1], float(row[2]), row[3])
                )
            except mariadb.Error as e:
                print(f"Error inserting data: {e}")


def main():
    fileName = requestFileName()
    tableName = requestTableName()
    cursor = connect_to_db()
    insert_csv_data(cursor, fileName, tableName)
    cursor.connection.commit()
    cursor.connection.close()

if __name__ == "__main__":
    main()

