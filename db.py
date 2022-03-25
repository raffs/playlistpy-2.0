import os
import pymysql
from flask import jsonify

db_user = os.environ.get('CLOUD_SQL_USERNAME')
db_password = os.environ.get('CLOUD_SQL_PASSWORD')
db_name = os.environ.get('CLOUD_SQL_DATABASE_NAME')
db_local_host = os.environ.get('DB_LOCAL_HOST')
db_connection_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME')

def open_connection():
    try:
        if os.environ.get('GAE_ENV') == 'standard':
            unix_socket = '/cloudsql/{}'.format(db_connection_name)
            conn = pymysql.connect(user=db_user, password=db_password,
                                unix_socket=unix_socket, db=db_name,
                                cursorclass=pymysql.cursors.DictCursor
                                )
        else:
            conn = pymysql.connect(user=db_user, password=db_password,
                                host=db_local_host, db=db_name)

    except pymysql.MySQLError as e:
        print(e)

    return conn

def conv_func(list_data):
    dic ={ "SONG_ID":list_data[0],
          "SONG_NAME":list_data[1],
          "SONG_ARTIST":list_data[2],
          "SONG_GENRE": list_data[3]
          }
    return dic

def get_songs():
    conn = open_connection()
    with conn.cursor() as cursor:
        result = cursor.execute('SELECT * FROM songs;')
        songs = cursor.fetchall()
        if result > 0:
           new_data=[]
           for i in songs:
             new_data.append(conv_func(i))

           got_songs = jsonify(new_data)

        else:
            got_songs = 'Nenhuma Musica Cadastrada na Playlist'
    conn.close()

    return got_songs
