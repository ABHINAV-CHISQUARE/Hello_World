import sqlite3

connection = sqlite3.Connection('my_learning.db')

try:
    cursor=connection.cursor()
    cursor.execute('''create table if not exists users(id integer primary key, name text,score integer)''')

    df_pd=pd.read
    connection.commit()
    print('record insertion successfully!')

    cursor.execute('select * from users')
    print('database content :',cursor.fetchall())

except sqlite3.Error as e:
    print(f'an error occured: {e}')
finally:
    connection.close()
    print('connection closed')