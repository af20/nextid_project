import sqlite3
from sqlite3 import Error
from os.path import exists


def create_connection(db_file):
  """ create a database connection to a SQLite database """
  conn = None
  try:
    conn = sqlite3.connect(db_file)
    #print(sqlite3.version)
  except Error as e:
    print('Error', e)
  finally:
    if conn:
      conn.close()



if __name__ == '__main__':
  FILE = 'database.db'
  file_exists = exists(FILE)
  print('file_exists', file_exists)
  if file_exists == False:
    with open(FILE, 'w') as f:
      f.write('')
  create_connection(FILE)
