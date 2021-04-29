import os
from flask import Flask, render_template,request,session,redirect,url_for,jsonify
#from flask_mail import Mail, Message
import mysql.connector
import schema2
from mysql.connector import errorcode
import functools
#import seating_chart
import seating_matrix
import new_mail
#import DBManager

class DBManager:
    #create connction to database
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
    
    #create tables in database
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

    #insert data from schema into tables
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
    
    #return information about student
    def get_student_data(self,id_no):
        self.cursor.execute('SELECT f_name,l_name FROM student WHERE student_id = %s ', (id_no,))
        f_name,l_name = self.cursor.fetchone()
        self.cursor.execute('SELECT course_code FROM course_student WHERE student_id = %s ', (id_no,))
        course = self.cursor.fetchone()
        return f_name,l_name,course

    #return locations for map page
    def get_locations(self,id_no):
            locations=[]
            #first attempt to get student exam venues
            self.cursor.execute('SELECT exam_id FROM student_exam WHERE student_id = %s ', (id_no,))
            exams = self.cursor.fetchall()
            for e in exams:
                self.cursor.execute('SELECT venue FROM exam WHERE exam_id = %s ', (e[0],))
                venue = self.cursor.fetchone();
                locations.append(venue[0])
            
            #if no venues returned - assume lecturer user
            if not exams:
                self.cursor.execute('SELECT mod_code FROM lect_module WHERE staff_id = %s ', (id_no,))
                modules = self.cursor.fetchall()
                for m in modules:
                    self.cursor.execute('SELECT venue FROM exam WHERE module_code  = %s ', (m[0],))
                    venue = self.cursor.fetchone();
                    locations.append(venue[0])
            return locations

    #get calendar dates
    def get_calendar_date(self,id_no):
        self.cursor.execute('SELECT exam_id FROM student_exam WHERE student_id = %s ', (id_no,))
        exams = self.cursor.fetchall()

    #gets all exams for students and returns a list of exam objects 
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
            self.cursor.execute('SELECT module_code,start_date,duration,venue,percent FROM exam WHERE exam_id = %s ', (e[0],))
            code,start_date,duration,venue,percent = self.cursor.fetchone()
            self.cursor.execute('SELECT DAYNAME(%s)',(start_date,))
            exam_day = self.cursor.fetchone()
            self.cursor.execute('SELECT TIME_FORMAT(%s,"%H:%i")',(start_date,))
            time = self.cursor.fetchone()
            self.cursor.execute('SELECT DATE_FORMAT(%s,"%d-%m-%Y")',(start_date,))
            exam_date = self.cursor.fetchone()
            self.cursor.execute('SELECT name FROM module WHERE code = %s ', (code,))
            name = self.cursor.fetchone()
            self.cursor.execute('SELECT lecturer_notes FROM module WHERE code = %s ', (code,))
            notes = self.cursor.fetchone()
            self.cursor.execute('SELECT seat_no FROM seating WHERE student_id = %s AND exam_id = %s ', (id_no,e[0],))
            seat_no = self.cursor.fetchone()
            m = seating_matrix.plot_seating_chart(venue,seat_no[0])
            exam_object = Exam(code,time,exam_date,start_date,exam_day,duration,name,venue,percent,notes,seat_no,m)
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
            self.cursor.execute('SELECT start_date,duration,venue,percent FROM exam WHERE module_code = %s ', (m[0],))
            start_date,duration,venue,percent = self.cursor.fetchone()
            self.cursor.execute('SELECT name,lecturer_notes FROM module WHERE code = %s ', (m[0],))
            name,notes = self.cursor.fetchone()
            self.cursor.execute('SELECT DAYNAME(%s)',(start_date,))
            exam_day = self.cursor.fetchone()
            self.cursor.execute('SELECT DATE_FORMAT(%s,"%d-%m-%Y")',(start_date,))
            exam_date = self.cursor.fetchone()
            self.cursor.execute('SELECT TIME_FORMAT(%s,"%H:%i")',(start_date,))
            time = self.cursor.fetchone()
            exam = Exam(m,time,exam_date,start_date,exam_day,duration,name,venue,percent,notes,0,"")
            lecturer_exam_list.append(exam)
        lecturer_object = Lecturer(id_no,f_name,l_name,lecturer_exam_list)        
        print('In lecturer object')
        return lecturer_object

    def get_admin_data(self,id_no):
        admin_exam_list=[]
        self.cursor.execute('SELECT f_name,l_name FROM admin where staff_id = %s ', (id_no,))
        f_name,l_name = self.cursor.fetchone()
        self.cursor.execute('SELECT exam_id FROM organise WHERE staff_id = %s ', (id_no,))
        try:
            exams = self.cursor.fetchall()
        except mysql.connector.errors.InterfaceError as ie:
            if ie.msg == 'No result set to fetch from.':
        # no problem, we were just at the end of the result set
                pass
            else:
                raise
        for e in exams:
            self.cursor.execute('SELECT module_code,start_date,duration,venue,percent FROM exam WHERE exam_id = %s ', (e[0],))
            code,start_date,duration,venue,percent = self.cursor.fetchone()
            self.cursor.execute('SELECT DAYNAME(%s)',(start_date,))
            exam_day = self.cursor.fetchone()
            self.cursor.execute('SELECT TIME_FORMAT(%s,"%H:%i")',(start_date,))
            time = self.cursor.fetchone()
            self.cursor.execute('SELECT DATE_FORMAT(%s,"%d-%m-%Y")',(start_date,))
            exam_date = self.cursor.fetchone()
            self.cursor.execute('SELECT name FROM module WHERE code = %s ', (code,))
            name = self.cursor.fetchone()
            self.cursor.execute('SELECT lecturer_notes FROM module WHERE code = %s ', (code,))
            notes = self.cursor.fetchone()
            exam_object = Exam(code,time,exam_date,start_date,exam_day,duration,name,venue,percent,notes,0,"")
            admin_exam_list.append(exam_object)
        admin_object = Admin(id_no,f_name,l_name,admin_exam_list)
        return admin_object

    def update_lecturer_notes(self,notes,module_code):
        self.cursor.execute('UPDATE module SET lecturer_notes = %s WHERE code=%s', (notes,module_code))
        self.connection.commit()

    def get_email_addresses(self, exam_id):
        self.cursor.execute('SELECT student_id FROM student_exam WHERE exam_id = %s',(exam_id,))
        ids = self.cursor.fetchall();
        emails = []
        for i in ids:
            self.cursor.execute('SELECT email FROM student WHERE student_id = %s',(i[0],))
            email = self.cursor.fetchone()
            emails.append(email)
        return emails

class User:
    def __init__(self,id_no,f_name,l_name,course):
        self.id_no = id_no
        self.f_name = f_name
        self.l_name = l_name
        self.course = course

class Exam:
    def __init__(self,module_code, time, exam_date,start_date,exam_day, duration,module_name,venue,percent,lecturer_notes,seat_no,seat_matrix):
        self.module_code = module_code
        self.time = time
        self.exam_date = exam_date
        self.start_date = start_date
        self.exam_day = exam_day
        self.duration = duration
        self.module_name = module_name
        self.venue = venue
        self.percent = percent
        self.lecturer_notes = lecturer_notes
        self.seat_no = seat_no
        self.seat_matrix = seat_matrix

class Lecturer:
    def __init__(self,lecturer_id,f_name,l_name,exam_list):
        self.lecturer_id = lecturer_id
        self.f_name = f_name
        self.l_name = l_name
        self.exam_list = exam_list

class Admin:
    def __init__(self,staff_id,f_name,l_name,exam_list):
        self.staff_id = staff_id
        self.f_name = f_name
        self.l_name = l_name
        self.exam_list = exam_list

server = Flask(__name__)
#mail= Mail(server)
server.secret_key = 'super secret key'
conn = None
user_in = None

#server.config['MAIL_SERVER']='smtp.gmail.com'
#server.config['MAIL_PORT'] = 587
#server.config['MAIL_USERNAME'] = 'exam.timetable.updates@gmail.com'
##server.config['MAIL_PASSWORD'] = 'fmjoukhqqbliejbw'
#server.config['MAIL_PASSWORD'] = 'Examtimetable'
#server.config['MAIL_USE_TLS'] = False
#server.config['MAIL_USE_SSL'] = True
#server.config['MAIL_DEBUG'] = True

@server.route("/mail",methods = ['POST','GET'])
def send_emails():
#    msg = Message('Hello', sender = 'exam.timetable.updates@gmail.com', recipients = ['niamhhennigan@gmail.com'])
#    msg.body = "Hello Flask message sent from Flask-Mail"
#    mail.send(msg)
#    return "Sent"
    if request.method == 'POST' and 'exam_id' in request.form:
        emails = conn.get_email_addresses(request.form["exam_id"])
        new_mail.sendmail(emails)
    return redirect(url_for('admin_home_page'))

@server.route('/',methods = ['POST','GET'])
def init():
    msg=''
    global conn
    if not conn:
        conn = DBManager(password_file='/run/secrets/db-password')
#        conn.create_database_tables()
#        conn.sample_data()
    return render_template('login2.html',msg="start")

@server.route('/login',methods = ['POST','GET'])
def login(): 
    msg = '' 
#    global user_in
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form: 
        username = request.form['username'] 
        password = request.form['password']
        conn.cursor.execute('SELECT * FROM student WHERE student_id = %s AND password = %s', (username, password, )) 
        student_account = conn.cursor.fetchone() 
        if student_account:
#            return render_template('check.html')
 
            create_session(username,password)
#            return render_template('check.html')
#            user_in = 'student'
            return redirect(url_for('home_page'))
        else:
            conn.cursor.execute('SELECT * FROM lecturer WHERE lecturer_id = %s AND password = %s', (username, password, ))
        lecturer_account = conn.cursor.fetchone()
        if lecturer_account:
            create_session(username,password)
            user_in = 'lecturer'
            return redirect(url_for('lect_home_page'))
        else:
            conn.cursor.execute('SELECT * FROM admin WHERE staff_id = %s AND password = %s', (username, password, ))
        admin_account = conn.cursor.fetchone()
        if admin_account:
            create_session(username,password)
            user_in='admin'
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
            return redirect(url_for("login"))
        return func()
    return secure_function

#this method needs testing
@server.route('/logout/')
def logout():
    #this may need to be session.pop()
    session.clear()
    return redirect(url_for("login"))

@server.route('/home/', methods = ['POST','GET'])
@login_required
def home_page():
    try:
        f_name,l_name,course = conn.get_student_data(session["username"])
        exam_list = conn.get_exam_data(session["username"])
    #    return render_template('check.html')
        user_in = User(session["username"],f_name,l_name,course)
        return render_template('home.html',user=user_in,exams=exam_list,m="")
    except Exception:
        return redirect(url_for('lect_home_page'))

@server.route('/admin_home/', methods = ['POST','GET'])
@login_required
def admin_home_page():
#    try:
   admin = conn.get_admin_data(session["username"])
   table_names = schema2.get_names()
   attributes = schema2.get_attributes()
   return render_template('admin_home.html',user = admin,table_names = table_names, attributes = attributes)
 #   except Exception:
 #       print("Error finding home page")

@server.route('/admin_updates/', methods = ['POST','GET'])
@login_required
def admin_updates():
    if request.method == 'POST' and 'actions' in request.form and 'tables' in request.form:
        if request.form["actions"] == "UPDATE" and 'attributes' in request.form and 'key' in request.form and 'key_value' in request.form:
            if 'second_key' in request.form:
                query = "UPDATE " + request.form["tables"] + " SET " +request.form["attributes"] +"=%s WHERE " + request.form["key"]+ " =%s AND " + request.form["second_key"]+" =%s"
                conn.cursor.execute(query, (request.form["updated_info"],request.form["key_value"],request.form["second_key_value"],))
                conn.connection.commit()
                return redirect(url_for('admin_home_page'))
            query = "UPDATE " + request.form["tables"] + " SET " +request.form["attributes"] +"=%s WHERE " + request.form["key"]+ " =%s" 
            conn.cursor.execute(query, (request.form["updated_info"],request.form["key_value"],))
            conn.connection.commit()
            return redirect(url_for('admin_home_page'))
        if request.form["actions"] == "DELETE"  and 'key' in request.form and 'key_value' in request.form:
            if 'second_key' in request.form:
                query = "DELETE from " + request.form["tables"] +" WHERE " + request.form["key"]+ " =%s AND " + request.form["second_key"]+" =%s"
                conn.cursor.execute(query, (request.form["key_value"],request.form["second_key_value"],))
                conn.connection.commit()
                return redirect(url_for('admin_home_page'))
            query = "DELETE FROM " + request.form["tables"] + " WHERE " + request.form["key"]+ " =%s"
            conn.cursor.execute(query, (request.form["key_value"],))
            conn.connection.commit()
            return redirect(url_for('admin_home_page'))
        if request.form["actions"] == "CREATE":
            if request.form["tables"] == "admin":
                attributes = "(staff_id,f_name,l_name,password)"
                number = "(%s,%s,%s,%s)"
            elif request.form["tables"] == "module":
                attributes = "code,name,semester,ECTs,lecturer_notes)"
                number = "(%s,%s,%s,%s,%s)"
            elif request.form["tables"] == "exam":
                attributes = "(exam_id,module_code,duration,venue,percent,start_date,end_date)"
                number = "(%s,%s,%s,%s,%s,%s,%s)"
            elif request.form["tables"] == "student":
                attributes = "(student_id,f_name,l_name,password,email)"
                number = "(%s,%s,%s,%s,%s)"
            elif request.form["tables"] == "lecturer":
                attributes = "(lecturer_id,f_name,l_name,password)"
                number = "(%s,%s,%s,%s)"
            elif request.form["tables"] == "course":
                attributes = "(code,name)"
                number = "(%s,%s)"
            elif request.form["tables"] == "lect_module":
                attributes = "(staff_id,mod_code)"
                number = "(%s,%s)"
            elif request.form["tables"] == "organise":
                attributes = "(staff_id,exam_id)"
                number = "(%s,%s)"
            elif request.form["tables"] == "student_exam":
                attributes = "(student_id,exam_id)"
                number = "(%s,%s)"
            elif request.form["tables"] == "course_module":
                attributes = "(course_code,mod_code)"
                number = "(%s,%s)"
            elif request.form["tables"] == "student_module":
                attributes = "(student_id,mod_code)"
                number = "(%s,%s)"
            elif request.form["tables"] == "course_student":
                attributes = "(course_code,student_id)"
                number = "(%s,%s)"
            elif request.form["tables"] == "seating":
                attributes = "(student_id,exam_id,seat_no)"
                number = "(%s,%s,%s)"

            query = "INSERT INTO "+request.form["tables"]+" "+attributes+" VALUES "+number

            if request.form["tables"] == "module" or request.form["tables"] == "student":
                input1= request.form["input1"]
                input2= request.form["input2"]
                input3= request.form["input3"]
                input4= request.form["input4"]
                input5= request.form["input5"]
                conn.cursor.execute(query,(input1,input2,input3,input4,input5,))

            elif request.form["tables"] == "course" or request.form["tables"] == "lect_module" or request.form["tables"] == "organise" or request.form["tables"] == "student_exam" or request.form["tables"] == "course_module" or request.form["tables"] == "student_module" or request.form["tables"] == "course_student":
                input1= request.form["input1"]
                input2= request.form["input2"]
                conn.cursor.execute(query,(input1,input2,))

            elif request.form["tables"] == "lecturer" or request.form["tables"] == "admin":
                input1= request.form["input1"]
                input2= request.form["input2"]
                input3= request.form["input3"]
                input4= request.form["input4"]
                conn.cursor.execute(query,(input1,input2,input3,input4,))

            elif request.form["tables"] == "seating":
                input1= request.form["input1"]
                input2= request.form["input2"]
                input3= request.form["input3"]
                conn.cursor.execute(query,(input1,input2,input3,))

            elif request.form["tables"] == "exam":
                input1= request.form["input1"]
                input2= request.form["input2"]
                input3= request.form["input3"]
                input4= request.form["input4"]
                input5= request.form["input5"]
                input6= request.form["input6"]
                input7= request.form["input7"]
                conn.cursor.execute(query,(input1,input2,input3,input4,input5,input6,input7,))
#            data1 = "33333333"
#            data2 = 'n'
#            data3 = 'h'
#            data4 = "pw"
#            data = "'33333333','n','h','pw'"
#            conn.cursor.execute(query,(data1,data2,data3,data4,))
            conn.connection.commit()
    return redirect(url_for('admin_home_page'))


@server.route('/lect_home/')
@login_required
def lect_home_page():
    try:
        lecturer_info = conn.get_lecturer_data(session["username"])
        return render_template('lect_home.html',lecturer = lecturer_info)
    except Exception:
        return redirect(url_for('admin_home_page'))

@server.route('/lecturer_updates/', methods = ['POST','GET'])
@login_required
def update_lect_notes():
    if request.method == 'POST' and 'notes' in request.form and 'module_code' in request.form:
        conn.update_lecturer_notes(request.form['notes'],request.form['module_code'])
        return redirect(url_for('lect_home_page'))
    return redirect(url_for('lect_home_page'))

@server.route('/calendarview/', methods = ['POST','GET'])
@login_required
def calendar():
    return render_template("json.html")

@server.route('/mapview/',methods = ['POST','GET'])
@login_required
def map_page():
    venues = conn.get_locations(session["username"])
    return render_template('map.html',locations=venues)

@server.route('/examinfo/')
@login_required
def info_page():
    return render_template("info.html")

@server.route('/login_again')
def login_again():
    return render_template('login2.html',msg="Please Log In")

@server.route('/calendar_view/data')
def return_data():
    start_date = request.args.get('start', '')
    end_date = request.args.get('end', '')
    events = []
    exam_list = conn.get_exam_data(session["username"])
    if exam_list:
        for e in exam_list:
            events.append({'title': e.module_name[0], 'start': e.start_date})
        hard_c = jsonify(events)
        return hard_c

    else:
        try:
            lecturer = conn.get_lecturer_data(session["username"])
            for e in lecturer.exam_list:
                    events.append({'title': e.module_name, 'start': e.start_date})
            hard_c = jsonify(events)
            return hard_c
        except Exception:
            pass
    
        try:
            admin = conn.get_admin_data(session["username"])
            for e in admin.exam_list:
                    events.append({'title': e.module_name, 'start': e.start_date})
            hard_c = jsonify(events)
            return hard_c
        except Exception:
            pass

if __name__ == '__main__':
    server.run(debug= True)
#    mail.init_app(server)
