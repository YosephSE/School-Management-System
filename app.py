from flask import Flask, url_for, render_template, request, flash, redirect, session
# import py mongo to connect with mongodb
from pymongo import MongoClient
# import bcrypt to secure passwords
import bcrypt
# import flask to mysql connector
from flask_mysqldb import MySQL
# send mail library
from flask_mail import Mail, Message
# import time
import datetime

app = Flask(__name__)

#connect to MYSQLDB
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1212'
app.config['MYSQL_DB'] = 'school_web'

#connect to mail server
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'BGPHMS@gmail.com'
app.config['MAIL_PASSWORD'] = 'vjkcslwthvdgerod'

# connect to mongoDB
client = MongoClient('mongodb+srv://leolittleprogrammer:kal-4617@cluster0.lld6hyg.mongodb.net/test')
credentials_db = client.get_database('dej-web')
users_credential = credentials_db.user_credentials
app.secret_key = '832445652e`'

# initialize
mysql = MySQL(app)
mail = Mail(app)

# email function
def send_email(subject, recipient_email, email_content):
    msg = Message(subject = subject,
                  recipients=[recipient_email],
                  sender=app.config.get("MAIL_USERNAME"))
    msg.body = email_content
    mail.send(msg)

# route to home
@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM posts ORDER BY ID DESC LIMIT 3;")
    posts = cur.fetchall()
    cur.close()

    length = len(posts)
    return render_template('public/index.html', posts = posts, length = length)

#  routes for clubs
@app.route('/itclub')
def itclub():
    return render_template('public/itclub.html')

@app.route('/SandIclub')
def SandIclub():
    return render_template('public/SandIclub.html')

# route for about page
@app.route('/about')
def about():
    return render_template('public/about.html')

# route for principals page 
@app.route('/principals')
def principals():
    return render_template('public/principals.html')

# route for teachers page 
@app.route('/teachers')
def teachers():
    return render_template('public/teachers.html')

# route for G9-G12 page 
@app.route('/G9')
def G9():
    return render_template('public/G9.html')

@app.route('/G10')
def G10():
    return render_template('public/G10.html')

@app.route('/G11')
def G11():
    return render_template('public/G11.html')

@app.route('/G12')
def G12():
    return render_template('public/G12.html')

# route for staffs page 
@app.route('/staffs')
def staffs():
    return render_template('public/staffs.html')

# route for topstudent page 
@app.route('/topstudents')
def topstudent():
    return render_template('public/tstudents.html')

# route for events page 
@app.route('/events')
def events():
    return render_template('public/events.html')

# route for sign in section 
@app.route('/sign_in', methods=['POST','GET'])
def signin():
    if request.method == 'POST':
        rq = request.form
        email = rq['email'].lower()
        password = rq['passwd'].lower()

        user_email = users_credential.find_one({'Email': email})
        if user_email:
            if email:
                # if bcrypt.checkpw(password, user_email['password']):
                    session['user_email'] = email
                    return redirect('/admin')
            else:
                return 'Invalid email or password'
        else:
            return "Email not found"
    else:
        return render_template('public/sign_in.html')

# route for sign up page

@app.route('/sign_up', methods=['POST','GET'])
def sign_up():
    if request.method == 'POST':
        rq = request.form
        name = rq['name']
        email = rq['email']
        password = rq['passwd']

# checking if the name or email is taken
        name_found = users_credential.find_one({"username": name})
        email_found = users_credential.find_one({"email": email})

        if name_found:
            return print("User name already exists!")
        elif email_found:
            return print("Email already exists!")
        else:
            hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        newUser = {
            'Name': name,
            'Email':email,
            'Password': hashed
        }
        users_credential.insert_one(newUser)
        return redirect(url_for('admin'))
    else:
        return render_template('public/sign_up.html')

# route for Blog page 
@app.route('/blog')
def blog():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM posts ORDER BY ID DESC")
    posts = cur.fetchall()
    cur.close()
    return render_template("public/blog.html", posts = posts)

# route for award page 
@app.route('/award')
def award():
    return render_template('public/award.html')

# route for admin page
@app.route('/admin')
def admin():
    return render_template('admin/admin.html')
# blog post
@app.route('/post', methods=['GET', 'POST'])
def post():
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        now = datetime.datetime.now()
        year, month, date = now.strftime('%Y-%m-%d').split('-')
        month = int(month)
        months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
        time = now.strftime('%I:%M %p')
        time_str = f'{months[month - 1]} {date}, {year} {time}'
        cur0 = mysql.connection.cursor()
        cur0.execute("INSERT INTO posts (date, title, content) VALUES (%s, %s, %s)", (time_str, title, content))
        mysql.connection.commit()
        cur0.close()
        return redirect(url_for('post'))
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM posts ORDER BY ID DESC")

    posts = cur.fetchall()
    cur.close()
    return render_template('admin/post.html', posts = posts)

# delete post
@app.route('/admin/delete_post/<int:post_id>', methods=['POST'])
def delete_post(post_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM posts WHERE id = %s", (post_id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('post'))


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')