import os
import time

os.makedirs("./data/uploads", exist_ok=True)

from flask import Flask, render_template, request, make_response, url_for, redirect, send_file
from flask_simple_captcha import CAPTCHA

from utils import hash
from users import User
from prints import Print
from permission import cheek_permission, log_in, log_out
from logger import Logger


app = Flask(__name__)

CAPTCHA_CONFIG = {
    'SECRET_CAPTCHA_KEY': 'nnqTwYKmiAiEuq9DHY13*IA^&JkCWJ6TNsmT*3dNY*EO52Ex1sz9y@*2zBwHl4#it*lQ0Z0A@gb5a$Opsli#ALU6t0yW1S0WELyncDSJpQ8pIbuCcn%EHHw6NW4AVCb1',
    'CAPTCHA_LENGTH': 2,
    'CAPTCHA_DIGITS': False,
    'EXPIRE_SECONDS': 600,
    'EXCLUDE_VISUALLY_SIMILAR': True,
    'ONLY_UPPERCASE': True
}

captcha = CAPTCHA(config=CAPTCHA_CONFIG)
app = captcha.init_app(app)
logger = Logger("log.txt")

@app.route("/", methods=['GET'])
def home():
    logger.log_request(request)
    permission_cheek = cheek_permission(request, 0)
    if permission_cheek[0]:
        logger.log(f"Home Requested by {permission_cheek[1].username}")
        prints = Print.get_prints_by_user(permission_cheek[1])
        return render_template('home.html', prints=prints)
    logger.log_permission_error(request)
    return redirect(url_for('login'))

@app.route('/print', methods=['GET', 'POST'])
def upload():
    logger.log_request(request)
    permission_cheek = cheek_permission(request, 0)
    if permission_cheek[0]:
        if request.method == "GET":
            return render_template('print.html')
        elif request.method == 'POST':
            user = permission_cheek[1]
            file = request.files['file']
            if file.filename.endswith('.stl'):
                file.save(f"./data/uploads/{file.filename}")
                color = request.form.get('color')
                due_in = request.form.get('date')
                requirements = request.form.get('reqs')
                print_uuid = user.create_print(color, int(due_in), requirements)
                os.rename(f"./data/uploads/{file.filename}", f"./data/uploads/{print_uuid}.{file.filename.split('.')[-1]}")
                logger.log(f"Print Created with ID: {print_uuid} by {user.username}")
                return render_template('print.html', message="Print Created with ID: "+str(print_uuid))
            else:
                logger.log_error(request, "Invalid File Type")
                return render_template('print.html', error="Invalid File Type")    
    logger.log_permission_error(request)
    return redirect(url_for('login'))
@app.route("/queue", methods=['GET'])
def queue():
    logger.log_request(request)
    permission_cheek = cheek_permission(request, 1)
    if permission_cheek[0]:
        all_prints = Print.get_all_prints()
        to_print = [print_data for print_data in all_prints if print_data.status == 0] 
        printing = [print_data for print_data in all_prints if print_data.status == 1]
        completed = [print_data for print_data in all_prints if print_data.status == 2]
        logger.log(f"Queue Requested by {permission_cheek[1].username}")
        return render_template('queue.html', to_print=to_print, printing=printing, done=completed)
    logger.log_permission_error(request)
    return redirect(url_for('login'))

@app.route("/login", methods=['GET', 'POST'])
def login():
    logger.log_request(request)
    if request.method == "GET":
        if cheek_permission(request, 0)[0]:
            return redirect(url_for('home'))
        new_captcha = captcha.create()
        return render_template('login.html', captcha=new_captcha)
    if request.method == 'POST':
        c_hash = request.form.get('captcha-hash')
        c_text = request.form.get('captcha-text').upper()
        if captcha.verify(c_text, c_hash):
            user_login = User.login(request.form.get("user"), request.form.get("password"))
            if user_login is not None:
                logger.log_login(user_login)
                return log_in(user_login)
            else:
                logger.log_invalid_login(request)
                msg = "Invalid Username or Password"
        else:
            logger.log_captcha_error(request)
            msg = "Invalid Captcha"
        new_captcha = captcha.create()
        return render_template('login.html', captcha=new_captcha,error = msg)

@app.route("/logout", methods=['GET'])
def logout():
    logger.log_request(request)
    logger.log_logout(cheek_permission(request, 0)[1])
    return log_out(request)

@app.route("/download/<id>", methods=['GET'])
def download(id):
    logger.log_request(request)
    permission_cheek = cheek_permission(request, 0)
    if permission_cheek[0]:
        print_data = Print.get_print_by_id(id)
        print(print_data.user, permission_cheek[1], permission_cheek[1].permission)
        if print_data.user != permission_cheek[1] and permission_cheek[1].permission == 0:
            logger.log_permission_error(request)
            return render_template('error.html', error="You do not have permission"),404
        if print_data is not None:
            try:
                logger.log(f"Download by {permission_cheek[1].username} for Print ID: {id}")
                return send_file(f"./data/uploads/{id}.stl", as_attachment=True)
            except FileNotFoundError:
                logger.log_error(request, "File Not Found with print ID: "+id)
                return render_template('error.html', error="File Not Found"),404
        else:
            logger.log_error(request, "Print Not Found with ID: "+id)
    logger.log_permission_error(request)
    return redirect(url_for('login'))

@app.route("/admin", methods=['GET'])
def admin():
    logger.log_request(request)
    permission_cheek = cheek_permission(request, 2)
    if permission_cheek[0]:
        users = User.get_all_users()
        return render_template('admin.html', users=users)
    logger.log_permission_error(request)
    return redirect(url_for('login'))

@app.route("/api/printing/<id>", methods=['POST'])
def printing(id):
    logger.log_request(request)
    permission_cheek = cheek_permission(request, 1)
    if permission_cheek[0]:
        print_data = Print.get_print_by_id(id)
        if print_data is not None:
            logger.log(f"Printing by {permission_cheek[1].username} for Print ID: {id}")
            print_data.update_status(1)
            return {"status":"success"}
        else:
            logger.log_error(request, "Print Not Found with ID: "+id)
    logger.log_permission_error(request)
    return {"status":"error"}

@app.route("/api/completed/<id>", methods=['POST'])
def completed(id):
    logger.log_request(request)
    permission_cheek = cheek_permission(request, 1)
    if permission_cheek[0]:
        print_data = Print.get_print_by_id(id)
        if print_data is not None:
            logger.log(f"Completed by {permission_cheek[1].username} for Print ID: {id}")
            print_data.update_status(2)
            return {"status":"success"}
        else:
            logger.log_error(request, "Print Not Found with ID: "+id)
    logger.log_permission_error(request)
    return {"status":"error"}

@app.route("/api/reprint/<id>", methods=['POST'])
def reprint(id):
    logger.log_request(request)
    permission_cheek = cheek_permission(request, 1)
    if permission_cheek[0]:
        print_data = Print.get_print_by_id(id)
        if print_data is not None:
            logger.log(f"Reprinting by {permission_cheek[1].username} for Print ID: {id}")
            print_data.update_status(0)
            return {"status":"success"}
        else:
            logger.log_error(request, "Print Not Found with ID: "+id)
    logger.log_permission_error(request)
    return {"status":"error"}

@app.route("/api/delete/<id>", methods=['POST'])
def deleteitem(id):
    logger.log_request(request)
    permission_cheek = cheek_permission(request, 0)
    print_data = Print.get_print_by_id(id)
    if print_data is None:
        logger.log_error(request, "Print Not Found with ID: "+id)
    else:
        print(permission_cheek[1], print_data.user)
        if permission_cheek[1].permission>0 or print_data.user == permission_cheek[1]:
            logger.log(f"Deleted by {permission_cheek[1].username} for Print ID: {id}")
            print_data.dete()
            return {"status":"success"}
    logger.log_permission_error(request)
    return {"status":"error"}

@app.route("/api/deleteuser/<id>", methods=['POST'])
def deleteuser(id):
    logger.log_request(request)
    permission_cheek = cheek_permission(request, 2)
    user = User.get_user(id)
    if user is None:
        logger.log_error(request, "User Not Found with ID: "+id)
    else:
        if permission_cheek[0] and user.permission<2:
            logger.log(f"Deleted User by {permission_cheek[1].username} for User ID: {id}")
            user.delete()
            return {"status":"success"}
    return {"status":"error"}

@app.route("/api/adduser", methods=['POST'])
def adduser():
    logger.log_request(request)
    permission_cheek = cheek_permission(request, 2)
    if permission_cheek[0]:
        username = request.json.get('username')
        password = request.json.get('password')
        permission = request.json.get('permission')
        try:
            permission = int(permission)
        except:
            pass
        if username is None or password is None or permission is None:
            logger.log_error(request, "Missing Data")
            return {"status":"error"}
        if type(permission) != int or permission < 0 or permission > 2:
            logger.log_error(request, "Invalid Permission")
            return {"status":"error"}
        user = User.create_user(username, password, permission)
        if user is not None:
            logger.log(f"Added User by {permission_cheek[1].username} for User ID: {user.id}")
            return {"status":"success"}
        else:
            logger.log_error(request, "User Already Exists")
    return {"status":"error"}


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

app.run("0.0.0.0", 5001)