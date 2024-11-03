from database import Database
from users import User
from datetime import datetime
import os
class Print:
    def __init__(self, uuid:int, user:User, color:str, date_made, date_due:int, requests:str, status:int):
        self.uuid = uuid
        self.user = user
        self.color = color
        self.date_made = date_made
        self.date_due = date_due
        self.date_due_presentable = "Not kids print" if date_due==-1 else "Due this friday" if date_due ==0 else datetime.fromtimestamp(date_due).strftime('%Y-%m-%d')
        self.add_date_presentable = datetime.fromtimestamp(date_made).strftime('%Y-%m-%d %H:%M:%S')
        self.requests = requests    
        self.status = status
        self.status_presentable = "To Print" if status == 0 else "Printing" if status == 1 else "Completed"
    @staticmethod
    def create_print(user:User, color:str, date_made:int, date_due:int, requests:str):
        db = Database()
        uuid = db.create_print(user.uuid, color, date_made, date_due, requests)
        db.close()
        return Print(uuid, user, color, date_made, date_due, requests, 0)
    @staticmethod
    def get_print_by_id(uuid:int):
        db = Database()
        print_data = db.get_print_by_id(uuid)
        db.close()
        if print_data is not None:
            return Print(print_data[0], User.user_from_database(print_data[1]), print_data[2], print_data[3], print_data[4], print_data[5], print_data[6])
        return None
    @staticmethod
    def get_all_prints():
        db = Database()
        prints = db.get_all_prints()
        db.close()
        return [Print(print_data[0],User.user_from_database(print_data[1]), print_data[2], print_data[3], print_data[4], print_data[5], print_data[6]) for print_data in prints]
    @staticmethod
    def get_prints_by_user(user:User):
        db = Database()
        prints = db.get_prints_by_user(user.id)
        db.close()
        return [Print(print_data[0], user, print_data[2], print_data[3], print_data[4], print_data[5], print_data[6]) for print_data in prints]
    def update_status(self, status:int):
        db = Database()
        db.update_print_status(self.uuid, status)
        db.close()
    
    def dete(self):
        db = Database()
        db.delete_print(self.uuid)
        db.close()
        os.remove(f"./data/uploads/{self.uuid}.stl")
    
    def __str__(self):
        return f"Print for {self.user.username} made on {self.date_made} due on {self.date_due} with requests {self.requests} and status {self.status}"
    def __repr__(self):
        return f"Print for {self.user.username} made on {self.date_made} due on {self.date_due} with requests {self.requests} and status {self.status}"