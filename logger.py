import datetime as dt
from pathlib import Path 

class Logger:
    def __init__(self, log_file):
        self.log_file ="./data/"+log_file
        file_path = Path(self.log_file) 
        if not file_path.exists(): 
            with open(file_path, 'w') as file: 
                pass
    def log(self, message):
        with open(self.log_file, 'a') as f:
            f.write(message + '\n')
    def log_request(self, request):
        self.log(f"Request from {request.remote_addr} at {dt.datetime.now()} for {request.path}")
    def log_login(self, user):
        self.log(f"Login from {user.username} at {dt.datetime.now()}")
    def log_logout(self, user):
        if user is not None:
            self.log(f"Logout from {user.username} at {dt.datetime.now()}")
    def log_permission_error(self, request):
        self.log(f"Permission error from {request.remote_addr} at {dt.datetime.now()} for {request.path}")
    def log_captcha_error(self, request):
        self.log(f"Captcha error from {request.remote_addr} at {dt.datetime.now()} for {request.path}")
    def log_invalid_login(self, request):
        self.log(f"Invalid login from {request.remote_addr} at {dt.datetime.now()} for {request.form.get('user')}")
    def log_error(self, request, error):
        self.log(f"Error from {request.remote_addr} at {dt.datetime.now()} for {request.path}: {error}")