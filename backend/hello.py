import os
from flask import Flask, render_template,request,session,redirect,url_for
import mysql.connector
import schema2
from mysql.connector import errorcode
import functools
#import seating_chart

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
               # self.cursor.execute('DROP TABLE IF EXISTS %s ', (table_name,))
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

    def get_locations(self,id_no):
            locations=[]
            self.cursor.execute('SELECT exam_id FROM student_exam WHERE student_id = %s ', (id_no,))
            exams = self.cursor.fetchall()
            for e in exams:
                self.cursor.execute('SELECT venue FROM exam WHERE exam_id = %s ', (e[0],))
                venue = self.cursor.fetchone();
                locations.append(venue[0])
            return locations

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
            self.cursor.execute('SELECT module_code,time,exam_date,duration,venue,percent FROM exam WHERE exam_id = %s ', (e[0],))
            code,time,exam_date,duration,venue,percent = self.cursor.fetchone()
            self.cursor.execute('SELECT DAYNAME(%s)',(exam_date,))
            exam_day = self.cursor.fetchone()
            self.cursor.execute('SELECT name FROM module WHERE code = %s ', (code,))
            name = self.cursor.fetchone()
            self.cursor.execute('SELECT lecturer_notes FROM module WHERE code = %s ', (code,))
            notes = self.cursor.fetchone()
            self.cursor.execute('SELECT seat_no FROM seating WHERE student_id = %s AND exam_id = %s ', (id_no,e[0],))
            seat_no = self.cursor.fetchone()
            exam_object = Exam(code,time,exam_date,exam_day,duration,name,venue,percent,notes,seat_no) 
            exam_list_details.append(exam_object)
        return exam_list_details
        
    def get_lecturer_data(self,id_no):
        lecturer_exam_list=[]
        self.cursor.execute('SELECT f_name,l_name FROM lecturer where lecturer_id = %s ', (id_no,))
        f_name,l_name = self.cursor.fetchone()
        self.cursor.execute('SELECT mod_code FROM lect_module WHERE staff_id = %s ', (id_no,))
        try:
            modules = self.cursor.fetchall()
        except mysql.connector.errors.InterfaceError as ie:
            if ie.msg == 'No result set to fetch from.':
        # no problem, we were just at the end of the result set
                pass
            else:
                raise
        for m in modules:
            self.cursor.execute('SELECT time,exam_date,duration,venue,percent FROM exam WHERE module_code = %s ', (m[0],))
            time,exam_date,duration,venue,percent = self.cursor.fetchone()
            self.cursor.execute('SELECT name,lecturer_notes FROM module WHERE code = %s ', (m[0],))
            name,notes = self.cursor.fetchone()
            self.cursor.execute('SELECT DAYNAME(%s)',(exam_date,))
            exam_day = self.cursor.fetchone()
            exam = Exam(m,time,exam_date,exam_day,duration,name,venue,percent,notes,0)
            lecturer_exam_list.append(exam)
        lecturer_object = Lecturer(id_no,f_name,l_name,lecturer_exam_list)        
        print('In lecturer object')
        return lecturer_object

    def update_lecturer_notes(self,notes,module_code):
        self.cursor.execute('UPDATE module SET lecturer_notes = %s WHERE code=%s', (notes,module_code))
        self.connection.commit()


class User:
    def __init__(self,id_no,f_name,l_name,course):
        self.id_no = id_no
        self.f_name = f_name
        self.l_name = l_name
        self.course = course

class Exam:
    def __init__(self,module_code, time, exam_date,exam_day, duration,module_name,venue,percent,lecturer_notes,seat_no):
        self.module_code = module_code
        self.time = time
        self.exam_date = exam_date
        self.exam_day = exam_day
        self.duration = duration
        self.module_name = module_name
        self.venue = venue
        self.percent = percent
        self.lecturer_notes = lecturer_notes
        self.seat_no = seat_no

#class Admin:
#    def __init__(self):

class Lecturer:
    def __init__(self,lecturer_id,f_name,l_name,exam_list):
        self.lecturer_id = lecturer_id
        self.f_name = f_name
        self.l_name = l_name
        self.exam_list = exam_list

server = Flask(__name__)
server.secret_key = 'super secret key'
conn = None
user_in = None

@server.route('/',methods = ['POST','GET'])
def init():
    msg=''
    global conn
    if not conn:
        conn = DBManager(password_file='/run/secrets/db-password')
        conn.create_database_tables()
        conn.sample_data()
    return render_template('login2.html',msg="start")

@server.route('/login',methods = ['POST','GET'])
def login(): 
    msg = '' 
    global user_in
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form: 
        username = request.form['username'] 
        password = request.form['password']
        conn.cursor.execute('SELECT * FROM student WHERE student_id = %s AND password = %s', (username, password, )) 
        student_account = conn.cursor.fetchone() 
        if student_account:
            create_session(username,password)
            return redirect(url_for('home_page'))
        else:
            conn.cursor.execute('SELECT * FROM lecturer WHERE lecturer_id = %s AND password = %s', (username, password, ))
        lecturer_account = conn.cursor.fetchone()
        if lecturer_account:
            create_session(username,password)
            return redirect(url_for('lect_home_page'))
        else:
            conn.cursor.execute('SELECT * FROM admin WHERE staff_id = %s AND password = %s', (username, password, ))
        admin_account = conn.cursor.fetchone()
        if admin_account:
            create_session(username,password)
            return redirect(url_for('admin_home_page'))
            #need to finish creating the admin objects and finsih the url
        else:
           msg = 'Incorrect username / password !'
    return redirect(url_for('login_again', msg = msg))

def create_session(username,password):
    session['loggedin'] = True
    session['id'] = password
    session["username"] = username

def login_required(func):
    @functools.wraps(func)
    def secure_function(*args, **kwargs):
        if "username" not in session:
            return redirect(url_for("login_again"))
        return func()
    return secure_function

#this method needs testing
@server.route('/logout/')
def logout():
    #this may need to be session.pop()
    session.clear()
    return redirect(url_for("login_again"))

@server.route('/home/', methods = ['POST','GET'])
@login_required
def home_page():
    f_name,l_name,course = conn.get_student_data(session["username"])
    exam_list = conn.get_exam_data(session["username"])
    user_in = User(session["username"],f_name,l_name,course)
    return render_template('home.html',user=user_in,exams=exam_list)

@server.route('/home/seating_chart',methods = ['POST','GET'])
@login_required
def plot_seating_chart():
#    if request.method == 'POST' and 'venue' in request.form and 'seat_no' in request.form:
#        seating_chart.plot_seating(request.form['venue'],request.form['seat_no'])
    return redirect(url_for(home_page))


@server.route('/admin_home/', methods = ['POST','GET'])
@login_required
def admin_home_page():
    return render_template('admin_home.html')

@server.route('/lect_home/')
@login_required
def lect_home_page():
    lecturer_info = conn.get_lecturer_data(session["username"])
    return render_template('lect_home.html',lecturer = lecturer_info)

@server.route('/lecturer_updates/', methods = ['POST','GET'])
@login_required
def update_lect_notes():
    if request.method == 'POST' and 'notes' in request.form and 'module_code' in request.form:
        conn.update_lecturer_notes(request.form['notes'],request.form['module_code'])
        return redirect(url_for('lect_home_page'))
    return redirect(url_for('lect_home_page'))

@server.route('/calendarview/')
@login_required
def calendar_page():
    return render_template('calendar.html')

#@server.route('/modal/')
#def modal():
#    return render_template('modal.html')

@server.route('/mapview/')
@login_required
def map_page():
    venues = conn.get_locations(session["username"])
    return render_template('map.html',locations=venues)

@server.route('/examofficeinfo/')
@login_required
def info_page():
    return render_template('info.html')

@server.route('/login_again')
def login_again():
    return render_template('login2.html',msg="Please Log In")

if __name__ == '__main__':
    server.run(debug= True)
