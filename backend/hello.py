import os
from flask import Flask, render_template
import mysql.connector
import schema2
from mysql.connector import errorcode


class DBManager:
    def __init__(self, database='example', host="db", user="root", password_file=None):
        pf = open(password_file, 'r')
        self.connection = mysql.connector.connect(
            user=user, 
            password=pf.read(),
            host=host, # name of the mysql service as set in the docker-compose file
            database=database,
            auth_plugin='mysql_native_password'
        )
        pf.close()
        self.cursor = self.connection.cursor()
    
    def populate_db(self):
        self.cursor.execute('DROP TABLE IF EXISTS blog')
        self.cursor.execute('CREATE TABLE blog (id INT AUTO_INCREMENT PRIMARY KEY, title VARCHAR(255))')
        self.cursor.executemany('INSERT INTO blog (id, title) VALUES (%s, %s);', [(i, 'Blog post #%d'% i) for i in range (1,7)])
        self.connection.commit()

    def populate_db2(self):
        self.cursor.execute('DROP TABLE IF EXISTS Student')
        self.cursor.execute('CREATE TABLE Student (id INT AUTO_INCREMENT PRIMARY KEY, password VARCHAR(255))')
        add_student = ('INSERT INTO Student(id, password) VALUES (123,"pw")')
        val=  ("123", 'pw')
        self.cursor.execute(add_student)
        self.connection.commit()

    def query_titles(self):
        self.cursor.execute('SELECT title FROM blog')
        rec = []
        for c in self.cursor:
            rec.append(c[0])
        return rec

    def fill_database(self):
        tables = schema2.get_tables()
        data = schema2.get_data()
        for table_name in tables:
            table_description = tables[table_name]
#            info = data[table_name+"info"]
            try:
                print("Creating table {}: ".format(table_name), end='')
                self.cursor.execute(table_description)
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                    print("already exists.")
                else:
                    print(err.msg)
            else:
                self.connection.commit()
                print("OK")

    def sample_data(self):
        data = schema2.get_data()
        instructions = schema2.get_instructions()
        names = schema2.get_names()
        i=0
        for item in data:
            inst = instructions[i]
            info = data[item]
            print(info)
            i +=1
            self.cursor.execute(inst,info)
            self.connection.commit()

    def student(self):
        add_student = ('INSERT INTO student(student_id, f_name, l_name,password) VALUES (123,"niamh","hen","pw")')
        self.cursor.execute(add_student)
        self.connection.commit()


server = Flask(__name__)
conn = None
newConn = None

#@server.route('/')
#    return render_template('login.html')

@server.route('/',methods = ['POST','GET'])
def init():
    msg=''
    global conn
    if not conn:
        conn = DBManager(password_file='/run/secrets/db-password')
        conn.populate_db()
        conn.populate_db2()
        conn.fill_database()
        #conn.student()
        conn.sample_data()


#    rec = conn.query_titles()

#    if request.method == 'POST' and 'id' in request.form and 'password' in request.form :
#        loginid = request.form['id']
#        password = request.form['password']
#        check = loginid + password
#        return check
#        conn.cursor.execute('SELECT * FROM Student WHERE id = % s AND password = % s', (loginid, password,))
#        #return render_template('home.html',blog=conn)
#        account = conn.fetchone()
#        if account:
##            session['loggedin'] = True
##            session['id'] = account['id']
##            session['username'] = account['username']
#            msg = 'Logged in successfully !'
#            return render_template('home.html')
#        else:
#            msg= 'Incorrect log in details'
    return render_template('login2.html',msg="start")

@server.route('/login', methods = ['POST','GET'])
def login(): 
    msg = '' 
#    if request.method == 'POST' and 'username' in request.form and 'password' in request.form: 
#        username = request.form['username'] 
#        password = request.form['password']
#        return render_template('home.html',blog=msg)
        #cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
        #conn.cursor.execute('SELECT * FROM Student WHERE username = % s AND password = % s', (username, password, )) 
        #account = cursor.fetchone() 
       # if account: 
       #     session['loggedin'] = True
       #     session['id'] = account['id'] 
       #     session['username'] = account['username'] 
       #     msg = 'Logged in successfully !'
       #     return render_template('home.html',blog=msg)
       # else: 
       #     msg = 'Incorrect username / password !'
    return render_template('home.html', blog = msg)

#def check_login():
#    msg=''
#    if request.method == 'POST' :
#        msg="ok"
#        return msg
#        #        loginid = request.form['id']
##        password = request.form['password']
##        check = loginid + password
##        return check
#    else:
#        msg='not ok '
#    return render_template('login2.html',msg=msg) 

@server.route('/home/', methods = ['POST','GET'])
def home_page():
    blog = conn.query_titles() 
    return render_template('home.html',blog=blog)

@server.route('/admin_home/', methods = ['POST','GET'])
def admin_home_page():
    return render_template('admin_home.html')

@server.route('/lect_home/')
def lect_home_page():
    return render_template('lect_home.html')

@server.route('/calendarview/')
def calendar_page():
    return render_template('calendar.html')

@server.route('/mapview/')
def map_page():
    return render_template('map.html')

@server.route('/examofficeinfo/')
def info_page():
    return render_template('info.html')


if __name__ == '__main__':
    server.run(debug= True)
