import os
from flask import Flask, render_template,request,session
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
        self.cursor = self.connection.cursor(buffered=True)
#        self.cursor(buffered=True)
    
    def create_database_tables(self):
        tables = schema2.get_tables()
        data = schema2.get_data()
        for table_name in tables:
            table_description = tables[table_name]
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
            i +=1
            try:
                self.cursor.executemany(inst,info)
                self.connection.commit()
            except mysql.connector.Error as err:
                    print(err.msg)
    
    def get_student_data(self,id_no):
        self.cursor.execute('SELECT f_name,l_name FROM student WHERE student_id = %s ', (id_no,))
        f_name,l_name = self.cursor.fetchone()
        self.cursor.execute('SELECT course_code FROM course_student WHERE student_id = %s ', (id_no,))
        course = self.cursor.fetchone()
        return f_name,l_name,course
        
    def get_exam_data(self,id_no):
        exam_list_details=[]
#        cursor2 = self.cursor(buffered=True)
        self.cursor.execute('SELECT exam_id FROM student_exam WHERE student_id = %s ', (id_no,))
        try:
            exams = self.cursor.fetchall()
        except mysql.connector.errors.InterfaceError as ie:
            if ie.msg == 'No result set to fetch from.':
        # no problem, we were just at the end of the result set
                pass
            else:
                raise
        for e in exams:
            self.cursor.execute('SELECT module_code,time,date,duration,venue FROM exam WHERE exam_id = %s ', (e[0],))
            code,time,date,duration,venue = self.cursor.fetchone()
            self.cursor.execute('SELECT name FROM module WHERE code = %s ', (code,))
            name = self.cursor.fetchone()
            self.cursor.execute('SELECT lecturer_notes FROM module WHERE code = %s ', (code,))
            notes = self.cursor.fetchone()
            exam_object = Exam(code,time,date,duration,name,venue,notes) 
            exam_list_details.append(exam_object)
        
        return exam_list_details
        

class User:
    def __init__(self,id_no,f_name,l_name,course):
        self.id_no = id_no
        self.f_name = f_name
        self.l_name = l_name
        self.course = course

class Exam:
    def __init__(self,module_code, time, date, duration,module_name,venue,lecturer_notes):
        self.module_code = module_code
        self.time = time
        self.dat = date
        self.duration = duration
        self.module_name = module_name
        self.venue = venue
        self.lecturer_notes = lecturer_notes

server = Flask(__name__)
conn = None
user_in = None
#cursorB = None

@server.route('/',methods = ['POST','GET'])
def init():
    msg=''
    global conn
    #global cursorB
    if not conn:
        conn = DBManager(password_file='/run/secrets/db-password')
        conn.create_database_tables()
        conn.sample_data()
        cursorB = conn.cursor(buffered=True)
    return render_template('login2.html',msg="start")

@server.route('/login', methods = ['POST','GET'])
def login(): 
    msg = '' 
    global user_in
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form: 
        username = request.form['username'] 
        password = request.form['password']
        conn.cursor.execute('SELECT * FROM student WHERE student_id = %s AND password = %s', (username, password, )) 
        account = conn.cursor.fetchone() 
        if account:
#            server.secret_key = 'super secret key'
#            session['loggedin'] = True
#            session['id'] = account['id'] 
#            session['username'] = account['id'] 
            f_name,l_name,course = conn.get_student_data(username)
            exam_list = conn.get_exam_data(username)
#            cursorB.execute('SELECT exam_id FROM student_exam WHERE student_id = %s ', (id_no,))
 #           exams = cursorB.fetchall()
            user_in = User(username,f_name,l_name,course)
            msg = 'Logged in successfully !'
            return render_template('home.html',user=user_in,exams=exam_list)
        else: 
           msg = 'Incorrect username / password !'
    return render_template('login2.html', msg = msg)

@server.route('/home/', methods = ['POST','GET'])
def home_page():
    blog = user_in.id_no
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
