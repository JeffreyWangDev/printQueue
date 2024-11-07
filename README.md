# 3d Printer Queue
## Used when mangaing many printers and people printing 

![image](https://github.com/user-attachments/assets/c61809f2-4e03-48b5-aa28-a2278b41c3bb)

Demo at [HERE](https://printqueue.jeffrey.hackclub.app/login) with the Super Admin log in as ``SAdmin:Pass12``. You can then create an account at /admin.
- Make sure to edit the user.py file and uncomment the random password generator when using this


# Fetures 
- Home Page: Displays user-specific prints.
- Upload Print: Allows users to upload and create print records.
- Queue Page: Shows the queue of prints (to print, printing, completed).
- Login/Logout: Handles user authentication with captcha verification.
- Download Print: Allows users to download print files.
- Admin Page: Displays a list of all users (admin only).
- Print Management API:
  - Printing: Updates print status to "printing".
  - Printing: Updates print status to "printing".
  - Completed: Updates print status to "completed".
  - Reprint: Updates print status to "reprint".
  - Delete Print: Deletes a print record.
- User Management API:
  - Add User: Adds a new user (admin only).
  - Delete User: Deletes a user record (admin only).
- Error Handling: Custom 404 error page.
- Logging: Logs various actions and errors.
- Permission Checks: Ensures users have the correct permissions for actions.

# Installation

1. Clone the Repository:
```
git clone https://github.com/jeffreywangdev/printQueue.git
cd printQueue
```

2. Install Dependencies:
```
pip install -r requirements.txt
```

3. Run the Application:
```
python main.py
```

4. Access the Application: Open your web browser and go to http://localhost:5001.

- Docker (Optional):
1. Build the Docker image:
```
docker build -t printqueue .
```

2. Run the Docker container:
```
docker run -p 80:80 printqueue
```
