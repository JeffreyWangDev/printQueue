import sqlite3
import random
from utils import hash
class Database:
    def __init__(self):
        self.conn = sqlite3.connect("./data/main.db")
        self.create_table()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                uuid INTEGER PRIMARY KEY NOT NULL,
                name TEXT NOT NULL,
                pwhash TEXT NOT NULL,
                permission INTEGER DEFAULT '0'
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS prints (
                uuid INTEGER PRIMARY KEY NOT NULL,
                user TEXT NOT NULL,
                color TEXT NOT NULL,
                date_made INTEGER NOT NULL,
                date_due INTEGER,
                requests TEXT,
                status INTEGER DEFAULT '0'
            )
        ''')
        self.conn.commit()
        cursor.close()
    
    def generateUUID(self, table, uuid = None):
        cursor = self.conn.cursor()
        if uuid is None:
            uuid = random.randint(100000, 999999)
        if table == "users":
            cursor.execute('''
                SELECT * FROM users WHERE uuid = ?
            ''', (uuid,))
        elif table == "prints":
            cursor.execute('''
                SELECT * FROM prints WHERE uuid = ?
            ''', (uuid,))
        fetched = cursor.fetchone()

        if fetched is not None:
            return self.generateUUID(table)
        return uuid

    def create_user(self, name:str, password:str, permission:int=0):
        pwhash = hash(password)
        uuid = self.generateUUID("users")
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO users (uuid, name, pwhash, permission) VALUES (?, ?, ?, ?)
        ''', (uuid, name, pwhash, permission))
        self.conn.commit()
        cursor.close()
    
    def login(self, username, password):
        pwhash = hash(password)
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT uuid FROM users WHERE name = ? AND pwhash = ?
        ''', (username, pwhash))
        fetched = cursor.fetchone()
        cursor.close()
        return fetched[0] if fetched is not None else None

    def get_user(self, uuid):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT * FROM users WHERE uuid = ?
        ''', (uuid,))
        fetched = cursor.fetchone()
        cursor.close()
        return fetched

    def get_user_by_username(self, username):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT * FROM users WHERE name = ?
        ''', (username,))
        fetched = cursor.fetchone()
        cursor.close()
        return fetched
    
    def get_all_user_uuids(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT uuid FROM users
        ''')
        fetched = cursor.fetchall()
        cursor.close()
        return fetched

    def delete_user(self, uuid):
        cursor = self.conn.cursor()
        cursor.execute('''
            DELETE FROM users WHERE uuid = ?
        ''', (uuid,))
        self.conn.commit()
        cursor.close()
    
    def create_print(self, user, color, date_made:int, date_due:int, requests):
        uuid = self.generateUUID("prints")
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO prints (uuid, user, color, date_made, date_due, requests) VALUES (?, ?, ?, ?, ?, ?)
        ''',(uuid,user,color,date_made,date_due,requests))
        self.conn.commit()
        cursor.close()
        return uuid
    def get_print_by_id(self,uuid):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT * FROM prints WHERE uuid = ?
        ''',(uuid,))
        fetched = cursor.fetchone()
        cursor.close()
        return fetched
    def get_all_prints(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT * FROM prints
        ''')
        fetched = cursor.fetchall()
        cursor.close()
        return fetched
    def get_prints_by_user(self,user):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT * FROM prints WHERE user = ?
        ''',(user,))
        fetched = cursor.fetchall()
        cursor.close()
        return fetched
    def update_print_status(self,uuid,status):
        cursor = self.conn.cursor()
        cursor.execute('''
            UPDATE prints SET status = ? WHERE uuid = ?
        ''',(status,uuid))
        self.conn.commit()
        cursor.close()
    def delete_print(self,uuid):
        cursor = self.conn.cursor()
        cursor.execute('''
            DELETE FROM prints WHERE uuid = ?
        ''',(uuid,))
        self.conn.commit()
        cursor.close()    
    def close(self):
        self.conn.close()