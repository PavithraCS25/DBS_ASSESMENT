import sqlite3
from sqlite3 import Error
from flask import Flask, jsonify
from make_predictions import MakePrediction
import datetime
import pandas as pd

class DAO:
    def dict_factory(self, cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d


    def load_predictions(self, filename, predicted_data):
        conn = sqlite3.connect('database.db')
        try:
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS "audit_test_file" ("file_id" INTEGER PRIMARY KEY AUTOINCREMENT,
            "filename"	TEXT NOT NULL UNIQUE)''')
        except Exception as E:
            print('Error :', E)
        else:
            print('table already available')

        try:
            rowid = cursor.execute('select case when rownum not null then rownum+1 else 1 end as rownum '
                           'from (select max(rowid)  as rownum from audit_test_file);').fetchone()[0]

            cursor.execute("INSERT INTO audit_test_file VALUES (?,?)", (rowid, filename))
            print('data inserted')
        except Exception as E:
            print('Error : ', E)
            conn.commit()

        if not predicted_data is None:
            try:
                cursor = conn.cursor()
                cursor.execute('''CREATE TABLE IF NOT EXISTS "predictions" ("file_id"	INTEGER NOT NULL,"track_id"	TEXT NOT NULL
                ,"title"	TEXT NOT NULL,"LR_classified_genre"	TEXT,"NN_classified_genre"	TEXT,
                "created_timestamp"	TEXT NOT NULL,"updated_timestamp"	TEXT)''')
            except Exception as E:
                print('Error :', E)

            try:
                predicted_data['file_id'] = rowid
                predicted_data.to_sql(name='predictions', con=conn, if_exists='append', index=False)
                print('data inserted')
            except Exception as E:
                print('Error : ', E)
                conn.commit()
        else:
            print('Dataframe empty')

    def get_audit_files(self):
        conn = sqlite3.connect('database.db')
        print(str(conn))
        conn.row_factory = self.dict_factory
        cur = conn.cursor()
        auditrecords = cur.execute('select * from audit_test_file;').fetchall()
        return jsonify(auditrecords)


    def prediction_all(self,file_id):
        conn = sqlite3.connect('database.db')
        print(str(conn))
        conn.row_factory = self.dict_factory
        cur = conn.cursor()
        if file_id == 'all':
            predictions = cur.execute('SELECT * FROM predictions p ,audit_test_file a '
                                      'where p.file_id = a.file_id;').fetchall()
        else:
            predictions = cur.execute(
                'SELECT * FROM predictions p ,audit_test_file a where p.file_id = a.file_id '
                'and p.file_id = ?', (file_id, )).fetchall()
        return jsonify(predictions)

    def get_prediction_trackid(self, track_id):
        conn = sqlite3.connect('database.db')
        print(str(conn))
        conn.row_factory = self.dict_factory
        cur = conn.cursor()
        predictions = cur.execute('SELECT * FROM predictions p,audit_test_file a  '
                                  'WHERE p.file_id = a.file_id and track_id = ?', (track_id,)).fetchone()
        return jsonify(predictions)

    def get_all_genres(self):
        conn = sqlite3.connect('database.db')
        print(str(conn))
        conn.row_factory = self.dict_factory
        cur = conn.cursor()
        genres = cur.execute('SELECT distinct LR_classified_genre FROM predictions;').fetchall()
        return jsonify(genres)

    def get_all_titles(self, genre):
        print(genre)
        conn = sqlite3.connect('database.db')
        print(str(conn))
        conn.row_factory = self.dict_factory
        cur = conn.cursor()
        if genre == 'all':
            titles = cur.execute('SELECT distinct title FROM predictions;').fetchall()
        else:
            titles = cur.execute('SELECT distinct title FROM predictions where LR_classified_genre = ?',
                                 (genre,)).fetchall()
        print(jsonify(titles))
        return jsonify(titles)

    def get_prediction_title(self, title):
        conn = sqlite3.connect('database.db')
        print(str(conn))
        conn.row_factory = self.dict_factory
        cur = conn.cursor()
        predictions = cur.execute('SELECT * FROM predictions p,audit_test_file a WHERE p.file_id = a.file_id and LOWER(title) = ?', (title.lower(),)).fetchone()
        return jsonify(predictions)

    def create_connection(self, db_file):
        """ create a database connection to a SQLite database """
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            print(sqlite3.version)
        except Error as e:
            print(e)
        finally:
            if conn:
                conn.close()

    def get_dao(self, filename, file):
        test_data = pd.read_csv(file)
        print(test_data)
        mp = MakePrediction()
        labels = mp.load_labels()
        x_test = mp.get_test_data(test_data)
        predictions = mp.make_predictions(x_test, labels)
        #predictions['last_file_name'] = filename
        predictions['created_timestamp'] = datetime.datetime.now()
        predictions['updated_timestamp'] = datetime.datetime.now()
        self.load_predictions(filename, predictions)