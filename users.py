from database import Database
import time
import random
import os
class Permission:
    user = 0
    admin = 1
    superadmin = 2


class User:
    def __init__(self, username, id, permission:int=0):
        self.username = username
        self.id = id
        self.permission = permission
        self.permission_pretty = ["User", "Admin", "Superadmin"][permission]

    @staticmethod
    def user_from_database(id):
        db = Database()
        user = db.get_user(id)
        db.close()
        if user is not None:
            return User(user[1], user[0], user[3])
        return None
    
    @staticmethod
    def login(username:str, password:str):
        db = Database()
        user = db.login(username,password)
        db.close()
        if user is not None:
            return User.user_from_database(user)
        return None
    
    @staticmethod
    def get_user(id):
        db = Database()
        user = db.get_user(id)
        db.close()
        
        if user is not None:
            user = User(user[1], user[0], user[3])
            return user
        return None
    
    @staticmethod
    def get_user_by_username(username):
        db = Database()
        user = db.get_user_by_username(username)
        db.close()
        if user is not None:
            return user
        return None
    
    @staticmethod
    def create_user(username:str, password:str, permission:int=0):
        if User.get_user_by_username(username) is not None:
            return None
        db = Database()
        db.create_user(username,password,permission)
        db.close()
        return User.login(username, password)
    
    @staticmethod
    def get_all_users():
        db = Database()
        users_id = db.get_all_user_uuids()
        db.close()
        print(users_id)
        users = [User.user_from_database(int(uuid[0])) for uuid in users_id]
        print(users)
        return users
    
    def create_print(self, color:str, due_in, requests:str):
        if due_in < 0:
            due_in = -1
        elif due_in == 0:
            due_in = 0
        else:
            due_in = time.time() + due_in*24*60*60
        db = Database()
        uuid = db.create_print(self.id, color, time.time(), due_in, requests)
        db.close()
        return uuid
    def is_admin(self):
        if self.permission == 1 or self.permission == 2:
            return True
        return False
    def is_superadmin(self):
        if self.permission == 2:
            return True
        return False
    
    def delete(self):
        db = Database()
        db.delete_user(self.id)
        db.close()
    
    def __str__(self):
        return f"User {self.username} with ID {self.id} and permission {self.permission}"
    def __repr__(self):
        return f"User {self.username} with ID {self.id} and permission {self.permission}"
    def __eq__(self, other):
        return self.id == other.id    

#if not os.path.isfile("./data/admin.txt"):
    # pw = str(random.randint(1000,100000))
pw = "Pass12"
a = User.create_user("SAdmin", pw, 2)
#with open("./data/admin.txt","w+") as file:
    #file.write(f"SAdmin {pw}")
